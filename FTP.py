activity_id = 80286974365

# importing libraries
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline
import numpy as np

# connecting to a training record data
conn = psycopg2.connect(host="localhost", database="garmin_data", user="postgres", password="*****")
df = pd.read_sql_query("""select timestamp, heart_rate, cadence, power from record 
where activity_id ={} order by timestamp asc""".format(activity_id), conn)
df['sec'] = (df['timestamp']-min(df['timestamp'])).dt.total_seconds()/60

# drawing a chart with three Y axis, more details here - https://matplotlib.org/3.4.3/gallery/ticks_and_spines/multiple_yaxis_with_spines.html
fig, ax = plt.subplots()
fig.subplots_adjust(right=0.75)

# the title of the chart
plt.title(str(min(df['timestamp']).date()) + " / Activity - " +str(activity_id))
twin1 = ax.twinx()
twin2 = ax.twinx()

# the distance between second and third y axis
twin2.spines.right.set_position(("axes", 1.1))

# option 2 - curved lines

# spline function, more details here - https://www.geeksforgeeks.org/how-to-plot-a-smooth-curve-in-matplotlib/
def spline(x, y, n):
    do_spline = make_interp_spline(x,y)
    x_ = np.linspace(x.min(), x.max(), n)
    y_ = do_spline(x_)
    return x_, y_

# 
p1, = ax.plot(spline(df.sec, df.heart_rate, 150)[0], spline(df.sec, df.heart_rate, 150)[1],"r-", label="HR")
p2, = twin1.plot(spline(df.sec, df.power, 150)[0], spline(df.sec, df.power, 150)[1], "b-", label="Power")
p3, = twin2.plot(spline(df.sec, df.cadence, 150)[0], spline(df.sec, df.cadence, 150)[1], "g-", label="Cadence")

# setiing limits for x and y axis
ax.set_xlim(0, 50)
ax.set_ylim(0, 200)
twin1.set_ylim(0, 400)
twin2.set_ylim(0, 120)

# setting labels and colors for axis
ax.set_xlabel("Time, min")
ax.set_ylabel("HR, bpm")
twin1.set_ylabel("Power, watts")
twin2.set_ylabel("Cadence, bpm")

ax.yaxis.label.set_color(p1.get_color())
twin1.yaxis.label.set_color(p2.get_color())
twin2.yaxis.label.set_color(p3.get_color())

tkw = dict(size=4, width=1.5)
ax.tick_params(axis='y', colors=p1.get_color(), **tkw)
twin1.tick_params(axis='y', colors=p2.get_color(), **tkw)
twin2.tick_params(axis='y', colors=p3.get_color(), **tkw)
ax.tick_params(axis='x', **tkw)

# adding the legend
ax.legend(handles=[p1, p2, p3])

# size of the chart
plt.rcParams['figure.figsize'] = [18, 10]
l_style = dict(color='gray', linestyle=':')
plt.axvline(x=9, **l_style)
plt.axvline(x=14, **l_style)
plt.axvline(x=20, **l_style)
plt.axvline(x=40, **l_style)

# add labels
style = dict(size=36, color='gray')
ax.text(5, 100, "1", ha='center', **style)
ax.text(12, 100, "2", ha='center', **style)
ax.text(17, 100, "3", ha='center', **style)
ax.text(30, 100, "4", ha='center', **style)
ax.text(43, 100, "5", ha='center', **style)
plt.show()


# ftp calculation
activity_id = 80286974365

conn = psycopg2.connect(host="localhost", database="garmin_data", user="postgres", password="*****")
df = pd.read_sql_query("""select timestamp, heart_rate, cadence, power, rank() over (order by timestamp asc) as rank_no from record 
where activity_id ={} order by timestamp asc""".format(activity_id), conn)

start = 20*60
end = 40*60
df = df.loc[((df['rank_no'] > start) & (df['rank_no'] < end))]
ftp = df['power'].mean()*0.95