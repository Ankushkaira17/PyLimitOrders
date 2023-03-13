from exec_params import Ticker_id,Quantity,Limit_price,Action
from limit_order_agent import LimitOrderAgent,Order
import unittest
from unittest.mock import MagicMock, patch

class Market_Data(price_listener):
    # Only for testing purposes
    #This simulates the testing market data for unittesting of our system
    def __init__(self):
        self.price_listener=price_listener()#also need to update our trading system to resolve integration issues
        self.mprices={}#store market prices for testing
        
    def OnPriceTick(self,product_id,price):
        try:
            self.price_listener.on_price_tick(product_id,price)## to avoid integration issues set sup system
        except:
            raise("Error")
        self.mprices[product_id]=price
class test_data():
# Set different orders with different data
    def order1(self):
        first_order=Order()
        first_order.action_flag=Action
        first_order.Quantity=Quantity
        first_order.limit_price=Limit_price
        first_order.product_id=Ticker_id
        return first_order
    def order2(self):
        first_order=Order()
        first_order.action_flag="Buy"
        first_order.Quantity=500
        first_order.limit_price=88
        first_order.product_id=Ticker_id
        return first_order
    def order3(self):
        first_order=Order()
        first_order.action_flag="Sell"
        first_order.Quantity=500
        first_order.limit_price=110
        first_order.product_id=Ticker_id
        return first_order
    def order4(self):
        first_order=Order()
        first_order.action_flag="Buy"
        first_order.Quantity=500
        first_order.limit_price=1200
        first_order.product_id="Google"
        return first_order
    def order5(self):
        first_order=Order()
        first_order.action_flag="Buy"
        first_order.Quantity=500
        first_order.limit_price=1100
        first_order.product_id="Google"
        return first_order
    def order6(self):
        first_order=Order()
        first_order.action_flag="Buy"
        first_order.Quantity=5000
        first_order.limit_price=1500
        first_order.product_id="Google"
        return first_order
    def order7(self):
        first_order=Order()
        first_order.action_flag="Buy"
        first_order.Quantity=5
        first_order.limit_price=4000
        first_order.product_id="Microsoft"
        return first_order
    def order8(self):
        first_order=Order()
        first_order.action_flag="Buy"
        first_order.Quantity=50
        first_order.limit_price=2000
        first_order.product_id="Microsoft"
        return first_order
    def order9(self):
        first_order=Order()
        first_order.action_flag="Buy"
        first_order.Quantity=20
        first_order.limit_price=6000
        first_order.product_id="Microsoft"
        return first_order

class unit_testing(unit_testing.TestCase):
    """
    Master testing class for unit testing
    """
    def __init__(self,):
        self.agent=LimitOrderAgent()
        self.data=test_data()
        self.market_data=Market_Data()

    @patch("LimitOrderAgent.add_order")
    def test_add_order(self,mock_add_order):
        """
        Test if the dictionary being built in add order method to keep track of the orders
        """
        self.agent.add_order(self.data.order1())
        self.assertEqual(len(self.agent.order_mem),1)
        self.agent.add_order(self.data.order4())
        self.agent.add_order(self.data.order7())
        self.assertEqual(len(self.agent.order_mem),3)
        self.agent.add_order(self.data.order2())
        self.assertEqual(len(self.agent.order_mem),3)

    @patch("LimitOrderAgent.execute_order")
    def test_execute_order_buy(self,mock_execute_order):
        """
        Test if the buy function works fine with no problems and check if basic IBM buy order executes
        """
        self.assertFalse(mock_execute_order.called)
        out=self.agent.execute_order(self.market_data.on_price_tick(self.data.order1.product_id,100),self.data.order1)
        self.assertTrue(mock_execute_order.called)
        self.assertEqual(mock_execute_order.call_count, 1)
        self.assertEqual(out,"buy")

    @patch("LimitOrderAgent.execute_order")
    def test_execute_order_sell(self,mock_execute_order):
        """
        Test if the sell function works fine with no problems and check if basic IBM sell order executes
        """
        self.assertFalse(mock_execute_order.called)
        out=self.agent.execute_order(self.market_data.on_price_tick(self.data.order3.product_id,120),self.data.order1)
        self.assertTrue(mock_execute_order.called)
        self.assertEqual(mock_execute_order.call_count, 1)
        self.assertEqual(out,"sell")

    @patch("LimitOrderAgent.implement_orders")
    def test_execute_order_sell(self,mock_start):
        """
        Test if the start trading function works fine by implementing a single IBM buy and sell
        After all the orders are executed then order mem will have zero orders to execute
        """
        self.assertFalse(mock_mock_start.called)
        self.agent.add_order(self.data.order1())
        self.agent.add_order(self.data.order3())
        self.agent.implement_orders()
        self.assertTrue(mock_start.called)
        self.assertEqual(mock_start.call_count, 1)
        self.assertEqual(len(self.agent.order_mem), 0)

    @patch("LimitOrderAgent.implement_orders")
    def test_multiple_orders(self,mock_start):
        """
        Test if the start trading function works fine by implementing  mutliple ticker data
        Finally after all the orders are implemented order memory should be empty.
        """
        self.agent.add_order(self.data.order1())
        self.agent.add_order(self.data.order4())
        self.agent.add_order(self.data.order7())
        self.agent.implement_orders()
        self.assertEqual(mock_start.call_count, 1)
        self.assertEqual(len(self.agent.order_mem), 0)

    @patch("LimitOrderAgent.implement_orders")
    def test_multiple_orders(self,mock_start):
        """
        Test if the start trading function throws an error if the price is none for an order
        """
        self.data.order1.price=None
        self.agent.add_order(self.data.order1())
        with self.assertRaises(Exception):
            self.agent.implement_orders()
        self.data.order1.price=100
# A series of similar test cases are implemented here
    @patch("LimitOrderAgent.implement_orders")
    def test_super_limit(self,mock_start):
        """
        Test if some orders are executed and some are left when it doesnt meet the limit order1
        conditions.All selling orders are implemented so finally there has to be 6 orders in memory
        """

        self.agent.add_order(self.data.order1())
        self.agent.add_order(self.data.order2())
        self.agent.add_order(self.data.order3())
        self.agent.add_order(self.data.order4())
        self.agent.add_order(self.data.order5())
        self.agent.add_order(self.data.order6())
        self.agent.add_order(self.data.order7())
        self.agent.add_order(self.data.order8())
        self.agent.add_order(self.data.order9())
        #set market data
        self.market_data.on_price_tick(self.data.order1.product_id,120)
        self.market_data.on_price_tick(self.data.order4.product_id,1700)
        self.market_data.on_price_tick(self.data.order7.product_id,5000)

        self.agent.implement_orders()
        self.assertEqual(len(self.agent.order_mem), 6)
    @patch("LimitOrderAgent.implement_orders")
    def test_super_limit(self,mock_start):
        """
        Test if some orders are executed and some are left when it doesnt meet the limit order1
        conditions.All buying orders are implemented so finally there has to be 3 orders in memory
        """

        self.agent.add_order(self.data.order1())
        self.agent.add_order(self.data.order2())
        self.agent.add_order(self.data.order3())
        self.agent.add_order(self.data.order4())
        self.agent.add_order(self.data.order5())
        self.agent.add_order(self.data.order6())
        self.agent.add_order(self.data.order7())
        self.agent.add_order(self.data.order8())
        self.agent.add_order(self.data.order9())
        #set market data
        self.market_data.on_price_tick(self.data.order1.product_id,85)
        self.market_data.on_price_tick(self.data.order4.product_id,1000)
        self.market_data.on_price_tick(self.data.order7.product_id,1500)

        self.agent.implement_orders()
        self.assertEqual(len(self.agent.order_mem), 3)

    @patch("LimitOrderAgent.implement_orders")
    def test_super_limit(self,mock_start):
        """
        Test if some orders are executed and some are left when it doesnt meet the limit order1
        conditions.All  orders are implemented so finally there has to be 0 orders in memory
        """

        self.agent.add_order(self.data.order1())
        self.agent.add_order(self.data.order2())
        self.agent.add_order(self.data.order3())
        self.agent.add_order(self.data.order4())
        self.agent.add_order(self.data.order5())
        self.agent.add_order(self.data.order6())
        self.agent.add_order(self.data.order7())
        self.agent.add_order(self.data.order8())
        self.agent.add_order(self.data.order9())
        #set market data
        self.market_data.on_price_tick(self.data.order1.product_id,85)
        self.market_data.on_price_tick(self.data.order4.product_id,1000)
        self.market_data.on_price_tick(self.data.order7.product_id,1500)

        self.agent.implement_orders()
        self.assertEqual(len(self.agent.order_mem), 3)

        #set market data again for sell orders
        self.market_data.on_price_tick(self.data.order1.product_id,120)
        self.market_data.on_price_tick(self.data.order4.product_id,1700)
        self.market_data.on_price_tick(self.data.order7.product_id,5000)
        self.assertEqual(len(self.agent.order_mem), 0)
