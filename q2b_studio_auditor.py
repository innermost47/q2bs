import time
import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import json
import os
from collections import defaultdict
import locale

try:
    locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")
except:
    try:
        locale.setlocale(locale.LC_TIME, "Spanish_Spain.1252")
    except:
        print("Warning: Could not set Spanish locale")


class Q2BStudioAuditor:
    def __init__(self):
        self.base_url = "https://www.q2bstudio.com"
        self.blog_url = f"{self.base_url}/blog-empresa-aplicaciones"
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
                "Referer": "https://www.google.com/",
                "DNT": "1",
            }
        )
        self.articles = {}
        self.articles_by_date = defaultdict(list)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_dir = f"q2b_audit_{timestamp}"
        os.makedirs(self.output_dir, exist_ok=True)

        print(f"Output directory: {self.output_dir}")

    def get_max_page_number(self):
        print("\nGetting maximum page number...")

        try:
            response = self.session.get(self.blog_url, timeout=15)
            soup = BeautifulSoup(response.content, "html.parser")

            pagination = soup.find("nav", {"aria-label": "Page navigation example"})
            if not pagination:
                print("Could not find pagination")
                return None

            page_links = pagination.find_all("a", class_="page-link")

            max_page = 1
            for link in page_links:
                href = link.get("href", "")
                if "/page/" in href:
                    try:
                        page_num = int(href.split("/page/")[-1])
                        if page_num > max_page:
                            max_page = page_num
                    except:
                        continue

            print(f"Maximum page number: {max_page:,}")
            return max_page

        except Exception as e:
            print(f"Error getting max page: {e}")
            return None

    def parse_spanish_date(self, date_str: str):
        try:
            date_parts = date_str.split(",", 1)
            if len(date_parts) > 1:
                clean_date = date_parts[1].strip()
            else:
                clean_date = date_str.strip()

            date_obj = datetime.strptime(clean_date, "%d de %B de %Y")
            return date_obj.strftime("%Y-%m-%d")
        except Exception as e:
            print(f"Could not parse date '{date_str}': {e}")
            return "UNKNOWN_DATE"

    def scrape_page(self, page_num):
        url = f"{self.blog_url}/page/{page_num}" if page_num > 1 else self.blog_url
        articles_on_page = []

        try:
            response = self.session.get(url, timeout=15)
            soup = BeautifulSoup(response.content, "html.parser")
            article_items = soup.find_all("div", class_="item-new")

            for item in article_items:
                try:
                    link_elem = item.find("a", href=True)
                    if not link_elem:
                        continue

                    article_url = self.base_url + link_elem["href"]
                    title_elem = item.find("div", class_="title")
                    title = title_elem.get_text().strip() if title_elem else "N/A"
                    tags_elem = item.find("div", class_="tags")
                    date_str = "N/A"
                    if tags_elem:
                        inner = tags_elem.find("div", class_="inner")
                        if inner:
                            text = inner.get_text().strip()
                            if "|" in text:
                                date_str = text.split("|")[1].strip()

                    parsed_date = self.parse_spanish_date(date_str)

                    article_data = {
                        "url": article_url,
                        "title": title,
                        "date_raw": date_str,
                        "date_parsed": parsed_date,
                        "page_num": page_num,
                    }

                    articles_on_page.append(article_data)

                except Exception as e:
                    print(f"Error parsing article: {e}")
                    continue

            return articles_on_page

        except Exception as e:
            print(f"Error scraping page {page_num}: {e}")
            return []

    def scrape_all_pages(self, max_page, start_page=1, sample_every=1):
        print(f"\nStarting scraping...")
        print(f"Pages to scrape: {start_page} to {max_page}")
        print(f"Sampling: every {sample_every} page(s)")
        print("-" * 60)

        total_pages = ((max_page - start_page) // sample_every) + 1
        scraped = 0

        for page_num in range(start_page, max_page + 1, sample_every):
            scraped += 1
            print(f"\n[{scraped}/{total_pages}] - Scraping page {page_num:,}...")

            articles_on_page = self.scrape_page(page_num)

            if articles_on_page:
                print(f"Found {len(articles_on_page)} articles")
                for article in articles_on_page:
                    self.articles[article["url"]] = article
                    self.articles_by_date[article["date_parsed"]].append(article)
            else:
                print(f"No articles found")

            time.sleep(0.5)

            if scraped % 100 == 0:
                print(
                    f"\nProgress: {scraped}/{total_pages} pages scraped, "
                    f"{len(self.articles):,} articles collected"
                )
                self.save_checkpoint()

        print(f"\nScraping complete!")
        print(f"Total articles collected: {len(self.articles):,}")
        self.save_checkpoint()

    def save_checkpoint(self):
        print(f"Saving checkpoint ({len(self.articles):,} articles)...")

        checkpoint_file = os.path.join(self.output_dir, "checkpoint.json")
        with open(checkpoint_file, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "timestamp": datetime.now().isoformat(),
                    "articles_count": len(self.articles),
                    "articles": list(self.articles.values()),
                },
                f,
                indent=2,
                ensure_ascii=False,
            )

        csv_file = os.path.join(self.output_dir, "articles.csv")
        with open(csv_file, "w", newline="", encoding="utf-8") as f:
            fieldnames = [
                "url",
                "title",
                "date_raw",
                "date_parsed",
                "page_num",
                "archive_url",
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(self.articles.values())

        report = self.generate_report()
        report_file = os.path.join(self.output_dir, "report.json")
        with open(report_file, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        daily_file = os.path.join(self.output_dir, "daily_summary.csv")
        with open(daily_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Date", "Article Count"])
            for date in sorted(report["daily_statistics"]["articles_per_day"].keys()):
                count = report["daily_statistics"]["articles_per_day"][date]
                writer.writerow([date, count])

        print("Checkpoint saved: CSV, JSON, Report, Daily summary")

    def generate_report(self):
        print("\nGenerating report...")
        all_unique_articles = list(self.articles.values())

        sorted_articles = sorted(
            all_unique_articles,
            key=lambda x: (
                x["date_parsed"] if x["date_parsed"] != "UNKNOWN_DATE" else "9999-12-31"
            ),
        )

        daily_stats = defaultdict(int)

        for article in all_unique_articles:
            daily_stats[article["date_parsed"]] += 1

        known_date_articles_per_day = {
            date: count for date, count in daily_stats.items() if date != "UNKNOWN_DATE"
        }

        total_unique_articles = len(all_unique_articles)
        num_known_dates = len(known_date_articles_per_day)

        average_per_day = (
            sum(known_date_articles_per_day.values()) / num_known_dates
            if num_known_dates > 0
            else 0
        )
        max_per_day = (
            max(known_date_articles_per_day.values()) if num_known_dates > 0 else 0
        )
        min_per_day = (
            min(known_date_articles_per_day.values()) if num_known_dates > 0 else 0
        )

        report = {
            "generated_at": datetime.now().isoformat(),
            "total_articles": total_unique_articles,
            "date_range": {
                "earliest": (
                    sorted_articles[0]["date_parsed"] if sorted_articles else None
                ),
                "latest": (
                    sorted_articles[-1]["date_parsed"] if sorted_articles else None
                ),
            },
            "daily_statistics": {
                "dates": num_known_dates,
                "articles_per_day": dict(sorted(daily_stats.items())),
                "average_per_day": average_per_day,
                "max_per_day": max_per_day,
                "min_per_day": min_per_day,
            },
            "cleaning_summary": {
                "initial_article_count": total_unique_articles,
                "final_article_count": total_unique_articles,
                "duplicates_removed": 0,
                "deduplication_rate": "0.00%",
            },
        }

        return report
