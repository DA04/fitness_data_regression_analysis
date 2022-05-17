"""PWC170 Probe (Physical Working Capacity at 170 bpm)
Source articles: https://www.brianmac.co.uk/pwc170.htm
http://sportwiki.to/%D0%9F%D1%80%D0%BE%D0%B1%D0%B0_PWC170
PWC170= W1 + (W2 - W1)(170 - f1)/(f2 – f1),
W1 - first power
W2 - second power
f1 - HR rate after 5 min under W1
f2 - HR rate after 5 min under W2
"""

# import libraries
import pandas as pd
import numpy as np
import psycopg2

conn = psycopg2.connect(host="localhost", database="garmin_data", user="postgres", password="*****")

# prepair the dataset
w1_df = pd.read_sql_query("""select to_char(timestamp, 'YYYY-MM') as month, heart_rate from record
                            where activity_id in (select activity_id from session where sub_sport = 'virtual_activity' 
                            and timestamp::text between '2020-10-31' and '2021-04-01')
                            and power between 125 and 135 and heart_rate > 80 and cadence between 80 and 90""", conn)
w1_df11 = w1_df.loc[w1_df.month == '2020-11']
w1_df03 = w1_df.loc[w1_df.month == '2021-03']

w2_df = pd.read_sql_query("""select to_char(timestamp, 'YYYY-MM') as month, heart_rate from record
                            where activity_id in (select activity_id from session where sub_sport = 'virtual_activity' 
                            and timestamp::text between '2020-10-31' and '2021-04-01')
                            and power between 175 and 185 and heart_rate > 80 and cadence between 80 and 90""", conn)
w2_df11 = w2_df.loc[w2_df.month == '2020-11']
w2_df03 = w2_df.loc[w2_df.month == '2021-03']

# first power HR rate estimation
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

fig, (ax1, ax2) = plt.subplots(1,2)
fig.suptitle('First and Last Months Heart Rate values distribution at 130 watts')
N1, bins1, patches1 = ax1.hist(w1_df11.heart_rate, bins=np.arange(110,190,1))
for i in range(19,20):
    patches1[i].set_facecolor('r')
ax1.set_ylim(0, 35)
ax1.set_xlabel("HR, bpm")
ax1.set_ylabel("Counts")
N2, bins2, patches2 = ax2.hist(w1_df03.heart_rate, bins=np.arange(110,190,1))
for i in range(16,17):
    patches2[i].set_facecolor('r')

ax2.set_ylim(0, 300)
ax2.set_xlabel("HR, bpm")
ax2.set_ylabel("Counts")
plt.rcParams['figure.figsize'] = [16, 4]
plt.show()

# second power HR rate estimation
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

fig, (ax1, ax2) = plt.subplots(1,2)
fig.suptitle('First and Last Months Heart Rate values distribution at 180 watts')
N1, bins1, patches1 = ax1.hist(w2_df11.heart_rate, bins=np.arange(110,190,1))
for i in range(65,66):
    patches1[i].set_facecolor('r')
ax1.set_ylim(0, 25)
ax1.set_xlabel("HR, bpm")
ax1.set_ylabel("Counts")
N2, bins2, patches2 = ax2.hist(w2_df03.heart_rate, bins=np.arange(110,190,1))
for i in range(50,51):
    patches2[i].set_facecolor('r')

ax2.set_ylim(0, 100)
ax2.set_yticks(np.arange(0,125,25))
ax2.set_xlabel("HR, bpm")
ax2.set_ylabel("Counts")
plt.rcParams['figure.figsize'] = [16, 4]
plt.show()

# Last month PWC170 probe calculation
W1 = 130
W2 = 180
f1 = 127
f2 = 161

from scipy.interpolate import interp1d

y_interp = interp1d([f1, f2], [W1, W2], fill_value="extrapolate")
f3 = 170
W3 = y_interp(f3)

import matplotlib.pyplot as plt

fig, (ax1, ax2) = plt.subplots(1,2)
fig.suptitle('Last month PWC170')
ax1.plot([W1, W2], [f1, f2], 'ro')
ax1.axline((W1, f1), (W2, f2))
ax1.text(W2+2, f2, "({},{})".format(W2, f2), size=10, color='r')
ax1.text(W1+2, f1, "({},{})".format(W1, f1), size=10, color='r')
ax1.set_xlim([120, 200])
ax1.set_ylim([120, 180])
ax1.set_xlabel("Power, watts")
ax1.set_ylabel("HR, bpm")

ax2.plot([W1, W2, W3], [f1, f2, f3], 'ro')
ax2.axline((W1, f1), (W2, f2))
ax2.axvline(x=W3, color='r', linestyle=':')
ax2.axhline(y=f3, color='r', linestyle=':')
ax2.text(W3-30, f3+3, "PWC170 = {}".format(np.round(W3, 2)), size=10, color='r')
ax2.set_xlim([120, 200])
ax2.set_ylim([120, 180])
ax2.set_xlabel("Power, watts")
ax2.set_ylabel("HR, bpm")
plt.rcParams['figure.figsize'] = [10, 4]
plt.show() 