import os
from bs4 import BeautifulSoup

target_dir = r"C:\Users\danie\Downloads\nexusbet-1to1"
deposit_file = os.path.join(target_dir, "profile_deposit.html")

with open(deposit_file, "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f.read(), "html.parser")

qr_img = soup.find("img", class_=lambda c: c and "qr" in c.lower())
if qr_img:
    print("Found QR code image:")
    print(qr_img.prettify())
else:
    print("QR code not found by class, looking for image src with 'qr'")

for el in soup.find_all("input"):
    print("Found input with value:", el.get("value"), "class:", el.get("class"))
for el in soup.find_all("div", class_=lambda c: c and "Address" in c):
    print("Found div with Address in class:", el.get("class"))
