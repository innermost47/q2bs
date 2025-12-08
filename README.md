# Q2BSTUDIO Content Farm Auditor

A Python-based investigation tool for analyzing industrial-scale automated content generation systems. Developed to document and analyze the publishing patterns of q2bstudio.com.

## Background

This tool was created following the discovery that my technical article about OBSIDIAN Neural (an open-source AI music VST plugin) was plagiarized, translated, and republished with commercial links injected by Q2BSTUDIO's automated system.

When their blog showed 36,516+ pages of content, I developed this auditor to systematically document their publishing volume and patterns.

**Full case study:** https://dev.to/innermost_47/when-ai-content-systems-reproduce-content-without-attribution-a-documented-case-study-1h0g

## Features

- **Systematic Blog Scraping:** Crawls through all pagination pages of Q2BSTUDIO's blog
- **Data Extraction:** Captures article titles, URLs, publication dates, and page numbers
- **Spanish Date Parsing:** Handles Spanish-language date formats
- **Statistical Analysis:** Generates comprehensive reports on publication patterns
- **Data Visualization:** Creates charts showing daily article production, timelines, and comparative statistics
- **Wayback Machine Integration:** Automatically archives sampled articles for evidence preservation
- **Checkpoint System:** Saves progress periodically to prevent data loss
- **CSV Export:** Exports all data in standard CSV format for further analysis

## Installation

```bash
git clone https://github.com/innermost47/q2bs.git
cd q2bs
python -m venv env
pip install -r requirements.txt
```

## Usage

### Basic Scraping

```bash
python main.py
```

The script will:

1. Detect the maximum number of blog pages (36,516+ as of December 2025)
2. Ask for confirmation before scraping
3. Scrape all articles systematically
4. Generate statistical reports
5. Create data visualizations
6. Optionally archive a sample to Wayback Machine

### Output Structure

After running, you'll get a timestamped directory:

```
q2b_audit_YYYYMMDD_HHMMSS/
├── articles.csv              # All articles with metadata
├── daily_summary.csv         # Articles per day
├── checkpoint.json           # Progress checkpoint
├── report.json              # Statistical analysis
├── archiving_checkpoint.json # Wayback archiving progress
├── articles_archived.csv    # Articles with archive URLs
├── archive_report.json      # Archiving statistics
├── wayback_urls.txt         # List of Wayback URLs
└── graphs/
    ├── 1_daily_articles.png     # Daily production chart
    ├── 2_timeline.png           # Publication timeline
    └── 3_stats_summary.png      # Statistical summary
```

## Key Findings (December 2025)

Based on analysis of the period November 20 - December 7, 2025:

- **144,966 articles documented** (partial dataset - computer crashed during scraping)
- **8,401 articles per day** on average
- **Peak day:** 10,251 articles (December 4, 2025)
- **Frequency:** 1 article every 10.3 seconds

For comparison (approximative):

- TechCrunch: ~40 articles/day
- The Verge: ~30 articles/day
- The New York Times: ~250 articles/day

## Files Description

### `q2b_studio_auditor.py`

Core scraping engine that:

- Fetches blog pages systematically
- Parses article metadata
- Handles Spanish date formats
- Generates statistical reports
- Manages checkpoints

### `q2b_data_visualizer.py`

Visualization module that creates:

- Daily article production bar charts
- Publication timeline graphs
- Comparative statistics with major publishers
- All charts with proper labeling and context

### `wayback_archiver.py`

Archiving system that:

- Submits URLs to Wayback Machine
- Checks for existing archives
- Handles retry logic for failed submissions
- Exports archive URLs for verification

### `main.py`

Entry point that orchestrates:

- User confirmation workflow
- Scraping execution
- Report generation
- Visualization creation
- Optional archiving

## Configuration

### Scraping Parameters

In `main.py`, you can adjust:

```python
# Scrape every Nth page (1 = all pages, 10 = every 10th page)
auditor.scrape_all_pages(max_page, start_page=1, sample_every=1)

# Archive sample size
archiver.archive_sample(sample_size=500)
```

### Rate Limiting

The script includes built-in delays to avoid overwhelming the target server:

- 0.5 seconds between page requests
- 3 seconds between Wayback Machine submissions
- 5-second retry delay on timeouts

## Ethical Considerations

This tool was developed for legitimate investigative purposes:

- Documenting publicly available information
- Analyzing content patterns
- Preserving evidence of plagiarism
- Supporting transparency in automated publishing

**Please use responsibly:**

- Respect robots.txt directives
- Don't overwhelm servers with requests
- Use for research and documentation purposes
- Comply with applicable laws and terms of service

## Known Issues

### Wayback Machine Archiving

The Wayback Machine integration may experience issues:

- **Timeout errors:** The Internet Archive's save service can be slow
- **Rate limiting:** Heavy usage may trigger temporary blocks
- **Archive verification:** Some archived URLs may not be immediately accessible
- **Incomplete snapshots:** Not all pages successfully archive on first attempt

**Workaround:** The script saves all URLs to `wayback_urls.txt` so you can verify archives manually or re-submit failed URLs later.

### Large Dataset Handling

For very large scrapes (30,000+ pages):

- Consider using `sample_every` parameter to sample pages
- Monitor disk space (CSV files can grow large)
- Be prepared for multi-hour runtime
- The checkpoint system helps recover from crashes

## Data Analysis Tips

### Using the CSV Files

```python
import pandas as pd

# Load articles
df = pd.read_csv('q2b_audit_TIMESTAMP/articles.csv')

# Find articles by keyword
keyword_articles = df[df['title'].str.contains('AI', case=False)]

# Articles by date
daily_counts = df['date_parsed'].value_counts().sort_index()

# Most common page numbers (detect patterns)
page_distribution = df['page_num'].value_counts()
```

### Checking for Your Content

```python
# Search for specific phrases
your_phrases = ['your unique phrase', 'another phrase']
matches = df[df['title'].str.contains('|'.join(your_phrases), case=False)]
print(f"Found {len(matches)} potential matches")
```

## Contributing

If you've experienced similar automated plagiarism or want to improve the tool:

1. Fork the repository
2. Create a feature branch
3. Add your improvements
4. Submit a pull request

Particularly welcome:

- Better date parsing for multilingual content
- Enhanced duplicate detection
- Content similarity analysis
- Additional visualization options

## Legal

This tool is provided for research, documentation, and investigative journalism purposes. Users are responsible for ensuring their use complies with applicable laws, including:

- Copyright law
- Computer fraud and abuse laws
- Terms of service agreements
- Data protection regulations

The author makes no warranties about the tool's functionality or the accuracy of data collected.

## Citation

If you use this tool in research or journalism, please cite:

```
CHARRETIER, A. (2025). Q2BSTUDIO Content Farm Auditor.
GitHub: https://github.com/innermost47/q2bs
Case study: https://dev.to/innermost_47/when-ai-content-systems-reproduce-content-without-attribution-a-documented-case-study-1h0g
```

## Contact

- **Author:** Anthony CHARRETIER
- **Website:** anthony-charretier.fr
- **GitHub:** https://github.com/innermost47

## License

MIT
