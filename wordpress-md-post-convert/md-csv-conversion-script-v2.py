import pandas as pd
import re
from collections import Counter
import string
from datetime import datetime

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
    stop_words = set(['and', 'the', 'of', 'to', 'a', 'in', 'for', 'is', 'on', 'that', 'by', 'this', 'with', 'i', 'you', 'it', 'not', 'or', 'be', 'are', 'from', 'at', 'as', 'your', 'have', 'more', 'can', 'an', 'was', 'we', 'will', 'my', 'one', 'all', 'their', 'has', 'so', 'if'])
    word_counts = Counter(w.lower() for w in words if w.lower() not in stop_words)
    return word_counts.most_common(1)[0][0] if word_counts else ""

# Function to read Markdown file and extract content
def read_markdown(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content

# Function to create a CSV row from Markdown content
def create_csv_row_from_md(markdown_content, csv_template_path, output_csv_path):
    # Extract title and SEO tags from the Markdown content
    title_match = re.search(r'### (.+)', markdown_content)
    title = title_match.group(1).strip() if title_match else 'Untitled'
    seo_tags_match = re.search(r'#### SEO High-Ranking Page Tags\s+(.+)', markdown_content, re.S)
    seo_tags = seo_tags_match.group(1).strip().replace('\n', ', ') if seo_tags_match else ''

    # Prepare content and keyphrases
    content = markdown_content.replace(title_match.group(0), '', 1) if title_match else markdown_content
    keyphrases = extract_keyphrases(content)

    # Generate post_name from title
    post_name = create_slug(title)

    # Set default values
    post_author_default = 'trioadmin'
    featured_image_default = ''
    post_category_default = 'AI'
    post_template_default = 'template-1'
    nsfw_post_default = 'field_587be16ffc2f2'
    featured_post_default = 1
    keep_trending_default = 1
    editors_choice_default = 1
    post_status_default = 'publish'
    post_date_default = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Create CSV row with all required data
    csv_row = {
        'post_title': title,
        'post_content': content,
        'post_excerpt': content[:100] + '...',  # First 100 characters of content as excerpt
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
        'keyphrases': keyphrases,
        'post_category': post_category_default,
        'post_tag': seo_tags,
        'editors_choice': editors_choice_default,
        'editors_note': '',
        'featured-post': featured_post_default,
        'keep_trending': keep_trending_default,
        'news_list_items': '',
        'nsfw_post': nsfw_post_default,
        'post_template': post_template_default
    }

    # Load the existing CSV template and append the new row
    try:
        posts_df = pd.read_csv(csv_template_path)
    except FileNotFoundError:
        # If the CSV template doesn't exist, create a new DataFrame
        posts_df = pd.DataFrame(columns=csv_row.keys())

    posts_df = pd.concat([posts_df, pd.DataFrame([csv_row])], ignore_index=True)

    # Save the updated DataFrame to a new CSV file
    posts_df.to_csv(output_csv_path, index=False)
    return output_csv_path

# Paths to your markdown file and the CSV template
markdown_file_path = 'E:/Github/orgs/ncgcloudhub/scripts/wordpress-md-post-convert/adobefirefly.md'  # Replace with the path to your markdown file
csv_template_path = 'E:/Github/orgs/ncgcloudhub/scripts/wordpress-md-post-convert/output.csv'  # Replace with the path to your existing CSV template

# Generate output CSV file name with the current date and time
output_csv_file_name = f"output_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
output_csv_path = f"E:/Github/orgs/ncgcloudhub/scripts/wordpress-md-post-convert/{output_csv_file_name}"

# Run the function to convert the markdown to CSV and save the output
final_output_csv_path = create_csv_row_from_md(read_markdown(markdown_file_path), csv_template_path, output_csv_path)
print(f"CSV file saved as: {final_output_csv_path}")
