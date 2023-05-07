### What's This?

This project is intended to create a dataset of positions, the best moves in those positions,
and the corresponding evaluations. The proposed moves and evaluations are provided by stockfish.

#### Example Row
```
rnbqkbnr/pppppppp/8/8/8/5N2/PPPPPPPP/RNBQKB1R b KQkq - 1 1|[{"eval": "PovScore(Cp(-17), BLACK)", "move": "g8f6"}, {"eval": "PovScore(Cp(-20), BLACK)", "move": "d7d5"}, {"eval": "PovScore(Cp(-41), BLACK)", "move": "d7d6"}]
```

#### Why?

This dataset of positions and evaluations could be used to train or evaluate new engines working
on different methodologies than stockfish.

### How?

* I took the games from the existing games dataset at https://lczero.org/blog/2018/09/a-standard-dataset/. 
* I used stockfish 15.1 with a search limit of 100000 nodes through the python-chess module and 
wrote the results to local sqlite databases. I sped up the task by parallelizing it across 8 c5.2xlarge  
ec2 hosts.
  * Node limit based on https://www.melonimarco.it/en/2021/03/08/stockfish-and-lc0-test-at-different-number-of-nodes/
  * You can see my script to get the evaluations for different positions in get_evals_2.py.
  * You can see the script I used to orchestrate the ec2 hosts in start_processing.sh.
  * After each host produces its own results in an evaluations.db database, you should merge the
resulting databases with sqlite itself after `scp`-ing them back to your local host?

### What if I just want the results?
You can see the results as a tsv file called evals.txt at https://drive.google.com/drive/folders/1IE24S-01M0nFRbemicvlYHdamXSAi340?usp=sharing

