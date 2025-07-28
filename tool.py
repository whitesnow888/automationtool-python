from playwright.sync_api import sync_playwright
import time
import pandas as pd

with sync_playwright() as p:
    # Launch Chromium browser
    browser = p.chromium.launch(headless=False)  # headless=False to see the browser
    page = browser.new_page()
    
    # Navigate to the URL
    page.goto("https://www.keishicho-gto.metro.tokyo.lg.jp/keishicho-u/reserve/offerList_detail?tempSeq=396&accessFrom=offerList")
    print("Navigated to the page")

    # Wait for the "WAITTIME" element to disappear, indicating site is ready
    page.wait_for_selector('#waitTime', state='detached', timeout=600000000)
    print("Site is ready for interaction.")
    
    # Click the login button
    page.click('.common-header-loginbtn')
    print("Clicked the login button")

    # Fill in login info
    page.fill('input[id="userLoginForm.userId"]', "k-ikeda@technosmile.co.jp")
    page.fill('input[id="userLoginForm.userPasswd"]', "Tokyo0Gaimen")

    # Click the login button
    page.click('input[type="submit"]')
    print("Clicked the login button after filling in credentials")

    page.goto("https://www.keishicho-gto.metro.tokyo.lg.jp/keishicho-u/reserve/offerList_detail?tempSeq=396")
    
    # Click the label associated with the checkbox
    page.click('label[for="reserveCaution"]')

    for i in range(10):
        # Check if the radio button is disabled
        page.wait_for_load_state('load', timeout=60000)  # Wait for 60 seconds
        radio_button = page.query_selector("input[value='1か月後＞']")
        if radio_button and radio_button.is_disabled():
            print("Radio button is disabled. Exiting loop.")
            break
        # Click the radio button for "1か月後＞"
        page.click("input[value='1か月後＞']")
        print(f"Clicked radio button for '1か月後＞' {i+1} times")

    for i in range(13):
        # Check if the radio button is disabled
        radio_button = page.query_selector("input[value='2週後＞']")
        if radio_button and radio_button.is_disabled():
            print("Radio button is disabled. Exiting loop.")
            break
        # Click the radio button for "2週後＞"
        page.click("input[value='2週後＞']")
        print(f"Clicked radio button for '2週後＞' {i+1} times")
            
    
    for i in range(3, 17):  # Loop through columns
        cell = page.query_selector(f"table tbody tr:nth-child(9) td:nth-child({i}).time--table.time--th--date.bordernone.tdSelect.enable")
        # cell = page.query_selector('table tbody tr:nth-child(9) td:nth-child({i}).time--table.time--th--date.bordernone.disable')
        if(cell):
            print("Cell found with the specified class. Clicking the cell...")
            cell.click()
            break
        else:
            print(f"{i}Cell with the specified class not found.")
    
    
    time.sleep(2)

    page.click('td#pc-0_6')
    page.click('td#pc-0_60')
    page.click('td#pc-0_66')

    # Click the Next button to proceed
    cell = page.query_selector('.c-btn_2.button-outline')
    cell.click()

    page.wait_for_load_state('load', timeout=60000)  # Wait for the page to load
    cell = page.query_selector('.c-btn_2.button-outline')
    cell.click()
    
    #read the main info from csv
    # Read the Excel file
    df = pd.read_excel('asd.xlsx', header=None)

    # The second row contains the data values
    data_values = df.iloc[:,1]

    print("Data values:", data_values.tolist())

    page.wait_for_load_state('load', timeout=60000)  # Wait for the page to load
    #input the data into the form
    page.fill('input[id="switch_8691"]', data_values[0])  # 国籍(1)
    # page.fill('input[id="item_2_textData"]', str(data_values[1]))  # 郵便番号
    # page.select_option('select[id="switch_8820_city"]', value=data_values[3])  # 住所（都道府県）
    # time.sleep(1)  # Wait for the options to load
    # page.select_option('select[id="switch_8820_town"]', value=data_values[4])  # 住所（町・大字）
    # time.sleep(1)  # Wait for the options to load
    # page.select_option('select[id="switch_8820_block"]', value=str(data_values[5]))  # 住所（丁目・字）
    











    time.sleep(300000)
    
    # Close the browser
    browser.close()