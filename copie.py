
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

src = sys.argv[1]
dst = sys.argv[2]
pathfile= sys.argv[3]
dataset= str(sys.argv[4])

if not os.path.exists(dst):
	os.makedirs(dst)

df= pd.read_csv(pathfile,  header=0)
df.sort_values(df.columns[0],ascending=True,inplace=True)


for index,row in df.iterrows():
	filename=str(row[0])
	if dataset.lower() == "geolife":
		if len(filename)==1:
			filename="00"+str(row[0])
		elif len(str(row[0]))==2:
			filename="0"+str(row[0])
	shutil.copy(src+filename+".csv", dst)
