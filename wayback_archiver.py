import requests
import csv
import json
import time
from datetime import datetime
import os
import random


class WaybackArchiver:
    def __init__(self, clean_data_dir):
        self.clean_data_dir = clean_data_dir
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
        )

        self.articles = []
        self.archived = 0
        self.failed = 0
        self.skipped = 0

    def load_data(self):
        csv_file = os.path.join(self.clean_data_dir, "articles.csv")

        if not os.path.exists(csv_file):
            print(f"Clean CSV not found: {csv_file}")
            return False

        print(f"Loading clean data from: {csv_file}")

        with open(csv_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            self.articles = list(reader)

        print(f"Loaded {len(self.articles):,} clean articles")
        return True

    def archive_to_wayback(self, url, retry=2):
        archive_api = "https://web.archive.org/save/"

        for attempt in range(retry):
            try:
                response = self.session.get(
                    archive_api + url, timeout=60, allow_redirects=True
                )

                if response.status_code == 200:
                    archive_url = response.url
                    if "web.archive.org" in archive_url:
                        return archive_url

                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                return f"https://web.archive.org/web/{timestamp}/{url}"

            except requests.exceptions.Timeout:
                print(f"Timeout (attempt {attempt + 1}/{retry})")
                if attempt < retry - 1:
                    time.sleep(5)
                    continue
                else:
                    return None
            except Exception as e:
                print(f"Error: {e}")
                if attempt < retry - 1:
                    time.sleep(3)
                    continue
                else:
                    return None

        return None

    def check_existing_archive(self, url):
        try:
            check_url = f"https://archive.org/wayback/available?url={url}"
            response = self.session.get(check_url, timeout=10)
            data = response.json()

            if data.get("archived_snapshots", {}).get("closest"):
                return data["archived_snapshots"]["closest"]["url"]

            return None
        except:
            return None

    def archive_sample(self, sample_size=500):
        print(f"Sample size: {sample_size}")
        print("-" * 60)

        to_archive = random.sample(self.articles, min(sample_size, len(self.articles)))
        print(f"Selected {len(to_archive)} random articles")

        print(f"\nStarting archiving process...")

        start_time = time.time()

        for i, article in enumerate(to_archive, 1):
            url = article.get("url", "")
            title = article.get("title", "N/A")[:50]

            print(f"\n[{i}/{len(to_archive)}] {title}...")
            print(f"  URL: {url}")

            if article.get("archive_url"):
                print(f"Already archived: {article['archive_url']}")
                self.skipped += 1
                continue

            archive_url = self.archive_to_wayback(url)

            if archive_url:
                article["archive_url"] = archive_url
                self.archived += 1
                print(f"Archived: {archive_url}")
            else:
                self.failed += 1
                print(f"Failed to archive")

            time.sleep(3)

            if i % 50 == 0:
                elapsed = time.time() - start_time

                print(f"\nProgress: {i}/{len(to_archive)}")
                print(
                    f"   Archived: {self.archived}, Failed: {self.failed}, Skipped: {self.skipped}"
                )

                self.save_checkpoint()

        elapsed = time.time() - start_time
        print(f"\nArchiving complete!")
        print(f"Time elapsed: {elapsed / 60:.1f} minutes")

    def save_checkpoint(self):
        checkpoint_file = os.path.join(self.clean_data_dir, "archiving_checkpoint.json")

        with open(checkpoint_file, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "timestamp": datetime.now().isoformat(),
                    "archived": self.archived,
                    "failed": self.failed,
                    "skipped": self.skipped,
                    "articles": self.articles,
                },
                f,
                indent=2,
                ensure_ascii=False,
            )

    def save_results(self):
        print("\nSaving archived data...")

        csv_file = os.path.join(self.clean_data_dir, "articles_archived.csv")
        with open(csv_file, "w", newline="", encoding="utf-8") as f:
            if self.articles:
                fieldnames = list(self.articles[0].keys())
                if "archive_url" not in fieldnames:
                    fieldnames.append("archive_url")

                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(self.articles)

        print(f"Saved: {csv_file}")

        archived_articles = [a for a in self.articles if a.get("archive_url")]

        report = {
            "generated_at": datetime.now().isoformat(),
            "total_articles": len(self.articles),
            "archived_count": len(archived_articles),
            "archive_rate": (
                f"{len(archived_articles) / len(self.articles) * 100:.2f}%"
                if self.articles
                else "0%"
            ),
            "stats": {
                "archived": self.archived,
                "failed": self.failed,
                "skipped": self.skipped,
            },
            "archived_urls": [
                {
                    "original_url": a["url"],
                    "archive_url": a.get("archive_url"),
                    "title": a.get("title"),
                    "date": a.get("date_parsed"),
                }
                for a in archived_articles
            ],
        }

        report_file = os.path.join(self.clean_data_dir, "archive_report.json")
        with open(report_file, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        print(f"Saved: {report_file}")

        urls_file = os.path.join(self.clean_data_dir, "wayback_urls.txt")
        with open(urls_file, "w", encoding="utf-8") as f:
            f.write("# Q2BSTUDIO Archive URLs\n")
            f.write(f"# Generated: {datetime.now().isoformat()}\n")
            f.write(f"# Total archived: {len(archived_articles)}\n\n")

            for article in archived_articles:
                f.write(f"{article.get('archive_url')}\n")

        print(f"Saved: {urls_file}")
