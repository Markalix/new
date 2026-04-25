from flask import Flask, request, jsonify
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Хранилище сессий
sessionStorage = {}


@app.route('/', methods=['POST'])
def main():
    # Flask сам преобразует JSON в словарь, ничего лишнего вызывать не нужно
    data = request.json

    response = {
        'session': data['session'],
        'version': data['version'],
        'response': {'end_session': False}
    }

    handle_dialog(data, response)
    return jsonify(response)


@app.route('/', methods=['GET'])
def index():
    return 'Сервер навыка Алисы запущен!'


def handle_dialog(req, res):
    # Используем .get(), чтобы код не падал, если ключа нет
    user_id = req['session']['user_id']

    if req['session']['new']:
        sessionStorage[user_id] = {
            'suggests': ["Не хочу.", "Не буду.", "Отстань!"]
        }
        res['response']['text'] = 'Привет! Купи слона!'
        res['response']['buttons'] = get_suggests(user_id)
        return

    # Обработка ответа пользователя
    utterance = req['request']['original_utterance'].lower()

    if utterance in ['ладно', 'куплю', 'покупаю', 'хорошо', 'я покупаю', 'я куплю']:
        res['response']['text'] = 'Слона можно найти на Яндекс.Маркете!'
        res['response']['end_session'] = True
        return

    # Обычный ответ
    res['response']['text'] = f"Все говорят '{req['request']['original_utterance']}', а ты купи слона!"
    res['response']['buttons'] = get_suggests(user_id)


def get_suggests(user_id):
    session = sessionStorage.get(user_id, {'suggests': ["Не хочу.", "Не буду.", "Отстань!"]})

    # Формируем кнопки
    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in session['suggests'][:2]
    ]

    # Обновляем список подсказок
    if len(session['suggests']) > 1:
        session['suggests'] = session['suggests'][1:]

    sessionStorage[user_id] = session

    if len(suggests) < 2:
        suggests.append({
            "title": "Ладно",
            "url": "https://market.yandex.ru/search?text=слон",
            "hide": True
        })

    return suggests


if __name__ == '__main__':
    app.run()
