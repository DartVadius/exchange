from app.stocks import bitfinex, bittrex, localbitcoins, coinbase, indacoin

classmap = {
    'bittrex': bittrex.Bittrex,
    'localbitcoins': localbitcoins.Localbitcoins,
    'coinbase': coinbase.Coinbase,
    'indacoin': indacoin.Indacoin
}
