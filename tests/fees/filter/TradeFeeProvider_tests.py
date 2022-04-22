import unittest

from core.options.exception.MissingOptionError import MissingOptionError

from fees.trade.TradeFeeProvider import TradeFeeProvider


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


if __name__ == '__main__':
    unittest.main()
