# Sipuron Project - AI Coding Agent Instructions

## Project Overview
Sipuron (סיפורונובמבר) is a Hebrew-language creative writing website for micro-fiction stories. Stories are collected via Google Forms, converted from CSV to YAML, and generated as static HTML pages with client-side filtering.

**Migration Status**: Migrating from Jekyll to pure Python static site generator. Jekyll-based code in `pages/` and `old_site_data/` directories are legacy - do NOT use Jekyll syntax in new code.

## Architecture & Data Flow

1. **Data Collection**: Stories submitted via Google Forms → exported as CSV
2. **Data Processing**: `scripts/sipuron_to_yaml.py` converts CSV → year-specific YAML files
3. **Data Storage**: Separate YAML file per year: `data/year_2025.yml`, `data/year_2024.yml`, etc.
4. **Generation**: Python script generates static HTML to `output/` directory
5. **Hosting**: Deployed to `https://gadial.net/sipuron` via GitHub Pages subfolder mounting

### CSV to YAML Conversion
- **Script**: `scripts/sipuron_to_yaml.py`
- **Usage**: `python scripts/sipuron_to_yaml.py <csv_filename>`
- **Input CSV**: `time, author, keyword, story` (keyword extracted from column 2 after first space)
- **Output**: `data/year_YYYY.yml` (auto-detected from filename or current date)
- **Structure**:
  ```yaml
  stories: [{time, author, keyword, story, length}, ...]
  keywords: [unique keywords list]
  authors: [unique authors list]
  ```
- **Note**: Script should extract year from CSV filename or use current year

### Static HTML Generation
- **Input**: Year-specific YAML files from `data/` directory
- **Output**: Static HTML files to `output/` directory:
  - `output/index.html` - landing page with Google Form iframe
  - `output/list_2025.html` - current year stories
  - `output/list_2024.html` - archived year stories
- **Template approach**: Use Python (Jinja2 or string templating) to generate HTML
- **Embedded assets**: Inline CSS and JavaScript (list.js + jQuery filtering logic) in each HTML file

## Story Data Structure
Each story has 5 fields:
- `time`: Submission timestamp
- `author`: Participant identifier
- `keyword`: Writing prompt word
- `story`: Micro-fiction text (preserve line breaks)
- `length`: Character count

## Interactive Features (JavaScript)
All list pages include:
- **list.js**: Client-side search/sort/filter (CDN: `//cdnjs.cloudflare.com/ajax/libs/list.js/1.5.0/list.min.js`)
- **jQuery**: Multi-select filter UI logic
- **Features**: Search in story text, sort by author/keyword/length, filter by author/keyword dropdowns
- **Hebrew/RTL**: All UI labels and text in Hebrew

## Key Conventions

### Language & Encoding
- **Primary language**: Hebrew (RTL text)
- **Encoding**: UTF-8 everywhere (`encoding="utf8"` in Python file I/O)
- **YAML**: `allow_unicode=True` in yaml.dump()
- **HTML**: `<meta charset="utf-8">` and `dir="rtl"` attributes

### File Organization
```
data/year_YYYY.yml          # Year-specific story data
scripts/sipuron_to_yaml.py  # CSV → YAML converter
scripts/generate_site.py    # YAML → HTML generator (to be created)
output/                     # Generated static HTML files
old_site_data/              # Legacy Jekyll data (ignore)
pages/                      # Legacy Jekyll templates (reference only)
```

## Common Workflows

### Adding New Year's Stories
1. Download CSV from Google Forms
2. Run: `python scripts/sipuron_to_yaml.py <filename>.csv`
3. Run: `python scripts/generate_site.py` (generates all HTML files)
4. Deploy: Copy `output/` contents to GitHub Pages repository

### Regenerating Site
```bash
python scripts/generate_site.py
```
Reads all `data/year_*.yml` files and regenerates entire `output/` directory.

### CSS Improvements
Current CSS is minimal. Consider:
- Better typography for Hebrew text
- Responsive design for mobile
- Improved spacing and visual hierarchy
- Better filter/sort UI controls
- Story card styling

## GitHub Pages Hosting
**Target URL**: `https://gadial.net/sipuron`

**Strategy**: Mount this project as subdirectory of main site:
- Main site: `gadial/blog` repository → `https://gadial.net`
- This project: Separate repository with `output/` as root
- GitHub Pages configuration: Custom domain subfolder or submodule approach

**Deployment**: Owner needs to configure DNS/subdirectory routing (see deployment docs).

## Dependencies
- **Python**: `yaml`, `csv`, `jinja2` (for HTML generation)
- **Frontend**: list.js (CDN), jQuery 3.4.1 (CDN)
- **Hosting**: GitHub Pages

## Migration Notes
- `pages/*.md` files use Jekyll Liquid syntax - convert to Python templates
- `old_site_data/sipuron.yml` is monolithic - split into separate year files
- All Jekyll data access (`site.data.sipuron.year_XXXX`) becomes Python YAML loading
