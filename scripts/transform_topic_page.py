#!/usr/bin/env python3
"""
Transform topic pages to match knowledge-engineering.html template.

Usage:
    python scripts/transform_topic_page.py pages/data-engineering.html
"""

import sys
import re
from pathlib import Path
from bs4 import BeautifulSoup
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Resource:
    url: str
    title: str
    source: str
    author: str
    time: str
    description: str
    category: str

def extract_resources(html_path: str) -> Dict[str, List[Resource]]:
    """Extract all resources from old-format topic page."""
    with open(html_path, 'r') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    resources_by_category = {}
    current_category = "Uncategorized"

    # Find all category headers and links
    reading_section = soup.find('section', class_='topic-reading')
    if not reading_section:
        reading_section = soup.find('main')

    if not reading_section:
        print(f"Warning: Could not find reading section in {html_path}")
        return {}

    # Iterate through all elements to maintain category context
    for element in reading_section.find_all(['h3', 'a']):
        if element.name == 'h3' and 'tcat' in element.get('class', []):
            current_category = element.get_text(strip=True)
            if current_category not in resources_by_category:
                resources_by_category[current_category] = []

        elif element.name == 'a' and 'tlink' in element.get('class', []):
            resource = Resource(
                url=element.get('href', ''),
                title=element.find('span', class_='tlink-title').get_text(strip=True) if element.find('span', class_='tlink-title') else '',
                source=element.find('span', class_='tlink-src').get_text(strip=True) if element.find('span', class_='tlink-src') else '',
                author=element.find('span', class_='tlink-author').get_text(strip=True) if element.find('span', class_='tlink-author') else '',
                time=element.find('span', class_='tlink-time').get_text(strip=True) if element.find('span', class_='tlink-time') else '',
                description=element.find('span', class_='tlink-desc').get_text(strip=True) if element.find('span', class_='tlink-desc') else '',
                category=current_category
            )

            if current_category not in resources_by_category:
                resources_by_category[current_category] = []
            resources_by_category[current_category].append(resource)

    return resources_by_category

def extract_context_content(html_path: str) -> dict:
    """Extract context panel content (lede, stat, terms)."""
    with open(html_path, 'r') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    content = {
        'title': '',
        'lede': '',
        'stat_num': '',
        'stat_label': '',
        'terms': [],
        'patterns': [],
        'accent_color': '#f97316',
        'next_page': '',
        'prev_page': '../index.html'
    }

    # Get title
    title_el = soup.find('h1', class_='topic-title')
    if title_el:
        content['title'] = title_el.get_text(strip=True)

    # Get lede
    lede_el = soup.find('p', class_='topic-lede')
    if lede_el:
        content['lede'] = str(lede_el.decode_contents())

    # Get stat
    stat_box = soup.find('div', class_='topic-stat-box')
    if stat_box:
        num_el = stat_box.find('span', class_='topic-stat-num')
        label_el = stat_box.find('span', class_='topic-stat-label')
        if num_el:
            content['stat_num'] = num_el.get_text(strip=True)
        if label_el:
            content['stat_label'] = label_el.get_text(strip=True)

    # Get terms
    terms_grids = soup.find_all('div', class_='topic-terms-grid')
    for i, grid in enumerate(terms_grids):
        terms_list = content['terms'] if i == 0 else content['patterns']
        for term in grid.find_all('div', class_='tterm'):
            name_el = term.find('span', class_='tterm-name')
            def_el = term.find('span', class_='tterm-def')
            if name_el and def_el:
                terms_list.append({
                    'name': name_el.get_text(strip=True),
                    'definition': def_el.get_text(strip=True)
                })

    # Get accent color from indicator
    indicator = soup.find('span', class_='topic-indicator')
    if indicator and indicator.get('style'):
        match = re.search(r'background:\s*(#[a-fA-F0-9]+)', indicator.get('style', ''))
        if match:
            content['accent_color'] = match.group(1)

    # Get navigation links
    next_link = soup.find('a', class_='topic-next')
    if next_link:
        content['next_page'] = next_link.get('href', '')

    return content

def generate_resource_rows(resources_by_category: Dict[str, List[Resource]], accent_color: str) -> str:
    """Generate HTML for resource rows in new format."""
    html_parts = []
    resource_counter = [1]  # Use list for mutable counter

    for category, resources in resources_by_category.items():
        cat_slug = category.lower().replace(' ', '-').replace('&', '').replace('+', '')
        # Category section (matches KE structure)
        html_parts.append(f'''
              <!-- {category} -->
              <div class="resources-section" data-category="{cat_slug}">
                <div class="category-header" onclick="toggleCategory(this)">
                  <span class="category-arrow">▼</span>
                  <span class="category-name">{category}</span>
                  <span class="category-count">{len(resources)}</span>
                </div>''')

        for i, r in enumerate(resources):
            tree_char = "├──" if i < len(resources) - 1 else "└──"
            cat_slug = category.lower().replace(' ', '-').replace('&', '').replace('+', '')
            resource_id = f"r-{resource_counter[0]:03d}"
            resource_counter[0] += 1

            html_parts.append(f'''
                <a href="{r.url}" target="_blank" class="resource-row" data-category="{cat_slug}" data-resource-id="{resource_id}">
                  <span class="resource-tree">{tree_char}</span>
                  <span class="resource-dot" style="background: {accent_color};"></span>
                  <span class="resource-title">{r.title}</span>
                  <span class="resource-source">{r.source}</span>
                  <span class="resource-author">{r.author}</span>
                  <span class="resource-time">{r.time}</span>
                  <span class="resource-arrow">→</span>
                </a>''')

        html_parts.append('''
              </div>''')

    return '\n'.join(html_parts)

def generate_terms_html(terms: List[dict]) -> str:
    """Generate HTML for key terms."""
    if not terms:
        return ''

    html = []
    for term in terms:
        html.append(f'''            <div class="term-row">
              <span class="term-name">{term['name']}</span>
              <span class="term-def">{term['definition']}</span>
            </div>''')
    return '\n'.join(html)

def count_resources(resources_by_category: Dict[str, List[Resource]]) -> int:
    """Count total resources."""
    return sum(len(resources) for resources in resources_by_category.values())

def generate_resource_data_js(resources_by_category: Dict[str, List[Resource]]) -> str:
    """Generate JavaScript resourceData object."""
    lines = ["    const resourceData = {"]

    resource_id = 1
    for category, resources in resources_by_category.items():
        for r in resources:
            rid = f"r-{resource_id:03d}"
            # Escape strings for JS
            title = r.title.replace("'", "\\'").replace('"', '\\"')
            desc = r.description.replace("'", "\\'").replace('"', '\\"')
            source = r.source.replace("'", "\\'")
            author = r.author.replace("'", "\\'")
            url = r.url

            lines.append(f"      '{rid}': {{ title: '{title}', source: '{source}', author: '{author}', scope: '{desc}', url: '{url}', granularity: 'implementation' }},")
            resource_id += 1

    lines.append("    };")
    return '\n'.join(lines)

def generate_category_descriptions_js(resources_by_category: Dict[str, List[Resource]], title: str) -> str:
    """Generate JavaScript categoryDescriptions object."""
    total = count_resources(resources_by_category)

    lines = ["    const categoryDescriptions = {"]
    lines.append(f"      'all': {{ title: 'All Resources', description: 'Browse the complete {title} collection.', count: {total} }},")

    for category, resources in resources_by_category.items():
        cat_slug = category.lower().replace(' ', '-').replace('&', '').replace('+', '')
        cat_title = category.replace("'", "\\'")
        lines.append(f"      '{cat_slug}': {{ title: '{cat_title}', description: '{cat_title} resources.', count: {len(resources)} }},")

    lines.append("    };")
    return '\n'.join(lines)

def main():
    if len(sys.argv) < 2:
        print("Usage: python transform_topic_page.py <input.html>")
        print("       python transform_topic_page.py pages/data-engineering.html")
        sys.exit(1)

    input_path = sys.argv[1]

    print(f"Extracting resources from {input_path}...")
    resources = extract_resources(input_path)
    context = extract_context_content(input_path)

    total = count_resources(resources)
    print(f"Found {total} resources in {len(resources)} categories:")
    for cat, items in resources.items():
        print(f"  - {cat}: {len(items)}")

    print(f"\nContext:")
    print(f"  Title: {context['title']}")
    print(f"  Accent: {context['accent_color']}")
    print(f"  Stat: {context['stat_num']} - {context['stat_label']}")
    print(f"  Terms: {len(context['terms'])}")

    # Generate the resource rows HTML
    resource_html = generate_resource_rows(resources, context['accent_color'])
    terms_html = generate_terms_html(context['terms'])
    patterns_html = generate_terms_html(context['patterns'])

    # Output to file
    output_dir = Path('scripts/output')
    output_dir.mkdir(exist_ok=True)

    input_name = Path(input_path).stem

    # Save resource rows
    with open(output_dir / f'{input_name}_resources.html', 'w') as f:
        f.write(resource_html)
    print(f"\nResource rows saved to: scripts/output/{input_name}_resources.html")

    # Save context data as JSON for reference
    import json
    context['resource_count'] = total
    context['categories'] = list(resources.keys())
    with open(output_dir / f'{input_name}_context.json', 'w') as f:
        json.dump(context, f, indent=2)
    print(f"Context data saved to: scripts/output/{input_name}_context.json")

    # Save terms HTML
    with open(output_dir / f'{input_name}_terms.html', 'w') as f:
        f.write(terms_html)
    print(f"Terms HTML saved to: scripts/output/{input_name}_terms.html")

    # Save JavaScript data
    resource_data_js = generate_resource_data_js(resources)
    category_desc_js = generate_category_descriptions_js(resources, context['title'])

    with open(output_dir / f'{input_name}_resourceData.js', 'w') as f:
        f.write(resource_data_js)
    print(f"Resource data JS saved to: scripts/output/{input_name}_resourceData.js")

    with open(output_dir / f'{input_name}_categoryDescriptions.js', 'w') as f:
        f.write(category_desc_js)
    print(f"Category descriptions JS saved to: scripts/output/{input_name}_categoryDescriptions.js")

if __name__ == '__main__':
    main()
