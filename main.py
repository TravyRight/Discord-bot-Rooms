import logging

from config import TOKEN, bot
from database.tables import create_tables


def main():
    try:
        logging.info(f"Bot start in progress...")

        create_tables()
        logging.debug(f"Database tables were created.")

        bot.load_extension("cogs.rooms.commands")
        bot.load_extension("cogs.rooms.events")
        logging.debug(f"Cogs were connected.")

    except Exception as e:
        logging.error(f"Failed to start bot. Error: {str(e)}")
        print(e)

    @bot.event
    async def on_ready():
        print("Bot is ready")

    bot.run(TOKEN)


if __name__ == "__main__":
    main()
