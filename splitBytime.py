import sys
import os
import numpy as np
import math
import itertools
import pandas as pd
import datetime as dt
import ntpath
import concurrent.futures
import psutil
import shutil


#inputs
#inputDirectory = sys.argv[1]
#outputDirectory = sys.argv[2]


	

def splitTraceByFixedSlices(trace):
	#try:

	df = pd.read_csv(trace,names=['lat','lng','timestamp'])
	try:
		df['timestamp']=pd.to_datetime(df['timestamp'], unit='ms')
	except:
		df['timestamp']=pd.to_datetime(df['timestamp'])
	#df['bin'] = df['timestamp']#.apply(lambda x: x)
	#print(df)
	minTime= df['timestamp'].min()
	maxTime= df['timestamp'].max()
	b=(maxTime-minTime)/2
	#df['bin'] = df['timestamp'].apply(lambda x: (x-pd.Timestamp.min).total_seconds() // sliceSize)
	df['bin'] = df['timestamp'].apply(lambda x: ((x-minTime)-b).total_seconds())
	df['c'] = df['bin'].apply(lambda x: 1 if x >= 0 else 0)
	return dict(tuple( df.groupby('c')))#,dict(tuple( df2.groupby('bin')))




def processCsvTraceFile(filename,inputDirectory,train,test):
	trace=os.path.join(inputDirectory, filename)
	#print("trace"+trace)
	name=ntpath.basename(trace).replace('.csv', '')
	name=name.split('-')[0]
	#print("name"+name)
	outDfSet1= splitTraceByFixedSlices(trace)
	#print(trace+" size="+str(len(outDfSet1)))
	for key, value in outDfSet1.items():
	 	#print(str(len(value)))
	 	if key==0:
	 		value.to_csv(os.path.join(train, name+".csv"),index=False,columns=['lat','lng','timestamp'],header=False)
	 	else:
	 		value.to_csv(os.path.join(test, name+".csv"),index=False,columns=['lat','lng','timestamp'],header=False)






#Start of script

NB_PROCESS = psutil.cpu_count(logical=False)

#inputs
inputDirectory = sys.argv[1]
train = sys.argv[2]
test = sys.argv[3]
#sliceSize = int(sys.argv[3]) # in seconds

# mkdir the output directory
if not os.path.exists(train):
	os.makedirs(train)
if not os.path.exists(test):
	os.makedirs(test)


# Create pool of processes
executor = concurrent.futures.ProcessPoolExecutor(NB_PROCESS)

#print("ici")
# For each trace launch the trace processing job
futures = [executor.submit(processCsvTraceFile,filename,inputDirectory,train,test) for filename in os.listdir(inputDirectory) if filename.endswith(".csv")]


# Wait for the processes to finish
concurrent.futures.wait(futures)
