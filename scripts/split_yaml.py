"""Split monolithic sipuron.yml into separate year files."""
import yaml
import os

# Read the old monolithic file
with open('old_site_data/sipuron.yml', encoding='utf8') as f:
    data = yaml.safe_load(f)

# Create data directory if needed
os.makedirs('data', exist_ok=True)

# Write each year to its own file
for year_key, year_data in data.items():
    year = year_key.replace('year_', '')
    output_file = f'data/year_{year}.yml'
    
    with open(output_file, 'w', encoding='utf8') as f:
        yaml.dump(year_data, f, allow_unicode=True)
    
    print(f"Created {output_file} with {len(year_data.get('stories', []))} stories")

print(f"\nTotal: {len(data)} year files created in data/ directory")
