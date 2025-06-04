import os
from datetime import datetime
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

# Configuration
site_url = "https://trinitycatholicmedia.github.io/tcm-pinterest-rss/"
posts_dir = "posts"
output_rss = "rss.xml"

# Create RSS root
rss = ET.Element("rss", version="2.0")
channel = ET.SubElement(rss, "channel")
ET.SubElement(channel, "title").text = "My Pinterest Content Feed"
ET.SubElement(channel, "link").text = site_url
ET.SubElement(channel, "description").text = "A feed for auto-publishing Pins to Pinterest"

# Scan posts directory for HTML files
for filename in sorted(os.listdir(posts_dir)):
    if filename.endswith(".html"):
        post_path = os.path.join(posts_dir, filename)
        with open(post_path, encoding="utf-8") as f:
            html = f.read()
        soup = BeautifulSoup(html, "html.parser")
        # Try to extract title, image, and description
        title = soup.find("h1") or soup.find("h2")
        title = title.text.strip() if title else filename
        img = soup.find("img")
        img_url = img["src"] if img and img.has_attr("src") else ""
        desc = soup.find("p")
        desc = desc.text.strip() if desc else ""
        # Create RSS item
        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "title").text = title
        ET.SubElement(item, "link").text = f"{site_url}{posts_dir}/{filename}"
        ET.SubElement(item, "description").text = desc
        ET.SubElement(item, "pubDate").text = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
        if img_url:
            ET.SubElement(item, "enclosure", url=img_url, type="image/jpeg")

# Write RSS feed to file
ET.ElementTree(rss).write(output_rss, encoding="utf-8", xml_declaration=True)