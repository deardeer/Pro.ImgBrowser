rootdir="../../img/img/img"
for index in {0..88}
do
	echo ${rootdir}${index}
	python saveimg.py ${rootdir}${index}
done
