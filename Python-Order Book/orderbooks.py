from operator import itemgetter
import pandas as pd
import xlwings as xw

class Orderbook:
    def __init__(self):
        self.columns = ['id','date','sell_buy','price','quantity']
        self.orderbook = []
        self.id = 0
        self.date = 1
        self.is_buy = 2
        self.price = 3
        self.quantity = 4
        
    def get_list_all_qty(self):
        l=[]
        for order in self.orderbook:
            l.append(order[self.quantity])
        return l
    
    def get_sum_all_qty(self):
        return sum(self.get_list_all_qty())
        
    def sort_buy(self):
        self.orderbook = sorted(self.orderbook, key = itemgetter(3), reverse = True)
        
    def sort_sell(self):
        self.orderbook = sorted(self.orderbook, key= itemgetter(3))
        
    def insert_order(self, order):
        list_order = order.my_order
        self.orderbook.append(list_order)
        if order.is_buy:
            self.sort_buy()
        else:
            self.sort_sell()
    
    def best_order(self):
        return self.orderbook[0]
    
    def best_date(self):
        return self.best_order()[1]
    
    def best_is_buy(self):
        return self.best_order()[2]

    def best_price(self):
        return self.best_order()[3]
    
    def best_quantity(self):
        return self.best_order()[4]
    
    def convert_orderbook_as_df(self):
        df = pd.DataFrame(self.orderbook, columns= self.columns)
        return df

    def display_df_topten(self):
        df = self.convert_orderbook_as_df()
        return df.head(10)
    

class OrderbookBuy(Orderbook):
    def __init__(self):
        Orderbook.__init__(self)
        

class OrderbookSell(Orderbook):
    def __init__(self):
        Orderbook.__init__(self)
    

class ExecutedOrders:
    def __init__(self):
        self.book = []
        
    def get_transaction_list(self):
        transact_list = {}
        j=1
        k=1
        for i in self.book:
            if j%2 == 1:
                transact_list[k] = i
                k+=1
            j+=1
        return transact_list
    
    def write_transactions(self, text_file):
        transactions = self.get_transaction_list()
        with open(text_file, 'a+') as f:
            f.truncate(0)
            for k in transactions.keys():
                order = transactions[k]
                id_ = k
                price = order[3]
                qty = order[4]
                sentence = 'Transaction :' + str(id_) + ', has been executed for a quantity of '+ str(qty)+' with a price of ' + str(price)
                f.write('\n')
                f.write(sentence)
    
    def transaction_list_as_df(self):
        """
        limit order = ['id','datetime','is_buy','price','qty']
        """
        dict_transaction = self.get_transaction_list()
        df = pd.DataFrame.from_dict(dict_transaction, orient = 'index')
        df.columns = ['id','datetime','is_buy','price','qty']
        df = df.drop(columns=['id', 'is_buy'])
        return df
    
    def write_transactions_in_excel(self, excel_file, sheet):
        START_CELL = "A1"
        book = xw.Book(excel_file)
        sheet = book.sheets[sheet]
        df_transac = self.transaction_list_as_df()
        sheet.clear_contents()
        sheet[START_CELL].options(pd.DataFrame, header=1, index =True, expand='table').value = df_transac

class Order:
    def __init__(self,order: list):
        if len(order) == 4:
            self.my_order = order
            self.id = order[0]
            self.date = order[1]
            self.is_buy = order[2]
            self.quantity = order[3]
            self.price = None
            self.is_market = True
            if self.is_buy:
                self.buy_sell = 'buy'
                self.counterparty = 'sell'

            else:
                self.buy_sell = 'sell'
                self.counterparty = 'buy'
            
        else:
            self.my_order = order
            self.id = order[0]
            self.date = order[1]
            self.is_buy = order[2]
            self.price = order[3]
            self.quantity = order[4]
            self.is_market = False
            if self.is_buy:
                self.buy_sell = 'buy'
                self.counterparty = 'sell'

            else:
                self.buy_sell = 'sell'
                self.counterparty = 'buy'

            
            
            
        
