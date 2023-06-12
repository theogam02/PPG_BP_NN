import os
import pandas as pd
import numpy as np
import preproc, getData, splitfiles, a_EpochtoPulse, feature, plot

dataset = pd.DataFrame(columns=np.arange(94))
# getData.getCase(1)
# preproc.cleanData(1)
# splitFiles.splitFiles(1)

for i in range(1):
    # getData.getCase(i)

    # preproc.cleanData(i)

    # splitFiles.splitFiles(i)

    totalTracks = os.listdir('Data/Case' + str(i+1) + '/Track1_split')
    for j in range(2):
        print('Hi')
        fileName = 'Data/Case' + str(i+1) + '/Track1_split/' + 'interval' + str(j) + '.csv'
        a_EpochtoPulse.epochToPulse(fileName)
        features = feature.features('a_output.csv')
        sbp = pd.read_csv('Data/Case' + str(i+1) + '/Track2_split/' + 'interval' + str(j) + '.csv').iloc[0]['Solar8000/ART_SBP']
        dbp = pd.read_csv('Data/Case' + str(i+1) + '/Track4_split/' + 'interval' + str(j) + '.csv').iloc[0]['Solar8000/ART_DBP']
        features = np.append(features, np.array([sbp, dbp]))
        tmp1 = dataset
        tmp2 = pd.DataFrame([features], columns=dataset.columns)
        dataset = pd.concat([tmp1, tmp2], axis=0)
        os.remove('a_output.csv')
dataset.to_csv('wav.csv', index=False)