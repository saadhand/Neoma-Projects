import pandas as pd
import matplotlib.pyplot as plt
from pandas.tseries.offsets import BDay
from datetime import datetime
import pandas_datareader as pdr


class FinData():
    """
    This class is a parent class which enables us to create a kind of template structure.
    We use this structure for the entire initial dataset.
    """

    _DATE_FORMAT = '%Y/%m/%d'
    _WINDOW_CTL = 'control'
    _WINDOW_EV = 'event'
    _ADJ_CLOSE = 'Adj Close'
    _VOLUME = 'Volume'
    _RETURN = 'return'
    _SHORT_NAME = 'shortName'
    _NAME_CORP = 'Tesla, Inc.'

    def __init__(self, ticker, ev_date):
        self.data = pd.DataFrame()
        self.ticker = ticker
        self.event_date = ev_date
        self.get_data()

    def window(self, window) -> pd.DataFrame:
        """
        This function aims to design a window (control or event) to work with
        """
        dates = self.get_dates(window)
        start, end = dates[0], dates[1]
        win = self.data[(self.data.index >= start) & (self.data.index <= end)]
        win = win.dropna(axis=0)
        return Window(self.ticker, self.event_date, win)

    def adj_close(self):
        """
        It returns the Adj Close series
        """
        return self.data[self._ADJ_CLOSE]

    def volume(self):
        """
        It returns the Volume series
        """
        return self.data[self._VOLUME]

    def ret(self):
        """
        It returns the Return series
        """
        return self.data[self._RETURN]

    def get_data(self):
        """
        It retrieves the data from yahoo finance thanks to pandas datareader
        """
        liste = self.get_dates()
        self.data = pdr.get_data_yahoo(
            self.ticker, start=liste[0], end=liste[1])
        self.data = self.calculate_pct_change(self.data)

    def get_company_name(self):
        return self._NAME_CORP

    def get_dates(self, wdw=None):
        """
        It returns the right timestamp according to the type of window we are working with
        """
        liste = []
        event_date = datetime.strptime(self.event_date, self._DATE_FORMAT)
        if wdw == self._WINDOW_CTL:
            start_date = event_date - BDay(120)
            end_date = event_date - BDay(6)
            end_date = end_date.strftime(self._DATE_FORMAT)
            start_date = start_date.strftime(self._DATE_FORMAT)
            liste.append(start_date)
            liste.append(end_date)

        elif wdw == self._WINDOW_EV:
            start_date = event_date
            end_date = event_date + BDay(5)
            end_date = end_date.strftime(self._DATE_FORMAT)
            start_date = start_date.strftime(self._DATE_FORMAT)
            liste.append(start_date)
            liste.append(end_date)

        else:
            start_date = event_date - BDay(120)
            end_date = event_date + BDay(5)
            end_date = end_date.strftime(self._DATE_FORMAT)
            start_date = start_date.strftime(self._DATE_FORMAT)
            liste.append(start_date)
            liste.append(end_date)
        return liste

    def plot_price_volume(self, window):
        """
        It plots graph with price and volume index depending on the window given in entry
        """
        fig, ax = plt.subplots()
        ax.plot(self.adj_close(), color="red")
        ax.set_xlabel("year", fontsize=14)
        ax.set_ylabel("Price in $", color="red", fontsize=14)
        ax2 = ax.twinx()
        ax2.plot(self.volume(), color="blue")
        ax2.set_ylabel("Volume in 100m", color="blue", fontsize=14)
        plt.title(str(self.ticker) + ' on ' + window)
        plt.axvline(datetime(2020, 8, 21), label='Tesla Stock Split')
        plt.legend()
        plt.show()

    def calculate_average_return(self):
        """
        It calculates the average return
        """
        return_mean = self.data[self._RETURN].mean()*100
        return return_mean

    def calculate_volatility(self):
        """
        It calculates the volatility
        """
        volatility = self.data[self._RETURN].std()*100
        return volatility

    def calculate_pct_change(self, data):
        """
        This function creates a column in Findata object by calculating the
        percentage change (return) between adj close price
        """
        data[self._RETURN] = data[self._ADJ_CLOSE].pct_change()
        return data


class Window(FinData):
    """
    This class inherits from Findata is a parent class which enables us to create a kind of template structure.
    We use this structure for control window and event window
    """

    def __init__(self, ticker, ev_date, df):
        FinData.__init__(self, ticker, ev_date)
        self.data = df
