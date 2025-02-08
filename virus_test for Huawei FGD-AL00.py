from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
import time
from datetime import datetime


capabilities = dict(
 deviceName="2HSYD23C02201674",
 platformName="Android",
 automationName="uiautomator2",
 noReset= True
)

appium_server_url = 'http://localhost:4723'
driver = webdriver.Remote(appium_server_url, options=UiAutomator2Options().load_capabilities(capabilities))

app_name = "" #紀錄當前app名稱

#設定WebDriver 在執行找元素的操作時，最大等待時間是 5 秒
driver.implicitly_wait(5)

#截圖並存現在時間
def screenshot():
    current_time = str(datetime.now().date())+"_"+str(datetime.now().time().strftime("%H%M%S"))
    driver.get_screenshot_as_file(app_name+"_"+current_time+'.png')
    print("截圖名稱："+app_name+"_"+current_time+'.png')


#點擊進到指定位置

driver.find_element(by=AppiumBy.XPATH, value='(//android.widget.TextView[@content-desc="文件管理"])').click()
driver.find_element(by=AppiumBy.XPATH, value='(//android.widget.RelativeLayout[@resource-id="com.huawei.filemanager:id/layout_file_detail"])[1]').click();
driver.find_element(by=AppiumBy.XPATH, value='//*[@text="Download"]').click();
driver.find_element(by=AppiumBy.XPATH, value='//*[@text="virus_test"]').click();

#依序開啟資料夾，最多可開啟12個資料夾
for project_folder in range(1,13):
    try:
        driver.implicitly_wait(5)
        driver.find_element(by=AppiumBy.XPATH, value='(//android.widget.ImageView[@resource-id="com.huawei.filemanager:id/file_icon"])['+str(project_folder)+']').click();
    except:
        print("全部project完成\n")
        break
    #依序安裝APP，最多一個資料夾內可以有12個apk
    for bd in range(1,13):
        
        if bd != 1 :
            driver.find_element(by=AppiumBy.XPATH, value='(//android.widget.TextView[@content-desc="文件管理"])').click()
        
        try:
            #點擊index
            driver.implicitly_wait(5)
            driver.find_element(by=AppiumBy.XPATH, value='(//android.widget.ImageView[@resource-id="com.huawei.filemanager:id/file_icon"])['+str(bd)+']').click();
        except:
            print("project完成\n")
            break

        #儲存APP名稱為變數
        driver.implicitly_wait(10)
        app_name = driver.find_element(by=AppiumBy.XPATH, value='//android.widget.TextView[@resource-id="com.huawei.appmarket:id/head_app_name"]').get_attribute("text")


        #檢查有無報毒提示
        try:
            driver.implicitly_wait(5)
            if(driver.find_element(by=AppiumBy.XPATH, value='//*[@text="发现恶意应用"]')):
                print("Fail：'"+app_name+"'報毒")
                
                #報毒時截圖
                screenshot()
                print("\n")
                driver.find_element(by=AppiumBy.XPATH, value='//*[@text="取消"]').click()
                driver.press_keycode(3)

                


        #安裝未爆毒執行以下
        except:
            driver.implicitly_wait(15)
            print("Pass：'"+app_name+"'未出現報毒")
             
            #未報毒截圖
            screenshot()

            #點擊checkbox
            driver.find_element(by=AppiumBy.XPATH, value='//android.widget.CheckBox[@resource-id="com.huawei.appmarket:id/hidden_card_checkbox"]').click();

            #點擊安裝
            driver.find_element(by=AppiumBy.XPATH, value='//android.widget.Button[@resource-id="com.huawei.appmarket:id/hidden_card_install_button_continue"]').click();

            #點擊密碼欄位輸入密碼後
            pw = driver.find_element(by=AppiumBy.XPATH, value='//*[@text="密码"]')
            pw.click();
            pw.send_keys("aa123456")

            #按確定完成安裝
            driver.find_element(by=AppiumBy.XPATH, value='//*[@text="确定"]').click();
             
            driver.find_element(by=AppiumBy.XPATH, value='//*[@text="打开"]').click();

            #等待開啟後紀錄packageName
            time.sleep(10)
            package_name = driver.current_package
            print("packagenmae="+package_name)
            time.sleep(3)

            #開啟10秒後返回首頁並刪除APP
            driver.press_keycode(3)
            driver.remove_app(package_name)
            print("完成\n")
        
    driver.press_keycode(4)