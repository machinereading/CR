# Coreference Resolution

## Introduction
This repository contains the code for replicating results from

* 
* 
* 

## Getting Started

* Install python3 requirements: `pip3 install -r requirements.txt`
* Build custom kernels by running `setup_all.sh`.
  * There are 3 platform-dependent ways to build custom TensorFlow kernels. Please comment/uncomment the appropriate lines in the script.


## Training Instructions
* `./train_coref.sh` preprocesses data before train.
* Experiment configurations are found in `experiments.conf`
* Choose an experiment. Change paths of data, word embedding and other parameters which you would like.
* Training: `python3 train.py <experiment>`
* Results are stored in the `logs` directory and can be viewed via TensorBoard.
* Evaluation: `python3 evaluate.py <experiment>`


## Other Quirks
* The training terminates automatically at 30k steps. The model generally converges at about 25k steps.
* If there are some errors when evaluating the development set, `v4_gold_conll` file may have errors. So, you should change the train, dev. set path of `verify_conll.py` and run it. Then, you may find some errors and fix them. 
  * Most of these kind of errors are caused by `ETRI` morphological analysis.
