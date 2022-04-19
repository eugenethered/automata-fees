from cache.holder.RedisCacheHolder import RedisCacheHolder


class TradeFeeProvider:

    def __init__(self, options):
        self.options = options
        self.cache = RedisCacheHolder()

    def get_account_trade_fee(self) -> float:
        pass

    def get_instrument_trade_fee(self, instrument) -> float:
        pass
