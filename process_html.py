import os
import glob
from bs4 import BeautifulSoup

scratch_dir = r"C:\Users\danie\.gemini\antigravity\brain\00acb5ea-cdc8-406d-b085-4ef641184300\scratch"
target_dir = r"C:\Users\danie\Downloads\nexusbet-1to1"

base_url = "https://kasowin.com"

files = glob.glob(os.path.join(scratch_dir, "*.network-response"))

for file_path in files:
    filename = os.path.basename(file_path)
    
    if filename.endswith(".css.network-response") or filename == "d4dbba7cd4889f6e.network-response":
        continue

    # We already built index.html, dashboard.html, and deposit.html perfectly.
    # We shouldn't overwrite deposit.html since we just built a beautiful one manually.
    if filename == "baseline_dashboard.network-response" or filename == "deposit.network-response":
        continue  
        
    page_name = filename.replace(".network-response", "")
    target_path = os.path.join(target_dir, f"{page_name}.html")

    with open(file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, 'html.parser')

    # Remove all script tags
    for script in soup.find_all('script'):
        script.decompose()

    # Rewrite asset URLs to absolute (CSS, images, etc.)
    for tag in soup.find_all(['link', 'img', 'source']):
        for attr in ['href', 'src', 'srcset']:
            if tag.has_attr(attr):
                val = tag[attr]
                if val.startswith('/') and not val.startswith('//'):
                    tag[attr] = base_url + val

    # Rewrite internal links (a tags) to .html
    for a in soup.find_all('a'):
        if a.has_attr('href'):
            val = a['href']
            if val.startswith('/') and not val.startswith('//'):
                if val == '/':
                    a['href'] = 'index.html'
                else:
                    clean_val = val[1:] # strip leading slash
                    
                    # Split out query params / hashes to attach them after .html
                    query_hash = ""
                    if '?' in clean_val:
                        parts = clean_val.split('?', 1)
                        clean_val = parts[0]
                        query_hash = '?' + parts[1]
                    elif '#' in clean_val:
                        parts = clean_val.split('#', 1)
                        clean_val = parts[0]
                        query_hash = '#' + parts[1]
                        
                    clean_val = clean_val.replace('/', '-')
                    a['href'] = clean_val + '.html' + query_hash

    # Inject our local styles.css into the head to apply the custom colors
    head = soup.head
    if head:
        new_link = soup.new_tag('link', rel='stylesheet', href='styles.css')
        head.append(new_link)

    # Save to the target directory
    with open(target_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))
        
    print(f"Processed {page_name} -> {target_path}")

print("All HTML files processed successfully!")
