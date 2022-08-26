trap 'echo "# $BASH_COMMAND"' DEBUG

#Script to launch the three attacks

# Parameters
urlTrain=$1
urlTest=$2
combi="$3"
workdir="$4" # the absolute path 
sc="$5" #"/home/hacker/projet_mobility/Combi"


cd ..
cd ..
echo $workdir
echo $PWD

which_attack="$workdir/Attack1"

mkdir $which_attack
#cd $which_attack

possibleLog="$which_attack""//log-AP-$combi-XXXXXXXXXXX.txt"



#AP-attack 
cellSize="800.meters"
json_ap="$sc/ap-attack.json"
log_ap=$(mktemp "$possibleLog") 
java -jar "$sc/"accio.jar run -workdir $which_attack -params "urlTrain=$urlTrain urlTest=$urlTest cellSize=$cellSize"  $json_ap >> $log_ap
acc_ap=$(bash "$sc/"getRate.sh "AP-Attack rate" $log_ap)
echo "$acc_ap"
bash "$sc/"getCsv.sh $log_ap $which_attack "MatMatchingKSetsnonObf/matches" "$workdir/"$combi-ap.csv

which_attack="$workdir/Attack2"
mkdir $which_attack
possibleLog1="$which_attack""//log-POI-$combi-XXXXXXXXXXX.txt"

#POI-attack 
json_poi="$sc/poi-attack.json"
log_poi=$(mktemp $possibleLog1) 
java -jar "$sc/"accio.jar run -workdir $which_attack -params "urltrain=$urlTrain urltest=$urlTest"  $json_poi >> $log_poi 
acc_poi=$(bash "$sc/"getRate.sh "POI-Attack rate" $log_poi)
echo "$acc_poi"
bash "$sc/"getCsv.sh $log_poi $which_attack "PoisReidentKSet/matches" "$workdir/"$combi-poi.csv

which_attack="$workdir/Attack3"
mkdir $which_attack
possibleLog2="$which_attack""//log-PIT-$combi-XXXXXXXXXXX.txt"

#PIT-attack
json_pit="$sc/pit-attack.json"
log_pit=$(mktemp $possibleLog2) 
java -jar "$sc/"accio.jar run -workdir $which_attack -params "urltrain=$urlTrain urltest=$urlTest"  $json_pit >> $log_pit
acc_pit=$(bash "$sc/"getRate.sh "PIT-Attack rate" $log_pit)
echo "$acc_pit"
bash "$sc/"getCsv.sh $log_pit $which_attack "MMCReIdentKSet/matches" "$workdir/"$combi-pit.csv

#Saving results
echo "$combi,AP-attack,$acc_ap" >> "$workdir/attacks.csv"  
echo "$combi,POI-attack,$acc_poi" >> "$workdir/attacks.csv"  
echo "$combi,PIT-attack,$acc_pit" >> "$workdir/attacks.csv"  

