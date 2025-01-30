
# MCMODLOCALIZERU

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

### JSON Localization App — это простое веб-приложение, которое переводит JSON-файлы локализации модов для игры Minecraft с английского на русский язык с использованием Google Translate API. Приложение предназначено для помощи разработчикам модов Minecraft и других пользователей, которым нужно локализовать свои JSON-файлы.
#### Данный инструмент не ломает ключи, но рекомендую делать резервные копии файлов локализации.

## Возможности

- Загрузка JSON-файла для локализации.
- Автоматический перевод всех строковых значений с английского на русский.
- Сохранение переведенного JSON-файла как `ru_ru.json`.
- Простой и интуитивно понятный интерфейс.
- Нет необходимости устанавливать Python или какие-либо зависимости вручную; приложение может распространяться как исполняемый файл.

## Требования

Для запуска этого проекта локально вам нужно установить следующее:

- [Python 3.x](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/installation/)

#### После компеляции в exe библиотеки не понадобится для его работы.

## Шаги по созданию и настройке проекта

### Шаг 1: Создание директории проекта

1. **Создайте новую папку на диске (С)** для вашего проекта, например, `json_localization_app`:
   ```sh
   mkdir C:\json_localization_app
   cd C:\json_localization_app
   ```

2. **Создайте необходимые файлы** внутри этой папки:
   - `app.py`
   - Папку `templates` с файлом `index.html`

### Шаг 2: Создание файла `app.py`

Создайте файл `app.py` в корне вашей директории (`C:\json_localization_app`) со следующим содержимым:

```python
import sys
import os
from flask import Flask, render_template, request, jsonify
import json
from deep_translator import GoogleTranslator

# Добавляем путь к шаблонам в системный путь
if getattr(sys, 'frozen', False):
    # Если это исполняемый файл, получаем путь к исполняемому файлу
    bundle_dir = sys._MEIPASS
else:
    # Если это обычный скрипт, используем текущую директорию
    bundle_dir = os.path.dirname(os.path.abspath(__file__))

# Обновленная функция для получения пути к шаблонам
def get_templates_path():
    return os.path.join(bundle_dir, 'templates')

# Обновляем путь к шаблонам в Flask
app = Flask(__name__, template_folder=get_templates_path())

translator = GoogleTranslator(source='en', target='ru')

@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        return f"Error loading template: {str(e)}"

@app.route('/translate', methods=['POST'])
def translate():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    input_file = request.files['file']
    
    # Проверка расширения файла
    if not input_file.filename.lower().endswith('.json'):
        return jsonify({'error': 'Invalid file type. Please upload a JSON file.'}), 400
    
    try:
        data = json.load(input_file)
        translated_data = {}
        for key, value in data.items():
            if isinstance(value, str):
                translated_value = translator.translate(value)
                translated_data[key] = translated_value
            else:
                translated_data[key] = value
        
        output_filename = 'ru_ru.json'
        with open(output_filename, 'w', encoding='utf-8') as output_file:
            json.dump(translated_data, output_file, ensure_ascii=False, indent=4)

        return jsonify({'success': True, 'filename': output_filename})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Открываем страницу в браузере после запуска сервера
    url = 'http://127.0.0.1:5000/'
    webbrowser.open(url)
    app.run(debug=False, host='0.0.0.0')
```

### Шаг 3: Создание файла `index.html`

Создайте папку `templates` внутри `C:\json_localization_app` и добавьте туда файл `index.html` со следующим содержимым:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JSON Localization</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background-color: #f4f4f4;
        }
        .container {
            width: 600px;
            background-color: white;
            padding: 20px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        h1 {
            text-align: center;
        }
        .form-group {
            margin-bottom: 15px;
        }
        .form-group label {
            display: block;
            margin-bottom: 5px;
        }
        .form-group input[type="file"] {
            width: 100%;
        }
        .form-group button {
            width: 100%;
            padding: 10px;
            background-color: #007bff;
            color: white;
            border: none;
            cursor: pointer;
        }
        .form-group button:hover {
            background-color: #0056b3;
        }
        .status {
            margin-top: 20px;
            padding: 10px;
            border-radius: 5px;
            text-align: center;
        }
        .status.success {
            background-color: #d4edda;
            color: #155724;
        }
        .status.error {
            background-color: #f8d7da;
            color: #721c24;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>JSON Localization</h1>
        <form id="uploadForm">
            <div class="form-group">
                <label for="file">Select JSON File:</label>
                <input type="file" id="file" name="file" accept=".json" required>
            </div>
            <div class="form-group">
                <button type="submit">Start</button>
            </div>
            <div class="status" id="status"></div>
        </form>
    </div>

    <script>
        document.getElementById('uploadForm').addEventListener('submit', function(event) {
            event.preventDefault();
            const statusDiv = document.getElementById('status');
            statusDiv.innerHTML = '';

            const fileInput = document.getElementById('file');
            const file = fileInput.files[0];

            console.log("Selected file:", file);

            // Проверка расширения файла на стороне клиента
            if (!file || !file.name.toLowerCase().endsWith('.json')) {
                statusDiv.className = 'status error';
                statusDiv.textContent = 'Ошибка: Выберите файл с расширением .json';
                return;
            }

            const formData = new FormData();
            formData.append('file', file);

            fetch('/translate', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                console.log("Server response:", data);
                if (data.success) {
                    statusDiv.className = 'status success';
                    statusDiv.textContent = `Файл успешно локализован и сохранен как ${data.filename}`;
                } else {
                    statusDiv.className = 'status error';
                    statusDiv.textContent = `Ошибка: ${data.error}`;
                }
            })
            .catch(error => {
                console.error("Fetch error:", error);
                statusDiv.className = 'status error';
                statusDiv.textContent = `Ошибка: ${error.message}`;
            });
        });
    </script>
</body>
</html>
```

### Шаг 4: Установка Python и pip

Если у вас еще не установлен Python и pip, выполните следующие шаги:

1. **Скачайте и установите Python** с официального сайта [python.org](https://www.python.org/downloads/).
2. **Добавьте Python в переменную среды PATH** во время установки.

Проверьте установку Python и pip:

```sh
python --version
pip --version
```

### Шаг 5: Установка зависимостей

1. **Откройте командную строку (Cmd)** или терминал и перейдите в директорию проекта:

   ```sh
   cd C:\json_localization_app
   ```

2. **Создайте и активируйте виртуальное окружение:**

   Виртуальное окружение позволяет изолировать зависимости вашего проекта от глобальных зависимостей на вашем компьютере.

   Создание виртуального окружения:
   ```sh
   python -m venv venv
   ```

   Активация виртуального окружения:
   ```sh
   venv\Scripts\activate  # На Windows
   source venv/bin/activate  # На macOS/Linux
   ```

3. **Установите необходимые зависимости:**

   После активации виртуального окружения выполните следующую команду для установки библиотек Flask, deep-translator и PyInstaller:

   ```sh
   pip install flask deep-translator pyinstaller
   ```

### Шаг 6: Запуск приложения

Теперь можно запустить ваше приложение Flask:

```sh
python app.py
```

Приложение запустит локальный сервер на `http://127.0.0.1:5000/` и автоматически откроет его в вашем браузере по умолчанию.

### Шаг 7: Использование приложения

1. **Откройте ваш веб-браузер** и перейдите по адресу `http://127.0.0.1:5000/`.

2. **Выберите JSON-файл для локализации:**
   
   - Нажмите кнопку "Select JSON File" (Выбрать JSON файл).
   - Выберите JSON-файл, который вы хотите локализовать.

3. **Нажмите кнопку "Start" (Старт):**
   
   - Нажмите кнопку "Start" для начала процесса перевода.
   - Приложение автоматически переведет все строковые значения в JSON-файле и сохранит результат как `ru_ru.json` в той же директории.

4. **Проверьте результат:**
   
   - Сообщение состояния укажет, был ли перевод успешен или возникли какие-либо ошибки.
   - Если всё прошло успешно, вы найдете файл `ru_ru.json` в папке проекта.

### Шаг 8: Упаковка приложения в исполняемый файл

Для упаковки приложения в исполняемый файл (.exe) для распространения выполните следующие шаги:

1. **Убедитесь, что вы находитесь в директории проекта** и виртуальное окружение активировано:

   ```sh
   cd C:\json_localization_app  # На Windows
   cd /path/to/json_localization_app  # На macOS/Linux
   venv\Scripts\activate  # На Windows
   source venv/bin/activate  # На macOS/Linux
   ```

2. **Выполните команду PyInstaller:**

   Команда для упаковки приложения в одноэкранный исполняемый файл:

   ```sh
   pyinstaller --onefile --add-data "templates;templates" app.py
   ```

   Для macOS/Linux используйте двоеточие вместо точки в параметре `--add-data`:

   ```sh
   pyinstaller --onefile --add-data "templates:templates" app.py  # На macOS/Linux
   ```

3. **Найдите собранный исполняемый файл:**

   Собранный исполняемый файл будет находиться в папке `dist`. Вы можете распространять этот файл пользователям, которые не нуждаются в установке Python или зависимостей.

### Полный пример структуры проекта

```
json_localization_app/
├── app.py
├── templates/
│   └── index.html
├── venv/
├── dist/
├── build/
├── .gitignore
├── LICENSE
└── README.md
```

### Пример использования команд

#### Клонирование репозитория:

```sh
git clone https://github.com/your_username/json_localization_app.git
cd json_localization_app
```

#### Создание и активация виртуального окружения:

```sh
python -m venv venv
venv\Scripts\activate  # На Windows
source venv/bin/activate  # На macOS/Linux
```

#### Установка зависимостей:

```sh
pip install flask deep-translator pyinstaller
```

#### Запуск приложения:

```sh
python app.py
```

#### Упаковка приложения в исполняемый файл:

```sh
pyinstaller --onefile --add-data "templates;templates" app.py  # На Windows
pyinstaller --onefile --add-data "templates:templates" app.py  # На macOS/Linux
```

### Решение проблем

- Если страница остается пустой после запуска приложения, проверьте консольные логи в вашем веб-браузере (F12) на наличие ошибок JavaScript.
- Убедитесь, что файл `index.html` существует в папке `templates` и имеет правильное имя.

## Внесение изменений в проект

Вклады приветствуются! Пожалуйста, форкните репозиторий и создайте pull request с вашими изменениями. Для крупных изменений, пожалуйста, откройте issue сначала, чтобы обсудить, что вы хотите изменить.

### Лицензия

Этот проект распространяется под лицензией MIT — см. файл [LICENSE](LICENSE) для деталей.

### Контакты

Если у вас есть вопросы или требуется дополнительная помощь, свяжитесь со мной по электронной почте aleksandr.pugachev.94@mail.ru или откройте issue в этом репозитории.

---

## Спасибо за использование MCModLocalizeRU!

### Благодарю Qwen2.5-Max от Alibaba за помощь в создании этого инструмента который облегчил мне работу по русифицированию модов для Minecraft.
