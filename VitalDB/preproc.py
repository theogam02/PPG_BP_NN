import csv
import pandas as pd
import matplotlib.pyplot as plt


def cleanData(case):
    # Cleaning the PPG Data
    tmp1 = pd.read_csv('Data/' + 'Case' + str(case) + '/track1.csv')
    tmp2 = pd.DataFrame(tmp1['Time'].ffill() + tmp1.groupby(tmp1['Time'].notnull().cumsum()).cumcount()/500, columns=['Time'])
    tmp1 = tmp1.drop('Time', axis=1)
    tmp1 = pd.DataFrame(tmp1['SNUADC/PLETH'])
    tmp1 = pd.concat([tmp2, tmp1], axis=1, join="inner")
    tmp1 = tmp1.dropna()
    tmp1.to_csv('Data/' + 'Case' + str(case) + '/track1.csv')

    # Cleaning the Diastolic BP Data
    tmp1 = pd.read_csv('Data/' + 'Case' + str(case) + '/track2.csv')
    tmp1 = tmp1.loc[tmp1['Solar8000/ART_DBP'] > 0]
    tmp1.to_csv('Data/' + 'Case' + str(case) + '/track2.csv')

    # Cleaning the Mean BP Data
    tmp1 = pd.read_csv('Data/' + 'Case' + str(case) + '/track3.csv')
    tmp1 = tmp1.loc[tmp1['Solar8000/ART_MBP'] > 0]
    tmp1.to_csv('Data/' + 'Case' + str(case) + '/track3.csv')

    #Cleaning the Systolic BP Data
    tmp1 = pd.read_csv('Data/' + 'Case' + str(case) + '/track4.csv')
    tmp1 = tmp1.loc[tmp1['Solar8000/ART_SBP'] > 0]
    tmp1.to_csv('Data/' + 'Case' + str(case) + '/track4.csv')