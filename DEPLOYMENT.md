# GitHub Pages and yearly update workflow

## Current repository setup

This repository already keeps the generated GitHub Pages site in `docs/`. Configure
GitHub Pages once with **Deploy from a branch**, branch `main`, folder `/docs`.

For each full Google Forms CSV export:

```bash
python3 scripts/sipuron_to_yaml.py stories_2026.csv
python3 scripts/generate_site.py
git add data/year_2026.yml docs/
git commit -m "Update 2026 stories"
git push
```

The import replaces the year's YAML file from the complete CSV export, so repeat
submissions are not appended or duplicated.

The older alternatives below are retained as historical deployment notes.

This document explains how to host the Sipuron project at `https://gadial.net/sipuron` as a subfolder of your main site.

## Architecture Overview

- **Main site**: `gadial/blog` repository → `https://gadial.net`
- **Sipuron project**: Separate repository → `https://gadial.net/sipuron`

## Option 1: Separate Repository with Custom Domain (Recommended)

This is the cleanest approach for maintaining separate projects.

### Steps:

1. **Create a new GitHub repository** for Sipuron:
   - Repository name: `sipuron` (or any name you prefer)
   - Make it public

2. **Push the output directory** to the new repository:
   ```bash
   cd output
   git init
   git add .
   git commit -m "Initial Sipuron site"
   git branch -M main
   git remote add origin https://github.com/gadial/sipuron.git
   git push -u origin main
   ```

3. **Enable GitHub Pages** for the sipuron repository:
   - Go to repository Settings → Pages
   - Source: Deploy from branch `main` / root folder
   - Custom domain: `gadial.net` (will be overridden with path)

4. **Configure DNS in your main blog repository**:
   
   In your `gadial/blog` repository, you need to set up URL rewrites or use GitHub's subpath mounting.
   
   **Method A: Using GitHub Actions (Recommended)**
   
   Create `.github/workflows/deploy-sipuron.yml` in your `blog` repository:
   
   ```yaml
   name: Deploy Sipuron Subfolder
   on:
     workflow_dispatch:
     schedule:
       - cron: '0 0 * * 0'  # Weekly on Sunday
   
   jobs:
     deploy:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v3
           with:
             repository: gadial/sipuron
             path: sipuron
         
         - name: Copy to blog
           run: |
             mkdir -p sipuron-output
             cp -r sipuron/* sipuron-output/
         
         - uses: actions/checkout@v3
           with:
             repository: gadial/blog
             path: blog
             token: ${{ secrets.GITHUB_TOKEN }}
         
         - name: Deploy subfolder
           run: |
             mkdir -p blog/sipuron
             cp -r sipuron-output/* blog/sipuron/
             cd blog
             git config user.name github-actions
             git config user.email github-actions@github.com
             git add sipuron
             git commit -m "Update Sipuron subfolder"
             git push
   ```

   **Method B: Git Submodules**
   
   In your `blog` repository:
   ```bash
   cd blog
   git submodule add https://github.com/gadial/sipuron.git sipuron
   git commit -m "Add Sipuron as submodule"
   git push
   ```
   
   Update the submodule when sipuron changes:
   ```bash
   git submodule update --remote sipuron
   git commit -am "Update Sipuron submodule"
   git push
   ```

## Option 2: Direct Integration (Simpler but Less Modular)

Keep the Sipuron output directly in the `blog` repository:

1. **In your blog repository**, create a `sipuron/` directory:
   ```bash
   cd ~/path/to/blog
   mkdir -p sipuron
   ```

2. **Copy the generated files**:
   ```bash
   cp -r ~/path/to/sipuron/output/* sipuron/
   git add sipuron
   git commit -m "Add Sipuron site"
   git push
   ```

3. **Update workflow**: Whenever you update Sipuron:
   ```bash
   # In sipuron project
   python scripts/generate_site.py
   
   # Copy to blog
   cp -r output/* ~/path/to/blog/sipuron/
   
   # Commit in blog repo
   cd ~/path/to/blog
   git add sipuron
   git commit -m "Update Sipuron stories"
   git push
   ```

## Automated Deployment Script

Create `scripts/deploy_to_blog.py` in the Sipuron project:

```python
"""Deploy generated site to the blog repository."""
import os
import shutil
import sys

BLOG_REPO_PATH = os.path.expanduser('~/path/to/blog')
SIPURON_SUBFOLDER = 'sipuron'

def deploy():
    if not os.path.exists(BLOG_REPO_PATH):
        print(f"Error: Blog repository not found at {BLOG_REPO_PATH}")
        sys.exit(1)
    
    # Regenerate site
    print("Generating site...")
    os.system('python scripts/generate_site.py')
    
    # Copy to blog
    target = os.path.join(BLOG_REPO_PATH, SIPURON_SUBFOLDER)
    print(f"Copying to {target}...")
    
    if os.path.exists(target):
        shutil.rmtree(target)
    
    shutil.copytree('output', target)
    print("Deployment complete!")
    print(f"\nNext steps:")
    print(f"  cd {BLOG_REPO_PATH}")
    print(f"  git add {SIPURON_SUBFOLDER}")
    print(f"  git commit -m 'Update Sipuron'")
    print(f"  git push")

if __name__ == '__main__':
    deploy()
```

## Verification

After deployment, your site should be accessible at:
- Main page: `https://gadial.net/sipuron/`
- Year pages: `https://gadial.net/sipuron/list_2025.html`

## Updating the Site

Complete workflow for adding new stories:

```bash
# 1. Download CSV from Google Forms and save as stories_2025.csv

# 2. Convert to YAML
python scripts/sipuron_to_yaml.py stories_2025.csv

# 3. Copy to data directory (if needed)
# The script already outputs to data/year_2025.yml

# 4. Regenerate site
python scripts/generate_site.py

# 5. Deploy (Option 1: separate repo)
cd output
git add .
git commit -m "Update stories"
git push

# OR Deploy (Option 2: direct integration)
python scripts/deploy_to_blog.py
cd ~/path/to/blog
git add sipuron
git commit -m "Update Sipuron stories"
git push
```

## Notes

- The `output/` directory is the complete static site - all files are self-contained
- No server-side processing required - pure HTML/CSS/JavaScript
- All CSS and JavaScript are embedded in the HTML files for portability
- Hebrew RTL text is properly configured with `dir="rtl"` and UTF-8 encoding
