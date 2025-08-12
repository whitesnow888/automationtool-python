from playwright.sync_api import sync_playwright
import time
import pandas as pd

with sync_playwright() as p:
    
    try:
            
        browser = p.chromium.launch(headless=True)  
        page = browser.new_page()

        # Navigate to the  URL
        page.goto("https://www.keishicho-gto.metro.tokyo.lg.jp/keishicho-u/reserve/offerList_detail?tempSeq=396&accessFrom=offerList")
        print("Navigated to the page")

        page.click('.common-header-loginbtn')
        print("Clicked the login button")

        page.fill('input[id="userLoginForm.userId"]', "k-ikeda@technosmile.co.jp")
        page.fill('input[id="userLoginForm.userPasswd"]', "Tokyo0Gaimen")

        page.click('input[type="submit"]')
        print("Clicked the login button after filling in credentials")

        page.goto("https://www.keishicho-gto.metro.tokyo.lg.jp/keishicho-u/reserve/offerList_detail?tempSeq=396")
        
        page.click('label[for="reserveCaution"]')

        for i in range(10):
            page.wait_for_load_state('load', timeout=60000)  # Wait for 60 seconds
            radio_button = page.query_selector("input[value='1か月後＞']")
            if radio_button and radio_button.is_disabled():
                print("Radio button is disabled. Exiting loop.")
                break
            page.click("input[value='1か月後＞']")
            print(f"Clicked radio button for '1か月後＞' {i+1} times")

        for i in range(10):
            page.wait_for_load_state('load')
            radio_button = page.query_selector("input[value='2週後＞']")
            if radio_button and radio_button.is_disabled():
                print("Radio button is disabled. Exiting loop.")
                break
            page.click("input[value='2週後＞']")
            print(f"Clicked radio button for '2週後＞' {i+1} times")
                
        
        flg = 0
        
        while flg < 300:
            time.sleep(3)
            page.wait_for_selector('#waitTime', state='detached', timeout=600000000)
            for i in range(3, 17):  
                cell = page.query_selector(f"table tbody tr:nth-child(4) td:nth-child({i}).time--table.time--th--date.bordernone.tdSelect.enable")
                if(cell):
                    print("Cell found with the specified class. Clicking the cell...")
                    cell.click()
                    flg = 1
                    break
                else:
                    print(f"{i}Cell with the specified class not found.")
            flg = flg + 1
        
        
        time.sleep(2)

        if(flg == 0):
            print("No available time slots found. Exiting.")
            browser.close()
            exit()
        page.click('td#pc-0_6')
        page.click('td#pc-0_66')
        page.click('td#pc-0_60')

        cell = page.query_selector('.c-btn_2.button-outline')
        cell.click()

        page.wait_for_load_state('load', timeout=60000)  # Wait for the page to load
        cell = page.query_selector('.c-btn_2.button-outline')
        cell.click()
        
        
        df = pd.read_excel('data.xlsx', header=None)

        data_values = df.iloc[:,1]
        print("Data values:", data_values.tolist())

        page.wait_for_load_state('load', timeout=60000)  # Wait for the page to load

        #page1
        page.fill('input[id="switch_8691"]', str(data_values[0]))  # 国籍(1)
        page.fill('input[id="switch_8692"]', str(data_values[1]))  # 国籍(2)
        page.fill('input[id="item_2_textData"]', str(data_values[2]))  # 郵便番号
        page.select_option('select[id="switch_8820_city"]', label=(data_values[3]))  # 住所（都道府県）
        time.sleep(1)  
        if(data_values[4] != ""):
            page.select_option('select[id="switch_8820_town"]', label=(data_values[4]))  # 住所（町・大字）
        time.sleep(1)  
        if(data_values[5] != ""):
            page.select_option('select[id="switch_8820_block"]', label=str(data_values[5]))  # 住所（丁目・字）

        page.fill('input[id="applicant_lastName"]', str(data_values[7]))  # 氏名(英文字入力)(氏)
        page.fill('input[id="applicant_firstName"]', str(data_values[8]))  # 氏名(英文字入力)(名)
        page.fill('input[id="switch_8695"]', str(data_values[9]))  # 生年月日
        page.fill('input[id="phoneNumber_8696"]', str(data_values[10]))  # 電話番号
        page.fill('input[id="switch_8697"]', str(data_values[11]))  # パスポート番号
        page.fill('input[id="switch_8698"]', str(data_values[12]))  # 免許発給国・地域
        page.fill('input[id="switch_8699"]', str(data_values[13]))  # 外国免許証の免許番号
        
        checkboxes = page.locator('p.u-mb6 label')
        for i in range(3):
            if(data_values[14+i]):
                checkboxes.nth(i).check()
                time.sleep(0.5)
                page.fill(f'input[id="checkList_8700_{1+i}_text"]', str(data_values[14+i]))
            
        print(data_values[17])
        if(data_values[17]):
            label = page.locator('label[for="radioList_8701_1"]')
            label.click()
            time.sleep(0.5)
            page.fill('input[id="radioList_8701_1_text"]', str(data_values[17]))
        else:
            label = page.locator('label[for="radioList_8701_2"]')
            label.click()
            time.sleep(0.5)

        if(data_values[18] == "あり"):
            label = page.locator('label[for="radioList_8702_1"]')
            label.click()
        else :
            label = page.locator('label[for="radioList_8702_2"]')
            label.click()

        #page2
        page.click('input[value="次へ"]')
        time.sleep(2)  # Wait for the next page to load
        page.wait_for_load_state('load', timeout=60000)  # Wait for the page to load
        page.fill('input[id="switch_8706"]', str(data_values[19]))  # 四輪車取得年
        page.fill('input[id="switch_8707"]', str(data_values[20]))  # 二輪車取得年
        page.fill('input[id="switch_8708"]', str(data_values[21]))  # 外国免許証の取得年
        page.fill('input[id="switch_8710"]', str(data_values[22]))  # 外国免許証の取得国・地域
        page.fill('input[id="switch_8711"]', str(data_values[23]))  
        page.fill('input[id="switch_8712"]', str(data_values[24]))  
        page.fill('input[id="switch_8714"]', str(data_values[25]))  
        page.fill('input[id="switch_8716"]', str(data_values[26]))  
        page.fill('input[id="switch_8717"]', str(data_values[27]))  
        page.fill('input[id="switch_8718"]', str(data_values[28]))  
        page.fill('input[id="switch_8720"]', str(data_values[29]))  
        page.fill('input[id="switch_8721"]', str(data_values[30]))  
        page.fill('input[id="switch_8722"]', str(data_values[31]))  
        page.fill('input[id="switch_8724"]', str(data_values[32]))  
        page.fill('input[id="switch_8726"]', str(data_values[33]))  
        page.fill('input[id="switch_8727"]', str(data_values[34]))  
        page.fill('input[id="switch_8728"]', str(data_values[35]))  
        page.fill('input[id="switch_8730"]', str(data_values[36]))  
        page.fill('input[id="switch_8731"]', str(data_values[37]))  
        page.fill('input[id="switch_8732"]', str(data_values[38]))  
        page.fill('input[id="switch_8734"]', str(data_values[39]))  
        page.fill('input[id="switch_8736"]', str(data_values[40]))  
        page.fill('input[id="switch_8737"]', str(data_values[41]))  
        page.fill('input[id="switch_8738"]', str(data_values[42]))  
        page.fill('input[id="switch_8740"]', str(data_values[43]))  
        page.fill('input[id="switch_8741"]', str(data_values[44]))  
        page.fill('input[id="switch_8742"]', str(data_values[45]))  
        page.fill('input[id="switch_8744"]', str(data_values[46]))  
        page.fill('input[id="switch_8746"]', str(data_values[47]))  
        page.fill('input[id="switch_8747"]', str(data_values[48]))  
        page.fill('input[id="switch_8748"]', str(data_values[49]))  
        page.fill('input[id="switch_8750"]', str(data_values[50]))  
        page.fill('input[id="switch_8751"]', str(data_values[51]))  
        page.fill('input[id="switch_8752"]', str(data_values[52]))  
        page.fill('input[id="switch_8754"]', str(data_values[53]))  

        #page3
        button = page.locator('#lastTab1')
        button.nth(2).click()
        page.wait_for_load_state('load', timeout=60000)  # Wait for the page to load
        page.fill('input[id="switch_8758"]', str(data_values[54]))  
        page.fill('input[id="switch_8759"]', str(data_values[55]))  
        page.fill('input[id="switch_8760"]', str(data_values[56]))  
        page.fill('input[id="switch_8762"]', str(data_values[57]))  
        page.fill('input[id="switch_8763"]', str(data_values[58]))  
        page.fill('input[id="switch_8764"]', str(data_values[59]))  
        page.fill('input[id="switch_8766"]', str(data_values[60]))  
        page.fill('input[id="switch_8768"]', str(data_values[61]))  
        page.fill('input[id="switch_8769"]', str(data_values[62]))  
        page.fill('input[id="switch_8770"]', str(data_values[63]))  
        page.fill('input[id="switch_8772"]', str(data_values[64]))  
        page.fill('input[id="switch_8773"]', str(data_values[65]))  
        page.fill('input[id="switch_8774"]', str(data_values[66]))  
        page.fill('input[id="switch_8776"]', str(data_values[67]))  
        page.fill('input[id="switch_8778"]', str(data_values[68]))  
        page.fill('input[id="switch_8779"]', str(data_values[69]))  
        page.fill('input[id="switch_8780"]', str(data_values[70]))  
        page.fill('input[id="switch_8782"]', str(data_values[71]))  
        page.fill('input[id="switch_8783"]', str(data_values[72]))  
        page.fill('input[id="switch_8784"]', str(data_values[73]))  
        page.fill('input[id="switch_8786"]', str(data_values[74]))  
        page.fill('input[id="switch_8788"]', str(data_values[75]))  
        page.fill('input[id="switch_8789"]', str(data_values[76]))  
        page.fill('input[id="switch_8790"]', str(data_values[77]))  
        page.fill('input[id="switch_8792"]', str(data_values[78]))  
        page.fill('input[id="switch_8793"]', str(data_values[79]))  
        page.fill('input[id="switch_8794"]', str(data_values[80]))  
        page.fill('input[id="switch_8796"]', str(data_values[81]))  
        page.fill('input[id="switch_8798"]', str(data_values[82]))  
        page.fill('input[id="switch_8799"]', str(data_values[83]))  
        page.fill('input[id="switch_8800"]', str(data_values[84]))  
        page.fill('input[id="switch_8802"]', str(data_values[85]))  
        page.fill('input[id="switch_8803"]', str(data_values[86]))  
        page.fill('input[id="switch_8804"]', str(data_values[87]))  
        page.fill('input[id="switch_8806"]', str(data_values[88]))  



        # time.sleep(10)
        #page3
        button = page.locator('#lastTab1')
        button.nth(4).click()
        
        page.wait_for_load_state('load', timeout=60000)  # Wait for the page to load
        if(data_values[89] == "はい"):
            page.click('label[for="radioList_8808_1"]')  # 現在、日本の運転免許は停止処分中ですか？
        else:
            page.click('label[for="radioList_8808_2"]')  

        if(data_values[90] == "はい"):
            page.click('label[for="radioList_8809_1"]')  # 運転免許に関する処分について
        else:
            page.click('label[for="radioList_8809_2"]')

        if(data_values[91] == "はい"):
            page.click('label[for="radioList_8810_1"]')  # 日本国内で無免許運転、酒気帯び・酒酔い運転、救護義務違反をしたことがありますか？
        else:
            page.click('label[for="radioList_8810_2"]')  

        if(data_values[92] == "はい"):
            #日本語により、日常会話のほか、質問に対する的確な応答ができますか？
            page.click('label[for="radioList_8811_1"]')  
        else:
            page.click('label[for="radioList_8811_2"]')  
            page.fill('input[id="fullName1_8812"]', str(data_values[93])) # 氏名(カタカナ入力)(氏)
            page.fill('input[id="fullName2_8812"]', str(data_values[94]))  # 氏名(カタカナ入力)(名) 
            page.fill('input[id="phoneNumber_8813"]',str(data_values[95]))  # 電話番号(カタカナ入力)

        if(data_values[96] == "はい"):
            page.click('label[for="radioList_8814_1"]')  
        else:
            page.click('label[for="radioList_8814_2"]')  

        if(data_values[97] == "持っている"):
            page.click('label[for="radioList_8815_1"]')
            page.fill('input[id="switch_8816"]', str(data_values[98]))  
            page.fill('input[id="switch_8817"]', str(data_values[99]))  
            page.fill('input[id="switch_8818"]', str(data_values[100]))  
        else:
            page.click('label[for="radioList_8815_2"]')

        page.click('input[value="確認へ進む"]')  # Click the button to proceed to confirmation
        page.wait_for_load_state('load', timeout=60000)  # Wait for the page to load
        page.click('input[value="申込む"]')

        browser.close()
        print(f"予約成功")
        with open("./結果.txt", "w", encoding="utf-8") as f:
            f.write("予約成功")

    except Exception as e:
        print(f"予約失敗")
        browser.close()
        with open("./結果.txt", "w", encoding="utf-8") as f:
            f.write("予約失敗")
