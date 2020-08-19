from for_fun.mastape_bot import BotTelegram


class payScr(BotTelegram):
    def script_processing(self):
        self.send_message("Hello")


bot = payScr()
bot.execute()
