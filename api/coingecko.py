import requests
import bot
import constants

class CoinGecko:
    """ Esta clase constituye una interfaz para interactuar con la API de ``coingecko.com``. 
    La clase define varios metodos para consultar los servicios de la web de CoinGecko los
    cuales retornan las respuestas en un formato fácil de manipular por el resto del programa."""

    _base_url = constants.COINGECKO_API_URL
    response = None

    def __init__(self, custom_base_url: str=None):
        if custom_base_url:
            self._base_url = custom_base_url

    def _request(self, url: str, parameters):
        try:
            self.response = requests.get(url, params=parameters)
            self.response.raise_for_status()
            return self.response.json()
        except Exception as e:
            raise e


    def get_simple_price(self, coin_id: str, vs_currency: str='usd', params: dict=None):
        """ Realiza una solicitud para obtener los datos de precio de una criptomoneda
            dada.

            Retorna:
                El precio de la criptomoneda """
        parameters = {
            'ids': coin_id,
            'vs_currencies': vs_currency
        }
        if params:
            parameters.update(params)
        return self._request(self._base_url + "/simple/price", parameters)
         