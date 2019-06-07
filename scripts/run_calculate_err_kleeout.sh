rm out
echo "program\t" "allerr\t" "data\t" "ctrl\t" >>out
for i in $(ls)      
do
	echo $i
	err=`find $i -name "*err*" |wc -l`
	data=`find $i -name "*data*" |wc -l`  
	ctrl=`find $i -name "*ctrl*"|wc -l`
        echo "$i\t" "$err\t" "$data\t" "$ctrl\t" >>out	
done

