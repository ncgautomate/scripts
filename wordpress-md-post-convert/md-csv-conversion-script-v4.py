import pandas as pd
import re
import glob
from collections import Counter
import string
from datetime import datetime
import os
import markdown  # Import the markdown library



# Function to convert title to a URL-friendly slug
def create_slug(title):
    title = re.sub(r'<[^>]+>', '', title)  # Remove HTML tags
    title = re.sub(r'&[^;]+;', '', title)  # Remove HTML entities
    title = title.lower()  # Convert to lowercase
    title = re.sub(r'[^a-z0-9\s-]', '', title)  # Remove non-alpha-numeric characters
    title = re.sub(r'[\s-]+', '-', title).strip('-')  # Replace spaces and repeated hyphens with single hyphen
    return title

# Function to extract keyphrases based on the most-used non-stop word in the content
def extract_keyphrases(content):
    words = content.translate(str.maketrans('', '', string.punctuation)).split()
    stop_words = set(['and', 'the', 'of', 'to', 'a', 'in', 'for', 'is', 'on', 'that', 'by', 'this', 'with', 'i', 'you', 'it', 'not', 'or', 'be', 'are', 'from', 'at', 'as', 'your', 'have', 'more', 'can', 'an', 'was', 'we'])
    words = [word for word in words if word not in stop_words]
    most_common_word = Counter(words).most_common(1)[0][0]
    return most_common_word

# Function to check if the CSV file needs a header
def csv_needs_header(csv_file_path):
    return not os.path.isfile(csv_file_path)

# Function to convert Markdown to HTML
def markdown_to_html(md_content):
    return markdown.markdown(md_content)

# Markdown conversion function with necessary extensions
def convert_md_to_html(md_content, title):
    extensions = ['extra', 'abbr', 'tables', 'sane_lists', 'codehilite']
    md = markdown.Markdown(extensions=extensions)
    md_html_content = md.convert(md_content)
    final_html_content = html_template.format(
        title=title,
        md_html_content=md_html_content,
        css_content=css_content
    )
    return final_html_content


# Function to process each markdown file
def process_markdown_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        md_lines = file.readlines()

    # Extract the title from the Markdown content (assuming it's the first line)
    title_match = re.match(r'^# (.+)', md_lines[0])
    title = title_match.group(1).strip() if title_match else "Default Title"

    # Join the Markdown content excluding the title and SEO tags
    md_content = ''.join(md_lines[1:])  # Exclude the first line which is the title
    md_content_without_seo = re.sub(r'#### SEO High-Ranking Page Tags.*', '', md_content, flags=re.DOTALL).strip()

    # Convert the Markdown content to HTML
    html_content = convert_md_to_html(md_content_without_seo, title)

    # Initialize default values
    post_author_default = 'trioadmin'
    post_date_default = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    post_status_default = 'publish'
    featured_image_default = 'default_image_url'
    editors_choice_default = '1'
    featured_post_default = '1'
    keep_trending_default = '1'

    # Extract SEO tags
    seo_tags_match = re.search(r'#### SEO High-Ranking Page Tags\n(.+)', md_content, re.DOTALL)
    seo_tags = seo_tags_match.group(1).strip() if seo_tags_match else ""

    # Generate post_name from the title
    post_name = create_slug(title)

    # Create the CSV row dictionary with updated fields and default values
    csv_row = {
        'post_title': title,
        'post_content': html_content,
        'post_excerpt': html_content[:100] + '...' if len(html_content) > 100 else html_content,
        'post_date': post_date_default,
        'post_name': post_name,
        'post_author': post_author_default,
        'post_status': post_status_default,
        'featured_image': featured_image_default,
        'post_format': 'standard',
        'comment_status': 'open',
        'ping_status': 'open',
        'robots_default': 'index, follow',
        'robots_noarchive': 'no',
        'robots_nosnippet': 'no',
        'robots_noimageindex': 'no',
        'robots_notranslate': 'no',
        'robots_max_snippet': '-1',
        'robots_max_videopreview': '-1',
        'robots_max_imagepreview': 'large',
        'keyphrases': extract_keyphrases(html_content),  # Using HTML content for keyphrases
        'post_category': 'AI',
        'post_tags': seo_tags,
        'editors_choice': editors_choice_default,
        'editors_note': '',
        'featured-post': featured_post_default,
        'keep_trending': keep_trending_default,
        'news_list_items': '',
        'post_template': 'template1'
    }

    return csv_row


# Main function to process all markdown files and append to CSV
def main():
    directory = 'E:/Github/orgs/ncgcloudhub/scripts/wordpress-md-post-convert/'
    headers_csv_path = directory + 'headers-only.csv'
    
    # Read the headers from headers-only.csv
    headers = pd.read_csv(headers_csv_path, nrows=0).columns.tolist()
    
    markdown_files = glob.glob(directory + '*.md')
    output_csv_file_name = f"output_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
    final_output_csv_path = directory + output_csv_file_name
    
    # Check if the CSV needs headers
    needs_header = csv_needs_header(final_output_csv_path)
    
    # Process each markdown file
    for file_path in markdown_files:
        post_data = process_markdown_file(file_path)
        df = pd.DataFrame([post_data], columns=headers)
        df.to_csv(final_output_csv_path, mode='a', header=needs_header, index=False)
        needs_header = False  # Only write headers once

    # Print the completion message with the path to the CSV file
    print(f"CSV file saved as: {final_output_csv_path}")

if __name__ == '__main__':
    main()
