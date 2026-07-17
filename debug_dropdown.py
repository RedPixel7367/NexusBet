import os
from bs4 import BeautifulSoup

target_dir = r"C:\Users\danie\Downloads\nexusbet-1to1"
deposit_file = os.path.join(target_dir, "profile_deposit.html")

with open(deposit_file, "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f.read(), "html.parser")

dropdown = soup.find("div", class_=lambda c: c and "Dropdown2_main__oaGd2" in c)
if dropdown:
    print(dropdown.prettify()[:1000])
else:
    print("No dropdown found.")
