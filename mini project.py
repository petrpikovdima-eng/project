
import time
from collections import deque
import random
import matplotlib.pyplot as plt
#initiate order class
class Order:
    def __init__(self, id, side, price, quantity, timestamp=None):
        self.id = id
        self.side = side
        self.price = price
        self.quantity = quantity
        self.timestamp = timestamp if timestamp else time.time()
    # represent order is a "nice" way whenever it has to be printed 
    def __repr__(self):
        return f"Order(id={self.id}, side={self.side}, price={self.price}, qty={self.quantity})"
    #order book class keeps track of orders and their prices
class OrderBook:
    def __init__(self):
        self.buys = {}
        self.sells = {} # key is price, value is list of orders
        self.profit = 0
    def addOrder(self, order):
        if order.side == "sell":
            if order.price not in self.sells:
                self.sells[order.price] = []  # create a new list if price not there
            self.sells[order.price].append(order)  # add the order to the list
        elif order.side == "buy":
            if order.price not in self.buys:
                self.buys[order.price] = []
            self.buys[order.price].append(order)


    def matchOrder(self):
        #make sure orders are sorted by fair - earliest - first - priniciple
        for price in self.buys:
            self.buys[price].sort(key=lambda o: o.timestamp)
        for price in self.sells:
            self.sells[price].sort(key=lambda o: o.timestamp)

        #update profit which comes from selling the cheapest orders to the biggest bid orders
        for buyprice in sorted(self.buys.keys())[:]: #sorted by cheapest first
            for sellprice in sorted(self.sells.keys(),reverse=True)[:]:#biggest first
                if buyprice >= sellprice: #only profitable condition
                    buy_order = self.buys[buyprice][0] # as both are sorted can always select the first one
                    sell_order = self.sells[sellprice][0]
                    tradequantity = min(buy_order.quantity, sell_order.quantity)
                    buy_order.quantity -= tradequantity
                    sell_order.quantity -= tradequantity
                    self.profit += (buyprice - sellprice) * tradequantity

                    #remove empty orders and remove from list of orders - orders that have been completed
                    if buy_order.quantity == 0:
                        self.buys[buyprice].pop(0)
                        if not self.buys[buyprice]:
                            del self.buys[buyprice]
                    if sell_order.quantity == 0:
                        self.sells[sellprice].pop(0)
                        if not self.sells[sellprice]:
                            del self.sells[sellprice]
    #testing nice order print
    def print_book(self, depth=5):
        print("\n--- ORDER BOOK ---")
        print("SELLS:")
        for price in sorted(self.sells.keys())[:depth]:
            orders = self.sells[price]
            total_qty = sum(o.quantity for o in orders)
            print(f"  {price}: {total_qty} | Orders: {orders}")

        print("BUYS:")
        for price in sorted(self.buys.keys(), reverse=True)[:depth]:
            orders = self.buys[price]
            total_qty = sum(o.quantity for o in orders)
            print(f"  {price}: {total_qty} | Orders: {orders}")

        print("------------------\n")
    def plot_book(self):
        # buy orders
        buy_prices = sorted(self.buys.keys())
        buy_quantities = [sum(o.quantity for o in self.buys[p]) for p in buy_prices]

        # sell orders
        sell_prices = sorted(self.sells.keys())
        sell_quantities = [sum(o.quantity for o in self.sells[p]) for p in sell_prices]

        plt.figure(figsize=(10,6))

        # plot buys as green bars
        plt.bar(buy_prices, buy_quantities, color='green', alpha=0.6, label='Buy Orders') #alpha is transparency, bars are slightly transparent to see overlap

        # plot sells as red bars
        plt.bar(sell_prices, sell_quantities, color='red', alpha=0.6, label='Sell Orders')

        plt.xlabel("Price")
        plt.ylabel("Quantity")
        plt.title("Order Book Visualization")
        plt.legend()
        plt.show()

def generate_random_order(order_id):
    side = random.choice(["buy", "sell"])       # randomly buy or sell
    price = random.randint(80, 100)            # random price around 100
    quantity = random.randint(1, 50)           # random quantity
    return Order(order_id, side, price, quantity)
ob = OrderBook()


num_orders = 15  # number of orders to simulate

for i in range(1, num_orders + 1):
    order = generate_random_order(i)
    print(f"New order: {order}")
    ob.addOrder(order)   # add to book
    ob.matchOrder()      # match immediately
    ob.print_book()      # see updated book after each order

print("Total profit:", ob.profit)
ob.plot_book()





        