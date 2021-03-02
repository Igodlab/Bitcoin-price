# Bitcoin-price

The purpose of this price analysis is to correlate diverse indicators for a cyclical (halving) behavior of Bitcoin price. The indicators used are based on price data but future developement could include on-chain data.  

## Bitcoin bull markets
Based on price history we have seen Bitcoin repeating a similar percentage price-apreciation througout its previous halving events. Bitcoin's fixed supply is reduced by one-half roughly every four years in a discontinuous piece-wise manner. The maximum supply of the asset is 21 million and the last Bitcoin ever to be created will be in 2140. So far, the market seems to react very well from near halving events up to several subsequent months of price increase. The past three halving events leading to bull markets have had a similar dynamic. Where the price percentage increase ranges from 100%-300% breaking to record all-time-high's (ATH) as the blow of top and then the start of a bear market with crashes of approximately 80% that never went lower than its previous ATH. A massive collective reaction to halving events seems to be an indicator that the reminder of Bitcoin's scarcity is crucial.

## Moving Averages
The indicators used here include simple moving averages (MA), supply, stock in circulation, price velocity and price acceleration.

#### Pi cycle
\begin{equation}
MA^{350}_{i} = \sum_{i=-350}^{i} x_i, \;\; i\in \mathcal{R}
\end{equation}
