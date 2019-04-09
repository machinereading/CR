# Coreference Resolution

## Introduction
* This repository contains "Korean Coreference Resolution model".  
* This model is based on [Kenton Lee's English Coreference Resolution model](https://github.com/kentonl/e2e-coref). And we applied it to Korean Coreference Resolution with referencing [Shin et al](http://semanticweb.kaist.ac.kr/home/images/2/2c/%EC%96%B8%EA%B8%89_%ED%8A%B9%EC%A7%88%EC%9D%84_%EC%9D%B4%EC%9A%A9%ED%95%9C_Bi-LSTM_%EA%B8%B0%EB%B0%98_%ED%95%9C%EA%B5%AD%EC%96%B4_%EC%83%81%ED%98%B8%EC%B0%B8%EC%A1%B0%ED%95%B4%EA%B2%B0_%EC%A2%85%EB%8B%A8%EA%B0%84_%ED%95%99%EC%8A%B5.pdf).


## Getting Started
* Install python3 requirements: `pip3 install -r requirements.txt`
* Build custom kernels by running `setup_all.sh`.
  * There are 3 platform-dependent ways to build custom TensorFlow kernels. Please comment/uncomment the appropriate lines in the script.
* Download `word2vec.txt` and save at here.


## Training Instructions
* `./train_coref.sh` preprocesses data before train.
* Experiment configurations are found in `experiments.conf`
* Choose an experiment. Change paths of data, word embedding and other parameters which you would like.
* Training: `python3 train.py <experiment>`
* Results are stored in the `logs` directory and can be viewed via TensorBoard.
* Evaluation: `python3 evaluate.py <experiment>`

## Pretrained model & ELMo embedding
* `logs` directory have a pretrained model, `MTA02-test`.
  * `MTA02-test` is a pretrained model of crowdsourcing data set.
* If you want to use pretrained `ELMo embedding`, download it in the input directory.


## Others
* The training terminates automatically at 30k steps. The model generally converges at about 25k steps.
* If there are some errors when evaluating the development set, `v4_gold_conll` file may have errors. So, you should change the train, dev. set path of `verify_conll.py` and run it. Then, you may find some errors and fix them. 
  * Most of these kind of errors are caused by `ETRI morphological analysis`.


## References
* [Kenton Lee et al., Higher-order Coreference Resolution with Coarse-to-fine Inference](https://arxiv.org/abs/1804.05392) in NAACL 2018
* [Shin et al., Korean Co-reference Resolution End-to-End Learning using Bi-LSTM with Mention Features](http://semanticweb.kaist.ac.kr/home/images/2/2c/%EC%96%B8%EA%B8%89_%ED%8A%B9%EC%A7%88%EC%9D%84_%EC%9D%B4%EC%9A%A9%ED%95%9C_Bi-LSTM_%EA%B8%B0%EB%B0%98_%ED%95%9C%EA%B5%AD%EC%96%B4_%EC%83%81%ED%98%B8%EC%B0%B8%EC%A1%B0%ED%95%B4%EA%B2%B0_%EC%A2%85%EB%8B%A8%EA%B0%84_%ED%95%99%EC%8A%B5.pdf) in HCLT 2018
  
## Licenses
* `CC BY-NC-SA` [Attribution-NonCommercial-ShareAlike](https://creativecommons.org/licenses/by-nc-sa/2.0/)
* If you want to commercialize this resource, [please contact to us](http://mrlab.kaist.ac.kr/contact)


## Publisher
[Machine Reading Lab](http://mrlab.kaist.ac.kr/) @ KAIST


## Acknowledgement
This work was supported by Institute for Information & communications Technology Promotion(IITP) grant funded by the Korea government(MSIT) (2013-0-00109, WiseKB: Big data based self-evolving knowledge base and reasoning platform)
