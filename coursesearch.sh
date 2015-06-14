#!/bin/bash
for (( i = 1; i < 18; i++))
do
	t=`expr $i / 10`
	r=`expr $i % 10`
	python src/course.py raw_data/COURSE$t$r.xls raw_data/$t$r
done
python src/course.py raw_data/COURSE0B.xls raw_data/0B
