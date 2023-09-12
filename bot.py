from telegram.ext import (ApplicationBuilder, CommandHandler,
                          MessageHandler, CallbackQueryHandler, filters)
import commands
import constants

# List of available coins in CoinGecko
coins = commands.loadCoinList()

def main():
    print("Starting bot...")
    app = ApplicationBuilder().token(constants.TOKEN).arbitrary_callback_data(True).build()

    app.add_handler(CommandHandler(constants.START_CMD, commands.startCmd))
    app.add_handler(CommandHandler(constants.HELP_CMD, commands.helpCmd))
    app.add_handler(CommandHandler(constants.BTC_PRICE_CMD, commands.getBTCCmd))
    app.add_handler(CommandHandler(constants.PRICE_CMD, commands.getCryptoCmd))
    app.add_handler(CommandHandler(constants.LIST_CMD, commands.listCmd))
    app.add_handler(MessageHandler(
        filters.TEXT & (~filters.COMMAND), commands.defaultMassage))
    app.add_handler(MessageHandler(filters.COMMAND, commands.unknownCmd))
    app.add_handler(CallbackQueryHandler(commands.updateButton))
    print("Configs done")

    app.run_polling(timeout=20)
    print("Bot finished")
