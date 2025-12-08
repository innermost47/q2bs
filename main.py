from q2b_data_visualizer import Q2BDataVisualizer
from q2b_studio_auditor import Q2BStudioAuditor
from wayback_archiver import WaybackArchiver


def main():
    print("=" * 60)
    print("Q2BSTUDIO PLAGIARISM AUDITOR")
    print("=" * 60)

    auditor = Q2BStudioAuditor()
    output_dir = auditor.output_dir
    max_page = auditor.get_max_page_number()

    if not max_page:
        print("Could not determine max page. Exiting.")
        return

    confirm_scrape = input(f"This will scrape {max_page:,} pages. Continue? (yes/no): ")
    confirm_archive = input(
        "Do you want to archive a sample of the articles to Wayback Machine? (yes/no): "
    )
    if confirm_scrape.lower() == "yes":
        auditor.scrape_all_pages(max_page, start_page=1, sample_every=1)
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
