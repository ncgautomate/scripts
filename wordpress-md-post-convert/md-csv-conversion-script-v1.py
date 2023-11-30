import csv
import re
from collections import Counter

# Function to calculate most used word for keyphrases (non-stop words)
def calculate_keyphrases(content):
    stop_words = set("""a about above after again against all am an and any are aren't as at be because been before 
                    being below between both but by can't cannot could couldn't did didn't do does doesn't doing 
                    don't down during each few for from further had hadn't has hasn't have haven't having he he'd 
                    he'll he's her here here's hers herself him himself his how how's i i'd i'll i'm i've if in 
                    into is isn't it it's its itself let's me more most mustn't my myself no nor not of off on once 
                    only or other ought our ours ourselves out over own same shan't she she'd she'll she's should 
                    shouldn't so some such than that that's the their theirs them themselves then there there's 
                    these they they'd they'll they're they've this those through to too under until up very was 
                    wasn't we we'd we'll we're we've were weren't what what's when when's where where's which while 
                    who who's whom why why's with won't would wouldn't you you'd you'll you're you've your yours 
                    yourself yourselves""".split())
    words = [word.lower() for word in re.findall(r'\w+', content)]
    words = [word for word in words if word not in stop_words]
    word_counts = Counter(words)
    most_common_word = word_counts.most_common(1)
    return most_common_word[0][0] if most_common_word else ''

# Function to generate post_name from post_title
def generate_post_name(title):
    return re.sub(r'\s+', '-', title).lower()

# Function to extract tags from markdown
def extract_tags(content):
    match = re.search(r"SEO High-Ranking Page Tags:(.*)", content)
    return match.group(1).strip() if match else ''

# Function to parse markdown content
def parse_markdown(md_content):
    lines = md_content.splitlines()
    title = lines[0].replace("Title:", "").strip()
    end_of_content = next((i for i, line in enumerate(lines) if line.startswith("SEO High-Ranking Page Tags")), len(lines))
    content = "\n".join(lines[1:end_of_content]).strip()
    tags = extract_tags(content)
    content = content.replace("SEO High-Ranking Page Tags:" + tags, "").strip()
    return title, content, [tag.strip() for tag in tags.split(',')]

# Load the provided markdown content
md_content_path = 'E:/Github/orgs/ncgcloudhub/scripts/wordpress-md-post-convert/adobefirefly.md'
with open(md_content_path, 'r', encoding='utf-8') as md_file:
    md_content = md_file.read()

# Process the markdown content
title, content, tags = parse_markdown(md_content)
keyphrases = calculate_keyphrases(content)
post_name = generate_post_name(title)

# Prepare the initial CSV row with extracted and generated data
csv_row = {
    "post_title": title, 
    "ID": "", 
    "post_content": content,
    "post_excerpt": "", 
    "post_date": "", 
    "post_name": post_name,
    "post_author": "trioadmin",
    "post_status": "publish",
    "featured_image": "",
    "post_format": "",
    "comment_status": "", 
    "ping_status": "", 
    "noindex": "",
    "keyphrases": keyphrases,
    "post_category": "AI Tools, AI",
    "post_tag": ", ".join(tags),
    # ... more fields to be populated ...
}

# Full list of headers based on the order provided
csv_headers = ["post_title", "ID", "post_content", "post_excerpt", "post_date", "post_name", "post_author",
               "post_status", "featured_image", "post_format", "comment_status", "ping_status", "noindex",
               "keyphrases", "post_category", "post_tag",
               # ... all other headers ...
              ]

# Define the output CSV file path
output_csv_path = 'E:/Github/orgs/ncgcloudhub/scripts/wordpress-md-post-convert/output_1.csv'

# Write the CSV data to the file
with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_headers)
    writer.writeheader()
    writer.writerow(csv_row)

print(f"CSV file has been written to {output_csv_path}")