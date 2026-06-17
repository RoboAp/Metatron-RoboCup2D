#!/bin/sh

export PYTHONPATH="${PYTHONPATH}:`pwd`"

TEAM_NAME="treino"
trap 'echo -e; pkill -f main_treino.py; exit 0' INT
i=1
while [ $i -le 11 ] ; do
    python3 main_treino.py -t $TEAM_NAME &
    sleep 0.5
    i=`expr $i + 1`
done


