import os
import xml.etree.ElementTree as ET
import httpx

# Define the input and output paths
sitemap_path = "c:/Users/georg/Desktop/AEGIS/Projects/gpai-consulting/Invoice_AI_repo/gpai-consulting/Documentation/External Modules/zep_graphiti_sitemap.xml"
output_dir = "c:/Users/georg/Desktop/AEGIS/Projects/gpai-consulting/Invoice_AI_repo/gpai-consulting/Documentation/External Modules/zep_graphiti_docs"

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Parse the XML sitemap
tree = ET.parse(sitemap_path)
root = tree.getroot()

# Define the namespace
namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

# Function to fetch content using MCP server
def fetch_content(url):
    try:
        response = httpx.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")
        return None

# Iterate through the URLs and process documentation links
for url in root.findall('ns:url', namespace):
    loc = url.find('ns:loc', namespace)
    if loc is not None:
        url_text = loc.text
        if "help.getzep.com" in url_text:
            # Append "/llms.txt" to the URL
            modified_url = f"{url_text}/llms.txt"

            # Fetch content from the modified URL
            content = fetch_content(modified_url)
            if content:
                # Generate a filename based on the URL
                filename = url_text.split("/")[-1] + "_llms.txt"
                output_path = os.path.join(output_dir, filename)

                # Save the content to a file
                with open(output_path, "w", encoding="utf-8") as file:
                    file.write(content)

print("Documentation URLs processed and saved using MCP server.")