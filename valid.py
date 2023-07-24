
class Valid():
    def __init__(self, bot, sql, masterAdmin):
        self.bot = bot
        self.sql = sql
        self.id = masterAdmin


    def official(self, func):
        def wraper(message):
            id_tg = message.from_user.id
            Id = self.sql.getAdmin(id_tg)
            if Id == None and id_tg!=self.id:
                self.bot.send_message(message.chat.id, "У тебя нет прав. Ты феминистка!") 
            else:
                return func(message)
        return wraper
