# Sipuron - סיפורונובמבר

A Hebrew-language creative writing website for micro-fiction stories, generated as a static site.

## Overview

Sipuron collects short stories (micro-fiction) via Google Forms and displays them on year-based pages with interactive filtering and search capabilities.

## Project Structure

```
sipuron/
├── data/                    # YAML data files (one per year)
│   ├── year_2021.yml
│   ├── year_2022.yml
│   ├── year_2023.yml
│   ├── year_2024.yml
│   ├── year_2025.yml
│   └── year_2026.yml
├── scripts/                 # Python tools
│   ├── sipuron_to_yaml.py  # CSV → YAML converter
│   ├── generate_site.py    # YAML → HTML generator
│   └── split_yaml.py       # One-time migration script
├── docs/                    # Generated static site (served by GitHub Pages)
│   ├── index.html
│   ├── list_2021.html
│   ├── list_2022.html
│   └── ...
├── old_site_data/          # Legacy Jekyll data (archived)
└── pages/                  # Legacy Jekyll templates (archived)
```

## Quick Start

### Adding New Stories

1. **Download CSV** from Google Forms
2. **Convert to YAML** (this replaces that year's complete data file):
   ```bash
   python3 scripts/sipuron_to_yaml.py stories_2026.csv
   # If the filename has no year:
   python3 scripts/sipuron_to_yaml.py responses.csv --year 2026
   ```
3. **Generate site**:
   ```bash
   python3 scripts/generate_site.py
   ```
4. Commit and push `data/` and `docs/`; GitHub Pages serves `docs/`.

## Features

### Story List Pages
- **Search**: Full-text search in story content
- **Sort**: By author, keyword, or length
- **Filter**: Multi-select dropdowns for authors and keywords
- **Responsive**: Mobile-friendly design
- **RTL Support**: Proper Hebrew text rendering

### Modern Design
- Gradient purple background
- Card-based story layout
- Hover effects and smooth transitions
- Tag-style keyword display
- Clean, accessible typography

## Data Format

### YAML Structure (per year file)
```yaml
stories:
  - time: "2025-11-01 10:30:00"
    author: "כותב/ת"
    keyword: "מילת_מפתח"
    story: "טקסט הסיפור..."
    length: 150
keywords:
  - "מילת_מפתח_1"
  - "מילת_מפתח_2"
authors:
  - "כותב/ת_1"
  - "כותב/ת_2"
```

### CSV Input Format
Google Forms exports with columns:
- Column 0: Timestamp
- Column 1: Author name
- Column 2: "כתבו: [keyword]" (keyword extracted after space)
- Column 3: Story text

## Scripts

### `sipuron_to_yaml.py`
Converts CSV from Google Forms to YAML format.

**Usage**:
```bash
python scripts/sipuron_to_yaml.py <csv_filename>
```

**Output**: `data/year_YYYY.yml` (year read from the filename or `--year`)

### `generate_site.py`
Generates complete static HTML site from YAML data files.

**Usage**:
```bash
python scripts/generate_site.py
```

**Output**: All HTML files in `docs/` directory

**Features**:
- Single template for all year pages
- Embedded CSS and JavaScript (no external files needed)
- Automatic year detection for current vs. archived pages
- Index page with links to all years

## Deployment

The `docs/` directory contains the complete static site. Deploy it to:
- **Target URL**: `https://gadial.net/sipuron`
- **Method**: See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions

Options:
1. Separate GitHub repository with submodule integration
2. Direct copy to main blog repository's `sipuron/` subfolder
3. GitHub Actions automation

## Dependencies

**Python**:
- `yaml` (PyYAML)
- `csv` (built-in)
- `os`, `pathlib` (built-in)
- `datetime` (built-in)

**Frontend** (CDN):
- list.js 1.5.0
- jQuery 3.4.1

## Development

### Modifying the Design

Edit `scripts/generate_site.py`:
- CSS is in the `<style>` block of `generate_list_page()` and `generate_index_page()`
- JavaScript filtering logic is at the bottom of `generate_list_page()`
- HTML structure can be modified in the template strings

### Testing Locally

The generated HTML files can be opened directly in a browser:
```bash
python scripts/generate_site.py
cd docs
start index.html  # Windows
# or
open index.html   # macOS
# or
xdg-open index.html  # Linux
```

## Migration from Jekyll

This project was migrated from Jekyll to a pure Python static generator:
- **Old**: Jekyll templates in `pages/`, data in `old_site_data/sipuron.yml`
- **New**: Python generator with year-separated YAML files

Legacy files are kept for reference but are not used in generation.

## License

Created for the Sipuron creative writing community.

## Support

For questions or issues, contact the site owner at gadial.net.
