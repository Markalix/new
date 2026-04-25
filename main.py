import json

from flask import Flask, request, jsonify
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
sessionStorage = {}


@app.route('/', methods=['POST'])
def main1():
    logging.info(f'Request: {request.json!r}')

    data = json.loads(request.get_json())

    response = {
        'session': data['session'],
        'version': data['version'],
        'response': {'end_session': False}
    }

    handle_dialog(data, response)
    logging.info(f'Response: {response!r}')
    return jsonify(response)


@app.route('/', methods=['GET'])
def main2():
    return '''
        <!DOCTYPE html>
        <html>
        <body>

        <h1>My First Heading</h1>
        <p>My first paragraph.</p>

        </body>
        </html>
    '''


def handle_dialog(req, res):
    user_id = req['session']['user_id']
    if req['session']['new']:
        sessionStorage[user_id] = {'suggests': ["Не хочу.", "Не буду.", "Отстань!"]}
        res['response']['text'] = 'Привет! Купи слона!'
        res['response']['buttons'] = get_suggests(user_id)
        return
    if req['request']['original_utterance'].lower() in ['ладно', 'куплю', 'покупаю', 'хорошо', 'я покупаю', 'я куплю']:
        res['response']['text'] = 'Слона можно найти на Яндекс.Маркете!'
        res['response']['end_session'] = True
        return
    res['response']['text'] = f"Все говорят '{req['request']['original_utterance']}', а ты купи слона!"
    res['response']['buttons'] = get_suggests(user_id)


def get_suggests(user_id):
    session = sessionStorage[user_id]
    suggests = [{'title': suggest, 'hide': True} for suggest in session['suggests'][:2]]
    session['suggests'] = session['suggests'][1:]
    sessionStorage[user_id] = session

    if len(suggests) < 2:
        suggests.append({"title": "Ладно", "url": "https://market.yandex.ru/search?text=слон", "hide": True})
    return suggests


if __name__ == '__main__':
    app.run()
