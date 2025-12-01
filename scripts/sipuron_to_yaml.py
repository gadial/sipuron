import os, sys
from typing_extensions import runtime
import yaml,csv

csv_filename = sys.argv[1]
yaml_filename = os.path.splitext(csv_filename)[0] + ".yaml"

stories = []
keywords = []
authors = []
with open(csv_filename, encoding="utf8") as csvfile:
    datareader = csv.reader(csvfile, delimiter=",", quotechar='"')
    for row_index, row in enumerate(datareader):
        if row_index == 0:
            continue
        if row[2] == '':
            keyword = ''
        else:
            keyword = row[2].split(" ")[1]
        stories.append({
            'time': row[0], 
            'author': row[1], 
            'keyword': keyword, 
            'story': row[3],
            'length': len(row[3])
            })
        if not row[1] in authors:
            authors.append(row[1])
        if not keyword in keywords:
            keywords.append(keyword)

result = {
    'year_2025': {
        'stories': stories,
        'keywords': keywords,
        'authors': authors
    }
}
print(yaml_filename)
with open(yaml_filename, 'w', encoding="utf8") as yamlfile:
    yaml.dump(result, yamlfile, allow_unicode=True)