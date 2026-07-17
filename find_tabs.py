import os
from bs4 import BeautifulSoup

target_dir = r"C:\Users\danie\Downloads\nexusbet-1to1"
deposit_file = os.path.join(target_dir, "profile_deposit.html")

with open(deposit_file, "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f.read(), "html.parser")

# Find elements that might be dropdowns
import re
for el in soup.find_all("div", class_=re.compile("Select", re.I)):
    print("Found Select:", el.get("class"))
for el in soup.find_all("div", class_=re.compile("Dropdown", re.I)):
    print("Found Dropdown:", el.get("class"))
for el in soup.find_all("div", class_=re.compile("WalletProfile", re.I)):
    classes = el.get("class", [])
    if any("select" in c.lower() or "dropdown" in c.lower() for c in classes):
        print("Found WalletProfile Dropdown:", classes)
