trap 'echo "# $BASH_COMMAND"' DEBUG

###*************** INPUT DATA *********************###
########################################################

urlTrain=$1
urlTest=$2
which_combi="$3"
workdir="$4"        #absolute path
echo $workdir
workdirattacks="$5"  #absolute path
echo $workdirattacks
workdirresults="$6" #absolute path
workdirutility="$7"
sc="$8"             #absolute path    #"/home/hacker/projet_mobility/Combi"
urlTestnobf="$9"
sc_oldHMC="/home/hacker/projet_mobility/LPPMs/LPPM-HMC/dist"
combi=$which_combi
cellSize="800.meters" # parameter for HMC cell size

combidir="$workdir/$which_combi"

mkdir $combidir
cd $combidir
echo "combidiiiiiiiiiir :$combidir"
t=${which_combi:0:1}

###*************** 1- Run LPPMs / composition of LPPMs *********************###
###############################################################################

for (( i=0; i<${#combi}; i++ )); do
  echo "${combi:$i:1}"

  	if [ "${combi:$i:1}" == "G" ]
	then
        echo "#LPPM $i # G"
		subworkdir="G"
		subworkdir=$(realpath $subworkdir)
		mkdir "$subworkdir"
		cd $subworkdir
		json="$sc/geoi.json"
		urlTest=$urlTest
		possibleLog="$PWD""//log-$which_combi-G-XXXXXXXXXXXXX.txt"
		echo $possibleLog
		echo $PWD
		log=$(mktemp "$possibleLog") 
		java -jar "$sc/"accio.jar run -workdir $subworkdir -params "url=$urlTest"  $json >> $log
		path_geoi=$(bash "$sc/"getPath.sh $log $subworkdir "GeoIndistinguishability/data")
		echo "$path_geoi"
		urlTest=$path_geoi
		cd .. 
    else
    	if [ "${combi:$i:1}" == "H" ]
    	then
    		echo "#LPPM $i # H"
    		subworkdir="H"
    		subworkdir=$(realpath $subworkdir)
			mkdir "$subworkdir"
			cd $subworkdir
			mkdir "data"
			json="$sc/hmc.json"
			urlTest=$urlTest
			urlTrain=$urlTrain
			possibleLog="$PWD""//log-$which_combi-H-XXXXXXXXXXXXX.txt"
			log=$(mktemp $possibleLog) 
			java -jar "$sc/"accio.jar run -workdir $subworkdir -params "urltrain=$urlTrain urltest=$urlTest cellSize=$cellSize"  $json >> $log
			path_H=$(bash "$sc/"getPath.sh $log $subworkdir "HeatMapConfusion/out")    #HMConfusion/out for old HMC
			echo "$path_H"
			urlTest=$path_H
			echo $urlTest
			cd .. 

    	else
    		echo "#LPPM $i # T"
    		subworkdir="T" #"$combidir/T"
    		subworkdir=$(realpath $subworkdir)
    		echo $subworkdir
			mkdir "$subworkdir"
			cd $subworkdir
			echo $urlTest
			python3 "$sc/"cutc.py $urlTest"/" "data-withoutID/"
			pathTest="data-withoutID/"
			pathTRL="T"
			mkdir "$pathTRL"
			java -jar "$sc/"trilaterationv3.jar "$pathTest/" $pathTRL"/" 0.6 1	
			python3 "$sc/"prepareTraceForAccio2.py $pathTRL "T-accio"
			urlTest="$subworkdir/T-accio"
			cd ..
    	fi
    fi	
done


###*************** 2- Run attacks : POI , PIT and AP attack ******************###
#################################################################################
echo $workdirattacks

echo $PWD
echo $urlTest
echo $urlTrain
echo $which_combi

bash "$sc/"run_attacks.sh $urlTrain $urlTest $which_combi  "$workdirattacks" $sc  

###*********** 3- GET PROTECTED AND NON-PROTECTED USERS "ID" ******************###
##################################################################################

python3 "$sc/"get_NP_P_usersPerCombi.py "$workdirattacks/" $which_combi "$workdirresults/"

# protected and non-protected files contain IDs of users.
protectedFile="$workdirresults/p-$which_combi.csv" 
protectedDir="$workdirresults/protected-by-$which_combi/"
python3 "$sc/"copie.py $urlTest"/" "$protectedDir/" $protectedFile "mdc"    


###***********4- EVALUATION OF PROTECTED USERS : STD metric************###
########################################################################

json="$sc/spatialTemporalDistortion.json"
possibleLog="$workdirutility""//log-STD-$which_combi-XXXXXXXXXXX.txt"  #modif
log=$(mktemp $possibleLog) 


java -jar "$sc/"accio.jar run -workdir $workdirutility -params "urltrain=$urlTestnobf urltest=$protectedDir"  $json >> $log
bash "$sc/"getCsv.sh $log $workdirutility "SpatioTemporalDistortiongeoi/avg" "$workdirutility/STD-$which_combi-protected.csv"
