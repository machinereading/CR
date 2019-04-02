#!/bin/sh
path1='./test/181130/test_data/'
path2='./test/181130/grouped_test_data/'
path3='./test/181130/PN_test_data/'
path4='./test/181130/'
path5='./test/181130/result_json/'

file1='train.result181130'
file2='test_result181130'
ZA_option='off'
ratio=1.0
mode='predict'
model='test_MTA02_without_NER'
max_document_size=100000
#recommend 100000 bytes

python3 make_document.py --input_path $path1 --output_path $path2 --max_document_size $max_document_size
python3 make_conll.py --input_path $path2 --previous_path $path2 --modified_path $path3 --output_path $path4 --output_file $file1 --mode $mode --ratio $ratio --ZA $ZA_option
python3 minimize.py --input_path $path4 --input_file $file1 --output_path $path4
python3 predict.py $model $path4$file1.jsonlines $path4$file2
python3 jsonlines_to_json.py --input_path $path3 --output_path $path5 --input_file $path4$file2

