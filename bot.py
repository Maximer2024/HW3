import telebot
from extensions import APIException, Converter
import config

bot = telebot.TeleBot(config.TOKEN)



@bot.message_handler(commands=['start', 'help'])
def start_help(message: telebot.types.Message):
    text = "Чтобы узнать цену валюты, введите команду в формате:\n<имя валюты> <в какую валюту перевести> <количество>\nПример: доллар рубль 100"
    bot.reply_to(message, text)



@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = "Доступные валюты: доллар, евро, рубль"
    bot.reply_to(message, text)



@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split()

        if len(values) != 3:
            raise APIException(
                "Неправильное количество параметров. Формат: <имя валюты> <в какую валюту перевести> <количество>.")

        base, quote, amount = values
        total_quote = Converter.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f"Ошибка пользователя: {e}")
    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать запрос.\n{e}")
    else:
        text = f"Цена {amount} {base} в {quote} — {total_quote}"
        bot.send_message(message.chat.id, text)


bot.polling()
