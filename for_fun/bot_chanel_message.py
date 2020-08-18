import telebot

token = "1351520640:AAFsCriT_CWY0CzfCZNqVYAHxKpT5QoO_74"
bot = telebot.TeleBot(token, parse_mode=None)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")


bot.polling()
