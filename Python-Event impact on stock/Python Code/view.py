
def display_recap(window_ctl, window_event, event_date, stat_ctl_window, stat_event_window, hypoth_test):
    """
    Function displaying the summary of the event analysis. 
    """
    print('\n')
    print('=================================================================')
    print('Corporation: ', window_ctl.get_company_name())
    print(' Ticker: ', window_ctl.ticker)
    print('\n')
    print('Event nature: Tesla Stock Split')
    print('   Event date: ', event_date)
    print('=================================================================')
    print('\n')
    print('===========')
    print('Summary')
    print('===========')
    print('\n')
    print('Control window')
    print('--------------')
    print('Average returns: ', window_ctl.calculate_average_return())
    print('Volatility: ', window_ctl.calculate_volatility())
    print('α: ', stat_ctl_window.ols_alpha())
    print('β: ', stat_ctl_window.ols_beta())
    print('\n')
    print('Event window')
    print('-------------')
    print('Average returns: ', window_event.calculate_average_return())
    print('Volatility: ', window_event.calculate_volatility())
    print('Abnormal returns: ', stat_event_window.abnorm_ret())
    print('Cumulative returns: ', stat_event_window.cum_abnorm_ret())
    print('\n')
    print('Hypothesis testing regarding the event window')
    print('Critical value right side: ', hypoth_test.critical_value())
    print('Critical value left side: ', hypoth_test.critical_value() * (-1))
    print('Test statitstic: ', hypoth_test.test_statistic())
    print('Test result: ', hypoth_test.test_hypothesis())

