"""
Cookie Clicker Simulator
"""

import simpleplot
import math

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0
#SIM_TIME = 100000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        self._current_time = 0.
        self._current_cps = 1.        
        self._current_cks = 0.
        self._total_cks = 0.
        self._history = [(0.0, None, 0.0, 0.0)]
            
    def __str__(self):
        """
        Return human readable state
        """
        self._msg = "Time:%s, Current Cookies:%s, CPS:%s, Total Cookies%s" % (self._current_time, self._current_cks, self._current_cps, self._total_cks)
        return self._msg
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._current_cks
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._current_cps
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._current_time
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """       
        return self._history

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        if (float(cookies) - self._current_cks) > 0.:
            self._result = math.ceil((float(cookies) - self._current_cks) / self._current_cps)
        else:
            self._result = 0.
        return self._result
    
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0.0
        """
        if time > 0.:
            self._current_time += time
            self._current_cks += time * self._current_cps
            self._total_cks += time * self._current_cps
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if self._current_cks >= cost:
            self._temp = (self._current_time, item_name, cost, self._total_cks)
            self._history.append(self._temp)
            self._current_cks -= cost
            self._current_cps += additional_cps
            
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """
    # innitial game
    buildinfo = build_info.clone()
    game = ClickerState()
    if_equal = False

    # loop for game processing
    while game.get_time() < duration or if_equal:
        if if_equal == False:
            timeleft = duration - game.get_time()
            item_to_buy = strategy(game.get_cookies(), game.get_cps(), game.get_history(), timeleft, buildinfo)
            if item_to_buy == None:
                timerest = duration - game.get_time()
                game.wait(timerest)
                break
            if game.get_cookies() < buildinfo.get_cost(item_to_buy):
                timetowait = game.time_until(buildinfo.get_cost(item_to_buy))
                if game.get_time() + timetowait <= duration:
                    game.wait(timetowait)
                    game.buy_item(item_to_buy, buildinfo.get_cost(item_to_buy), buildinfo.get_cps(item_to_buy))
                    buildinfo.update_item(item_to_buy)    
                else:
                    timerest = duration - game.get_time()
                    game.wait(timerest)
            else:
                game.buy_item(item_to_buy, buildinfo.get_cost(item_to_buy), buildinfo.get_cps(item_to_buy))
                buildinfo.update_item(item_to_buy)
            if game.get_time() == duration:
                if_equal = True
                timeleft = 0.
        else:
            item_to_buy = strategy(game.get_cookies(), game.get_cps(), game.get_history(), timeleft, buildinfo)
            if item_to_buy != None and game.get_cookies() >= buildinfo.get_cost(item_to_buy):
                game.buy_item(item_to_buy, buildinfo.get_cost(item_to_buy), buildinfo.get_cps(item_to_buy))
                buildinfo.update_item(item_to_buy)
            else:
                if_equal = False
    return game

def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic (and broken) strategy does not properly
    check whether it can actually buy a Cursor in the time left.  Your
    simulate_clicker function must be able to deal with such broken
    strategies.  Further, your strategy functions must correctly check
    if you can buy the item in the time left and return None if you
    can't.
    """
    return "Cursor"

def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that will never buy anything, but
    that you can use to help debug your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
    name = None
    item_list = build_info.build_items()
    min_cost = float('inf')
    for item in item_list:
        price = build_info.get_cost(item)
        if price < min_cost and (cookies + (cps * time_left)) >= price:
            min_cost = price
            name = item
    return name

def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    name = None
    item_list = build_info.build_items()
    max_cost = -float('inf')
    for item in item_list:
        price = build_info.get_cost(item)
        if price > max_cost and (cookies + (cps * time_left)) >= price:
            max_cost = price
            name = item   
    return name

def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    """
    # best ration of CPS / cost
    name = None
    item_list = build_info.build_items()
    max_ratio = -float('inf')
    for item in item_list:
        price = build_info.get_cost(item)
        cps_item = build_info.get_cps(item)
        if cps_item / price > max_ratio and (cookies + (cps * time_left)) >= price:
            max_ratio = cps_item / price
            name = item
    return name
        
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    history = state.get_history()
    history = [(item[0], item[3]) for item in history]
    simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """    
    run_strategy("Cursor", SIM_TIME, strategy_best)

    # Add calls to run_strategy to run additional strategies
    # run_strategy("Cheap", SIM_TIME, strategy_cheap)
    # run_strategy("Expensive", SIM_TIME, strategy_expensive)
    # run_strategy("Best", SIM_TIME, strategy_best)
    
run()
#print simulate_clicker(provided.BuildInfo({'Cursor': [15.0, 50.0]}, 1.15), 16.0, strategy_cursor_broken)
#print simulate_clicker(provided.BuildInfo({'Cursor': [15.0, 0.10000000000000001], 'Portal': [1666666.0, 6666.0], 'Shipment': [40000.0, 100.0], 'Grandma': [100.0, 0.5], 'Farm': [500.0, 4.0], 'Time Machine': [123456789.0, 98765.0], 'Alchemy Lab': [200000.0, 400.0], 'Factory': [3000.0, 10.0], 'Antimatter Condenser': [3999999999.0, 999999.0], 'Mine': [10000.0, 40.0]}, 1.15), 10000000000.0, strategy_expensive)


