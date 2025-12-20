# Q2BSTUDIO Auditor

![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

A Python-based investigation tool for analyzing industrial-scale automated content generation systems. Developed to document and analyze the publishing patterns of q2bstudio.com.

## Featured Investigation

**This case was investigated and published by Numerama (December 2024):**  
[Qui sont ces parasites qui pillent les articles à l'ère de l'IA ? On a remonté la piste d'une immense ferme à contenus](https://www.numerama.com/cyberguerre/2140051-qui-sont-ces-parasites-qui-pillent-les-articles-a-lere-de-lia-on-a-remonte-la-piste-dune-immense-ferme-a-contenus.html)

The investigation revealed an industrial-scale AI content farm publishing up to **10,275 articles per day** (one every 8.4 seconds), with over **210,000 articles** documented.

---

## Background

This tool was created following the discovery that my technical article about [OBSIDIAN Neural](https://github.com/innermost47/ai-dj) (an open-source AI music VST plugin) was reproduced, translated, and republished with commercial links injected by Q2BSTUDIO's automated system.

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

## Requirements

- Python 3.10+
- pip (Python package manager)

### Python Dependencies

```bash
requests
beautifulsoup4
matplotlib
```

All dependencies are listed in `requirements.txt` and will be installed automatically.

## Installation

```bash
git clone https://github.com/innermost47/q2bs.git
cd q2bs
python -m venv env
source env/bin/activate  # On macOS/Linux
# or: env\Scripts\activate  # On Windows
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

### Resume from Checkpoint

The auditor includes a checkpoint system that allows you to resume interrupted scraping sessions:

```bash
python main.py
```

When you run the script, you'll be presented with:

1. A list of existing checkpoint directories
2. Option to select a checkpoint to resume from
3. Option to start fresh (new scraping)
4. Option to visualize-only mode (skip scraping)

**The script automatically:**

- Calculates which page to resume from based on article IDs
- Avoids duplicate articles
- Continues in the same output directory
- Preserves all previously scraped data

**Example workflow:**

```
Available checkpoints:
0. Start fresh (new scraping)
1. q2b_audit_20251208_103810 - 242,191 articles - 2025-12-08T10:38:10

Select checkpoint number (0 for fresh start): 1
Visualize only (skip scraping)? (yes/no): no

Loading checkpoint from: q2b_audit_20251208_103810
Loaded 242,191 articles from checkpoint
Min article ID scraped (last article): 91,643
Calculated resume page: 27,373

Resuming from page 27,373
This will scrape 10,184 pages (from 27,373 to 37,556). Continue? (yes/no):
```

### Visualization-Only Mode

If you want to regenerate visualizations without re-scraping:

```bash
python main.py
```

Then:

1. Select an existing checkpoint
2. Answer "yes" to "Visualize only (skip scraping)?"

This will:

- Load the existing data
- Regenerate all reports
- Create fresh visualizations
- Skip the scraping phase entirely

**Use cases:**

- Update graphs with new styling
- Generate reports after manual data cleaning
- Create visualizations for different time periods

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

For comparison (industry estimates - approximate):

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

Main entry point that orchestrates:

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

### Sample Visualizations

The tool generates three types of visualizations:

#### 1. Statistical Summary (Last 4 weeks)

![Stats Summary Example](graphs/3_stats_summary.png)

#### 2. Publication Timeline

![Timeline Example](graphs/2_timeline.png)

#### 3. Daily Production

![Daily Production Example](graphs/1_daily_articles.png)

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
CHARRETIER, A. (2025). Q2BSTUDIO Auditor.
GitHub: https://github.com/innermost47/q2bs
Case study: https://dev.to/innermost_47/when-ai-content-systems-reproduce-content-without-attribution-a-documented-case-study-1h0g
```

## Contact

- **Author:** Anthony CHARRETIER
- **Website:** https://anthony-charretier.fr
- **GitHub:** https://github.com/innermost47

## License

MIT License

Copyright (c) 2025 Anthony CHARRETIER

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
