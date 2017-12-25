root="./img/*"
counter=0
for file in ${root}
do 
	#echo $temp_file 
	#echo 'origin' $file
	var=`echo $file|sed 's/[ ]/\\\ /g'` 
	#echo $var
	echo mv $var  "./img/"${counter}".png"
	let "counter=$counter+1"
done
#echo $counter
