
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
type_protection=str(sys.argv[2]) 
outputDir= sys.argv[3]

###******** Description of parameters *********###
# pathDir : the path directory where  the genereted files np-$lppm.csv are stored
# type_protection: "single" if we apply a single LPPM (ex: H, G, T) or "multi" if we apply multiple LPPM as a composition (ex: HT, GTH, ..)
# outputDir : the path directory for the resulting csv file , which contains IDs


single=["G","T" ,"H"]
combi=[ "HGT" ,"HTG" ,"TGH" ,"THG", "GHT", "GTH", "HT", "HG", "TH", "TG", "GH", "GT"]

if type_protection.lower() == "single":
	filename_H= "np-H.csv"
	df1 = pd.read_csv(pathDir+filename_H,names=['id'])
	list_NPusers= list(df1["id"])
	for s in single: 
		f = "np-"+str(s)+".csv"
		df=pd.read_csv(pathDir+f,names=['id'])
		list_NPusers= list(set(list(df["id"])) & set(list_NPusers))
	list_NPusers.remove("id")
	df_NPsingleLPPM = pd.DataFrame(columns=['id'])
	df_NPsingleLPPM['id'] = list_NPusers
	df_NPsingleLPPM.to_csv(outputDir+"/np-singleLPPM.csv",index=False)

if type_protection.lower() == "multi":
	filename_HT= "np-HT.csv"
	df1 = pd.read_csv(pathDir+filename_HT,names=['id'])
	list_NPusers = list(df1["id"])
	for c in combi: 
		f = "np-"+str(c)+".csv"
		df=pd.read_csv(pathDir+f,names=['id'])
		list_NPusers= list(set(list(df["id"])) & set(list_NPusers))
	list_NPusers.remove("id")
	df_NPcombiLPPM = pd.DataFrame(columns=['id'])
	df_NPcombiLPPM['id'] = list_NPusers
	df_NPcombiLPPM.to_csv(outputDir+"/np-multiLPPM.csv",index=False)