import os
from bs4 import BeautifulSoup

target_dir = r"C:\Users\danie\Downloads\nexusbet-1to1"
deposit_file = os.path.join(target_dir, "profile_deposit.html")

with open(deposit_file, "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f.read(), "html.parser")

dropdown = soup.find("div", class_=lambda c: c and "Dropdown2_main__oaGd2" in c)
if dropdown:
    options = dropdown.find_all("div", class_=lambda c: c and "Dropdown2_dropdownEl__tTIhL" in c)
    if options:
        print("First option HTML:")
        print(options[0].prettify()[:1000])
    else:
        print("No options found with class Dropdown2_dropdownEl__tTIhL")
    
    menu = dropdown.find("div", class_=lambda c: c and "Dropdown2_dropdown__ULp_Y" in c)
    if menu:
        print("\nMenu classes:", menu.get("class"))
        print("Menu style:", menu.get("style"))
