import markdown
import os
import re
from datetime import datetime
import csv
import glob
from collections import Counter
import string
import colorama
from colorama import Fore, Back, Style


colorama.init()
# Exclude list of files from reading
# exclude_files = ['README.md', 'notes.md']


# Define your CSS content for styling the HTML
css_content = """
/* Table styles */
table {
    border-collapse: collapse;
    width: 100%;
    margin-bottom: 1em;
}
th, td {
    border: 1px solid #dddddd;
    text-align: left;
    padding: 8px;
}

/* Code block styles */
pre, code {
    background-color: #f5f5f5;
    border: 1px solid #cccccc;
    display: block;
    padding: 10px;
    overflow-x: auto;
    font-family: monospace;
}

/* General body styling */
body {
    font-family: Arial, sans-serif;
    line-height: 1.6;
}
"""

# HTML template including the head with CSS styles
html_template = """<!DOCTYPE html>
<html>
<head>
    <title>{title}</title>
    <meta http-equiv="Content-type" content="text/html;charset=UTF-8">
    <style>
    {css_content}
    </style>
</head>
<body>
{md_html_content}
</body>
</html>"""

# Markdown conversion function with necessary extensions
# Markdown conversion function with necessary extensions


def convert_md_to_html(md_content, title):
    extensions = ['extra', 'abbr', 'tables', 'sane_lists', 'codehilite']
    md = markdown.Markdown(extensions=extensions)
    md_html_content = md.convert(md_content)
    final_html_content = html_template.format(
        title=title, md_html_content=md_html_content, css_content=css_content)
    return final_html_content


# Function to create a URL-friendly slug
def create_slug(title):
    title = re.sub(r'[^\w\s-]', '', title.lower())
    return re.sub(r'[\s-]+', '-', title).strip('-')

# Function to extract keyphrases based on the most-used non-stop word in the content


def extract_keyphrases(content):
    words = content.translate(str.maketrans(
        '', '', string.punctuation)).split()
    stop_words = set(['and', 'the', 'of', 'to', 'a', 'in', 'for', 'is', 'on', 'that', 'by', 'this', 'with', 'i',
                     'you', 'it', 'not', 'or', 'be', 'are', 'from', 'at', 'as', 'your', 'have', 'more', 'can', 'an', 'was', 'we'])
    words = [word for word in words if word not in stop_words]
    most_common_word = Counter(words).most_common(1)[0][0]
    return most_common_word


# Adjusted Regular Expression for SEO tags
# working almost 100%
seo_tags_pattern = re.compile(
    r'(?i)(?:##?#?\s?SEO(?: High[- ]Ranking)? (?:Page )?Tags[:\n] ?|\*{1,3}\s?SEO(?: High[- ]Ranking)? (?:Page )?Tags[:\n] ?|SEO High[- ]ranking page Tags: ?)(.+?)(?:\n\n|\Z)', re.DOTALL)
# seo_tags_pattern = re.compile(
#    r'(?i)(?:\*{2,3}\s*SEO High[-\s]*Ranking Page Tags:\s*|\bSEO Tags\b|\bSEO High[-\s]*Ranking Page Tags:|\*{2,3} SEO High[-\s]*Ranking Page Tags:|\bSEO High[-\s]*ranking page Tags:)(.+?)(?=\n\n|\Z|\[|\*{2,3})',
#    re.DOTALL
# )


# When calling the function, pass the exclude_files list as an argument:
exclude_files = ['README.md', 'notes.md']  # Define this outside the function

# Function to process each markdown file


def process_markdown_file(file_path, directory, default_image_url, exclude_files):
    # to skip files in the exclude_files list
    for file in os.listdir(directory):
        if file not in exclude_files:
            # Process the file
            pass

    filename_without_ext = os.path.splitext(os.path.basename(file_path))[0]
    image_file_name = filename_without_ext + '.webp'
    image_file_path = os.path.join(directory, image_file_name)

    # Check if the corresponding webp image file exists in the directory, otherwise use default
    featured_image = "https://dev.trionxai.com/wp-content/uploads/" + \
        image_file_name if os.path.exists(
            image_file_path) else default_image_url

    with open(file_path, 'r', encoding='utf-8') as file:
        md_content = file.read()  # Read the entire Markdown file content

    # Extract the title from the Markdown content
    md_lines = md_content.split('\n')

    # Search for a line with # or ## at the beginning, consider the first 3 lines
    title_match = None
    for i in range(min(3, len(md_lines))):
        match = re.match(r'^(#+) (.+)', md_lines[i])
        if match:
            title_match = match
            break

    # If no match found, use a default title
    if not title_match:
        title = "Default Title"
    else:
        title_level, title = title_match.groups()

        # Remove the # or ## prefix from the title
        title = title.strip()
        title = re.sub(r'^#+\s*', '', title)  # Remove # or ## at the beginning

        # Adjust title level for SEO tags removal
        title_level = min(3, len(md_lines))  # Maximum title level is 3
        md_lines = md_lines[title_level:]

    # Find SEO tags using the keyword "SEO" in a case-insensitive manner
    seo_tags_match = re.search(r'\bSEO\b', md_content, re.IGNORECASE)

    if seo_tags_match:
        seo_tags_start = seo_tags_match.start()
        # Assume tags end with a new line
        seo_tags_end = md_content.find('\n', seo_tags_start)
        seo_tags = md_content[seo_tags_start:seo_tags_end].strip()
    else:
        seo_tags = ""

    # Prepare the Markdown content excluding the title line for HTML conversion
    md_content_without_title_and_seo = '\n'.join(md_lines)
    md_content_without_title_and_seo = re.sub(
        r'\bSEO\b.*', '', md_content_without_title_and_seo, flags=re.IGNORECASE)

    # Convert the Markdown content to HTML
    html_content = convert_md_to_html(md_content_without_title_and_seo, title)

    # Remove the <title> tag content and anything after "SEO High-Ranking Page Tags"
    html_content = re.sub(r'<title>.*</title>', '',
                          html_content, flags=re.DOTALL)
    html_content = re.sub(
        r'<h4>SEO High-Ranking Page Tags</h4>.*', '', html_content, flags=re.DOTALL)

    # Initialize default values
    post_author_default = 'trioadmin'
    # post_date_default = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    post_status_default = 'publish'
    # default_image_url   = 'https://dev.trionxai.com/wp-content/uploads/ai-image.webp'  #'https://dev.trionxai.com/wp-content/uploads/ai-image.webp'
    editors_choice_default = '1'
    featured_post_default = '1'
    keep_trending_default = '1'

    # Extract SEO tags using a regex that matches the various provided patterns
    seo_tags_match = seo_tags_pattern.search(md_content)
    if seo_tags_match:
        # Clean up the extracted tags
        seo_tags = seo_tags_match.group(1).strip()
        # Remove trailing newlines, commas, and periods
        seo_tags = re.sub(r'[\n,.]+$', '', seo_tags)
    else:
        seo_tags = ""

    # Generate post_name from the title
    post_name = create_slug(title)

    # Create the CSV row dictionary with updated fields and default values
    csv_row = {
        'post_title': title,
        'post_content': html_content,  # Using converted HTML content
        'post_excerpt': html_content[:100] + '...' if len(html_content) > 100 else html_content,
        'post_date': '',  # post_date_default,
        'post_name': post_name,
        'post_author': post_author_default,
        'post_status': post_status_default,
        'featured_image': featured_image,
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
        'keyphrases': extract_keyphrases(html_content),
        'post_category': 'AI',
        'post_tag': seo_tags,
        'editors_choice': editors_choice_default,
        'editors_note': '',
        'featured-post': featured_post_default,
        'keep_trending': keep_trending_default,
        'news_list_items': '',
        'post_template': 'template1'
    }

    return csv_row


def main():
    # 'D:/TrionxAI/scripts/wordpress-md-post-convert/'
    directory = 'E:/Github/orgs/ncgcloudhub/all-scripts/scripts/wordpress-md-post-convert'
    # 'https://trionxai.com/wp-content/uploads/ai-image.webp' # PROD
    default_image_url = 'https://dev.trionxai.com/wp-content/uploads/ai-image.webp'
    # markdown_files = glob.glob(os.path.join(directory, '*.md'))
    # List the filenames to exclude from processing
    exclude_files = ['README.md',
                     'notes.md']

    # headers_csv_path = 'D:/TrionxAI/scripts/wordpress-md-post-convert/headers-only.csv'  # Update with the correct path
    headers_csv_path = os.path.join(directory, 'headers-only.csv')
    markdown_files = glob.glob(os.path.join(directory, '*.md'))
    output_csv_file_name = 'output.csv'
    csv_file_path = os.path.join(directory, output_csv_file_name)
    try:
        # Read the headers from headers-only.csv
        with open(headers_csv_path, mode='r', encoding='utf-8') as headers_file:
            headers = headers_file.readline().strip().split(',')

        # Check if the CSV file exists and needs headers
        needs_header = not os.path.exists(csv_file_path)

        # Write headers if needed and data to the CSV file
        with open(csv_file_path, 'a', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=headers)

            if needs_header:
                writer.writeheader()

            # Define the list of files to exclude
            exclude_files = ['README.md', 'notes.md']

            for md_file_path in markdown_files:
                # Check if the current file is in the list of files to exclude
                if os.path.basename(md_file_path) in exclude_files:
                    continue  # Skip the rest of the loop and process the next file
                # process_markdown_file(md_file_path)
                csv_row = process_markdown_file(
                    md_file_path, directory, default_image_url, exclude_files)

                # Ensure csv_row has keys exactly matching the headers
                row_to_write = {header: csv_row.get(
                    header, '') for header in headers}

                writer.writerow(row_to_write)
                pass

    except PermissionError as e:
        print(f"{Back.RED}{Fore.WHITE}Permission error: Your file {output_csv_file_name} is open. Please make sure to close your file and re-run the script.{Style.RESET_ALL}")
        return  # or sys.exit(1) to exit the script entirely

    except FileNotFoundError as e:
        print(f"{Back.RED}{Fore.WHITE}File not found error: The file {e.filename} does not exist. Please check the path and try again.{Style.RESET_ALL}")
        return  # or sys.exit(1) to exit the script entirely

    except Exception as e:
        print(
            f"{Back.RED}{Fore.WHITE}An unexpected error occurred: {e} {Style.RESET_ALL}")
        return  # or sys.exit(1) to exit the script entirely

    print(f"{Back.YELLOW}{Fore.WHITE}CSV file saved as: {csv_file_path}")


if __name__ == '__main__':
    main()


# Creating README.md Files based on the script.
def create_readme(directory, output_file='README.md'):
    files = os.listdir(directory)
    with open(output_file, 'w') as readme:
        readme.write('# Project Title\n\n')
        readme.write('## Overview\n\nDescription of your project.\n\n')
        readme.write('## Files in this Project\n')
        for file in files:
            readme.write(f'- {file}\n')

        # Add more sections as needed
        readme.write('\n## Usage\n\nHow to use this project.\n\n')
        readme.write(
            '## License\n\nThis project is licensed under the MIT License.\n')


create_readme(
    'E:/Github/orgs/ncgcloudhub/all-scripts/scripts/wordpress-md-post-convert')
