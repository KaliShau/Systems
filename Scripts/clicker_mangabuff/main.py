import os
import time
from pathlib import Path
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException

def load_config():
    env_path = Path(__file__).parent / '.env'
    if not env_path.exists():
        env_path = Path.home() / '.mangabuff' / '.env'
    
    load_dotenv(env_path)

load_config()

CONFIG = {
    'email': os.getenv('EMAIL'),
    'password': os.getenv('PASSWORD'),
    'login_url': os.getenv('LOGIN_URL'),
    'clicker_url': os.getenv('CLICKER_URL'),
    'click_button_selector': os.getenv('CLICK_BUTTON_SELECTOR'),
    'clicks_count': int(os.getenv('CLICKS_COUNT', 100)),
    'delay': float(os.getenv('DELAY_BETWEEN_CLICKS', 0.5)),
    'headless': os.getenv('HEADLESS', 'false').lower() == 'true',
    'timeout': int(os.getenv('TIMEOUT', 60)),
    'retries': int(os.getenv('RETRIES', 3))
}

def validate_config():
    required = ['email', 'password', 'login_url', 'clicker_url', 'click_button_selector']
    for var in required:
        if not CONFIG[var]:
            raise ValueError(f'Отсутствует обязательная переменная: {var}')

def init_firefox():
    opts = FirefoxOptions()
    if CONFIG['headless']:
        opts.add_argument("--headless")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--window-size=1920,1080")
    opts.set_preference("dom.webdriver.enabled", False)
    opts.set_preference("useAutomationExtension", False)
    opts.set_preference("network.http.phishy-userpass-length", 255)
    
    service = Service(
        executable_path='/usr/local/bin/geckodriver',
        log_path=os.path.join(os.getcwd(), 'geckodriver.log')
    )
    
    driver = webdriver.Firefox(service=service, options=opts)
    driver.set_page_load_timeout(CONFIG['timeout'])
    driver.implicitly_wait(10)
    return driver

def login(driver):
    print("⌛ Выполняю вход...")
    for attempt in range(1, CONFIG['retries'] + 1):
        try:
            print(f"Попытка {attempt} из {CONFIG['retries']}")
            driver.get(CONFIG['login_url'])
            
            # Ждем либо email поле, либо password поле, либо кнопку входа
            WebDriverWait(driver, CONFIG['timeout']).until(
                lambda d: d.find_elements(By.CSS_SELECTOR, "input[type='email'], input[type='password'], button[type='submit'], .login-button")
            )
            
            # Поиск элементов с более гибкими селекторами
            email_field = driver.find_element(By.CSS_SELECTOR, "input[type='email'], input[name='email'], #email")
            password_field = driver.find_element(By.CSS_SELECTOR, "input[type='password'], input[name='password'], #password")
            submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit'], .login-button, .btn-login")
            
            email_field.clear()
            email_field.send_keys(CONFIG['email'])
            
            password_field.clear()
            password_field.send_keys(CONFIG['password'])
            
            submit_btn.click()
            
            # Ждем успешного входа
            WebDriverWait(driver, CONFIG['timeout']).until(
                lambda d: d.current_url != CONFIG['login_url'] or
                d.find_elements(By.CSS_SELECTOR, ".user-avatar, .logout-btn, .profile-icon, .account-info")
            )
            print("✓ Вход выполнен успешно")
            return True
            
        except Exception as e:
            print(f"⚠ Ошибка при попытке {attempt}: {type(e).__name__}: {str(e)}")
            if attempt < CONFIG['retries']:
                print("Повторная попытка через 5 секунд...")
                time.sleep(5)
                driver.refresh()
            else:
                print("❌ Все попытки входа завершились ошибкой")
                raise
    
    return False

def perform_clicks(driver):
    print(f"🔍 Перехожу на страницу кликера: {CONFIG['clicker_url']}")
    driver.get(CONFIG['clicker_url'])
    
    print("🔍 Поиск кнопки для кликов...")
    for attempt in range(1, CONFIG['retries'] + 1):
        try:
            button = WebDriverWait(driver, CONFIG['timeout']).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, CONFIG['click_button_selector']))
            )
            
            print(f"🖱️ Начинаю выполнять {CONFIG['clicks_count']} кликов...")
            for i in range(1, CONFIG['clicks_count'] + 1):
                try:
                    button.click()
                    print(f"✅ Клик {i}")
                    time.sleep(CONFIG['delay'])
                except Exception as e:
                    print(f"⚠ Ошибка при клике {i}: {str(e)}")
                    button = driver.find_element(By.CSS_SELECTOR, CONFIG['click_button_selector'])
            
            print("🎉 Все клики успешно выполнены!")
            return True
            
        except TimeoutException:
            print(f"❌ Не удалось найти кнопку по селектору: {CONFIG['click_button_selector']}")
            if attempt < CONFIG['retries']:
                print(f"Попытка {attempt + 1} из {CONFIG['retries']}")
                driver.refresh()
                time.sleep(3)
            else:
                print("ℹ️ Текущий HTML страницы:")
                print(driver.page_source[:2000])
                raise
        except Exception as e:
            print(f"❌ Неожиданная ошибка: {str(e)}")
            raise
    
    return False

def main():
    validate_config()
    driver = None
    
    try:
        driver = init_firefox()
        
        if not login(driver):
            raise Exception("Не удалось выполнить вход")
            
        if not perform_clicks(driver):
            raise Exception("Не удалось выполнить клики")
            
    except KeyboardInterrupt:
        print("\n🛑 Скрипт остановлен по запросу пользователя (Ctrl+C)")
    except Exception as e:
        print(f"❌ Критическая ошибка: {type(e).__name__}: {str(e)}")
        if driver:
            screenshot_path = os.path.join(os.getcwd(), 'error_screenshot.png')
            driver.save_screenshot(screenshot_path)
            print(f"📸 Скриншот сохранен: {screenshot_path}")
    finally:
        if driver:
            driver.quit()
            print("🛑 Браузер закрыт")

if __name__ == "__main__":
    main()