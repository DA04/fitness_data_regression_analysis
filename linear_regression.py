# data analysis before linear model fit
import pandas as pd
import psycopg2

activity_id = 77485450073

conn = psycopg2.connect(host="localhost", database="garmin_data", user="postgres", password="*****")
df = pd.read_sql_query("""select rank_no, power, heart_rate from (select record_id, power, heart_rate, 
                                rank () over (order by timestamp asc) as rank_no 
                                from record where activity_id = {}) tbl 
                                where tbl.rank_no between {} and {}""".format(activity_id, start*60,end*60), conn)

fig, (ax1, ax2) = plt.subplots(1,2)
plt.rcParams['figure.figsize'] = [12, 5]
ax1.hist(df.heart_rate)

# ax1.title('Heart Rate values distribution')
ax1.set_xlabel("Heart Rate, bpm")
ax1.set_ylabel("Counts")
ax2.hist(df.power)
ax2.set_xlabel("Power, watts")
ax2.set_ylabel("Counts")
plt.show()

# Correlation matrix
import numpy as np
from mlxtend.plotting import heatmap

cm = np.corrcoef(df.values.T)
hm = heatmap(cm, row_names=df.columns, column_names=df.columns)
plt.show()

# OLS model
import statsmodels.api as sm
X = df[['power']]
y = df['heart_rate']

X = sm.add_constant(X)
model = sm.OLS(y, X).fit()
predictions = model.predict(X)
results = model.summary()
print(results)
dir(model)

# Linear regression chart
import matplotlib.pyplot as plt
import numpy as np

plt.scatter(df.power, df.heart_rate, marker='o', label='record_id', s=8)
plt.suptitle('Power and Heart Rate relation fitted line plot', fontsize=14)
plt.title('HR[bpm] = {}+{}*Power[watts]'.format(round(model.params[0],2), round(model.params[1],2)), fontsize=10)
plt.rcParams['figure.figsize'] = [6, 6]
plt.plot(df.power, model.params[0]+model.params[1]*df.power, color='red')
plt.xlabel("Power, watts")
plt.ylabel("HR, bpm")

plt.show()