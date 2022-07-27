import pywedge as pw
import pandas as pd
df = pd.read_csv (r'G:\vgsales.csv')
df.head()
df.columns
mc=pw.Pywedge_Charts(df, c=None, y="Global_Sales")
charts=mc.make_charts()