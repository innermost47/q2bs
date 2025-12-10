from q2b_data_visualizer import Q2BDataVisualizer
from q2b_studio_auditor import Q2BStudioAuditor
from wayback_archiver import WaybackArchiver
import os
import glob
from datetime import datetime


def list_checkpoints():
    checkpoints = sorted(glob.glob("q2b_audit_*"), reverse=True)
    return [d for d in checkpoints if os.path.isdir(d)]


def select_checkpoint():
    checkpoints = list_checkpoints()
    if not checkpoints:
        print("No existing checkpoints found.")
        return None, False

    print("\nAvailable checkpoints:")
    print("0. Start fresh (new scraping)")
    for i, checkpoint in enumerate(checkpoints, 1):
        try:
            checkpoint_file = os.path.join(checkpoint, "checkpoint.json")
            if os.path.exists(checkpoint_file):
                import json

                with open(checkpoint_file, "r") as f:
                    data = json.load(f)
                    count = data.get("articles_count", "?")
                    timestamp = data.get("timestamp", "?")
                print(f"{i}. {checkpoint} - {count:,} articles - {timestamp}")
            else:
                print(f"{i}. {checkpoint}")
        except:
            print(f"{i}. {checkpoint}")

    while True:
        choice = input("\nSelect checkpoint number (0 for fresh start): ").strip()
        try:
            choice_num = int(choice)
            if choice_num == 0:
                return None, False
            if 1 <= choice_num <= len(checkpoints):
                selected_checkpoint = checkpoints[choice_num - 1]

                visualize_only = (
                    input("Visualize only (skip scraping)? (yes/no): ").strip().lower()
                    == "yes"
                )

                return selected_checkpoint, visualize_only
            else:
                print(f"Please enter a number between 0 and {len(checkpoints)}")
        except ValueError:
            print("Please enter a valid number")


def main():
    print("=" * 60)
    print("Q2BSTUDIO PLAGIARISM AUDITOR")
    print("=" * 60)

    checkpoint_dir, visualize_only = select_checkpoint()

    auditor = Q2BStudioAuditor(create_output_dir=(checkpoint_dir is None))

    start_page = 1
    max_page = None

    if checkpoint_dir:
        loaded = auditor.load_checkpoint(checkpoint_dir)

        if visualize_only:
            print("\n" + "=" * 60)
            print("VISUALIZATION MODE - Skipping scraping")
            print("=" * 60)

            if not loaded:
                print("Failed to load checkpoint. Cannot visualize.")
                return

            report = auditor.generate_report()
            visualizer = Q2BDataVisualizer(input_dir=auditor.output_dir)
            visualizer.create_visualizations(report)

            print(f"\nALL DONE! Check folder: {auditor.output_dir}")
            return

        if loaded:
            max_page = auditor.get_max_page_number()
            if not max_page:
                print("Could not determine max page. Exiting.")
                return

            start_page = auditor.calculate_resume_page(max_page, articles_per_page=9)
            print(f"\nResuming from page {start_page:,}")
        else:
            print("Failed to load checkpoint. Starting fresh.")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            auditor.output_dir = f"q2b_audit_{timestamp}"
            os.makedirs(auditor.output_dir, exist_ok=True)
            print(f"Output directory: {auditor.output_dir}")
            max_page = auditor.get_max_page_number()
    else:
        max_page = auditor.get_max_page_number()

    output_dir = auditor.output_dir

    if not max_page:
        print("Could not determine max page. Exiting.")
        return

    if start_page > max_page:
        print(f"Already scraped all pages (up to {max_page:,}). Nothing to do!")
        report = auditor.generate_report()
        visualizer = Q2BDataVisualizer(input_dir=output_dir)
        visualizer.create_visualizations(report)
        print(f"\nALL DONE! Check folder: {output_dir}")
        return

    pages_to_scrape = max_page - start_page + 1
    confirm_scrape = input(
        f"This will scrape {pages_to_scrape:,} pages (from {start_page:,} to {max_page:,}). Continue? (yes/no): "
    )

    confirm_archive = input(
        "Do you want to archive a sample of the articles to Wayback Machine? (yes/no): "
    )

    if confirm_scrape.lower() == "yes":
        auditor.scrape_all_pages(max_page, start_page=start_page, sample_every=1)
    else:
        print("Aborted scraping.")
        return

    report = auditor.generate_report()

    visualizer = Q2BDataVisualizer(input_dir=output_dir)
    visualizer.create_visualizations(report)

    if confirm_archive.lower() == "yes":
        archiver = WaybackArchiver(output_dir)
        if not archiver.load_data():
            print("Aborted archiving due to data loading failure.")
            return

        sample_size = 500
        print(f"Archiving a sample of {sample_size} articles...")
        archiver.archive_sample(sample_size)
        archiver.save_results()
        print("Archiving complete.")
    else:
        print("Skipping archiving.")

    print(f"\nALL DONE! Check folder: {output_dir}")


if __name__ == "__main__":
    main()
