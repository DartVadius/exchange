from app.stocks import bittrex, localbitcoins, coinbase, indacoin, spectrocoin, shapeshift, changelly

classmap = {
    'bittrex': bittrex.Bittrex,
    'localbitcoins': localbitcoins.Localbitcoins,
    'coinbase': coinbase.Coinbase,
    'indacoin': indacoin.Indacoin,
    'spectrocoin': spectrocoin.Spectrocoin,
    'shapeshift': shapeshift.Shapeshift,
    'changelly': changelly.Changelly
}
