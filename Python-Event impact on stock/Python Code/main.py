"""
This Code was writen by:
Josselin Massé
Saad Handar
"""


def main():
    from fin_models import FinData
    from stats import StatSolution, HypoTest
    from view import display_recap

    # Param
    TICKER = 'TSLA'
    TICKER_SP = '^GSPC'
    EVENT_DATE = '2020/08/21'

    # Get Data from Yahoo Finance
    stock = FinData(TICKER, EVENT_DATE)
    sp500 = FinData(TICKER_SP, EVENT_DATE)

    # Design each window to work with
    wdw_ctl_stock = stock.window('control')
    wdw_ctl_sp500 = sp500.window('control')
    wdw_even_stock = stock.window('event')
    wdw_even_sp500 = sp500.window('event')

    # Get stats from window series
    stat_ctl_stock = StatSolution(wdw_ctl_sp500.ret(), wdw_ctl_stock.ret())
    stat_even_stock = StatSolution(wdw_even_sp500.ret(), wdw_even_stock.ret())
    hypoth_test = HypoTest(stat_even_stock, stat_ctl_stock)

    # Display recap in Python Console
    display_recap(wdw_ctl_stock, wdw_even_stock, EVENT_DATE,
                  stat_ctl_stock, stat_even_stock, hypoth_test)

    # Plot price
    wdw_ctl_stock.plot_price_volume('control window')
    stock.plot_price_volume('control and avent window')
    wdw_even_stock.plot_price_volume('event window')


if __name__ == '__main__':
    main()
