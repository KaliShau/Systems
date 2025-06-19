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
from selenium.common.exceptions import TimeoutException, NoSuchElementException

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
    'timeout': int(os.getenv('TIMEOUT', 30))  # Добавляем таймаут в конфиг
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
    opts.set_preference("dom.webdriver.enabled", False)
    opts.set_preference("useAutomationExtension", False)
    service = Service(executable_path='/usr/local/bin/geckodriver')
    
    # Увеличиваем таймауты для Firefox
    driver = webdriver.Firefox(service=service, options=opts)
    driver.set_page_load_timeout(CONFIG['timeout'])
    driver.implicitly_wait(10)
    return driver

def login(driver):
    print("⌛ Выполняю вход...")
    try:
        driver.get(CONFIG['login_url'])
        
        # Ждем появления формы входа
        WebDriverWait(driver, CONFIG['timeout']).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email'], input[type='password']"))
        )

        email_field = driver.find_element(By.CSS_SELECTOR, "input[type='email']")
        password_field = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
        submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit'], .login-button")

        email_field.send_keys(CONFIG['email'])
        password_field.send_keys(CONFIG['password'])
        submit_btn.click()

        # Ждем успешного входа (либо изменения URL, либо появления элемента профиля)
        WebDriverWait(driver, CONFIG['timeout']).until(
            lambda d: d.current_url != CONFIG['login_url'] or
            d.find_elements(By.CSS_SELECTOR, ".user-avatar, .logout-btn, .profile-icon")
        )
        print("✓ Вход выполнен успешно")
        
    except TimeoutException:
        print("⚠ Превышено время ожидания загрузки страницы входа")
        raise
    except Exception as e:
        print(f"❌ Ошибка при входе: {str(e)}")
        raise

def perform_clicks(driver):
    print(f"🔍 Перехожу на страницу кликера: {CONFIG['clicker_url']}")
    driver.get(CONFIG['clicker_url'])
    
    print("🔍 Поиск кнопки для кликов...")
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
                # Пробуем снова найти кнопку на случай изменения DOM
                button = driver.find_element(By.CSS_SELECTOR, CONFIG['click_button_selector'])
                
    except TimeoutException:
        print(f"❌ Не удалось найти кнопку по селектору: {CONFIG['click_button_selector']}")
        print("ℹ️ Текущий HTML страницы:")
        print(driver.page_source[:1000])  # Выводим часть HTML для диагностики
        raise
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {str(e)}")
        raise

def main():
    validate_config()
    driver = None
    
    try:
        driver = init_firefox()
        login(driver)
        perform_clicks(driver)
        print("🎉 Все клики успешно выполнены!")
    except KeyboardInterrupt:
        print("\n🛑 Скрипт остановлен по запросу пользователя (Ctrl+C)")
    except Exception as e:
        print(f"❌ Критическая ошибка: {type(e).__name__}: {str(e)}")
    finally:
        if driver:
            driver.quit()
            print("🛑 Браузер закрыт")

if __name__ == "__main__":
    main()