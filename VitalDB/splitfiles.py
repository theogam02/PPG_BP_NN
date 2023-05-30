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
            print('Interval overlap')
            return True
    return False

def splitFiles(case):
    # Read the CSV file 
    ppgData = pd.read_csv('Data/Case' + str(case) + '/track1.csv')
    sbpData = pd.read_csv('Data/Case' + str(case) + '/track4.csv')
    dbpData = pd.read_csv('Data/Case' + str(case) + '/track2.csv')

    ppgGaps = checkGaps(ppgData, 'ppg')
    sbpGaps = checkGaps(sbpData, 'bp')
    dbpGaps = checkGaps(dbpData, 'bp')
    gapsOverall = ppgGaps + sbpGaps + dbpGaps
    print(gapsOverall)

    # Cut off any excess measurements from the tracks
    minLen = min(len(ppgData), len(sbpData), len(dbpData))
    print(minLen)

    # Calculate the number of samples in a 20-second interval
    intervalSamples = int(20 / 0.002)
    bpInterval = int(20/2)

    # Split the data into 20-second intervals
    ppgIntervals = []
    for i in range(0, len(ppgData) - intervalSamples, intervalSamples):
        if not checkIntervalOverlap([ppgData.iloc[i]['Time'], ppgData.iloc[i+intervalSamples]['Time']], gapsOverall): 
            ppgIntervals.append(ppgData[i:i+intervalSamples])
    sbpIntervals = []
    for i in range(0, len(sbpData) - bpInterval, bpInterval):
        if not checkIntervalOverlap([sbpData.iloc[i]['Time'], sbpData.iloc[i+bpInterval]['Time']], gapsOverall): 
            sbpIntervals.append(sbpData[i:i+intervalSamples])
    dbpIntervals = []
    for i in range(0, len(dbpData) - bpInterval, bpInterval):
        if not checkIntervalOverlap([dbpData.iloc[i]['Time'], dbpData.iloc[i+bpInterval]['Time']], gapsOverall): 
            dbpIntervals.append(dbpData[i:i+intervalSamples])

    # Average out the BP values
    for i in range(len(sbpIntervals)):
        tmp = sbpIntervals[i]['Solar8000/ART_SBP'].mean()
        sbpIntervals[i] = pd.DataFrame({'Solar8000/ART_SBP': [tmp]})
    for i in range(len(dbpIntervals)):
        tmp = dbpIntervals[i]['Solar8000/ART_DBP'].mean()
        dbpIntervals[i] = pd.DataFrame({'Solar8000/ART_DBP': [tmp]})

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

splitFiles(2)