python stage_1.py &
python stage_2.py &
python stage_3.py &

read -n 1
  kill $(pgrep -f 'stage_1.py')
  kill $(pgrep -f 'stage_2.py')
  kill $(pgrep -f 'stage_3.py')
