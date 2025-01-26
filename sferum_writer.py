import time
import random
import requests
import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def print_message_in_stars(message):
    # Эмодзи для украшения
    star_emoji = "⭐"

    # Создаем рамочку
    border_char = "★"
    border_line = border_char * 10  # Делаем рамочку по длине сообщения

    # Выводим рамочку с сообщением
    print(border_line)
    print(f"{star_emoji} {message} {star_emoji}")
    print(border_line)

# Функция для сохранения куков в файл
def save_cookies(driver, path):
    with open(path, 'wb') as file:
        pickle.dump(driver.get_cookies(), file)

# Функция для загрузки куков из файла
def load_cookies(driver, path):
    try:
        with open(path, 'rb') as file:
            cookies = pickle.load(file)
            for cookie in cookies:
                driver.add_cookie(cookie)
    except FileNotFoundError:
        print("Файл с куками не найден. Необходимо войти вручную.")

# Основной код
cookie_file = "cookies.pkl"  # Файл для хранения куков

# Настраиваем веб-драйвер
driver = webdriver.Chrome()  # Убедитесь, что у вас установлен webdriver для Chrome
driver.get("https://web.vk.me/")  # Замените на URL вашего мессенджера

# Пытаемся загрузить куки
load_cookies(driver, cookie_file)

# Перезагружаем страницу, чтобы применить куки
driver.get("https://web.vk.me/")

# Проверяем, авторизован ли пользователь
try:
    driver.find_element(By.CSS_SELECTOR, ".ComposerInput__input")
    print("Успешная загрузка куков. Пользователь авторизован.")
except:
    print("Необходима авторизация.")
    print_message_in_stars("Отблагодарить можно на boosty https://boosty.to/apicraft/donate\nВойдите в мессенджер, клик на получателе сообщений и нажмите Enter здесь для продолжения...")
    input("Нажмите Enter")
    save_cookies(driver, cookie_file)  # Сохраняем куки после ручного входа


# Ищем поле для отправки сообщений
message_input = driver.find_element(By.CSS_SELECTOR, ".ComposerInput__input.ComposerInput__input.ComposerInput__input")

def get_next_line(filename, state_file):
    try:
        # Читаем состояние: индекс текущего четырёхстишья и строки
        try:
            with open(state_file, 'r') as f:
                state = f.read().strip()
                if state:
                    quatrain_index, line_index = map(int, state.split(','))
                else:
                    quatrain_index, line_index = 0, 0
        except FileNotFoundError:
            quatrain_index, line_index = 0, 0

        # Читаем файл с текстом
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()

        # Разделяем на четырёхстишья
        quatrains = content.strip().split('\n\n')
        total_quatrains = len(quatrains)

        # Получаем текущий четырёхстишье и строки в нём
        current_quatrain = quatrains[quatrain_index].split('\n')
        total_lines_in_quatrain = len(current_quatrain)

        # Возвращаем текущую строку или разделитель
        if line_index < total_lines_in_quatrain:
            result = current_quatrain[line_index]
            line_index += 1
        else:
            result = '***'
            line_index = 0
            quatrain_index = (quatrain_index + 1) % total_quatrains  # Переход к следующему четырёхстишью

        # Обновляем состояние
        with open(state_file, 'w') as f:
            f.write(f"{quatrain_index},{line_index}")

        return result

    except Exception as e:
        return f"Ошибка: {e}"

# Функция генерации случайного текста
def generate_text_api():
  

    # API для шуток
    url = "https://v2.jokeapi.dev/joke/Any?lang=en&type=single"  # Анекдоты
    # url = "https://api.quotable.io/random"  # Цитаты
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if "joke" in data:  # Для JokeAPI
            return data["joke"]
        elif "content" in data:  # Для Quotable
            return data["content"]
    return "Ошибка получения текста."

# Отправляем сообщения
for _ in range(60):  # 60 отправок
    random_text = get_next_line('quatrains.txt', 'state.txt')
    message_input.send_keys(random_text)
    message_input.send_keys(Keys.ENTER)  # Отправка сообщения
    pause = random.uniform(10, 20)  # Случайная пауза
    print(f"Отправлено сообщение: {random_text}. Пауза: {pause:.2f} секунд.")
    time.sleep(pause)

print("Готово!")
driver.quit()



