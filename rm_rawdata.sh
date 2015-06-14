#!/bin/bash
for (( i = 1; i < 18; i++))
do
	t=`expr $i / 10`
	r=`expr $i % 10`
	rm -f raw_data/$t$r/* 
done
rm -f raw_data/0B/*
