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
    
    # Check file extension
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
