trap 'echo "# $BASH_COMMAND"' DEBUG

traindir="$1"
testdir="$2"
workdir="$3"
sc="$4"




# Split mobility traces 24h #
#############################

subtraces="$workdir/splitdata"
mkdir $subtraces
#urlSubTestnobf="$workdir/../MultiLPPM/Results/np-by-multiLPPM"

echo $testdir
echo "$subtraces"
python3 "$sc/"splitTracesByFixedSlices_functional.py "$testdir/" "$subtraces" 86400
python3 "$sc/"prepareTraceForAccio.py "$subtraces/" "$subtraces-accio"


# Single LPPM workflow    #
###########################

#bash "$sc/"run_workflow_SingleLPPM_MooD.sh "$traindir" "$subtraces-accio" $workdir $sc
for lppm in "H" "G" "T"
do
echo "********** $lppm ***********"
bash "$sc/"run_exp.sh "$traindir" "$subtraces-accio" $lppm "$workdir/LPPMs" "$workdir/Attacks" "$workdir/Results" "$workdir/Utility"  $sc "$subtraces-accio"
done
python3 "$sc/"bestSTD.py "$workdir/Utility/" "single" "$workdir/Results/"
python3 "$sc/"prepareListNP.py "$workdir/Results/" "single" "$workdir/Results/"
pathDirFGS="$workdir/Results/np-by-singleFineGrained/" 					
npFile="$workdir/Results/np-singleLPPM.csv"
python3 "$sc/"copie.py "$subtraces-accio/" $pathDirFGS $npFile "mdc"    


# Multi LPPM workflow    #
##########################
for lppm in  "HT" "HG" "TH" "TG" "GH" "GT" "HGT" "HTG" "TGH" "THG" "GHT" "GTH" 
do
echo "********** $lppm ***********"
bash "$sc/"run_exp.sh "$traindir" "$pathDirFGS/" $lppm "$workdir/LPPMs" "$workdir/Attacks" "$workdir/Results" "$workdir/Utility"  $sc "$subtraces-accio"
done
python3 "$sc/"bestSTD.py "$workdir/Utility/" "multi" "$workdir/Results/"
python3 "$sc/"prepareListNP.py "$workdir/Results/" "multi" "$workdir/Results/"

pathDirFGM="$workdir/Results/np-by-multiFineGrained/" 					
npFile="$workdir/Results/np-multiLPPM.csv"
python3 "$sc/"copie.py "$subtraces-accio/" $pathDirFGM $npFile "mdc"    #modif


