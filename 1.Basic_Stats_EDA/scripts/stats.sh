#!/bin/bash
FILE=$1

if [ $# -ne 1 ]
then
echo "Error: Wrong number of arguments. Please input a tweet file"
exit 1
fi

#COUNT: The number of lines in the file
COUNT=`cat $FILE | wc -l` 

if [ $COUNT -lt 10000 ]
then
echo "Error: Input file should have at least 10000 lines"
exit 1

else
echo $COUNT
head -n 1 $FILE

COUNT2=`tail -n 10000 $FILE | grep -i "potus" | wc -l`
COUNT3=`head -n 200 $FILE | tail -n 101 | grep -w "fake" | wc -l`
echo $COUNT2
echo $COUNT3
exit 0

fi

#The first line of the file (i.e., the header row)
#The number of lines in the last 10,000 rows of the file that contain the string “potus” (case-insensitive).
#Of rows 100 – 200 (inclusive), how many of them that contain the word “fake”
