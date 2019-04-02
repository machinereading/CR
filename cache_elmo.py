from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
import h5py
import json
import sys
import os


def build_elmo():
  print("function build_elmo")
  token_ph = tf.placeholder(tf.string, [None, None])
  len_ph = tf.placeholder(tf.int32, [None])
  print("before module")
  elmo_module = hub.Module("https://tfhub.dev/google/elmo/2")
  print("after module")
  lm_embeddings = elmo_module(
      inputs={"tokens": token_ph, "sequence_len": len_ph},
      signature="tokens", as_dict=True)
  word_emb = lm_embeddings["word_emb"]
  lm_emb = tf.stack([tf.concat([word_emb, word_emb], -1),
                     lm_embeddings["lstm_outputs1"],
                     lm_embeddings["lstm_outputs2"]], -1)
  return token_ph, len_ph, lm_emb

def cache_dataset(data_path, session, token_ph, len_ph, lm_emb, out_file):
  with open(data_path) as in_file:
    for doc_num, line in enumerate(in_file.readlines()):
      example = json.loads(line)
      sentences = example["sentences"]
      max_sentence_length = max(len(s) for s in sentences)
      tokens = [[""] * max_sentence_length for _ in sentences]
      text_len = np.array([len(s) for s in sentences])

      for i, sentence in enumerate(sentences):
        for j, word in enumerate(sentence):
          if word.find("/") == -1:
              print(word)
          temp_word = word
          #print(temp_word, word)
          tokens[i][j] = temp_word
      tokens = np.array(tokens)
      #batch_size = 10
      size = 20
      base = 0
#print(text_len.size)
#for j in range(int(text_len.size/20)):
      tf_lm_emb = session.run(lm_emb, feed_dict={token_ph: tokens, len_ph: text_len})
      base += size
      file_key = example["doc_key"].replace("/", ":")
      #print(file_key)
      group = out_file.create_group(file_key)
      for i, (e, l) in enumerate(zip(tf_lm_emb, text_len)):
        e = e[:l, :, :]
        group[str(i)] = e
      if doc_num % 10 == 0:
        print("Cached {} documents in {}".format(doc_num + 1, data_path))

if __name__ == "__main__":
  token_ph, len_ph, lm_emb = build_elmo()
  print("elmo downloading")
  os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
  #tf_config = tf.ConfigProto(device_count = {'GPU': 0})
  gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.9)

  with tf.Session(config=tf.ConfigProto(gpu_options=gpu_options)) as session:
#with tf.Session() as session:
    session.run(tf.global_variables_initializer())
    with h5py.File("elmo_cache.hdf5", "a") as out_file:
      for json_filename in sys.argv[1:]:
        cache_dataset(json_filename, session, token_ph, len_ph, lm_emb, out_file)
        print ('done', json_filename)
