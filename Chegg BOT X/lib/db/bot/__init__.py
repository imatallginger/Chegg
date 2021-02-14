from discord.ext.commands import Bot as BotBase
from apscheduler.schedulers.asyncio import AsyncIOScheduler


PREFIX = "+"
OWNER_IDS = [618038532665114624]

class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.ready = False
        self.guild = None
        self.scheduler = AsyncIOScheduler()
        

        super().__init__(command_prefix = PREFIX, owner_ids = OWNER_IDS)
    
    def run(self, version):
        self.VERSION = version

        with open("./lib/bot/token.0", "r", encoding="utf-8") as tf:
            self.TOKEN = tf.read()

        print("Running bot...")
        super().run(self.TOKEN, reconnect=True)

    async def on_connect(self):
        print("BOT has been CONNECTED!")

    async def on_disconnect(self):
        print("BOT has been DISCONNECTED!")

    async def on_ready(self):
        if not self.ready:
            self.ready = True
            self.guild = self.get_guild(746850984701198437)
            print("BOT is ready!")
        
        else:
            print("BOT reconnected!")

    async def on_message(self, message):
        pass

bot = Bot()