from app.stocks import bitfinex, bittrex, localbitcoins, coinbase

classmap = {
    'bittrex': bittrex.Bittrex,
    'localbitcoins': localbitcoins.Localbitcoins,
    'coinbase': coinbase.Coinbase
}
