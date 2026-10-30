"""Generate static HTML pages for Sipuron stories."""
import yaml
import os
from pathlib import Path
from datetime import datetime

def load_year_data(year):
    """Load story data for a specific year."""
    yaml_file = f'data/year_{year}.yml'
    if not os.path.exists(yaml_file):
        return None
    
    with open(yaml_file, encoding='utf8') as f:
        return yaml.safe_load(f)

def generate_list_page(year, data, is_current_year=False):
    """Generate HTML for a year's story list page."""
    
    stories = data.get('stories', [])
    authors = data.get('authors', [])
    keywords = data.get('keywords', [])
    
    # Build story HTML
    stories_html = []
    for story in stories:
        story_text = story['story'].replace('\n', '<br>')
        stories_html.append(f'''
        <li>
            <div class="story-card">
                <div class="story-meta">
                    <h2 class="author">{story['author']}</h2>
                    <span class="keyword">{story['keyword']}</span>
                </div>
                <p class="story">{story_text}</p>
                <div hidden class="length">{story['length']}</div>
            </div>
        </li>''')
    
    stories_list = '\n'.join(stories_html)
    
    # Build author options
    author_options = '\n'.join([f'<option value="{author}">{author}</option>' for author in authors])
    
    # Build keyword options
    keyword_options = '\n'.join([f'<option value="{keyword}">{keyword}</option>' for keyword in keywords])
    
    # Page title
    title = f'סיפורונובמבר {year}' if not is_current_year else 'סיפורונובמבר - הסיפורים'
    
    html = f'''<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/list.js/1.5.0/list.min.js"></script>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
    <style>
        * {{
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
            padding: 20px;
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            padding: 30px;
        }}
        
        h1 {{
            color: #764ba2;
            text-align: center;
            margin-bottom: 10px;
            font-size: 2.5em;
        }}
        
        .back-link {{
            text-align: center;
            margin-bottom: 20px;
        }}
        
        .back-link a {{
            color: #667eea;
            text-decoration: none;
            font-size: 1.1em;
        }}
        
        .back-link a:hover {{
            text-decoration: underline;
        }}
        
        .controls {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 30px;
        }}
        
        .control-group {{
            margin-bottom: 15px;
        }}
        
        .control-group:last-child {{
            margin-bottom: 0;
        }}
        
        label {{
            display: block;
            font-weight: bold;
            color: #333;
            margin-bottom: 5px;
        }}
        
        input[type="text"].search {{
            width: 100%;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 6px;
            font-size: 16px;
            transition: border-color 0.3s;
        }}
        
        input[type="text"].search:focus {{
            outline: none;
            border-color: #667eea;
        }}
        
        .button-group {{
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            margin-bottom: 15px;
        }}
        
        button.sort {{
            background: #667eea;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
            transition: background 0.3s;
        }}
        
        button.sort:hover {{
            background: #764ba2;
        }}
        
        select {{
            width: 100%;
            padding: 10px;
            border: 2px solid #ddd;
            border-radius: 6px;
            font-size: 14px;
            background: white;
        }}
        
        select:focus {{
            outline: none;
            border-color: #667eea;
        }}
        
        .list {{
            list-style: none;
            padding: 0;
            margin: 0;
        }}
        
        .list li {{
            margin-bottom: 20px;
        }}
        
        .story-card {{
            background: white;
            border: 1px solid #e0e0e0;
            border-right: 4px solid #667eea;
            border-radius: 8px;
            padding: 20px;
            transition: box-shadow 0.3s, transform 0.2s;
        }}
        
        .story-card:hover {{
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            transform: translateY(-2px);
        }}
        
        .story-meta {{
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 15px;
            flex-wrap: wrap;
        }}
        
        .story-meta h2 {{
            margin: 0;
            font-size: 1.3em;
            color: #333;
        }}
        
        .keyword {{
            background: #667eea;
            color: white;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: bold;
        }}
        
        .length-tag {{
            background: #e0e0e0;
            color: #666;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.85em;
        }}
        
        .story {{
            color: #444;
            line-height: 1.8;
            font-size: 1.05em;
            margin: 0;
            white-space: pre-line;
        }}
        
        @media (max-width: 768px) {{
            body {{
                padding: 10px;
            }}
            
            .container {{
                padding: 15px;
            }}
            
            h1 {{
                font-size: 1.8em;
            }}
            
            .button-group {{
                flex-direction: column;
            }}
            
            button.sort {{
                width: 100%;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>רשימת הסיפורונים של סיפורונובמבר {year}</h1>
        <div class="back-link">
            <a href="index.html">← חזרה לעמוד הראשי</a>
        </div>
        
        <div id="sipuron-list">
            <div class="controls">
                <div class="control-group">
                    <label for="story-search">חיפוש בטקסט הסיפורים</label>
                    <input type="text" class="search" id="story-search" placeholder="הקלידו טקסט לחיפוש..."/>
                </div>
                
                <div class="control-group">
                    <label>מיון</label>
                    <div class="button-group">
                        <button class="sort" data-sort="author">מיון לפי שם מזהה</button>
                        <button class="sort" data-sort="keyword">מיון לפי מילת מפתח</button>
                        <button class="sort" data-sort="length">מיון לפי אורך</button>
                    </div>
                </div>
                
                <div class="control-group">
                    <label for="authors_filter">סינון לפי שם מזהה</label>
                    <select name="authors" id="authors_filter" multiple size="5">
                        <option value="הכל">הכל</option>
                        {author_options}
                    </select>
                </div>
                
                <div class="control-group">
                    <label for="keywords_filter">סינון לפי מילת מפתח</label>
                    <select name="keywords" id="keywords_filter" multiple size="5">
                        <option value="הכל">הכל</option>
                        {keyword_options}
                    </select>
                </div>
            </div>
            
            <ul class="list">
                {stories_list}
            </ul>
        </div>
    </div>
    
    <script type="text/javascript">
    $(document).ready(function(){{
        var options = {{
            valueNames: ['author', 'keyword', 'length', 'story'],
            searchColumns: ['story']
        }};
        var postList = new List('sipuron-list', options);
        
        // Store all stories data for cross-filtering
        var allStories = postList.items.map(function(item) {{
            return {{
                author: item.values().author,
                keyword: item.values().keyword
            }};
        }});
        
        // Store all original options
        var allAuthors = [];
        var allKeywords = [];
        $('#authors_filter option').each(function() {{
            if ($(this).val() !== "הכל") {{
                allAuthors.push($(this).val());
            }}
        }});
        $('#keywords_filter option').each(function() {{
            if ($(this).val() !== "הכל") {{
                allKeywords.push($(this).val());
            }}
        }});
        
        function passes_filters(item){{
            var selected_authors = $('#authors_filter').val();
            var selected_keywords = $('#keywords_filter').val();
            
            if ((selected_authors.includes("הכל") || selected_authors.length == 0 || selected_authors.includes(item.values().author)) &&
                (selected_keywords.includes("הכל") || selected_keywords.length == 0 || selected_keywords.includes(item.values().keyword))){{
                return true;
            }} else {{
                return false;
            }}
        }}
        
        function updateFilterOptions() {{
            var selected_authors = $('#authors_filter').val() || [];
            var selected_keywords = $('#keywords_filter').val() || [];
            
            // Remove "הכל" from selections for filtering logic
            selected_authors = selected_authors.filter(function(a) {{ return a !== "הכל"; }});
            selected_keywords = selected_keywords.filter(function(k) {{ return k !== "הכל"; }});
            
            // Get available authors based on selected keywords
            var availableAuthors = new Set();
            var availableKeywords = new Set();
            
            allStories.forEach(function(story) {{
                var keywordMatch = selected_keywords.length === 0 || selected_keywords.includes(story.keyword);
                var authorMatch = selected_authors.length === 0 || selected_authors.includes(story.author);
                
                if (keywordMatch) {{
                    availableAuthors.add(story.author);
                }}
                if (authorMatch) {{
                    availableKeywords.add(story.keyword);
                }}
            }});
            
            // Rebuild author options
            var currentAuthors = $('#authors_filter').val() || [];
            $('#authors_filter').empty();
            $('#authors_filter').append('<option value="הכל">הכל</option>');
            
            allAuthors.forEach(function(author) {{
                if (availableAuthors.has(author)) {{
                    var selected = currentAuthors.includes(author) ? ' selected' : '';
                    $('#authors_filter').append('<option value="' + author + '"' + selected + '>' + author + '</option>');
                }}
            }});
            
            // Rebuild keyword options
            var currentKeywords = $('#keywords_filter').val() || [];
            $('#keywords_filter').empty();
            $('#keywords_filter').append('<option value="הכל">הכל</option>');
            
            allKeywords.forEach(function(keyword) {{
                if (availableKeywords.has(keyword)) {{
                    var selected = currentKeywords.includes(keyword) ? ' selected' : '';
                    $('#keywords_filter').append('<option value="' + keyword + '"' + selected + '>' + keyword + '</option>');
                }}
            }});
        }}
        
        // Handle click to deselect
        $('#authors_filter, #keywords_filter').on('mousedown', 'option', function(e) {{
            e.preventDefault();
            var select = $(this).parent();
            var option = $(this);
            
            if (option.prop('selected')) {{
                option.prop('selected', false);
            }} else {{
                option.prop('selected', true);
            }}
            
            select.trigger('change');
            return false;
        }});
        
        $('#authors_filter').change(function() {{
            updateFilterOptions();
            postList.filter(passes_filters);
        }});
        
        $('#keywords_filter').change(function() {{
            updateFilterOptions();
            postList.filter(passes_filters);
        }});
    }});
    </script>
</body>
</html>'''
    
    return html

def generate_index_page(available_years):
    """Generate the main index page with links to all years."""
    
    # Build year links
    year_links = []
    for year in sorted(available_years, reverse=True):
        if year == datetime.now().year:
            year_links.append(f'<li><a href="list_{year}.html">סיפורונים של שנת {year} (שנה נוכחית)</a></li>')
        else:
            year_links.append(f'<li><a href="list_{year}.html">סיפורונים של שנת {year}</a></li>')
    
    links_html = '\n'.join(year_links)
    
    html = f'''<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>סיפורונובמבר</title>
    <style>
        * {{
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
            padding: 20px;
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            padding: 40px;
        }}
        
        h1 {{
            color: #764ba2;
            text-align: center;
            margin-bottom: 30px;
            font-size: 3em;
        }}
        
        .intro {{
            text-align: center;
            margin-bottom: 40px;
            font-size: 1.2em;
            color: #555;
        }}
        
        .year-links {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 40px;
        }}
        
        .year-links h2 {{
            color: #333;
            margin-top: 0;
            margin-bottom: 15px;
        }}
        
        .year-links ul {{
            list-style: none;
            padding: 0;
            margin: 0;
        }}
        
        .year-links li {{
            margin-bottom: 10px;
        }}
        
        .year-links a {{
            display: block;
            padding: 12px 20px;
            background: white;
            color: #667eea;
            text-decoration: none;
            border-radius: 6px;
            border: 2px solid #667eea;
            transition: all 0.3s;
            font-size: 1.1em;
        }}
        
        .year-links a:hover {{
            background: #667eea;
            color: white;
            transform: translateX(-5px);
        }}
        
        .form-section {{
            margin-top: 40px;
        }}
        
        .form-section h2 {{
            color: #764ba2;
            text-align: center;
            margin-bottom: 20px;
        }}
        
        iframe {{
            width: 100%;
            border: none;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }}
        
        @media (max-width: 768px) {{
            body {{
                padding: 10px;
            }}
            
            .container {{
                padding: 20px;
            }}
            
            h1 {{
                font-size: 2em;
            }}
            
            iframe {{
                min-height: 1500px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>סיפורונובמבר</h1>
        
        <div class="intro">
            <p>ברוכות וברוכים הבאים לאתר סיפורונובמבר!</p>
        </div>
        
        <div class="year-links">
            <h2>צפייה בסיפורים</h2>
            <ul>
                {links_html}
            </ul>
        </div>
        
        <div class="form-section">
            <h2>הגשת סיפור חדש</h2>
            <iframe src="https://docs.google.com/forms/d/e/1FAIpQLSfClQAom_bDmTV9QTgIt3T4VH9x3f_5rs1LIRZpxKkXq0EuQQ/viewform?embedded=true" width="640" height="1792" frameborder="0" marginheight="0" marginwidth="0">Loading…</iframe>
        </div>
    </div>
</body>
</html>'''
    
    return html

def main():
    """Generate all HTML pages."""
    # Create output directory (docs for GitHub Pages)
    os.makedirs('docs', exist_ok=True)
    
    # Find all year files
    data_dir = Path('data')
    year_files = sorted(data_dir.glob('year_*.yml'))
    
    available_years = []
    current_year = datetime.now().year
    
    # Generate list page for each year
    for year_file in year_files:
        year = year_file.stem.replace('year_', '')
        year_num = int(year)
        
        if year_num not in available_years:
            available_years.append(year_num)
        
        data = load_year_data(year)
        if data:
            is_current = year_num == current_year
            html = generate_list_page(year, data, is_current)
            
            output_file = f'docs/list_{year}.html'
            with open(output_file, 'w', encoding='utf8') as f:
                f.write(html)
            
            print(f"Generated {output_file} ({len(data.get('stories', []))} stories)")
    
    # Generate index page
    index_html = generate_index_page(available_years)
    with open('docs/index.html', 'w', encoding='utf8') as f:
        f.write(index_html)
    
    print(f"\nGenerated docs/index.html")
    print(f"\nTotal: {len(available_years)} list pages + 1 index page")
    print(f"All files ready in docs/ directory!")

if __name__ == '__main__':
    main()
