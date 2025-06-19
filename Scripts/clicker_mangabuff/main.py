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
    if CONFIG['headless'] or os.getenv('CI_MODE'):
        opts.add_argument("--headless")
    
    # Критические настройки для CI
    opts.add_argument("--disable-gpu")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--window-size=1920,1080")
    
    # Увеличенные таймауты для CI
    service = Service(
        executable_path='/usr/local/bin/geckodriver',
        service_args=['--log', 'debug'],
        log_output="geckodriver.log"
    )
    
    # Явное ожидание драйвера
    driver = webdriver.Firefox(
        service=service,
        options=opts,
        timeout=30 
    )
    return driver

def login(driver):
    print("⌛ Выполняю вход...")
    try:
        driver.set_page_load_timeout(45)  # Увеличенный таймаут загрузки
        driver.get(CONFIG['login_url'])
        
        # Дополнительные ожидания для CI
        WebDriverWait(driver, 45).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        
        # Альтернативные селекторы
        email_field = WebDriverWait(driver, 45).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email'], input[name='email']"))
        )
        email_field.send_keys(CONFIG['email'])
        
        password_field = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password'], input[name='password']"))
        )
        password_field.send_keys(CONFIG['password'])
        
        submit_btn = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit'], .login-button, input[type='submit']"))
        )
        submit_btn.click()
        
        # Проверка успешного входа
        WebDriverWait(driver, 45).until(
            lambda d: "login" not in d.current_url.lower()
        )
        
    except Exception as e:
        driver.save_screenshot("login_error.png")
        print("🔄 Попытка альтернативного метода входа...")
        raise

def perform_clicks(driver):
    print("🔍 Поиск кнопки для кликов...")
    button = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, CONFIG['click_button_selector']))
    )
    
    print(f"🖱️ Начинаю выполнять клики...")
    for i in range(1, CONFIG['clicks_count'] + 1):
        button.click()
        print(f"✅ Клик {i}")
        time.sleep(CONFIG['delay'])

def main():
    validate_config()
    driver = init_firefox()
    
    try:
        login(driver)
        perform_clicks(driver)
        print("🎉 Все клики успешно выполнены!")
    except KeyboardInterrupt:
        print("\n🛑 Скрипт остановлен по запросу пользователя (Ctrl+C)")
    except Exception as e:
        driver.save_screenshot("error.png")
        print(f"Скриншот ошибки сохранён как error.png")
        raise
    finally:
        driver.quit()
        print("🛑 Браузер закрыт")

if __name__ == "__main__":
    main()