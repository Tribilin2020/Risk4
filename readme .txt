Hello! Nice to see you come to my Git files :)

Feel Welcome!




THE MODEL***************************************************************************************

The objective of this script is to model how a simulated portfolio of stocks is expected to react to different market trajectories.

To proxy the trajectories, you need to input a stock ticker. Let’s say you want to simulate the AI trade deteriorating, you could proxy that by simulating a decline in NVIDIA’s stock of 30%.

Other use-cases: what happens if oil prices decline? Input an oil index or an oil company. What happens if there is a broader market crash? Model that by inputting the S&P500.

The model is very simple and straightforward. It works only with historical prices and calculates from them the correlations, volatilities and resulting betas.

HOW TO USE IT?**********************************************************************************

First off, you need to install the pandas and yahoo finance libraries into python. You can use the commands in the requirements file on this repository. They are needed to import historical price data for your chosen stocks from the yahoo database.

To then use the model, you just need to input the following datapoints in the box at the start of the python file:

• The simulated stock holdings. You should do this using tickers and percentages. Use 30 for 30%.
• Input either “7” or “30” to use that timeframe for the correlations and volatilities. You can literally only use 7 or 30.
• Input the ticker of your chosen stock proxy and its expected move. +30 means an increase of 30%

You can add more holdings by increasing the tickers in the portfolio, just follow the same syntax. For global stocks use the dot protocol, GROW.L is an example for a stock in London. You can also input ETFs.




Enjoy and I hope it helps you to manage your risk,

P.S. Don’t go too hard on AI stocks. Looks overbought.

Developed by Nicolas Braun.
