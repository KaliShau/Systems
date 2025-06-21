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


def load_config():
    config = {
        'email': os.environ.get('EMAIL'),
        'password': os.environ.get('PASSWORD'),
        'login_url': os.environ.get('LOGIN_URL'),
        'clicker_url': os.environ.get('CLICKER_URL'),
        'click_button_selector': os.environ.get('CLICK_BUTTON_SELECTOR'),
        'clicks_count': int(os.environ.get('CLICKS_COUNT', 100)),
        'delay': float(os.environ.get('DELAY_BETWEEN_CLICKS', 0.5)),
        'headless': os.environ.get('HEADLESS', 'false').lower() == 'true'
    }
    
    if None in config.values():
        env_path = Path(__file__).parent / '.env'
        if not env_path.exists():
            env_path = Path.home() / '.mangabuff' / '.env'
        
        if env_path.exists():
            load_dotenv(env_path)
            config.update({
                'email': os.getenv('EMAIL'),
                'password': os.getenv('PASSWORD'),
                'login_url': os.getenv('LOGIN_URL'),
                'clicker_url': os.getenv('CLICKER_URL'),
                'click_button_selector': os.getenv('CLICK_BUTTON_SELECTOR'),
                'clicks_count': int(os.getenv('CLICKS_COUNT', 100)),
                'delay': float(os.getenv('DELAY_BETWEEN_CLICKS', 0.5)),
                'headless': os.getenv('HEADLESS', 'false').lower() == 'true'
            })
    
    return config

CONFIG = load_config()

def validate_config():
    required = ['email', 'password', 'login_url', 'clicker_url', 'click_button_selector']
    for var in required:
        if not CONFIG[var]:
            raise ValueError(f'Отсутствует обязательная переменная: {var}')

def init_firefox():
    opts = FirefoxOptions()
    if CONFIG['headless']:
        opts.add_argument("--headless")
    opts.set_preference("dom.webdriver.enabled", False)
    opts.set_preference("useAutomationExtension", False)
    service = Service(executable_path='/usr/local/bin/geckodriver') 
    driver = webdriver.Firefox(service=service, options=opts)
    driver.maximize_window()
    return driver

def login(driver):
    print("⌛ Выполняю вход...")
    driver.set_page_load_timeout(60)

    for _ in range(3):
        try:
            driver.get(CONFIG['login_url'])
            WebDriverWait(driver, 10).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            break
        except:
            print("🔄 Повторная попытка загрузки страницы...")
            time.sleep(5)
    
    email_field = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 
            "input[type='email'], input[name='email'], #email, [aria-label='Email']"))
    )
    email_field.send_keys(CONFIG['email'])
    
    password_field = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR,
            "input[type='password'], input[name='password'], #password"))
    )
    password_field.send_keys(CONFIG['password'])
    
    submit_btn = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR,
            "button[type='submit'], .login-button, [value='Login']"))
    )
    submit_btn.click()
    
    WebDriverWait(driver, 30).until(
        lambda d: "login" not in d.current_url.lower()
    )
    print("✓ Вход выполнен успешно")
    print("⌛ Переход на страницу кликов...")
    driver.get(CONFIG["clicker_url"])

def perform_clicks(driver):
    print("🔍 Поиск кнопки для кликов...")
    
    successful_clicks = 0
    attempts = 0
    max_attempts = CONFIG['clicks_count'] * 2  
    
    while successful_clicks < CONFIG['clicks_count'] and attempts < max_attempts:
        try:
            button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, CONFIG['click_button_selector']))
            )
            
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
            time.sleep(0.2)  
            
            button.click()
            successful_clicks += 1
            print(f"✅ Клик {successful_clicks}")
            time.sleep(CONFIG['delay'])
            
        except (StaleElementReferenceException, ElementClickInterceptedException, NoSuchElementException) as e:
            print(f"⚠️ Ошибка при клике {successful_clicks + 1}: {str(e)[:100]}... Попытка восстановления...")
            time.sleep(1)  
            
        attempts += 1
    
    if successful_clicks < CONFIG['clicks_count']:
        print(f"⚠️ Выполнено только {successful_clicks} из {CONFIG['clicks_count']} кликов")
    else:
        print(f"🎉 Все {CONFIG['clicks_count']} кликов успешно выполнены!")

def main():
    validate_config()
    driver = init_firefox()
    
    try:
        login(driver)
        perform_clicks(driver)
    except KeyboardInterrupt:
        print("\n🛑 Скрипт остановлен по запросу пользователя (Ctrl+C)")
    except Exception as e:
        print(f"Ошибка: ", e)
        raise
    finally:
        driver.quit()
        print("🛑 Браузер закрыт")

if __name__ == "__main__":
    main()