#!/bin/bash

ec2_instances=("ec2-52-91-200-94.compute-1.amazonaws.com" "ec2-44-201-150-11.compute-1.amazonaws.com" "ec2-34-207-194-195.compute-1.amazonaws.com" "ec2-3-89-88-39.compute-1.amazonaws.com" "ec2-54-174-195-183.compute-1.amazonaws.com" "ec2-44-208-34-189.compute-1.amazonaws.com" "ec2-44-203-97-111.compute-1.amazonaws.com" "ec2-3-84-3-154.compute-1.amazonaws.com")

for ((idx = 0; idx<${#ec2_instances[*]}; ++idx)); do
	ec2_instance="${ec2_instances[$idx]}"
	echo $ec2_instance $idx
	scp -i stockfish.pem ec2-user@$ec2_instance:~/evaluations.db ./evaluations_$idx.db
	sqlite3 evaluations_$idx.db .dump > dump_$idx.sql
	sqlite3 all_evaluations.db < dump_$idx.sql
done



