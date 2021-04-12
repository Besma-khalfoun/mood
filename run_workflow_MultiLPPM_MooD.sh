trap 'echo "# $BASH_COMMAND"' DEBUG


datadir="$1"
workdir="$2"
sc="$3"

###************************ Multi LPPMs ************************###
###################################################################


# 1- Run the composition of LPPMs , related attacks and STD metric ( for protected users).



for lppm in   "HGT" "HTG" "TGH" "THG" "GHT" "GTH" "HT" "HG" "TH" "TG" "GH" "GT"
do
echo "********** $lppm ***********"
bash "$sc/"run_exp.sh "$datadir/train-accio" "$workdir/../SingleLPPM/Results/np-by-singleLPPM" $lppm "$workdir/LPPMs" "$workdir/Attacks" "$workdir/Results" "$workdir/Utility"  $sc "$datadir/test-accio"
done


###******************** Extraction of users***********************###
#####################################################################

# 1- Protected users with best utility metric
python3 "$sc/"bestSTD.py "$workdir/Utility/" "multi" "$workdir/Results/"


# 2- Non protected users by multi LPPMs ( i.e. re-identified users). 

python3 "$sc/"prepareListNP.py "$workdir/Results/" "multi" "$workdir/Results/"


urlTestnobf="$workdir/../Data/test-accio"
pathDirMulti="$workdir/Results/np-by-multiLPPM/" 					
npFile="$workdir/Results/np-multiLPPM.csv"
python3 "$sc/"copie.py $urlTestnobf"/" $pathDirMulti $npFile "mdc"    #modif