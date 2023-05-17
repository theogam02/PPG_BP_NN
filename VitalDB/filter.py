import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy as sci


def bandPass(case):
    sig = pd.read_csv('Data/Case' + str(case) + '/track1.csv')
    x = np.array(sig['Time'])
    y = np.array(sig['SNUADC/PLETH'])
    print(type(y))

    y = sci.signal.sosfilt(sci.signal.butter(2, 3, fs=500, output='sos'), y)
    newSig = pd.DataFrame(data={'Time':x, 'SNUADC/PLETH':y})
    newSig.iloc[50000:55000].plot(title='Filtered PPG', x='Time', y='SNUADC/PLETH')
    sig.iloc[50000:55000].plot(title='PPG', x='Time', y='SNUADC/PLETH')
    plt.show()

    tmp = sig.iloc[50000:51000]
    tmp.to_csv('example.csv')

bandPass(2)