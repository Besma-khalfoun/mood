
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
import csv

pathDir = sys.argv[1]
c=sys.argv[2]
outputDir = sys.argv[3]
#finegraine=sys.argv[4]

###******** Description *********###
# the script aims to get ids of protected and non protected users and put them in results.
# pathDir : the path directory where  the genereted files of AP, POI, PIT attacks are stored 
# c: to precise the combination ( or single LPPM). ex : H, G, T, HT, ..... 
# outputDir : the path directory for np-$c.csv and p-$c-csv 

if not os.path.exists(outputDir):
	os.makedirs(outputDir)

P=[]   #list of protected users
NP=[]  #list of unprotected users

#combinations=["H","G","T","HT","HG","TH","TG","GH","GT","HGT","HTG","TGH","THG","GHT","GTH"]

def mergeFiles(inputDir,c):
	# Function to merge different files of a given composition of LPPMs.
	# Read files resulting from the considered attacks  , each file contains two columns : the 1 st column = the real ID , the 2 nd column = the predicted ID.
	filename_ap= c+"-ap.csv"
	filename_poi= c+"-poi.csv"
	filename_pit= c+"-pit.csv"
	df1 = pd.read_csv(inputDir+filename_ap,names=['id','id-ap-p'])
	df2 = pd.read_csv(inputDir+filename_poi,names=['id','id-poi-p'])
	df3 = pd.read_csv(inputDir+filename_pit,names=['id','id-pit-p'])
	df1.sort_values('id',ascending=True,inplace=True)
	df2.sort_values('id',ascending=True,inplace=True)
	df3.sort_values('id',ascending=True,inplace=True)
	df2.drop(df2.columns[0],axis=1,inplace=True)
	df3.drop(df3.columns[0],axis=1,inplace=True)
	frames = [df1, df2, df3]
	df = pd.concat(frames, axis=1, sort=False)
	return df



df=mergeFiles(pathDir,c)
for index, row in df.iterrows():
	if str(row['id']).split('_')[0] == str(row['id-ap-p']) or str(row['id']) == str(row['id-poi-p']) or str(row['id']) == str(row['id-pit-p']):
		NP.append(str(row['id']))

	else:
		P.append((str(row['id'])))

NP = list(set(NP))
P = list(set(P))

df_NP = pd.DataFrame({'id':NP})
df_NP.sort_values(df_NP.columns[0],ascending=True,inplace=True)
df_NP.to_csv(outputDir+"/np-"+c+".csv",index=False)

df_P = pd.DataFrame({'id':P})
df_P.sort_values(df_P.columns[0],ascending=True,inplace=True)
df_P.to_csv(outputDir+"/p-"+c+".csv",index=False)
