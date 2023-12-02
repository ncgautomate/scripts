import os
import markdown

# Define the root directory where your Markdown files are located
root_dir = "E:\\Github\\orgs\\ncgcloudhub\\scripts\\wordpress-md-post-convert"

# CSS styles to be included within the HTML for table and code block formatting
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
def convert_md_to_html(md_content):
    extensions = ['extra', 'abbr', 'tables', 'sane_lists', 'codehilite']
    md = markdown.Markdown(extensions=extensions)
    return md.convert(md_content)

# Walk through the directory and convert each Markdown file
for subdir, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith('.md'):
            file_path = os.path.join(subdir, file)
            html_file_path = file_path.replace('.md', '.html')

            # Read the Markdown content from the file
            with open(file_path, 'r', encoding='utf-8') as md_file:
                md_content = md_file.read()

            # Convert the Markdown content to HTML
            md_html_content = convert_md_to_html(md_content)
            final_html_content = html_template.format(
                title=file.replace('.md', ''),
                md_html_content=md_html_content,
                css_content=css_content
            )

            # Write the final HTML content to a new file
            with open(html_file_path, 'w', encoding='utf-8') as html_file:
                html_file.write(final_html_content)
            print(f"Converted {file} to HTML.")

print("Conversion complete.")
