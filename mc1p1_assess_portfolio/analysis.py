"""MC1-P1: Analyze a portfolio."""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
from util import get_data, plot_data

# This is the function that will be tested by the autograder
# The student must update this code to properly implement the functionality
def assess_portfolio(sd, ed , syms , allocs, sv, rfr=0.0,sf=252.0, gen_plot=False):

    # Read in adjusted closing prices for given symbols, date range
    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)  # automatically adds SPY
    prices = prices_all[syms]  # only portfolio symbols
    prices_SPY = prices_all['SPY']  # only SPY, for comparison later


    # forward fill and backward fill nans in the df
    prices= prices.fillna(method="ffill")
    prices=prices.fillna(method="bfill")

    # Get daily portfolio value
    #First normalize allocations
    # add code here to compute daily portfolio values
    #normalize the data
    prices_norm=prices/prices.ix[0,:]

    for i, alloc in enumerate(allocs):
        prices_norm.ix[:,[i]]=prices_norm.ix[:,[i]]*alloc*sv


    prices_norm["port_val"]=prices_norm.sum(axis=1)
    port_val=prices_norm["port_val"]

    daily_returns=(port_val[1:]/port_val[:-1].values) -1

        

    # Get portfolio statistics (note: std_daily_ret = volatility)
    #code for stats
    cr=(prices_norm.ix[-1,-1]-prices_norm.ix[0,-1])/prices_norm.ix[0,-1]
   
    #adr
    adr=daily_returns.mean()

    #sddr, std deviation of daily returns
    sddr=daily_returns.std()

    #Sharpe Ratio
    sr =(252.0**(1.0/2.0)*adr)/sddr

    # Compare daily portfolio value with SPY using a normalized plot
    if gen_plot:
        # add code to plot here

        df_temp = pd.concat([port_val, prices_SPY], keys=['Portfolio', 'SPY'], axis=1)
        df_temp.plot()
        plt.show()
        pass

    # Add code here to properly compute end value
    ev = prices_norm["port_val"].iloc[-1]

    return cr, adr, sddr, sr, ev

def test_code():
    # This code WILL NOT be tested by the auto grader
    # It is only here to help you set up and test your code

    # Define input parameters
    # Note that ALL of these values will be set to different values by
    # the autograder!
    print "ADDITIIONAL TEST CASES"
    start_date = dt.datetime(2011, 1, 1)
    end_date = dt.datetime(2011, 12, 31)
    symbols = ['WFR', 'ANR', 'MWW', 'FSLR']
    allocations = [0.25, 0.25, 0.25, 0.25]
    start_val = 1000000
    risk_free_rate = 0.0
    sample_freq = 252

    cr, adr, sddr, sr, ev = assess_portfolio(sd=start_date, ed=end_date, \
                                             syms=symbols, \
                                             allocs=allocations, \
                                             sv=start_val, \
                                             gen_plot=False)

    print "Sharpe Ratio:", sr
    print "EXPECTED SHARPE -1.93664660013"
    print "ADR", adr
    print "Expected ADR  -0.00405018240566"

    start_date = dt.datetime(2010,1,1)
    end_date = dt.datetime(2010,12,31)
    symbols = ['GOOG', 'AAPL', 'GLD', 'XOM']
    allocations = [0.2, 0.3, 0.4, 0.1]
    start_val = 1000000  
    risk_free_rate = 0.0
    sample_freq = 252

    # Assess the portfolio
    cr, adr, sddr, sr, ev = assess_portfolio(sd = start_date, ed = end_date,\
        syms = symbols, \
        allocs = allocations,\
        sv = start_val, \
        gen_plot = False)

    # Print statistics
    print "Start Date:", start_date
    print "End Date:", end_date
    print "Symbols:", symbols
    print "Allocations:", allocations
    print "Sharpe Ratio:", sr
    print "expected SHARPE 1.51819"
    print "Volatility (stdev of daily returns):", sddr
    print "Average Daily Return:", adr
    print "expected adr 0.000957366234238"
    print "Cumulative Return:", cr
    print "expected cum_ret=0.255646784534"
    print "end value of portfolio", ev


if __name__ == "__main__":
    test_code()
