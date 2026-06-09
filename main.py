import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager

USERNAME = "your_username" #enter ur username here like mine is _nub.programmer_
PASSWORD = "your_password" #enter ur password here like mine is .... 
CHAT_URL = "https://www.instagram.com/direct/t/17845098993270951/"
INTERVAL = 1 # interval would recommend 10-20 seconds if u wanna do it for a long time but only for 5 or 10 minutes then u can do 1 or 0.1 seconds

options = Options()
options.add_argument("-headless")
options.set_preference("general.useragent.override", "Mozilla/5.0 (X11; Linux x86_64; rv:133.0) Gecko/20100101 Firefox/133.0")

print("Setting up background browser...")
service = Service(GeckoDriverManager().install())
driver = webdriver.Firefox(service=service, options=options)

try:
    print("Navigating to Instagram...")
    driver.get("https://www.instagram.com/accounts/login/")
    
    username_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='username'], input[type='text']"))
    )
    password_input = driver.find_element(By.CSS_SELECTOR, "input[name='password'], input[type='password']")
    
    username_input.send_keys(USERNAME)
    password_input.send_keys(PASSWORD)
    password_input.send_keys(Keys.ENTER)
    
    time.sleep(10)  
    driver.get(CHAT_URL)
    
    try:
        not_now_btn = WebDriverWait(driver, 8).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Not Now']"))
        )
        not_now_btn.click()
    except:
        pass

    print("\n[SUCCESS] Bot loop active!")
    while True:
        try:
            chat_box = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "div[role='textbox'][contenteditable='true']"))
            )
            
            chat_box.click()
            time.sleep(0.3)
            
            chat_box.send_keys(Keys.CONTROL + "a")
            chat_box.send_keys(Keys.BACKSPACE)
            time.sleep(0.3)
            
            for letter in "yes":
                chat_box.send_keys(letter)
                time.sleep(0.15)  
            
            time.sleep(0.3)  
            chat_box.send_keys(Keys.ENTER)
            print(f" -> Sent 'yes' successfully at {time.strftime('%H:%M:%S')}")
            
            time.sleep(INTERVAL)
            
        except Exception:
            driver.save_screenshot("loop_error.png")
            time.sleep(10)

except Exception as main_error:
    print(f"\n[ERROR] Script crashed entirely: {main_error}")
    driver.save_screenshot("critical_error.png")
finally:
    driver.quit()
