import pandas as pd
import re
import glob
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
    stop_words = set(['and', 'the', 'of', 'to', 'a', 'in', 'for', 'is', 'on', 'that', 'by', 'this', 'with', 'i', 'you', 'it', 'not', 'or', 'be', 'are', 'from', 'at', 'as', 'your', 'have', 'more', 'can', 'an', 'was', 'we'])
    words = [word for word in words if word not in stop_words]
    most_common_word = Counter(words).most_common(1)[0][0]
    return most_common_word

# Function to process each markdown file
def process_markdown_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    # Extract data from markdown (Placeholder for actual extraction logic)
    # For example, assume title is the first line and post_tag is the last line
    lines = content.split('\n')
    title = lines[0].strip()
    post_tag = lines[-1].strip()

    # Extract other necessary data or use defaults
    post_name = create_slug(title)
    post_author = 'trioadmin'  # Default value
    post_status = 'publish'
    featured_image = 'default_image_url'  # Default value or prompt for input
    keyphrases = extract_keyphrases(content)
    post_category = 'AI'  # Default value or prompt for input

    # Return extracted data as a dictionary
    return {
        'post_title': title,
        'post_content': content,
        'post_name': post_name,
        'post_author': post_author,
        'post_status': post_status,
        'featured_image': featured_image,
        'keyphrases': keyphrases,
        'post_category': post_category,
        'post_tag': post_tag
    }

# Main function to process all markdown files and append to CSV
# Main function to process all markdown files and append to CSV
def main():
    markdown_files = glob.glob('E:/Github/orgs/ncgcloudhub/scripts/wordpress-md-post-convert/*.md')  # Update this path with the directory of your Markdown files
    output_csv_file_name = f"output_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
    csv_file_path = f"E:/Github/orgs/ncgcloudhub/scripts/wordpress-md-post-convert/{output_csv_file_name}"  # Update this path with the directory for your CSV file

    for file_path in markdown_files:
        post_data = process_markdown_file(file_path)
        df = pd.DataFrame([post_data])
        df.to_csv(csv_file_path, mode='a', header=False, index=False)  # Append to the same CSV file

if __name__ == '__main__':
    main()
