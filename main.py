import telebot
from config import keys, TOKEN
from exctension import Convert, APIException

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    text = f'Привет, {message.from_user.username}!\n\nДля подсчета валюты введите в следующем формате:  <имя валюты, цену которой он хочет узнать> <имя валюты, в которой надо узнать цену первой валюты> <количество первой валюты>.\n\nПример: USD RUB 1\n\nДля того чтобы узнать доступные валюты введите /values'
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['values'])
def values(message):
    text = 'Доступные валюты:'
    for i, key in enumerate(keys):
        text += f'\n{i+1}. {key}'
    bot.send_message(message.chat.id, text)

@bot.message_handler(content_types=['text'])
def get_price(message):
    try:
        values= message.text.split(' ')
        if len(values) != 3:
            raise APIException('Некорректный ввод данных')
        base, quote, amount = values
        total_base = Convert.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка : {e}')
    else:
        text = f'{amount} {base} = {total_base:.1f} {quote}'
        bot.send_message(message.chat.id, text)

bot.polling()