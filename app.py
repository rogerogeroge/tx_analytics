from flask import Flask, render_template
import subprocess

app = Flask(__name__)

# Функция для выполнения скрипта
def run_script(script_path):
    try:
        result = subprocess.run(['python', script_path], capture_output=True, text=True, encoding='utf-8')
        return result.stdout  # Возвращаем вывод скрипта
    except Exception as e:
        return str(e)


# Главная страница
@app.route('/')
def home():
    return "Перейдите на /partner1 или /partner2, чтобы увидеть результаты работы скриптов."

# Страница для скрипта партнера 1
@app.route('/nomis')
def partner1():
    output = run_script('nomis.py')  # Укажи путь к первому скрипту
    return render_template('result.html', output=output)

# Страница для скрипта партнера 2
@app.route('/notcoin')
def partner2():
    output = run_script('notcoin.py')  # Укажи путь ко второму скрипту
    return render_template('result.html', output=output)

if __name__ == '__main__':
    app.run(debug=True)


