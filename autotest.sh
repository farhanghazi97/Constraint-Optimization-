#!/bin/sh
RCol='[0m'    # Text Reset
On_Red='[41m';
On_Gre='[42m';

passcounter=0
failcounter=0
totalcounter=0

for f in `find -L tests -name *.in`
do
    f=`echo $f | sed -E 's/tests\/(.+).in/\1/'`
    python3 cspOptimizer.py  "tests/$f.in" > "tests/$f.out"

    echo "Test \"$f\""

    cspresult=`tail -n 1 tests/$f.out`
    cspexpect=`tail -n 1 tests/$f.exp`

    if [ "$cspresult" == "$cspexpect" ]; then
    	passcounter=$((passcounter+1))
    else
    	echo ""
    	echo "expected:"
    	echo "< $cspexpect"
    	echo ""
    	echo "got:"
    	echo "> $cspresult"
    	echo ""
    	failcounter=$((failcounter+1))
    fi
    totalcounter=$((totalcounter+1))
done

if [ $failcounter == "0" ]; then
	echo " "
	echo "${On_Gre}          All tests passed!          ${RCol}"
else
	if [ $failcounter == "1" ]; then
		echo " "
		echo "${On_Red}             ${failcounter} failure               ${RCol}"
	else
		echo " "
		echo "${On_Red}             ${failcounter} failures              ${RCol}"
	fi
fi

echo "---"
echo "Completed: $totalcounter, Passed: $passcounter, Failed: $failcounter"
echo " "

unset passcounter
unset failcounter
unset totalcounter
