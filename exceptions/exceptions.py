""" En este modulo se encuentran las excepciones personalizadas que pueden 
ocurrir durante la ejecucion del bot"""

class NotFoundCrypto(Exception):
    """ No se ha encontrado la crypto que se busca en la lista de criptomonedas"""
    def __str__(self) -> str:
        return super().__str__("The crypto was not found")
    pass