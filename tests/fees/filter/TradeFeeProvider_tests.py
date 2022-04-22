import unittest

from cache.holder.RedisCacheHolder import RedisCacheHolder
from core.constants.not_available import NOT_AVAILABLE
from core.options.exception.MissingOptionError import MissingOptionError

from fees.trade.TradeFeeProvider import TradeFeeProvider
from fees.trade.exception.NoTradeFeeError import NoTradeFeeError


class TradeFeeProviderTestCase(unittest.TestCase):

    def test_should_raise_option_error_when_no_options_provided(self):
        with self.assertRaises(MissingOptionError) as mo:
            TradeFeeProvider(None, None)
        self.assertEqual('missing option please provide options ACCOUNT_TRADE_FEE_KEY and INSTRUMENT_TRADE_FEE_KEY', str(mo.exception))

    def test_should_raise_option_error_when_account_trade_fee_key_is_missing(self):
        with self.assertRaises(MissingOptionError) as mo:
            options = {}
            TradeFeeProvider(options, None)
        self.assertEqual('missing option please provide option ACCOUNT_TRADE_FEE_KEY', str(mo.exception))

    def test_should_raise_option_error_when_instrument_trade_fee_key_is_missing(self):
        with self.assertRaises(MissingOptionError) as mo:
            options = {
                'ACCOUNT_TRADE_FEE_KEY': 'market:account:trade:key'
            }
            TradeFeeProvider(options, None)
        self.assertEqual('missing option please provide option INSTRUMENT_TRADE_FEE_KEY', str(mo.exception))

    def test_should_return_none_when_trade_fee_is_not_available(self):
        options = {
            'ACCOUNT_TRADE_FEE_KEY': 'market:account:trade:key',
            'INSTRUMENT_TRADE_FEE_KEY': 'market:{instrument}:trade:key',
            'AUTO_CONNECT': False
        }

        # need this to bypass cache
        RedisCacheHolder.re_initialize()
        RedisCacheHolder(options)

        fee_provider = TradeFeeProvider(options, None)
        result = fee_provider.return_appropriate_value(NOT_AVAILABLE, 'Instrument')
        self.assertEqual(None, result, 'NOT_AVAILABLE should be None')

    def test_should_return_trade_fee(self):
        options = {
            'ACCOUNT_TRADE_FEE_KEY': 'market:account:trade:key',
            'INSTRUMENT_TRADE_FEE_KEY': 'market:{instrument}:trade:key',
            'AUTO_CONNECT': False
        }

        # need this to bypass cache
        RedisCacheHolder.re_initialize()
        RedisCacheHolder(options)

        fee_provider = TradeFeeProvider(options, None)
        result = fee_provider.return_appropriate_value(0.00, 'Instrument')
        self.assertEqual(0.0, result, 'Actual value of 0.0 should be returned')

    def test_should_raise_no_trade_fee_error_when_(self):
        with self.assertRaises(NoTradeFeeError) as ntf:
            options = {
                'ACCOUNT_TRADE_FEE_KEY': 'market:account:trade:key',
                'INSTRUMENT_TRADE_FEE_KEY': 'market:{instrument}:trade:key',
                'AUTO_CONNECT': False
            }

            # need this to bypass cache
            RedisCacheHolder.re_initialize()
            RedisCacheHolder(options)

            fee_provider = TradeFeeProvider(options, None)
            fee_provider.return_appropriate_value(None, 'Instrument')

        self.assertEqual('No trade fee for Instrument', str(ntf.exception), 'None value should raise and exception')


if __name__ == '__main__':
    unittest.main()
