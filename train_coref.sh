#!/bin/sh
corpus_dir=$1
name=$2
path='./'$name'/'
grouped_document=$path'train/'
modified_document=$path'modified_train/'

ZA_option='off'
ratio=0.9
mode='train'
max_document_size=100000
#recommend 100000 bytes

mkdir $path
mkdir $grouped_document
mkdir $PN_candidates

python3 make_document.py --input_path $corpus_dir --output_path $grouped_document --max_document_size $max_document_size
python3 make_conll.py --input_path $grouped_document --previous_path $grouped_document --modified_path $modified_document --output_path $path --output_file $name --mode $mode --ratio $ratio --ZA $ZA_option
python3 minimize.py --input_path $path --input_file train.$name --output_path $path
python3 minimize.py --input_path $path --input_file dev.$name --output_path $path
python3 get_char_vocab.py --input_path $path --file_name $name
mv ./char_vocab.$name.txt ./$name/char_vocab.$name.txt
python3 filter_embeddings.py word2vec.txt ./$name/train.$name.jsonlines ./$name/dev.$name.jsonlines
mv word2vec.txt.filtered ./$name/word2vec.$name.txt.filtered
python3 cache_elmo.py ./$name/train.$name.jsonlines ./$name/dev.$name.jsonlines
mv elmo_cache.hdf5 ./$name/elmo_cache.$name.hdf5
