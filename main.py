import logging

from config import TOKEN, bot
from database.tables import create_tables


def main():
    logging.info(f"Bot start in progress...")

    create_tables()
    logging.debug(f"Database tables were created.")

    bot.load_extension("cogs.rooms.commands")
    bot.load_extension("cogs.rooms.events")
    logging.debug(f"Cogs were connected.")

    # connect locale
    bot.i18n.load("Discord-bot-Rooms/locale/")
    logging.debug(f"locale were loaded.")

    @bot.event
    async def on_ready():
        print("Bot is ready")

    bot.run(TOKEN)


if __name__ == "__main__":
    main()
