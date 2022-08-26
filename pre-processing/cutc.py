#cut First id column
import csv
import pywraps2 as s2
import sys
import os
import numpy as np
import math
import itertools
import pandas as pd
import functools
import operator
import ntpath
import concurrent.futures
import psutil
import gc
import time


inputDirectory = sys.argv[1]
outputDirectory = sys.argv[2]

# mkdir the output directory
if not os.path.exists(outputDirectory):
	os.makedirs(outputDirectory)

for filename in os.listdir(inputDirectory):
	if filename.endswith(".csv"):
		df = pd.read_csv(inputDirectory+filename, names=['id','lat','lng','timestamp'],encoding ='iso-8859-1')
		df.drop(df.columns[0],axis=1,inplace=True)
		df.to_csv(outputDirectory+filename,index=False,header=False)

