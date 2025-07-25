from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    # Launch Chromium browser
    browser = p.chromium.launch(headless=False)  # headless=False to see the browser
    page = browser.new_page()
    
    # Navigate to the URL
    page.goto("https://www.keishicho-gto.metro.tokyo.lg.jp/keishicho-u/reserve/offerList_detail?tempSeq=396&accessFrom=offerList")
    print("Navigated to the page")

    # Click the login button
    page.click('.common-header-loginbtn')
    print("Clicked the login button")

    # Wait for the page to fully load
    page.wait_for_load_state('load')  # or 'networkidle' for a more robust wait

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
    
    # print("Please click on the target element to continue...")
    # page.wait_for_selector('.time--table.time--th--date.bordernone.tdSelect.enable')
    # page.eval_on_selector('.time--table.time--th--date.bordernone.tdSelect.enable', '''
    #     element => new Promise(resolve => {
    #         element.addEventListener('click', () => resolve());
    #     })
    # ''')
    # print("Detected click on the target element. Continuing...")

    
    # page.wait_for_load_state('load')  # or 'networkidle' for a more robust wait
    # page.click('input[class="c-btn_2 button-outline"]')
    # page.wait_for_load_state('load')  # or 'networkidle' for a more robust wait
    # page.click('input[class="c-btn_2 button-outline"]')

    # print("Please click on the target element to continue...")
    # page.wait_for_selector('.time--table.time--th--date.bordernone.tdSelect.enable')
    # page.eval_on_selector('.time--table.time--th--date.bordernone.tdSelect.enable', '''
    #     element => new Promise(resolve => {
    #         element.addEventListener('click', () => resolve());
    #     })
    # ''')
    # print("Detected click on the target element. Continuing...")

    # print("Please click on the target element to continue...")
    # page.wait_for_selector('.time--table.time--th.enable.bordernone.tdSelect')
    # page.eval_on_selector('.time--table.time--th.enable.bordernone.tdSelect', '''
    #     element => new Promise(resolve => {
    #         element.addEventListener('click', () => resolve());
    #     })
    # ''')
    # print("Detected click on the target element. Continuing...")

    # Wait for 30 seconds
    time.sleep(3000)
    
    # Close the browser
    browser.close()