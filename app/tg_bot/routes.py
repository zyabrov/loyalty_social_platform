from app.tg_bot import bp
from flask import request, current_app, url_for
from flask_login import login_required, current_user
import requests
from app.users.models import User


@bp.route('/update_webhook', methods=['GET'])
def update_webhook():
    delete_webhook()
    set_webhook()
    return get_webhook_info()

@bp.route('/set_webhook', methods=['GET'])
def set_webhook():
    api_url = f"https://api.telegram.org/bot{current_app.config['BOT_TOKEN']}/setWebhook"
    data = {"url": current_app.config['WEBHOOK_URL']}
    headers = {"content-type": "application/json"}
    r = requests.post(api_url, json=data, headers=headers)
    print('response: ', r.json())
    if r.status_code == 200:
        webhook_info = r.json()
        print('webhook_info: ', webhook_info)
    else:
        print('Error: ', r.status_code)
    return 'Webhook info: ' + str(webhook_info)

@bp.route('/get_webhook_info', methods=['GET'])
def get_webhook_info():
    r = requests.get('https://api.telegram.org/bot' + current_app.config['BOT_TOKEN'] + '/getWebhookInfo')
    if r.status_code == 200:
        webhook_info = r.json()
        print('webhook_info: ', webhook_info)
    return webhook_info

@bp.route('/delete_webhook', methods=['GET'])
def delete_webhook():
    r = requests.get('https://api.telegram.org/bot' + current_app.config['BOT_TOKEN'] + '/deleteWebhook')
    if r.status_code == 200:
        webhook_info = r.json()
        print('webhook_info: ', webhook_info)
    return webhook_info


class InlineKeyboard:
    def __init__(self):
        self.keyboard = []

    def add_button(self, text, url):
        button = {
            'text': text,
            'url': url
        }
        self.keyboard.append([button])

    def to_dict(self):
        return {'inline_keyboard': self.keyboard}

@bp.route('/', methods=['GET','POST'])
def receive_update():
    if request.method == 'POST':
        print('request: ', request.json)
        chat_id = request.json['message']['chat']['id']
        print('chat_id: ', chat_id)
        text = request.json['message']['text']
        print('text: ', text)
        if '/start' in text:
            id = int(text.split(' ')[1])
            if id:
                user = User.query.get(id)
                if user:
                    start(request.json['message'], user)
                else:
                    send_message(chat_id, 'User not found')
            else:
                send_message(chat_id, 'Invalid start command')
        else:
            send_message(chat_id, 'Invalid command')

        return {'ok': True}

def start(message, user: User):
    if user.query.filter_by(telegram_id=message['from']['id']).first() is None:
        keyboard = InlineKeyboard()
        user.update(telegram_id=message['from']['id'], telegram_username=message['from']['username'])
        keyboard.add_button('Go to Dashboard', f'{current_app.config['WEBAPP_URL']}/dashboard')
        reply_markup = keyboard.to_dict()
        print('reply_markup: ', reply_markup)
        return send_message(message['from']['id'], 'You have successfully activated notifications', reply_markup=reply_markup)
    else:
        return send_message(message['from']['id'], 'This telegram id is already in use')

def send_message(chat_id, text, reply_markup=None):
    method = 'sendMessage'
    token = current_app.config['BOT_TOKEN']
    url = f'https://api.telegram.org/bot{token}/{method}'
    data = {
        'chat_id': chat_id,
        'text': text
    }
    if reply_markup:
        data['reply_markup'] = reply_markup
    r = requests.post(url, json=data)
    print('response: ', r.text)
    return r

def send_notification(chat_id, text, buttons):
    keyboard=InlineKeyboard()
    for button in buttons:
        keyboard.add_button(text=button['text'], url=current_app.config["WEBAPP_URL"] + button['url'])
    reply_markup = keyboard.to_dict()
    return send_message(chat_id, text, reply_markup=reply_markup)