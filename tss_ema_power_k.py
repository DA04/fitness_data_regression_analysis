# importing libraries
import pandas as pd

# prepairing dataset
df = pd.read_csv('merged.csv', index_col=0)
df = df.loc[df.timestamp > '2020-12-26']
df = df.loc[df.timestamp < '2021-04-01']
df['date'] = pd.to_datetime(df['timestamp']).dt.date
df = df[['date', 'TSS', 'coeff']]

# generating training season dates range
import datetime
base = datetime.datetime.today()
base = max(df.date)
date_list = [base - datetime.timedelta(days=x) for x in range(95)]

ds = pd.DataFrame({'date': date_list})
ds = pd.merge(ds, df, on='date', how='left')
ds = ds.sort_values(by='date')
ds['TSS'] = ds['TSS'].fillna(0)

# EMA calculation
ds['ewm'] = ds['TSS'].ewm(span=7).mean()

import matplotlib.pyplot as plt

# drawing a chart with three Y axis, more details here - https://matplotlib.org/3.4.3/gallery/ticks_and_spines/multiple_yaxis_with_spines.html
fig, ax = plt.subplots()
fig.subplots_adjust(right=0.65)

# the title of the chart
twin1 = ax.twinx()
twin2 = ax.twinx()

# the distance between second and third y axis
twin2.spines.right.set_position(("axes", 1.1))

# metrics
p1 = ax.bar(ds.date, ds.TSS, color='limegreen', label = 'TSS')
p2 = twin1.plot(ds.date, ds['ewm'], linestyle="--", color='purple', label='EMA for TSS wtih 7-days span')
p3 = twin2.plot(ds.date, ds.coeff, marker="D", linestyle="", alpha=0.8, color="r", label='k value on the date')

# setiings for labels and legends
ax.set_ylim(0, 135)
twin1.set_ylim(0, 80)
twin2.set_ylim(0, 1)
plt.axhline(y=ds.coeff.mean(), color='red', linestyle=':', label ='k values mean')
plt.rcParams['figure.figsize'] = [18, 7]
ax.set_xlabel("Dates")
ax.set_ylabel("TSS")
twin1.set_ylabel("EMA")
twin2.set_ylabel("k value")
fig.suptitle('\n'.join(['Distribution of Power coefficient (k) during the training season (HR[bpm] = b+k*Power[watts])', 
                        'in comparison to TSS and EMA for TSS with 7-days span']), y=0.95, x=0.45)
fig.legend(loc='center', bbox_to_anchor=(0.4, 0), shadow=False, ncol=2)
plt.show()