
"""
The trading system can be improved by the following suggestions:
-->Firstly on_tick _price function should take one argument in, just the product id and return the price value 
(but not take price as input even though it was impleemnted for testing It shouldnt be implemented like this)
-->There has to be each user inventory consisting of[balance,balance_stocks,buying_power,etc]
-->All the functions have to improved to work on async for example lets say while executing the order either a simple 
or limit agent should be with no overhead.Async Modularities around buy and sell have to be developed to increase 
scalability and real time performance.
 -->As the number of ticker values increases there has to be a centralized ticker data source which
 gives information about tickers in real time to various parts of our system with O(constant) resources.
 Trading system should be developed to incorporate this.

"""

#Folowing code is the start of limit order agen.
from exec_params import Ticker_id,Quantity,Limit_price,Action
from limit_order_agent import Limit_Order_Agent
import execution_client
import price_listener #->current market price
from test import Market_Data





class Order(enum):
    """
    enum structre to hold all order data informations
    """
    action_flag=Action #set with default IBM values
    Quantity=Quantity
    limit_price=Limit_price
    product_id=Ticker_id

class LimitOrderAgent(Limit_Order_Agent):
    """
    Limit orders are executed by calls to this agent class which has following methods
    add_order:to ad a new order to the queue of orders to be executed
    """
    def __init__(self,):
        self.price_listener=Market_Data()# for testing purpsoes set this with test data
        self.execution_client=execution_client()
        self.order_mem={}#stores orders in the following structre with key being name of the stock[name:[Order,Order,Order],name:[Order]]

        super().__init__()


    def add_order(self,order):
        """
        params:Order enum containing all details in an order
        returns None
        adds the order to the order_mem to be executed later
        """
        name=order.product_id# key value in our dictionary
        if name in self.order_mem:# Build dictionary with key as ticker name and value as order details
            self.order_mem[name].append(order)
        else:
            self.order_mem[name]=[order]

    def execute_order(self,market_price,order):
        """
        params:
        market_price:current market price of ticker.
        order:current order to be executed.
        returns the action taken
        buy or sell the order or do nothing based on the limit order rules.
        returns a flag value indicating if an order is executed or not.
        """
        if order.action_flag=="Buy":
            if(order.limit_price>=market_price):# check limit [price]
                try:
                    self.execution_client.buy(order.product_id,order.Quantity)# provide the buy call to the sup trading system
                    return "buy"
                except:
                    raise("Execution error Buy")
            else:
                return "no buy"#return no buy if it doent meet orders
        elif order.action_flag=="Sell":
            if(order.limit_price<=market_price):# check limit [price] condition
                try:
                    self.execution_client.sell(order.product_id,order.Quantity)# provide the sell call to the sup trading system
                    return "sell"
                except:
                    raise("Execution error Sell")
            else:
                return "no-sell"#return no sell if it doent meet orders
    def implement_orders(self,):
        """
        params:nothing required
        returns None
        Just call to implement the remaining orders in the order memory.
        This function can be further improved by threading to have concurrent processing of orders to improve real
        time efficiency and execute the orders in O(1).
        """
        for i in self.order_mem.keys():
            curr_category=self.order_mem[i]
            curr_mprice=self.price_listener.mprices[curr_category]
            for j in range(len(curr_category)):
                curr_order=curr_category[j]
                output=self.execute_order(curr_mprice,curr_order)
                if(output=="buy" or output=="sell"):
                    self.order_mem[curr_category].pop(j)
