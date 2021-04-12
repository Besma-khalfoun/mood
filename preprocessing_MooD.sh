dataset=$1 # The Directory path of mobility dataset 
workdir=$2 #  Main working directory
sc=$3     

###******************* DATA PROCESS *********************###
############################################################

#Split data chronologically into Train/Test data:  
python3 "$sc/"splitBytime.py $dataset "$workdir/train" "$workdir/test"

Train="$workdir/train"
Test="$workdir/test"

## -DATA preparation For Accio Tool ##
######################################

python3 "$sc/"prepareTraceForAccio1.py $Train "$workdir/train-accio" 
python3 "$sc/"prepareTraceForAccio1.py $Test "$workdir/test-accio" 


