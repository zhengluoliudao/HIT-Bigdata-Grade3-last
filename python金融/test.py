import tushare as ts
cons = ts.get_apis()
df_day =ts.bar("IF1801",conn=cons,asset='X',freq='D')
df_1min =ts.bar("IF1801",conn=cons,asset='X',freq='1min')
print(df_day)