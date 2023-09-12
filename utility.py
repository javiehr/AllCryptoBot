""" 
En este modulo se definen ciertas funciones y clases utilitarias 
para la implementacion de diversos algoritmos y tareas
"""

from api.coingecko import CoinGecko
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import exceptions.exceptions as exceptions
import bot
import datetime


class Crypto:
    """ Clase que representa una criptomoneda.

    Atributos:\n
    ``id`` - id de la criptomonedan\n
    ``name`` - nombre de la criptomoneda\n
    ``symbol`` - simbolo de la criptomoneda\n
    ``price`` - precio de la criptomoneda\n
    ``last_updated`` - Ultima vez que se actualizo la info en tiempo Unix"""

    def __init__(self, id: str, name: str, symbol: str, price: float = None, last_updated = None):
        self.id = id
        self.name = name
        self.symbol = symbol
        self.price = price
        self.last_updated = last_updated


def searchCrypto(data: list, symbol: str) -> dict:
    """ Esta funcion busca en la lista introducida en el parametro data la 
        crypto definida en el parametro symbol. La busqueda se implementa
        mediante un algoritmo de BUSQUEDA BINARIA.

        Retorna:
            Un diccionario con los atributos id, symbol y name de la crypto,
            en caso de no encontar el elemento, retorna un diccionario vacio """

    symbol.lower()
    left = 0
    right = len(data)

    while left <= right:
        middle = int((right + left) / 2)
        item = data[middle]['symbol']
        if item == symbol:
            return data[middle]
        else:
            if symbol > item:
                left = middle + 1
            else:
                right = middle - 1
    return {}


def linearSearchCrypto(coin_list: list, symbol: str) -> dict:
    """ Esta funcion busca en la lista introducida en el parametro ``data`` la 
        crypto definida en el parametro ``symbol``. La busqueda se implementa
        mediante un algoritmo de BUSQUEDA LINEAL.

        Retorna:
            Un diccionario con los atributos ``'id'``, ``'symbol'`` y ``'name'`` de la crypto,
            en caso de no encontar el elemento, retorna un diccionario vacio"""

    for item in coin_list:
        if item['symbol'] == symbol:
            return item
    return {}


def priceFormattedText(crypto: Crypto):
    if crypto.price >= 1:
        price_str = "{:,.2f}".format(crypto.price)
    else:
        price_str = "{:.5f}".format(crypto.price)
    last_time = datetime.datetime.fromtimestamp(crypto.last_updated).strftime("%d/%m/%Y - %H:%M:%S")

    return f"<b>{crypto.name} ({crypto.symbol.upper()})</b>\n<code>{price_str}</code>  USD\n\n<i>{last_time} GMT+0000</i>"


def getCrypto(symbol: str):
    """ Retorna un objeto ``Crypto`` con la informacion basica de la criptomoneda
    definida por el parametro ``symbol`` incluyendo el atributo ``price``, el cual contiene
    el precio de la criptomoneda y el atributo ``last_updated``"""
    if symbol == 'btc':
        crypto_info = {
            'id': 'bitcoin',
            'name': 'Bitcoin',
            'symbol': 'btc'
        }
    else:
        crypto_info = linearSearchCrypto(bot.coins, symbol)
    if crypto_info == {}:
        raise exceptions.NotFoundCrypto
    else:
        try:
            r = CoinGecko().get_simple_price(crypto_info['id'], params={'include_last_updated_at': 'true'})
            return Crypto(crypto_info['id'],
                          crypto_info['name'],
                          crypto_info['symbol'],
                          r[crypto_info['id']]['usd'],
                          r[crypto_info['id']]['last_updated_at'])
        except Exception as e:
            print(e)


def buildUpdateInKeyb(callback_data):
    key = [InlineKeyboardButton("Actualizar", callback_data=callback_data)]
    keyb_markup = InlineKeyboardMarkup([key])
    return keyb_markup