kw=$1
f=$2
line=$(grep "$kw" $f) 
tab=', ' read -r -a array <<< "$line"
echo "${array[3]}"


# for index in "${!array[@]}"
# do
#     echo "$index ${array[index]}"
# done 

