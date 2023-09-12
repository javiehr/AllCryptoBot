from telegram import Update  # , InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import exceptions.exceptions as exceptions
import constants
import utility
import json
# import bot


def loadCoinList() -> list:
    with open("mcsorted.json") as f:
        coin_list = json.load(f)
        print("Coin list loaded...")
    return coin_list


async def startCmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(update)
    await update.message.reply_text(f"<b>Hola, {update.message.from_user.first_name}!!!</b>\nCon este bot puedes consultar \
el precio de cualquier criptomoneda. Escribe el comadno /help para más información o \
/list para ver una lista de los comandos disponibles.", parse_mode='HTML')


async def helpCmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("<b>Ayuda del bot</b>\nCon este bot puedes consultar el precio de cualqueir criptomoneda \
en el mercado. Para ello solo debes utilizar el comando /p seguido de las siglas de la cripto que deseas consultar\n\n\
<i>Ejemplo:\n    /p eth</i>\n\nTambién, con el comando /p_btc puedes consultar directamente el precio del Bitcoin", parse_mode='HTML')


async def defaultMassage(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
"No se reconoce como un comando \¡Consulta la lista de comandos en /list!", reply_to_message_id=update.message.message_id)


async def unknownCmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("No comas tanta pinga y pon un comando que sirva")


async def listCmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("<b>Lista de Comandos</b>\n/start - Mensaje de bienvenida\n/help - Ayuda del bot\n\
/p <i>«symbol»</i> - Consulta el precio de la ciptomoneda pasada como argumento\n/p_btc - Consulta el precio del Bitcoin", parse_mode='HTML')


async def getBTCCmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        btc_data = utility.getCrypto('btc')
        update_inkey_markup = utility.buildUpdateInKeyb(btc_data)
        await update.message.reply_text(utility.priceFormattedText(btc_data),
                                        parse_mode='HTML',
                                        reply_markup=update_inkey_markup)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)


async def getCryptoCmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        crypto_symbol = context.args[0].lower()
        crypto_data = utility.getCrypto(crypto_symbol)
        update_inkey_markup = utility.buildUpdateInKeyb(crypto_data)
        await update.message.reply_text(utility.priceFormattedText(crypto_data),
                                        parse_mode='HTML',
                                        reply_markup=update_inkey_markup)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
    except exceptions.NotFoundCrypto:
        await update.message.reply_text("La ciptomoneda que solicitaste no se ha encontrado")
    except IndexError:
        await update.message.reply_text(f"¡Debes proporcionar una criptomoneda para buscar! Intenta con /{constants.PRICE_CMD} bnb")


async def updateButton(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        query = update.callback_query
        await query.answer()
        crypto_data = query.data
        crypto_data = utility.getCrypto(crypto_data.symbol)
        await query.message.edit_text(utility.priceFormattedText(crypto_data),
                                      parse_mode="HTML",
                                      reply_markup=utility.buildUpdateInKeyb(crypto_data))
    except Exception as e:
        print(e)

""" async def inlineKeyboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keys = [
        [
            InlineKeyboardButton("Opcion 1", callback_data="1"),
            InlineKeyboardButton("Opcion 2", callback_data="2", )
        ],
        [InlineKeyboardButton("Opcion 3", callback_data="3")],
        [InlineKeyboardButton("Opcion 4", callback_data="4")]
    ]
    keys_markup = InlineKeyboardMarkup(keys)
    print(update.effective_user.language_code)
    if update.effective_user.language_code == "es":
        STRING = "Elige una opcion"
    else:
        STRING = "Chose an option"

    await update.message.reply_text(STRING, reply_markup=keys_markup)


async def keyboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = ReplyKeyboardMarkup(
        [
            [KeyboardButton("Keyboard Opcion 1")],
            [KeyboardButton("Keyboard Opcion 2")]
        ], one_time_keyboard=True, resize_keyboard=True
    )
    await update.message.reply_text("Seleccione una opcion del teclado", reply_markup=keyboard)


async def buttonsHandler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text(f"Has seleccionado la opcion {query.data}")
 """
