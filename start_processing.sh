#!/bin/bash

ec2_instances=("ec2-52-91-200-94.compute-1.amazonaws.com" "ec2-44-201-150-11.compute-1.amazonaws.com" "ec2-34-207-194-195.compute-1.amazonaws.com" "ec2-3-89-88-39.compute-1.amazonaws.com" "ec2-54-174-195-183.compute-1.amazonaws.com" "ec2-44-208-34-189.compute-1.amazonaws.com" "ec2-44-203-97-111.compute-1.amazonaws.com" "ec2-3-84-3-154.compute-1.amazonaws.com")

game_files=("1.pgn" "2.pgn" "3.pgn" "4.pgn" "5.pgn" "6.pgn" "7.pgn" "8.pgn")

start_processing() {
	scp -i stockfish.pem get-pip.py ec2-user@$1:~ && \
	scp -i stockfish.pem get_evals_2.py ec2-user@$1:~ && \
	scp -i stockfish.pem $2 ec2-user@$1:~/games.pgn && \
	ssh -i ./stockfish.pem ec2-user@$1 "python3 get-pip.py" && \
	ssh -i ./stockfish.pem ec2-user@$1 "pip3 install python-chess" && \
	ssh -i ./stockfish.pem ec2-user@$1 "sudo yum groupinstall 'Development Tools'" && \
	ssh -i ./stockfish.pem ec2-user@$1 "rm -rf Stockfish" && \
	ssh -i ./stockfish.pem ec2-user@$1 "sudo rm -rf /usr/bin/stockfish" && \
	ssh -i ./stockfish.pem ec2-user@$1 "git clone https://github.com/official-stockfish/Stockfish.git" && \
	ssh -i ./stockfish.pem ec2-user@$1 "cd Stockfish/src && make net && make -j clean build ARCH=x86-64" && \
	ssh -i ./stockfish.pem ec2-user@$1 "sudo ln -s ~/Stockfish/src/stockfish /usr/bin/stockfish" && \
	ssh -i ./stockfish.pem ec2-user@$1 "sudo yum install sqlite" && \
	ssh -i ./stockfish.pem ec2-user@$1 "sudo yum install tmux" && \
	ssh -i ./stockfish.pem ec2-user@$1 "tmux new-session -d -s "evals" python3 get_evals_2.py"
}

for ((idx = 0; idx<${#ec2_instances[*]}; ++idx)); do
	ec2_instance="${ec2_instances[$idx]}"
	game_file="${game_files[$idx]}"
	echo $ec2_instance
	echo $game_file
	start_processing $ec2_instance $game_file
done

