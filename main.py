from playwright.sync_api import sync_playwright
import time
def write_to_text(content, url="result.txt"):
    with open(url, "w", encoding="utf-8") as f:
        f.write(content)
def extract_name(full_string):
    name_part = full_string.replace("Avv. ", "")
    parts = name_part.split()
    name = parts[0]
    surname = " ".join(parts[1:]) if len(parts) > 1 else ""
    return name, surname
def extract_data(base_url, province):
    url = base_url + province
    try:
        with sync_playwright() as p:
            # Launch browser with more reliable settings
            browser = p.chromium.launch(
                headless=True,
                timeout=60000,
                slow_mo=100
            )
            context = browser.new_context(
                viewport={'width': 1280, 'height': 1024},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            )
            page = context.new_page()
            page.set_default_timeout(60000)
            # Navigate to page with retries
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    page.goto(url, timeout=60000, wait_until="domcontentloaded")
                    page.wait_for_selector("body", state="attached", timeout=30000)
                    break
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise
                    time.sleep(2)
            # Extract Lawyers Profile
            print("Extracting Lawyers...")
            result = f""
            while True:
                lawyers_section = page.query_selector('section#trova-avvocato')
                if not lawyers_section:
                    print("Lawyers section not found")
                    break
                lawyers_profile_btns = lawyers_section.query_selector_all(".trova-avvocato-scheda a:has-text('Visualizza profilo')")
                for btn in lawyers_profile_btns:
                    href = btn.get_attribute('href')
                    if not href:
                        continue
                    try:
                        new_page = page.context.new_page()
                        new_page.goto("https://avvocato360.it" + href, wait_until="domcontentloaded", timeout=15000)
                        new_page.wait_for_selector("body", state="attached", timeout=30000)
                        new_result = province.replace('-', ' ').title() + "\t"
                        try:
                            profile_name_section = new_page.query_selector('div.avvocato-profilo-nome h1')
                            if profile_name_section:
                                profile_name_text = profile_name_section.text_content().strip()
                                name, surname = extract_name(profile_name_text)
                                new_result += f"{name}\t{surname}"
                            else:
                                new_result += "\t\t"  # Empty name and surname if not found
                            contact_divs = new_page.query_selector_all('div.avvocato-contatti .contatto .col-9')
                            contact_info = []
                            def is_phone_number(text):
                                if text.startswith('+'):
                                    return text[1:].isdigit() and len(text) > 1  # At least 1 digit after +
                                return text.isdigit() and len(text) > 0
                            def is_email(text):
                                return '@' in text and '.' in text.split('@')[-1]
                            phone_numbers = 0
                            emails = 0
                            for i, div in enumerate(contact_divs):
                                text = div.text_content().strip()
                                if is_phone_number(text):
                                    contact_info.append(text)
                                    phone_numbers = phone_numbers + 1
                                if phone_numbers == 2:
                                    break
                            # Ensure we have exactly 2 phone number slots
                            if phone_numbers < 2:
                                for _ in range(phone_numbers, 2):
                                    contact_info.append("")
                            for i, div in enumerate(contact_divs):
                                text = div.text_content().strip()
                                if is_email(text):
                                    contact_info.append(text)
                                    emails = emails + 1
                                if emails == 2:
                                    break
                            if emails < 2:
                                for _ in range(emails, 2):
                                    contact_info.append("")
                            contact_str = "\t".join(contact_info)
                            new_result += "\t" + contact_str
                            print(new_result)
                            result += new_result + "\n"
                        except Exception as e:
                            print(f"New page error")
                    except Exception as e:
                        print(f"Failed to process")
                    finally:
                        if 'new_page' in locals():
                            new_page.close()
                next_page_btn = page.query_selector('a.pagination-elm.goto-last')
                if not next_page_btn:
                    break
                print("Moving to next page...")
                next_page_btn.click()
                page.wait_for_load_state('domcontentloaded')
            return result
    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        try:
            context.close()
            browser.close()
        except:
            pass
provinces = ["Roma", "Milano", "Napoli", "Torino", "Brescia", "Bari", "Palermo", "Bergamo", "Catania", "Bologna", "Salerno", "Firenze", "Padova", "Verona", "Caserta", "Treviso",
"Genova", "Lecce", "Cosenza", "Reggio-calabria", "Parma", "Cagliari", "Monza"]
res = ""
for i, prov in enumerate(provinces):
    res += extract_data('https://avvocato360.it/avvocato-amministrativista/', prov)
write_to_text(res)