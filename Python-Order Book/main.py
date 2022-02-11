
def main() -> None:
    # Import modules where we set our classes and functions
    from orderbooks import OrderbookBuy, OrderbookSell, ExecutedOrders, Order
    import processing as pr
    import view as vw
    
    DISPLAY = 1000
    NB_ORDERS = 10000
    SIGMA = 10
    MU = 200
    
    # Instantiate text files
    text_file_transactions = 'executed.txt'
    text_file_spread = 'spreads.txt'
    excel_file = 'book.xlsx'
    sheet_spread = 'spread'
    sheet_price = 'price'

    # Instantiate our objects
    orderbook_buy = OrderbookBuy()
    orderbook_sell = OrderbookSell()
    executed_orders = ExecutedOrders()
    list_spread = {}

    # Generate random orders
    list_orders = pr.generate_orders(NB_ORDERS, MU, SIGMA)

    # Process orders
    count = 0
    for o in list_orders:
        if count % DISPLAY == 0:
            vw.display_top_10(orderbook_buy, orderbook_sell, count, DISPLAY)
        order = Order(o)
        pr.process_orders(order, orderbook_buy, orderbook_sell,
                          executed_orders, list_spread)
        count += 1

    # Write orders and spreads in text files
    executed_orders.write_transactions(text_file_transactions)
    pr.write_spread(list_spread, text_file_spread)

    # Write orders and spreads in excel files
    pr.write_spread_in_excel(list_spread, excel_file, sheet_spread)
    executed_orders.write_transactions_in_excel(excel_file, sheet_price)


if __name__ == '__main__':
   main()