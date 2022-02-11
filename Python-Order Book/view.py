import pandas as pd


def display_top_10(orderbook_buy,orderbook_sell, count, every_nth_order):
    buy = orderbook_buy.display_df_topten()
    sell = orderbook_sell.display_df_topten()
    sell = sell.drop(columns=['id', 'date', 'sell_buy'])
    buy = buy.drop(columns=['id', 'date', 'sell_buy'])
    sell = sell.rename(columns={"price": "price_sell",
                                "quantity": "quantity_sell"})
    buy = buy.rename(columns={"price": "price_buy",
                              "quantity": "quantity_buy"})
    buy = buy[["quantity_buy", "price_buy"]]
    result = pd.concat([buy, sell], axis=1)
    print(result)
    return None

    