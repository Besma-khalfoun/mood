kw="Run"
f=$1
workdir=$2
key=$3
csv=$4

line=$(grep "$kw" $f) 
IFS=': '; read -r -a array <<< "$line"

startID="${array[1]}"


for out in $workdir/run-$startID*
do
	#echo "$out"
	runFile="$out"
done 


#jq -r ".report.artifacts  | .[] | select(.name==\"$key\") | .value | to_entries[] | [.key, .value] | @csv" $run > tmp.csv
#jq -r ".report.artifacts  | .[] | select(.name==\"$key\") | .value | .uri" $runFile

#jq -r ".report.duration" $runFile >> $csv
jq -r ".report.artifacts  | .[] | select(.name==\"$key\") | .value | to_entries[] | [.key, .value] | @csv" $runFile >> $csv


#for index in "${!array[@]}"
#do
#    echo "$index ${array[index]}"
#done 
#pour recuperer le chemin des donnee protegée 
# bash "$sc/"getCsv.sh $log ./accio "MatMatchingKSetsnonObf/matches" "$run_output/outgeoi.csv"
#path_promesse=$(bash getPath.sh $log ./accio "Promesse/data")
