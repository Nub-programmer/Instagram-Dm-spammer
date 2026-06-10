import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager

def start_automation(username, password, chat_url, message, interval, stop_event, log_callback=print):
    options = Options()
    options.add_argument("-headless")
    options.set_preference("general.useragent.override", "Mozilla/5.0 (X11; Linux x86_64; rv:133.0) Gecko/20100101 Firefox/133.0")

    log_callback("Setting up background browser...")
    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=options)

    try:
        log_callback("Navigating to Instagram...")
        driver.get("https://www.instagram.com/accounts/login/")
        
        username_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='username'], input[type='text']"))
        )
        password_input = driver.find_element(By.CSS_SELECTOR, "input[name='password'], input[type='password']")
        
        username_input.send_keys(username)
        password_input.send_keys(password)
        password_input.send_keys(Keys.ENTER)
        
        log_callback("Login submitted. Waiting for authentication...")
        
        for _ in range(20):
            if stop_event.is_set():
                log_callback("[SYSTEM] Loop stopped during auth phase.")
                return
            time.sleep(0.5)
        
        log_callback("Jumping to target chat thread...")
        driver.get(chat_url)
        
        try:
            not_now_btn = WebDriverWait(driver, 8).until(
                EC.element_to_be_clickable((By.XPATH, "//button[text()='Not Now']"))
            )
            not_now_btn.click()
        except:
            pass

        log_callback("[SUCCESS] Spammer engine sequence armed!")
        while not stop_event.is_set():
            try:
                chat_box = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "div[role='textbox'][contenteditable='true']"))
                )
                
                chat_box.click()
                time.sleep(0.3)
                
                chat_box.send_keys(Keys.CONTROL + "a")
                chat_box.send_keys(Keys.BACKSPACE)
                time.sleep(0.3)
                
                for letter in message:
                    if stop_event.is_set():
                        break
                    chat_box.send_keys(letter)
                    time.sleep(0.15)  
                
                if stop_event.is_set():
                    break
                    
                time.sleep(0.3)  
                chat_box.send_keys(Keys.ENTER)
                log_callback(f" -> Sent '{message}' successfully at {time.strftime('%H:%M:%S')}")
                
                start_sleep = time.time()
                while time.time() - start_sleep < interval:
                    if stop_event.is_set():
                        break
                    time.sleep(0.2)
                    
            except Exception:
                driver.save_screenshot("loop_error.png")
                time.sleep(5)

    except Exception as e:
        log_callback(f"[ERROR] Execution error: {e}")
        driver.save_screenshot("critical_error.png")
    finally:
        driver.quit()
        log_callback("[SYSTEM] Background browser closed securely.")
