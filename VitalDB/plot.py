import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from scipy.fft import fft, ifft

import a_EpochtoPulse

def pltData(case):
    # PPG
    ppg = pd.read_csv('Data/' + 'Case' + str(case) + '/track1.csv')
    ppg = ppg.iloc[100000:105000]
    ppg.plot(title='PPG', x='Time', y='SNUADC/PLETH')

    # DBP
    dbp = pd.read_csv('Data/' + 'Case' + str(case) + '/track2.csv')
    dbp = dbp.iloc[0:3000]
    dbp.plot(title='DBP', x='Time', y='Solar8000/ART_DBP')

    # MBP
    mbp = pd.read_csv('Data/' + 'Case' + str(case) + '/track3.csv')
    mbp = mbp.iloc[0:3000]
    mbp.plot(title='MBP', x='Time', y='Solar8000/ART_MBP')

    # SBP
    sbp = pd.read_csv('Data/' + 'Case' + str(case) + '/track4.csv')
    sbp = sbp.iloc[0:3000]
    sbp.plot(title='SBP', x='Time', y='Solar8000/ART_SBP')

    plt.show()

    # # FFT of PPG
    # x = ppg['Time']
    # print(x, type(x))
    # y = ppg['SNUADC/PLETH']
    # ppgFFT = fft(x)
    # plt.plot(500, ppgFFT, title='FFT')

    # plt.show()

def pltEpoch(path):
    epoch = pd.read_csv(path)
    epoch.plot(title='PPG', x='Time', y='SNUADC/PLETH')
    plt.show()

# pltEpoch('Data/Case1/Track1_split/interval0.csv')
# pltEpoch('Data/Case55/Track1_split/interval187.csv')
# a_EpochtoPulse.epochToPulse('Data/Case55/Track1_split/interval187.csv')
# pltEpoch('a_output.csv')