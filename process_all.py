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
        file_html = f.read()

    if "<head>" in file_html.lower() or "<head " in file_html.lower():
        combined_html = file_html
    else:
        combined_html = f"<!DOCTYPE html><html translate='no'>{str(head_tag)}{file_html}</html>"
        
    # Overwrite the user's hardcoded balance to $1000.00
    combined_html = combined_html.replace("$2498<span>.54</span>", "$1000<span>.00</span>")
    combined_html = combined_html.replace("$2498.54", "$1000.00")
    combined_html = combined_html.replace("2498.54", "1000.00")
        
    soup = BeautifulSoup(combined_html, "html.parser")

    for s in soup.find_all("script"):
        s.decompose()

    for st in soup.find_all("style"):
        if "#nprogress" in st.text:
            st.decompose()

    preloader = soup.find("div", class_="Preloader_main__i_x_y")
    if preloader:
        preloader.decompose()

    if soup.head and not soup.find("link", href="styles.css"):
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
                a["href"] = href[1:].replace("/", "_") + ".html"
                
    # Connect sidebar buttons
    button_mapping = {
        "Home": "dashboard.html",
        "Profile": "profile.html",
        "Live Support": "#",
        "Deposit": "profile_deposit.html",
        "Withdraw": "profile_withdraw.html",
        "VIP-Club": "vip.html",
        "About Us": "about-us.html",
        "Promotions": "promotions.html",
        "Sponsorships": "sponsorships.html",
        "Licenses & Security": "licenses-security.html",
        "Feedback About Us": "feedback.html",
        "News": "news.html",
        "Games": "original-games.html",
        "Slots": "licensed-slots.html",
        "Verification": "profile_verification.html",
        "Settings": "profile_settings.html",
        "Transactions": "profile_transactions.html",
        "Bonuses": "profile_bonuses.html"
    }
    
    # Fix sidebar buttons
    for nav in soup.find_all("div", class_="Side_nav__TUWgM"):
        text_div = nav.find("div", class_="Side_navText__QY6zP")
        if text_div and text_div.text in button_mapping:
            nav.name = "a"
            nav["href"] = button_mapping[text_div.text]
            nav["style"] = "text-decoration: none; color: inherit; display: flex; cursor: pointer;"
            
    # Fix top buttons (Games/Slots)
    for top_btn in soup.find_all("div", class_="Side_topButton__vCSZN"):
        span = top_btn.find("span")
        if span and span.text in button_mapping:
            top_btn.name = "a"
            top_btn["href"] = button_mapping[span.text]
            top_btn["style"] = "text-decoration: none; color: inherit; display: flex; cursor: pointer;"

    # Fix profile sub-navigation buttons
    for profile_nav in soup.find_all("div", class_="Profile_switchEl__X_7nG"):
        span = profile_nav.find("span")
        if span and span.text in button_mapping:
            profile_nav.name = "a"
            profile_nav["href"] = button_mapping[span.text]
            profile_nav["style"] = "text-decoration: none; color: inherit; display: flex; cursor: pointer;"

    # Fix header <button> elements (Home, Profile, Bonuses, VIP, Deposit)
    for btn in soup.find_all("button"):
        btn_text = btn.text.strip()
        # For the deposit button, it might just be "Deposit" or nested
        if not btn_text:
            span = btn.find("span")
            if span:
                btn_text = span.text.strip()
                
        if btn_text in button_mapping:
            btn.name = "a"
            btn["href"] = button_mapping[btn_text]
            btn["style"] = btn.get("style", "") + " text-decoration: none; color: inherit; display: inline-flex; align-items: center; justify-content: center; cursor: pointer;"

    # Fix Deposit Tabs (Crypto vs Fiat)
    for method_tab in soup.find_all("div", class_="WalletProfile_method__ipfA0"):
        span = method_tab.find("span")
        if span:
            if "Bank Card" in span.text:
                method_tab.name = "a"
                method_tab["href"] = "profile_deposit_fiat.html"
                method_tab["style"] = method_tab.get("style", "") + " text-decoration: none; color: inherit; display: flex; cursor: pointer;"
            elif "Crypto" in span.text:
                method_tab.name = "a"
                method_tab["href"] = "profile_deposit.html"
                method_tab["style"] = method_tab.get("style", "") + " text-decoration: none; color: inherit; display: flex; cursor: pointer;"

    final_html = str(soup)
    
    js_snippet = """
<script>
(function() {
    // Dropdown toggle logic
    const dropdowns = document.querySelectorAll(".Dropdown2_main__oaGd2");
    dropdowns.forEach(dropdown => {
        // Make the parent relative so the absolute menu positions correctly below it
        dropdown.style.position = "relative";
        
        const input = dropdown.querySelector(".Dropdown2_input__c_MRs");
        const menu = dropdown.querySelector(".Dropdown2_dropdown__ULp_Y");
        const menuInner = dropdown.querySelector(".Dropdown2_dropdownIn__MhXbF");
        
        if (input && menu) {
            // Force hidden and proper positioning initially
            menu.style.display = "none";
            menu.style.position = "absolute";
            menu.style.top = "100%";
            menu.style.left = "0";
            menu.style.marginTop = "8px";
            menu.style.zIndex = "99999";
            menu.style.width = "100%";
            menu.style.opacity = "1";
            menu.style.visibility = "visible";
            menu.style.pointerEvents = "auto";
            
            // Fix scrolling on the inner container
            if (menuInner) {
                menuInner.style.maxHeight = "280px";
                menuInner.style.overflowY = "auto";
                menuInner.style.pointerEvents = "auto";
            }
            
            input.addEventListener("click", (e) => {
                e.preventDefault();
                e.stopPropagation();
                const isVisible = menu.style.display === "block";
                
                // Close any open menus
                document.querySelectorAll(".Dropdown2_dropdown__ULp_Y").forEach(m => m.style.display = "none");
                
                if (!isVisible) {
                    menu.style.display = "block";
                }
            });
            
            // Handle option selection
            const options = menu.querySelectorAll(".Dropdown2_dropdownEl__tTIhL");
            options.forEach(opt => {
                opt.style.cursor = "pointer";
                opt.style.pointerEvents = "auto";
                
                opt.addEventListener("click", (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    const optContent = opt.querySelector(".Dropdown2_contentIn__kRnA_");
                    const inputContent = input.querySelector(".Dropdown2_contentIn__kRnA_");
                    if (optContent && inputContent) {
                        inputContent.innerHTML = optContent.innerHTML;
                    }
                    menu.style.display = "none";
                });
            });
        }
    });
    
    // Close dropdowns when clicking anywhere else on the page
    document.addEventListener("click", () => {
        document.querySelectorAll(".Dropdown2_dropdown__ULp_Y").forEach(m => m.style.display = "none");
    });
})();
</script>
</body>
"""
    final_html = final_html.replace("</body>", js_snippet)

    with open(out_file, "w", encoding="utf-8") as f:
        f.write(final_html)
    print(f"Processed {basename} -> {target_filename}")
