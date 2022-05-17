# Regression Analysis for fitness data
 This repo contains following scripts examples:
 1. FTP test general chart example built from parsed FIT data with Python and visualized with the help of matplotlib. [The script](FTP.py) contains basic calculations for FTP value.
 ![FTP test chart example](/ftp_test.png)
 2. PWC170 modified probe example based on regular cycling trainings. [The script](/PWC170.py) contains the logic for getting input data for PWC170 formula and graphical extrapolation to find PWC170 value.
 ![PWC170](/pwc170_last.png)
 3. Linear regression model to calculate training performance over the training season. [The script](/linear_regression.py) includes example for one training model fit and chart.
![OLS](/ols.png)
4. [The script](/np_tss_calc.py) contains functions for normalized power (NP) and Training Stress Score (TSS) calculations.
5. [The script](/tss_ema_power_k.py) contains dataset rows generation to analyze TSS scores and their Exponential Moving Average (EMA) against power coefficient k (HR[bpm] = b+k*Power[watts]) dynamics during the training season. Matplotlib chart is also provided.
![Training Season](/training_season.png)