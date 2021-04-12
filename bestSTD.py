
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
# pathDir : the path directory where  the genereted files with ID and STD of protected users are stored 
# type_protection: "single" if we apply a single LPPM (ex: H, G, T) or "multi" if we apply multiple LPPM as a composition (ex: HT, GTH, ..)
# outputDir : the path directory for the resulting csv file , which contains ['id','LPPM','STD'] 

# This function look for a value (an ID for example) in the column col from df , if exists return its corresponding STD 
def getSTD(df,value,ncol):
	for index,row in df.iterrows():
		if str(int(row[ncol]))==str(value):  #modif
			return row[ncol+1]
		else:
			continue
	return 9999999

if type_protection.lower() == "single":
	filename_H= "STD-H-protected.csv"
	filename_G= "STD-G-protected.csv"
	filename_T= "STD-T-protected.csv"
	df1 = pd.read_csv(pathDir+filename_H,names=['id','STD H'])
	df2 = pd.read_csv(pathDir+filename_G,names=['id','STD G'])
	df3 = pd.read_csv(pathDir+filename_T,names=['id','STD T'])
	list_protectedUsers= df2["id"].tolist()+ df3["id"].tolist()+df1["id"].tolist()
	list_protectedUsers=list(set(list_protectedUsers))          # to discard the redundancy 
	df_singleLPPM = pd.DataFrame(columns=['id', 'LPPM', 'STD'])
	for l in list_protectedUsers:
		v_H=getSTD(df1,l,0)
		v_G=getSTD(df2,l,0)
		v_T=getSTD(df3,l,0)
		if v_G == -1 and v_T ==-1 and v_H != -1:
			df_singleLPPM=df_singleLPPM.append({'id' : l , 'LPPM' : 'H', 'STD': v_H} , ignore_index=True)
		if v_G == -1 and v_H ==-1 and v_T != -1:
			df_singleLPPM=df_singleLPPM.append({'id' : l , 'LPPM' : 'T', 'STD': v_T} , ignore_index=True)
		if v_T == -1 and v_H ==-1 and v_G != -1:
			df_singleLPPM=df_singleLPPM.append({'id' : l , 'LPPM' : 'G', 'STD': v_G} , ignore_index=True)
		
		if v_G == -1 and v_T != -1 and v_H != -1:
			if min(v_T,v_H)==v_T:
				df_singleLPPM=df_singleLPPM.append({'id' : l , 'LPPM' : 'T', 'STD': v_T} , ignore_index=True)
			else:
				df_singleLPPM=df_singleLPPM.append({'id' : l , 'LPPM' : 'H', 'STD': v_H} , ignore_index=True)
		if v_T == -1 and v_G != -1 and v_H != -1:
			if min(v_G,v_H)==v_G:
				df_singleLPPM=df_singleLPPM.append({'id' : l , 'LPPM' : 'G', 'STD': v_G} , ignore_index=True)
			else:
				df_singleLPPM=df_singleLPPM.append({'id' : l , 'LPPM' : 'H', 'STD': v_H} , ignore_index=True)
		if v_H == -1 and v_T != -1 and v_G != -1:
			if min(v_T,v_G)==v_T:
				df_singleLPPM=df_singleLPPM.append({'id' : l , 'LPPM' : 'T', 'STD': v_T} , ignore_index=True)
			else:
				df_singleLPPM=df_singleLPPM.append({'id' : l , 'LPPM' : 'G', 'STD': v_G} , ignore_index=True)
		
		if v_H != -1 and v_T != -1 and v_G != -1:
			if min(v_T,v_H,v_G)==v_T:
				df_singleLPPM=df_singleLPPM.append({'id' : l , 'LPPM' : 'T', 'STD': v_T} , ignore_index=True)
			elif min(v_T,v_H,v_G)==v_H:
				df_singleLPPM=df_singleLPPM.append({'id' : l , 'LPPM' : 'H', 'STD': v_H} , ignore_index=True)
			else:
				df_singleLPPM=df_singleLPPM.append({'id' : l , 'LPPM' : 'G', 'STD': v_G} , ignore_index=True)
	df_singleLPPM.to_csv(outputDir+"/result-single-user-centric-LPPM.csv",index=False)
if type_protection.lower() == "multi":


	filename_HT= "STD-HT-protected.csv"
	filename_HG= "STD-HG-protected.csv"
	filename_GT= "STD-GT-protected.csv"
	filename_GH= "STD-GH-protected.csv"
	filename_TH= "STD-TH-protected.csv"
	filename_TG= "STD-TG-protected.csv"
	filename_THG= "STD-THG-protected.csv"
	filename_TGH= "STD-TGH-protected.csv"
	filename_GTH= "STD-GTH-protected.csv"
	filename_GHT= "STD-GHT-protected.csv"
	filename_HGT= "STD-HGT-protected.csv"
	filename_HTG= "STD-HTG-protected.csv"

	df1 = pd.read_csv(pathDir+filename_HT,names=['id','STD HT'])
	df2 = pd.read_csv(pathDir+filename_HG,names=['id','STD HG'])
	df3 = pd.read_csv(pathDir+filename_GT,names=['id','STD GT'])
	df4 = pd.read_csv(pathDir+filename_GH,names=['id','STD GH'])
	df5 = pd.read_csv(pathDir+filename_TH,names=['id','STD TH'])
	df6 = pd.read_csv(pathDir+filename_TG,names=['id','STD TG'])
	df7 = pd.read_csv(pathDir+filename_THG,names=['id','STD THG'])
	df8 = pd.read_csv(pathDir+filename_TGH,names=['id','STD TGH'])
	df9 = pd.read_csv(pathDir+filename_GTH,names=['id','STD GTH'])
	df10 = pd.read_csv(pathDir+filename_GHT,names=['id','STD GHT'])
	df11 = pd.read_csv(pathDir+filename_HGT,names=['id','STD HGT'])
	df12 = pd.read_csv(pathDir+filename_HTG,names=['id','STD HTG'])

	list_protectedUsers= df2["id"].tolist()+ df3["id"].tolist()+df1["id"].tolist()+df4["id"].tolist()+df5["id"].tolist()+df6["id"].tolist()+df7["id"].tolist()+df8["id"].tolist()+df9["id"].tolist()+df10["id"].tolist()+df11["id"].tolist()+df12["id"].tolist()
	list_protectedUsers=list(set(list_protectedUsers))          # to discard the redundancy 
	df_multiLPPM = pd.DataFrame(columns=['id', 'LPPM', 'STD'])
	for l in list_protectedUsers:
		v_HT=getSTD(df1,l,0)
		v_HG=getSTD(df2,l,0)
		v_GT=getSTD(df3,l,0)
		v_GH=getSTD(df4,l,0)
		v_TH=getSTD(df5,l,0)
		v_TG=getSTD(df6,l,0)
		v_THG=getSTD(df7,l,0)
		v_TGH=getSTD(df8,l,0)
		v_GTH=getSTD(df9,l,0)
		v_GHT=getSTD(df10,l,0)
		v_HGT=getSTD(df11,l,0)
		v_HTG=getSTD(df12,l,0)
		
		if min(	v_HT,v_HG,v_GT,v_GH,v_TH,v_TG,v_THG,v_TGH,v_GTH,v_GHT,v_HGT,v_HTG)== v_HT:
			df_multiLPPM=df_multiLPPM.append({'id' : l , 'LPPM' : 'HT', 'STD': v_HT} , ignore_index=True)

		if min(	v_HT,v_HG,v_GT,v_GH,v_TH,v_TG,v_THG,v_TGH,v_GTH,v_GHT,v_HGT,v_HTG)== v_HG:
			df_multiLPPM=df_multiLPPM.append({'id' : l , 'LPPM' : 'HG', 'STD': v_HG} , ignore_index=True)

		if min(	v_HT,v_HG,v_GT,v_GH,v_TH,v_TG,v_THG,v_TGH,v_GTH,v_GHT,v_HGT,v_HTG)== v_GT:
			df_multiLPPM=df_multiLPPM.append({'id' : l , 'LPPM' : 'GT', 'STD': v_GT} , ignore_index=True)

		if min(	v_HT,v_HG,v_GT,v_GH,v_TH,v_TG,v_THG,v_TGH,v_GTH,v_GHT,v_HGT,v_HTG)== v_GH:
			df_multiLPPM=df_multiLPPM.append({'id' : l , 'LPPM' : 'GH', 'STD': v_GH} , ignore_index=True)

		if min(	v_HT,v_HG,v_GT,v_GH,v_TH,v_TG,v_THG,v_TGH,v_GTH,v_GHT,v_HGT,v_HTG)== v_TH:
			df_multiLPPM=df_multiLPPM.append({'id' : l , 'LPPM' : 'TH', 'STD': v_TH} , ignore_index=True)

		if min(	v_HT,v_HG,v_GT,v_GH,v_TH,v_TG,v_THG,v_TGH,v_GTH,v_GHT,v_HGT,v_HTG)== v_TG:
			df_multiLPPM=df_multiLPPM.append({'id' : l , 'LPPM' : 'TG', 'STD': v_TG} , ignore_index=True)

		if min(	v_HT,v_HG,v_GT,v_GH,v_TH,v_TG,v_THG,v_TGH,v_GTH,v_GHT,v_HGT,v_HTG)== v_THG:
			df_multiLPPM=df_multiLPPM.append({'id' : l , 'LPPM' : 'THG', 'STD': v_THG} , ignore_index=True)

		if min(	v_HT,v_HG,v_GT,v_GH,v_TH,v_TG,v_THG,v_TGH,v_GTH,v_GHT,v_HGT,v_HTG)== v_TGH:
			df_multiLPPM=df_multiLPPM.append({'id' : l , 'LPPM' : 'TGH', 'STD': v_TGH} , ignore_index=True)

		if min(	v_HT,v_HG,v_GT,v_GH,v_TH,v_TG,v_THG,v_TGH,v_GTH,v_GHT,v_HGT,v_HTG)== v_GTH:
			df_multiLPPM=df_multiLPPM.append({'id' : l , 'LPPM' : 'GTH', 'STD': v_GTH} , ignore_index=True)

		if min(	v_HT,v_HG,v_GT,v_GH,v_TH,v_TG,v_THG,v_TGH,v_GTH,v_GHT,v_HGT,v_HTG)== v_GHT:
			df_multiLPPM=df_multiLPPM.append({'id' : l , 'LPPM' : 'GHT', 'STD': v_GHT} , ignore_index=True)

		if min(	v_HT,v_HG,v_GT,v_GH,v_TH,v_TG,v_THG,v_TGH,v_GTH,v_GHT,v_HGT,v_HTG)== v_HGT:
			df_multiLPPM=df_multiLPPM.append({'id' : l , 'LPPM' : 'HGT', 'STD': v_HGT} , ignore_index=True)

		if min(	v_HT,v_HG,v_GT,v_GH,v_TH,v_TG,v_THG,v_TGH,v_GTH,v_GHT,v_HGT,v_HTG)== v_HTG:
			df_multiLPPM=df_multiLPPM.append({'id' : l , 'LPPM' : 'HTG', 'STD': v_HTG} , ignore_index=True)
	df_multiLPPM.to_csv(outputDir+"/result-multi-LPPM.csv",index=False)