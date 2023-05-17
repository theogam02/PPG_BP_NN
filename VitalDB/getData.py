import os
import requests
import json
import csv
import pandas as pd

#r = requests.get('http://api.vitaldb.net/22f7c87e40887e437db5e0f6bde5e3df254d79f5')
# trks = requests.get('http://api.vitaldb.net/trks')

# with open('Data/allMeasurements.csv', 'w') as out:
#     out.write(trks.text)

# trks = pd.read_csv('Data/allMeasurements.csv')

# readings = ['SNUADC/PLETH', 'Solar8000/ART_DBP', 'Solar8000/ART_MBP', 'Solar8000/ART_SBP']
# trks = trks[trks['tname'].isin(readings)]

# max = trks.max()['caseid']
# caseList = []

# for i in range(1, max):
#     tmp = trks[trks['caseid'] == i]
#     if len(tmp) == 4:
#         caseList.append(tmp)
# print(len(caseList))

# trks = pd.concat(caseList)
# trks.to_csv('Data/caseList.csv')

def getCase(case):
    trks = pd.read_csv('Data/caseList.csv')
    for i in range(4):
        tmp = requests.get('http://api.vitaldb.net/' + trks.iloc[4*(case-1)+i]['tid'])
        if not os.path.exists('Data/Case' + str(case)):
            os.mkdir('Data/Case' + str(case))
        with open('Data/Case' + str(case) + '/track' + str(i+1) + '.csv', 'w') as out:
            out.write(tmp.text)