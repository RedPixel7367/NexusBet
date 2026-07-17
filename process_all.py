import os
import glob
from bs4 import BeautifulSoup

target_dir = r"C:\Users\danie\Downloads\nexusbet-1to1"
head_file = r"C:\Users\danie\.gemini\antigravity\brain\00acb5ea-cdc8-406d-b085-4ef641184300\scratch\profile.network-response"

with open(head_file, "r", encoding="utf-8") as f:
    head_html = f.read()
head_soup = BeautifulSoup(head_html, "html.parser")
head_tag = head_soup.find("head")

raw_files = glob.glob(os.path.join(target_dir, "raw_*.html"))

for raw_file in raw_files:
    basename = os.path.basename(raw_file)
    target_filename = basename.replace("raw_", "")
    out_file = os.path.join(target_dir, target_filename)
    
    with open(raw_file, "r", encoding="utf-8") as f:
        body_html = f.read()

    combined_html = f"<!DOCTYPE html><html translate='no'>{str(head_tag)}{body_html}</html>"
    soup = BeautifulSoup(combined_html, "html.parser")

    for s in soup.find_all("script"):
        s.decompose()

    for st in soup.find_all("style"):
        if "#nprogress" in st.text:
            st.decompose()

    preloader = soup.find("div", class_="Preloader_main__i_x_y")
    if preloader:
        preloader.decompose()

    if not soup.find("link", href="styles.css"):
        style_link = soup.new_tag("link", rel="stylesheet", href="styles.css")
        soup.head.append(style_link)

    for img in soup.find_all("img"):
        src = img.get("src")
        if src and src.startswith("/"):
            img["src"] = "https://kasowin.com" + src

    for link in soup.find_all("link"):
        href = link.get("href")
        if href and href.startswith("/") and not href == "styles.css":
            link["href"] = "https://kasowin.com" + href

    for a in soup.find_all("a"):
        href = a.get("href")
        if href:
            if href == "/":
                a["href"] = "dashboard.html"
            elif href.startswith("/") and not href.startswith("//"):
                # Turn "/profile/bonuses" into "profile_bonuses.html"
                a["href"] = href[1:].replace("/", "_") + ".html"
            
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(str(soup))
    print(f"Processed {basename} -> {target_filename}")
