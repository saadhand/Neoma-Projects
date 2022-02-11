import numpy as np  
import pandas as pd
from datetime import datetime
from datetime import timedelta
import xlwings as xw
from typing import List
from orderbooks import Orderbook, OrderbookBuy, OrderbookSell, ExecutedOrders, Order


def generate_orders(nbr:int, mean:int, std:int)-> List[list]:
    """
    Generate random orders:
        market order = ['id','datetime','is_buy','qty']
        limit order = ['id','datetime','is_buy','price','qty']

    """
    LIMIT_ORDER = 1
    MARKET_ORDER = 0
    BINARY = 2
    LOW_QTY = 100
    HIGH_QTY = 100000
    DATETIME_FORMAT_LIMIT = "%d/%m/%Y %H:%M:%S"
    DATETIME_FORMAT_MARKET = "%d/%m/%Y %H:%M:00"
    
    orders_list=[]
    sub_order_history=[]
    for i in range(nbr):
        sub_order_history=[]
        date=datetime.now()
        date+=timedelta(minutes=i)
        order_type=np.random.randint(BINARY)
        if order_type==LIMIT_ORDER:
            sub_order_history.append(i+1) 
            sub_order_history.append(date.strftime(DATETIME_FORMAT_LIMIT))
            sub_order_history.append(np.random.randint(BINARY))
            sub_order_history.append(round(np.random.normal(mean,std),2)) 
            sub_order_history.append(np.random.randint(LOW_QTY,HIGH_QTY)) 
            orders_list.append(sub_order_history)
        elif order_type==MARKET_ORDER:
            sub_order_history.append(i+1) 
            sub_order_history.append(date.strftime(DATETIME_FORMAT_MARKET)) 
            sub_order_history.append(np.random.randint(BINARY)) 
            sub_order_history.append(np.random.randint(LOW_QTY,HIGH_QTY)) 
            orders_list.append(sub_order_history)
    return orders_list

def process_orders(order:Order, orderbook_buy:OrderbookBuy, orderbook_sell:OrderbookSell,
                   executed_orders:ExecutedOrders , list_spread: dict)-> None:
    """
	Itermezzo function which specified which function to use depending on the type order (limit or market)
    Sort orderbook before processing orders
	"""
    orderbook_buy.sort_buy()
    orderbook_sell.sort_sell()
    list_spread[order.date] = get_spread(orderbook_buy, orderbook_sell)
    
    if order.is_market:
        process_market_orders(order, orderbook_buy, orderbook_sell, executed_orders)
    else:
        process_limit_orders(order, orderbook_buy, orderbook_sell, executed_orders)


def process_market_orders(order:Order, orderbook_buy:OrderbookBuy, 
                          orderbook_sell:OrderbookSell, executed_orders:ExecutedOrders)->None:
    """
	A market order can be executed if there is some quantity in the counterparty orderbook or cancelled if there is no
    counterparty.
	"""
    orderbook_counterparty = get_orderbook_counterparty(order, orderbook_buy, orderbook_sell)
    if orderbook_counterparty.orderbook:
        execute_best(order, orderbook_buy, orderbook_sell, executed_orders)


def process_limit_orders(order:Order, orderbook_buy:OrderbookBuy, 
                         orderbook_sell:OrderbookSell, executed_orders:ExecutedOrders)->None:
    """
    If counterparty orderbook is not empty and order price is greater than the best sell, the order is treated as a marketorder
    one.
    Else, the order is immediately stored in the orderbook.
    """
    orderbook_counterparty = get_orderbook_counterparty(order, orderbook_buy, orderbook_sell)
    orderbook = get_orderbook(order, orderbook_buy, orderbook_sell)
    if orderbook_counterparty.orderbook:
        best_price_counterparty = get_price_bestorder_counterparty(order, orderbook_buy, orderbook_sell)
        if order.is_buy:
            if order.price >= best_price_counterparty:
                process_market_orders(order, orderbook_buy, orderbook_sell, executed_orders)
            else:
                orderbook.insert_order(order)
        else:
            if order.price <= best_price_counterparty:
                process_market_orders(order, orderbook_buy, orderbook_sell, executed_orders)
            else:
                orderbook.insert_order(order)
    else:
        orderbook.insert_order(order)


def get_orderbook_counterparty(order:Order, orderbook_buy:OrderbookBuy, orderbook_sell:OrderbookSell)->Orderbook:
    """
    Depending on the order (buy or sell order), it returns the orderbook of the counterparty.
    If the order is a buy order, it returns the sell orderbook object
    """
    if order.counterparty == 'buy':
        return orderbook_buy
    else:
        return orderbook_sell

def get_orderbook(order:Order, orderbook_buy:OrderbookBuy, orderbook_sell:OrderbookSell)->Orderbook:
    """
    Depending on the order (buy or sell order), it returns the orderbook of the order.
    If the order is a buy order, it returns the buy orderbook object
    """
    if order.counterparty == 'buy':
        return orderbook_sell
    else:
        return orderbook_buy
        
def get_sum_quantity_counterparty(order:Order, orderbook_buy:OrderbookBuy, orderbook_sell:OrderbookSell)->int:
    """
    It returns the whole quantity of the counterparty orderbook.
    """
    orderbook_counterparty = get_orderbook_counterparty(order, orderbook_buy, orderbook_sell)
    return orderbook_counterparty.get_total_quantity()
    
def get_price_bestorder_counterparty(order:Order, orderbook_buy:OrderbookBuy, orderbook_sell:OrderbookSell)->float:
    """
    It returns the best price of the counterparty orderbook.
    """
    orderbook_counterparty = get_orderbook_counterparty(order, orderbook_buy, orderbook_sell)
    return orderbook_counterparty.best_price()
        
def get_spread(orderbook_buy:OrderbookBuy, orderbook_sell:OrderbookSell)-> float:
    """
    It calculates the spread.
    If there is no counterparty, the spread is defined as None value.
    """
    if orderbook_buy.orderbook:
        if orderbook_sell.orderbook:
            spread = orderbook_sell.best_price() - orderbook_buy.best_price()
        else:
            spread = None
    else:
        spread = None
    return spread

def write_spread(list_spread:dict, text_file:str)-> None:
    """
    It writes our list_spread in a text file
    """
    with open(text_file, 'a+') as f:
        f.truncate(0)
        for k in list_spread.keys():
            spread = list_spread[k]
            time = k
            sentence = 'At time '+ str(time)+ ', the spread value is : ' + str(spread)
            f.write('\n')
            f.write(sentence)

def execute_best(order:Order, orderbook_buy:OrderbookBuy, orderbook_sell:OrderbookSell,
                 executed_orders:ExecutedOrders)-> None:
    """
    if quantity is greater than the quantity of the counterparty, resize the order to the quantity of the counterparty.
    while quantity of the order is not null, fill the order step by step
    take the best order and 

    """
    QTY_IDX = -1
    orderbook_counterparty= get_orderbook_counterparty(order, orderbook_buy, orderbook_sell)
    orderbook_counterparty_list = orderbook_counterparty.orderbook
    sum_counterparty_list = orderbook_counterparty.get_sum_all_qty()
    resize_quantity(order, sum_counterparty_list)
    
    i=0
    order_modified = [] 
    best_order_modified = []
    while int(order.quantity) > 0:
        best_order= orderbook_counterparty_list[i]
        qty_diff = order.quantity - best_order[QTY_IDX]
        if qty_diff>=0:
            order_modified = order.my_order.copy()
            order_modified[QTY_IDX] = best_order[QTY_IDX]
            executed_orders.book.append(best_order)
            executed_orders.book.append(order_modified)
            order.quantity = qty_diff
            orderbook_counterparty_list.remove(best_order)
        else:
            best_order_modified = best_order.copy()
            best_order_modified[QTY_IDX] = order.quantity
            executed_orders.book.append(best_order_modified)
            order.my_order[QTY_IDX] = order.quantity
            executed_orders.book.append(order.my_order)
            best_order[QTY_IDX] = abs(qty_diff)
            order.quantity = 0
            
def resize_quantity(order:Order, orderbook_size:int)->None:
    """
    Considering the fact that if the counterparty orderbook has not enough quantity, the order has to be partially filled
    and cancelled, we resize the order at the sum of the quantity in the orderbook counterparty 
    """
    if order.quantity >= orderbook_size:
        order.quantity = orderbook_size
        
def spread_as_df(spread_list:dict)->None:
    """
    It converts the spread_list (dictionary) in a dataframe

    """
    col = ['time','spread']
    df = pd.DataFrame(list(spread_list.items()), columns=col)
    return df

def write_spread_in_excel(spread_list:dict, excel_file:str, sheet:str)->None:
    """
    It converts the spread list as a df and writes it in excel with xlwings lib
    """
    START_CELL = "A1"
    book = xw.Book(excel_file)
    sheet = book.sheets[sheet]
    df_spread = spread_as_df(spread_list)
    sheet.clear_contents()
    sheet[START_CELL].options(pd.DataFrame, header=1, index =True, expand='table').value = df_spread

