import os
import pandas as pd
import numpy as np
import shutil
import preproc, getData, splitfiles, a_EpochtoPulse, filter, plot, sqi

dataset = pd.DataFrame(columns=np.arange(74))
# getData.getCase(1)
# preproc.cleanData(1)
# splitfiles.splitFiles(1)

def remove_directory(directory_path):
    try:
        shutil.rmtree(directory_path)
        print(f"Directory '{directory_path}' and its files have been successfully removed.")
    except OSError as e:
        print(f"Error: {e.filename} - {e.strerror}")

for i in range(1,2):
    getData.getCase(i+1)

    preproc.cleanData(i+1)

    splitfiles.splitFiles(i+1)

    if os.path.exists('Data/Case' + str(i+1) + '/Track1_split'):
        totalTracks = os.listdir('Data/Case' + str(i+1) + '/Track1_split')
        print(len(totalTracks))
        for j in range(1):
            fileName = 'Data/Case' + str(i+1) + '/Track1_split/' + 'interval' + str(j) + '.csv'
            # print(fileName)
            sbp = pd.read_csv('Data/Case' + str(i+1) + '/Track2_split/' + 'interval' + str(j) + '.csv').iloc[0]['Solar8000/ART_SBP']
            dbp = pd.read_csv('Data/Case' + str(i+1) + '/Track4_split/' + 'interval' + str(j) + '.csv').iloc[0]['Solar8000/ART_DBP']
            # print('sbp: ', sbp, 'dbp: ', dbp)
            # print('type sbp: ', type(sbp), 'type dbp: ', type(dbp))
            if 50 <= sbp <= 300 and 30 <= dbp <= 250:
                a_EpochtoPulse.epochToPulse(fileName)
                if os.path.exists('a_output.csv') and sqi.sqitest('a_output.csv') != 1:
                    features = filter.features('a_output.csv')
                    if len(features) == 72:
                        features = np.append(features, np.array([sbp, dbp]))
                        # print(len(features))
                        tmp1 = dataset
                        tmp2 = pd.DataFrame([features], columns=dataset.columns)
                        dataset = pd.concat([tmp1, tmp2], axis=0)
                    # os.remove('a_output.csv')
            elif os.path.exists('a_output.csv'): os.remove('a_output.csv')
    
    remove_directory('Data/Case' + str(i+1))
dataset.to_csv('wav.csv', index=False)