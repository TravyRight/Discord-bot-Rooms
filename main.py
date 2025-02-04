import logging

from config import TOKEN, bot


def main():
    try:
        logging.info(f"Bot start in progress...")
        # logging.debug(f"Database tables were created.")

    except Exception as e:
        logging.error(f"Failed to start bot. Error: {str(e)}")
        print(e)

    @bot.event()
    async def on_ready():
        print("Bot is ready")

    bot.run(TOKEN)


if __name__ == "__main__":
    main()
