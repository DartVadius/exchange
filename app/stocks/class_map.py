from app.stocks import bitfinex, bittrex, localbitcoins, coinbase, indacoin, spectrocoin

classmap = {
    'bittrex': bittrex.Bittrex,
    'localbitcoins': localbitcoins.Localbitcoins,
    'coinbase': coinbase.Coinbase,
    'indacoin': indacoin.Indacoin,
    'spectrocoin': spectrocoin.Spectrocoin,
}
