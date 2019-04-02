from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
import json

import tensorflow as tf
import coref_model as cm
import util
import os

os.environ["CUDA_VISIBLE_DEVICES"] = "1"

def predict_coreference(_model, _session, input_filename, output_filename):
  model = _model
  session = _session
  with open(output_filename, "w", encoding='utf-8') as output_file:
    with open(input_filename, 'r', encoding='utf-8') as input_file:
      for example_num, line in enumerate(input_file.readlines()):
        example = json.loads(line)
        tensorized_example = model.tensorize_example(example, is_training=False)
        feed_dict = {i:t for i,t in zip(model.input_tensors, tensorized_example)}
        _, _, _, top_span_starts, top_span_ends, top_antecedents, top_antecedent_scores = session.run(model.predictions, feed_dict=feed_dict)
        predicted_antecedents = model.get_predicted_antecedents(top_antecedents, top_antecedent_scores)
        example["predicted_clusters"], _ = model.get_predicted_clusters(top_span_starts, top_span_ends, predicted_antecedents)
        output_file.write(json.dumps(example))
        output_file.write("\n")
        if example_num % 100 == 0:
          print("Decoded {} examples.".format(example_num + 1))   


if __name__ == "__main__":
  # Input file in .jsonlines format.
  input_filename = sys.argv[2]

  # Predictions will be written to this file in .jsonlines format.
  output_filename = sys.argv[3]
  
  config = util.initialize_from_env()
  model = cm.CorefModel(config)

  session = tf.Session()
  model.restore(session)
#  with tf.Session() as session:
#    model.restore(session)
  predict_coreference(model, session, input_filename, output_filename)
'''
    with open(output_filename, "w", encoding='utf-8') as output_file:
      with open(input_filename, 'r', encoding='utf-8') as input_file:
        for example_num, line in enumerate(input_file.readlines()):
          example = json.loads(line)
          tensorized_example = model.tensorize_example(example, is_training=False)
          feed_dict = {i:t for i,t in zip(model.input_tensors, tensorized_example)}
          _, _, _, top_span_starts, top_span_ends, top_antecedents, top_antecedent_scores = session.run(model.predictions, feed_dict=feed_dict)
          predicted_antecedents = model.get_predicted_antecedents(top_antecedents, top_antecedent_scores)
          example["predicted_clusters"], _ = model.get_predicted_clusters(top_span_starts, top_span_ends, predicted_antecedents)

          output_file.write(json.dumps(example))
          output_file.write("\n")
          if example_num % 100 == 0:
            print("Decoded {} examples.".format(example_num + 1))
'''
