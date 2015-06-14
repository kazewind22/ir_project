#!/bin/bash
for((i=1;i<=17;i++))
do
	filelist=$(ls ir_project/$i)
	for file in $filelist
	do
		./content ir_project/$i/$file
	done
done