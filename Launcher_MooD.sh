trap 'echo "# $BASH_COMMAND"' DEBUG

# Starting script of MooD

config_file=$(realpath "$1")   # Configuration file
sc=$(realpath "$2")            # Path Directory of all the scripts
td=$(date '+%Y-%m-%d-%H-%M-%S')

outputDir="$3_$td"             # Name of our main directory + current time
outSingleLPPM="$outputDir/SingleLPPM"
outMultiLPPM="$outputDir/MultiLPPM"
outFinegrained="$outputDir/FineGrained"
outData="$outputDir/Data"

# Create the arborescence of MooD

mkdir "$outputDir"
outputDir=$(realpath $outputDir)
mkdir $outSingleLPPM
outSingleLPPM=$(realpath $outSingleLPPM)
mkdir $outMultiLPPM
outMultiLPPM=$(realpath $outMultiLPPM)
mkdir $outFinegrained
outFinegrained=$(realpath $outFinegrained)
mkdir $outData
outData=$(realpath $outData)

for case in $outSingleLPPM $outMultiLPPM $outFinegrained
	do
		mkdir "$case/LPPMs"
		mkdir "$case/Attacks"
		mkdir "$case/Utility"
		mkdir "$case/Results"

	done

# Read from configuration file  #
#################################

dataset=$(jq --raw-output ".datasets|.[]" "$config_file")
echo $dataset
#name=$(jq --raw-output ".nameOutput|.[]" "$config_file")
#echo $name


# Preprocessing stage   #
#########################

bash "$sc/"preprocessing_MooD.sh $dataset $outData $sc 

  ########################################################################################################
# #                                      Single LPPM stage                                               #
# ########################################################################################################
 echo "############################      Single LPPM Search       #######################################"
 echo $outData
 echo $outSingleLPPM
 bash "$sc/"run_workflow_SingleLPPM_MooD.sh "$outData/train-accio" "$outData/test-accio" $outSingleLPPM $sc 

# ########################################################################################################
# #                                    Composition of  LPPMs stage                                       #
# ########################################################################################################

 echo "############################      Multi-LPPM Search       #######################################"
 bash "$sc/"run_workflow_MultiLPPM_MooD.sh $outData $outMultiLPPM $sc
 

###########################################################################################################
#                                       Fine Grained protection stage                                     #
###########################################################################################################
#"$outMultiLPPM/Results/np-by-multiLPPM" à la place du 2 eme arg

bash run_workflow_FineGrained_MooD.sh "$outData/train-accio" "$outMultiLPPM/Results/np-by-multiLPPM" $outFinegrained $sc