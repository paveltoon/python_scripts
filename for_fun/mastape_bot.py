import datetime
import telebot
from abc import ABC, abstractmethod


class BotTelegram(ABC):
    def __init__(self):
        self.bot = telebot.TeleBot("1351520640:AAFsCriT_CWY0CzfCZNqVYAHxKpT5QoO_74")
        self.chat_id = 198971955

    @abstractmethod
    def script_processing(self):
        pass

    def execute(self):
        start_time = datetime.datetime.now()
        self.send_message("Начал работать")
        self.script_processing()
        timer = datetime.datetime.now() - start_time
        self.send_message(f"Закончил работать за {timer}")

    def send_message(self, text):
        self.bot.send_message(self.chat_id, text)
