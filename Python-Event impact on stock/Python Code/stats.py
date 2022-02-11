import statsmodels.api as sm
import numpy as np
from math import sqrt
import scipy.stats as ss


class StatSolution():
    """
    This class aims to provide all kinds of stat measure we need
    """
    _ALPHA_INDEX = 0
    _BETA_INDEX = 1
    
    def __init__(self, xseries, yseries):
        self.x = xseries
        self.y = yseries
        self.x_np = self.x.to_numpy()
        self.y_np = self.y.to_numpy()

    def ols(self):
        """
        It computes OLS model with X (xseries) and Y(yseries).
        """
        X_sm = sm.add_constant(self.x)
        model = sm.OLS(self.y, X_sm)
        results = model.fit()
        return results

    def ols_summary(self):
        """
        It returns the statistic summary of OLS model.
        Bonus
        """
        print(self.ols().summary())

    def ols_params(self)-> float:
        """
        It computes Alpha and Beta.
        Used to answer to the question 12 and 13.
        """
        return self.ols().params

    def ols_alpha(self)-> float:
        """
        It computes Alpha.
        Used to answer to the question 12 and 13.
        """
        return self.ols_params()[self._ALPHA_INDEX]

    def ols_beta(self)-> float:
        """
        It computes Beta.
        Used to answer to the question 12 and 13.
        """
        return self.ols_params()[self._BETA_INDEX]

    def expect_ret(self)-> np.array:
        """
        It computes the abnormal returns serie.
        Used to answer to the question 12 and 13.
        """
        x = self.x_np
        f = lambda t: t*self.ols_beta() + self.ols_alpha()
        vfunc = np.vectorize(f)
        return vfunc(x)

    def abnorm_ret(self)-> np.array:
        """
        It computes the abnormal returns serie.
        Used to answer to the question 13.
        """
        return np.subtract(self.y_np, self.expect_ret())

    def std_abnorm_ret(self)-> float:
        """
        It computes the standard deviation of the abnormal returns serie.
        Used to answer to the question 15.
        """
        return np.std(self.abnorm_ret())

    def cum_abnorm_ret(self)-> float:
        """
        This function aims to answer to the question 14.
        It computes the abnormal return for any kind of window
        """
        return np.sum(self.abnorm_ret())


class HypoTest():
    _SIGNIFICANCE_LVL = 0.05
    _SQRT_STAT_MODEL = 6
    
    def __init__(self, stat_even_stock, stat_ctl_stock):
        self.stat_even_stock = stat_even_stock
        self.stat_ctl_stock = stat_ctl_stock
    
    def critical_value(self):
        """
        This function aims to answer to the question 16.
        It computes the critical value depending on the significance level
        """
        val = 1 - self._SIGNIFICANCE_LVL/2
        return ss.norm.ppf(val)
    
    def test_statistic(self):
        """
        This function aims to answer to the question 15.
        It computes the test statistic
        """
        car_eve_wdw = self.stat_even_stock.cum_abnorm_ret()
        sqrt_six = sqrt(self._SQRT_STAT_MODEL)
        std_ctl_wdw = self.stat_ctl_stock.std_abnorm_ret()
        test_stat = car_eve_wdw/(sqrt_six * std_ctl_wdw)
        return test_stat
    
    def test_hypothesis(self):
        h0_rule = """Since the value is within the range of the critical values, We cannot reject H0:
                    the CAR of the event window is not different than 0"""
        h1_rule = """"Since the value is not within the range of the critical values, We do reject H0:
                    the CAR of the event window is different than 0"""
        test_stat_absoluted = abs(self.test_statistic())
        if test_stat_absoluted < self.critical_value():
            return h0_rule
        else:
            return h1_rule