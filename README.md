# Algorithmic-Trading-with-Python
This repository contains python code for different strategies used for algorithmic trading.For every strategy i have plotted the gross performance and the cumulative returns.
I have followed the book Python for Algorithmic Trading by Yves Hilpisch.
1) The first file illustrates the SMA strategy (Simple Moving Average). This is a popular technical analysis tool, used mainly to identify trends, it is one of the most commonly used indicators across all financial markets.
2) The second file illustrates the momentum based strategy applied on Gold prices.Momentum strategies exploit a tendency for a stock's prior returns and prior news about its earnings to predict future returns. It includes both cross-sectional momentum startegy and time series momentum. I have shown time series strategy applied on AAPL stock

3) The third strategy is known as mean reversion. Mean reversion is a financial theory which suggests that, after an extreme price move, asset prices tend to return back to normal or average levels. Prices routinely oscillate around the mean or average price but tend to return to that same average price over and over.We set a threshold value and if the SMA rises above or dips below the threshold we short or buy respectively.

4) The fourth file contains 2 machine learning based strategies which predict future market movement using linear regression and logistic regression respectively. 
The first strategy uses previously recorded price or 'n' prices known as lags to predict the next price. 
Seconds strategy uses logistic regression to classify the next value as +1 or -1 to go long or short respectively. This reduces the prediction to a basic classififcation problem.







5) The fifth file contains a deep neural network which predicts the market movement similar to Logistic regression.It uses tensorflow and keras libraries to achieve this.
6) The event based backtesting folder contains the code for event based backtesting of a certain stock, in this case apple.  On a basic
level, an event is characterized by the arrival of new data. Backtesting a trading strategy for the Apple Inc. stock based on end-of-day data, an event
would be a new closing price for the Apple stock. It can also be a change in an interest rate, or the hitting of a stop loss level.

7)  The Kelly Criterion is a mathematical formula that helps investors and gamblers calculate what percentage of their money they should allocate to each investment or bet.







 
 
I hope you learnt something new today Cheers :)
