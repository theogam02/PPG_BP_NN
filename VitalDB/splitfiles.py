#code splits track files into 20 sec csv files
import pandas as pd
import os

# Checks for gaps in the tracks that may have been caused by the preprocessing.
# Takes in 2 inputs: 1. The track 2. The type of track, ppg or bp.
def checkGaps(track, type):
    gaps = []
    if type == 'ppg':
        for i in range(len(track) - 1):
            gap = track.iloc[i+1]['Time'] - track.iloc[i]['Time']
            if gap > 0.0021: gaps.append([i, gap, [track.iloc[i]['Time'], track.iloc[i+1]['Time']]])
    else:
        for i in range(len(track) - 1):
            gap = track.iloc[i+1]['Time'] - track.iloc[i]['Time']
            if gap > 2.1: gaps.append([i, gap, [track.iloc[i]['Time'], track.iloc[i+1]['Time']]])
    return gaps

def checkIntervalOverlap(interval, intervals):
    for i in range(len(intervals)):
        if intervals[i][2][0] < interval[0] < intervals[i][2][1] or intervals[i][2][0] < interval[1] < intervals[i][2][1]:
            # print('Interval overlap')
            return True
    return False

def splitFiles(case):
    # Read the CSV file 
    ppgData = pd.read_csv('Data/Case' + str(case) + '/track1.csv')
    sbpData = pd.read_csv('Data/Case' + str(case) + '/track4.csv')
    dbpData = pd.read_csv('Data/Case' + str(case) + '/track2.csv')

    if len(ppgData) > 10 and len(sbpData) > 10 and len(dbpData) > 10:
        # Cut off any excess measurements from the tracks
        startTime = max(ppgData.iloc[0]['Time'], sbpData.iloc[0]['Time'], dbpData.iloc[0]['Time'])
        endTime = min(ppgData.iloc[-1]['Time'], sbpData.iloc[-1]['Time'], dbpData.iloc[-1]['Time'])

        # print('Startime:', startTime, 'Endtime:', endTime)

        ppgData = ppgData.loc[startTime <= ppgData['Time']]
        ppgData = ppgData.loc[ppgData['Time'] <= endTime]
        sbpData = sbpData.loc[startTime <= sbpData['Time']]
        sbpData = sbpData.loc[sbpData['Time'] <= endTime]
        dbpData = dbpData.loc[startTime <= dbpData['Time']]
        dbpData = dbpData.loc[dbpData['Time'] <= endTime]

        # print('Startimes: ', ppgData.iloc[0]['Time'], sbpData.iloc[0]['Time'], dbpData.iloc[0]['Time'])

        # ppgGaps = checkGaps(ppgData, 'ppg')
        # sbpGaps = checkGaps(sbpData, 'bp')
        # dbpGaps = checkGaps(dbpData, 'bp')
        # gapsOverall = ppgGaps + sbpGaps + dbpGaps
        # gapsOverall = ppgGaps
        # print(gapsOverall)

        # Calculate the number of samples in a 20-second interval
        intervalSamples = int(20 / 0.002)
        bpInterval = int(20/2)

        # Split the data into 20-second intervals
        ppgIntervals = []
        for i in range(0, len(ppgData) - intervalSamples, intervalSamples):
            # if not checkIntervalOverlap([ppgData.iloc[i]['Time'], ppgData.iloc[i+intervalSamples]['Time']], gapsOverall): 
            startTime, endTime = ppgData.iloc[i]['Time'], ppgData.iloc[i+intervalSamples-1]['Time']
            if endTime - startTime > 18:
                ppgIntervals.append(ppgData[i:i+intervalSamples])
        # sbpIntervals = []
        # for i in range(0, len(sbpData) - bpInterval, bpInterval):
        #     if not checkIntervalOverlap([sbpData.iloc[i]['Time'], sbpData.iloc[i+bpInterval]['Time']], gapsOverall): 
        #         sbpIntervals.append(sbpData[i:i+bpInterval])
        # dbpIntervals = []
        # for i in range(0, len(dbpData) - bpInterval, bpInterval):
        #     if not checkIntervalOverlap([dbpData.iloc[i]['Time'], dbpData.iloc[i+bpInterval]['Time']], gapsOverall): 
        #         dbpIntervals.append(dbpData[i:i+bpInterval])



        # Segmenting the BP intervals according to the ppg split
        sbpIntervals = []
        dbpIntervals = []
        for i in range(len(ppgIntervals)):
            interval = [ppgIntervals[i].iloc[0]['Time'], ppgIntervals[i].iloc[-1]['Time']]
            tmp = sbpData.loc[interval[0] <= sbpData['Time']]
            tmp = tmp.loc[tmp['Time'] <= interval[1]]
            #if len(tmp) != 0:
            sbpIntervals.append(tmp)
            tmp = dbpData.loc[interval[0] <= dbpData['Time']]
            tmp = tmp.loc[dbpData['Time'] <= interval[1]]
            #if len(tmp) != 0:
            dbpIntervals.append(tmp)

        

        # Average out the BP values. Some intervals may be empty so we ignore them.
        for i in range(len(sbpIntervals)):
            if len(sbpIntervals[i]) > 5:
                start, finish = sbpIntervals[i].iloc[0]['Time'], sbpIntervals[i].iloc[-1]['Time']
                tmp = sbpIntervals[i]['Solar8000/ART_SBP'].mean()
                sbpIntervals[i] = pd.DataFrame({'start': [start], 'finish': [finish], 'Solar8000/ART_SBP': [tmp]})
            else:
                sbpIntervals[i] = pd.DataFrame({'start': [None], 'finish': [None], 'Solar8000/ART_SBP': [None]})
                # print(i, sbpIntervals[i])
        for i in range(len(dbpIntervals)):
            if len(dbpIntervals[i]) > 5:
                start, finish = dbpIntervals[i].iloc[0]['Time'], dbpIntervals[i].iloc[-1]['Time']
                tmp = dbpIntervals[i]['Solar8000/ART_DBP'].mean() 
                dbpIntervals[i] = pd.DataFrame({'start': [start], 'finish': [finish], 'Solar8000/ART_DBP': [tmp]})
            else:
                dbpIntervals[i] = pd.DataFrame({'start': [None], 'finish': [None], 'Solar8000/ART_DBP': [None]})
                # print(i, dbpIntervals[i])

        # Make new csv files
        if not os.path.exists('Data/Case' + str(case) + '/Track1_split'): os.mkdir('Data/Case' + str(case) + '/Track1_split')
        if not os.path.exists('Data/Case' + str(case) + '/Track2_split'): os.mkdir('Data/Case' + str(case) + '/Track2_split')
        if not os.path.exists('Data/Case' + str(case) + '/Track4_split'): os.mkdir('Data/Case' + str(case) + '/Track4_split')
        for i, interval in enumerate(ppgIntervals):
            interval.to_csv('Data/Case' + str(case) + '/Track1_split/interval' + str(i) + '.csv')
        for i, interval in enumerate(sbpIntervals):
            interval.to_csv('Data/Case' + str(case) + '/Track2_split/interval' + str(i) + '.csv')
        for i, interval in enumerate(dbpIntervals):
            interval.to_csv('Data/Case' + str(case) + '/Track4_split/interval' + str(i) + '.csv')
