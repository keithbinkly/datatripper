#!/usr/bin/env python3
"""
Generate a complete topic page from extracted content + KE template.

Usage:
    python scripts/generate_topic_page.py pages/data-engineering.html
"""

import sys
import json
import re
from pathlib import Path
from bs4 import BeautifulSoup

def load_ke_template():
    """Load knowledge-engineering.html as template."""
    with open('pages/knowledge-engineering.html', 'r') as f:
        return f.read()

def load_extracted_data(page_name: str):
    """Load previously extracted data."""
    output_dir = Path('scripts/output')

    with open(output_dir / f'{page_name}_context.json', 'r') as f:
        context = json.load(f)

    with open(output_dir / f'{page_name}_resources.html', 'r') as f:
        resources_html = f.read()

    with open(output_dir / f'{page_name}_terms.html', 'r') as f:
        terms_html = f.read()

    with open(output_dir / f'{page_name}_resourceData.js', 'r') as f:
        resource_data_js = f.read()

    with open(output_dir / f'{page_name}_categoryDescriptions.js', 'r') as f:
        category_desc_js = f.read()

    return context, resources_html, terms_html, resource_data_js, category_desc_js

def generate_page(input_path: str):
    """Generate new page from template + extracted content."""
    page_name = Path(input_path).stem
    template = load_ke_template()
    context, resources_html, terms_html, resource_data_js, category_desc_js = load_extracted_data(page_name)

    soup = BeautifulSoup(template, 'html.parser')

    # 1. Update <title>
    title_tag = soup.find('title')
    if title_tag:
        title_tag.string = f"{context['title']} | data-centered"

    # 2. Update meta description
    meta_desc = soup.find('meta', attrs={'name': 'description'})
    if meta_desc:
        # Generate description from lede
        lede_text = BeautifulSoup(context['lede'], 'html.parser').get_text()[:150]
        meta_desc['content'] = lede_text

    # 3. Update header brand/title
    brand = soup.find('span', class_='brand')
    if brand:
        brand.string = context['title']

    # 4. Update resource count
    count_span = soup.find('span', class_='resource-count')
    if count_span:
        count_span.string = f"{context['resource_count']} resources"

    # 5. Update topic indicator color (in CSS)
    # Find and replace the cyan topic indicator color with page accent
    style_tag = soup.find('style')
    if style_tag and style_tag.string:
        # Replace topic indicator background color
        style_content = style_tag.string
        # The topic indicator in KE uses --cyan, we'll add an override
        style_content = style_content.replace(
            '.topic-indicator {',
            f'.topic-indicator {{ background: {context["accent_color"]} !important;'
        )
        style_tag.string = style_content

    # 6. Update context panel lede
    context_lede = soup.find('p', class_='context-lede')
    if context_lede:
        context_lede.clear()
        context_lede.append(BeautifulSoup(context['lede'], 'html.parser'))

    # 7. Update stat box
    stat_num = soup.find('span', class_='stat-num')
    stat_label = soup.find('span', class_='stat-label')
    if stat_num:
        stat_num.string = context['stat_num']
    if stat_label:
        stat_label.string = context['stat_label'].upper()

    # 8. Update navigation links
    back_link = soup.find('a', class_='back-link')
    next_link = soup.find('a', class_='next-link')
    if next_link and context.get('next_page'):
        next_link['href'] = context['next_page']

    # 9. Replace resources scroll content
    resources_scroll = soup.find('div', class_='resources-scroll')
    if resources_scroll:
        resources_scroll.clear()
        resources_scroll.append(BeautifulSoup(resources_html, 'html.parser'))

    # 10. Update category tabs
    category_tabs_div = soup.find('div', class_='category-tabs')
    if category_tabs_div and context.get('categories'):
        category_tabs_div.clear()
        # Add "All" tab
        all_tab = soup.new_tag('button', attrs={'class': 'category-tab active', 'data-category': 'all'})
        all_tab.string = 'All'
        category_tabs_div.append(all_tab)
        # Add category tabs (first 6 to avoid overflow)
        for cat in context['categories'][:6]:
            cat_slug = cat.lower().replace(' ', '-').replace('&', '').replace('+', '')
            short_name = cat.split()[0][:8]  # First word, max 8 chars
            tab = soup.new_tag('button', attrs={'class': 'category-tab', 'data-category': cat_slug})
            tab.string = short_name
            category_tabs_div.append(tab)

    # 11. Update category description
    cat_desc = soup.find('div', class_='category-description')
    if cat_desc:
        title_el = cat_desc.find('div', class_='category-description-title')
        text_el = cat_desc.find('div', class_='category-description-text')
        count_el = cat_desc.find('div', class_='category-description-count')
        if title_el:
            title_el.string = 'All Resources'
        if text_el:
            text_el.string = f"Browse the complete {context['title']} collection."
        if count_el:
            count_el.string = f"{context['resource_count']} resources"

    # 10. Remove viewers-row (infographics/slide decks - KE specific)
    viewers_row = soup.find('div', class_='viewers-row')
    if viewers_row:
        viewers_row.decompose()

    # 11. Update key terms
    terms_panel = soup.find('div', class_='terms-grid')
    if terms_panel and terms_html:
        terms_panel.clear()
        terms_panel.append(BeautifulSoup(terms_html, 'html.parser'))

    # 12. Update accent colors throughout (replace cyan references with page accent)
    # This is for resource dots and other accent elements
    html_str = str(soup)

    # Replace accent-cyan with page-specific accent class
    accent_class = page_name.replace('-', '_')

    # Add custom CSS for this page's accent
    accent_css = f'''
    /* Page-specific accent override */
    .topic-indicator {{ background: {context["accent_color"]} !important; }}
    .resource-dot {{ background: {context["accent_color"]} !important; }}
    .panel.accent-page .panel-header {{ border-left-color: {context["accent_color"]}; }}
    '''

    # Insert before </style>
    html_str = html_str.replace('</style>', accent_css + '\n  </style>')

    # 13. Replace resourceData and categoryDescriptions in script
    # Find script section and replace the data objects
    # Use markers to find start/end of each object

    # Replace categoryDescriptions - find from declaration to next const
    cat_start = html_str.find('const categoryDescriptions = {')
    if cat_start != -1:
        # Find the closing of categoryDescriptions (it ends with '};' before 'const resourceData')
        res_start = html_str.find('const resourceData = {')
        if res_start != -1:
            # Replace everything from cat_start to res_start
            html_str = html_str[:cat_start] + category_desc_js + '\n\n    ' + html_str[res_start:]

    # Replace resourceData - find from declaration to end marker (comment or function)
    res_start = html_str.find('const resourceData = {')
    if res_start != -1:
        # Find the end by looking for the next major section (function declarations)
        # resourceData ends with '};' then blank lines before functions
        end_markers = ['function updateCategory', '// ═══════════════', 'function toggleCategory']
        end_pos = len(html_str)
        for marker in end_markers:
            pos = html_str.find(marker, res_start)
            if pos != -1 and pos < end_pos:
                end_pos = pos

        # Find the last '};' before end_pos
        search_region = html_str[res_start:end_pos]
        last_close = search_region.rfind('};')
        if last_close != -1:
            actual_end = res_start + last_close + 2
            html_str = html_str[:res_start] + resource_data_js + html_str[actual_end:]

    # Output
    output_path = Path('scripts/output') / f'{page_name}_new.html'
    with open(output_path, 'w') as f:
        f.write(html_str)

    print(f"Generated: {output_path}")
    return output_path

def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_topic_page.py <input.html>")
        sys.exit(1)

    input_path = sys.argv[1]
    generate_page(input_path)

if __name__ == '__main__':
    main()
