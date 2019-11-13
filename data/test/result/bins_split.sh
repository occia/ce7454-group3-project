
#ls *.jpg | while read jpg
#do
#	echo "$jpg " `echo $jpg  | awk -F_ '{printf("%s",$1)}'`
#done > utkface.txt


ls *.jpg | while read jpg
do
	age=`echo $jpg  | awk -F_ '{printf("%02d",$1)}'`
	mkdir -p "$age"
	mv "$jpg" "$age"
done 
