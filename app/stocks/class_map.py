from app.stocks import bitfinex, bittrex, localbitcoins

classmap = {
    'bittrex': bittrex.Bittrex,
    'localbitcoins': localbitcoins.Localbitcoins
}
