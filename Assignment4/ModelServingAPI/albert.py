# -*- coding: utf-8 -*-
"""ALBERT

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/18mmiol1c1YE4VnlIrwqJNivHOqDYwpHI
"""

# try:
#     import colab
#     !pip install --upgrade pip
# except:
#     pass

!pip install -q tfx==0.25.0
!pip install -q tensorflow-text  # The tf-text version needs to match the tf version

print("Restart your runtime enable after installing the packages")

# Commented out IPython magic to ensure Python compatibility.
import glob
import os
import pprint
import re
import tempfile
from shutil import rmtree
from typing import List, Dict, Tuple, Union

import numpy as np
import pandas as pd
import tensorflow as tf
import tensorflow_data_validation as tfdv
import tensorflow_hub as hub
import tensorflow_model_analysis as tfma
import tensorflow_transform as tft
import tensorflow_transform.beam as tft_beam
from tensorflow_transform.beam.tft_beam_io import transform_fn_io
from tensorflow_transform.saved import saved_transform_io
from tensorflow_transform.tf_metadata import (dataset_metadata, dataset_schema,
                                              metadata_io, schema_utils)
from tfx.components import (Evaluator, ExampleValidator, ImportExampleGen,
                            ModelValidator, Pusher, ResolverNode, SchemaGen,
                            StatisticsGen, Trainer, Transform)
from tfx.components.base import executor_spec
from tfx.components.trainer.executor import GenericExecutor
from tfx.dsl.experimental import latest_blessed_model_resolver
from tfx.proto import evaluator_pb2, example_gen_pb2, pusher_pb2, trainer_pb2
from tfx.types import Channel
from tfx.types.standard_artifacts import Model, ModelBlessing
from tfx.utils.dsl_utils import external_input

import tensorflow_datasets as tfds
import tensorflow_model_analysis as tfma
import tensorflow_text as text

from tfx.orchestration.experimental.interactive.interactive_context import \
    InteractiveContext

# %load_ext tfx.orchestration.experimental.interactive.notebook_extensions.skip

num_gpus_available = len(tf.config.experimental.list_physical_devices('GPU'))
print("Num GPUs Available: ", num_gpus_available)
assert num_gpus_available > 0

!mkdir /content/tfds/

def clean_before_download(base_data_dir):
    rmtree(base_data_dir)
    

def delete_unnecessary_files(base_path):
    counter = 0
    file_list = ["dataset_info.json", "label.labels.txt", "feature.json"]

    for f in file_list:
        try:
            os.remove(os.path.join(base_path, f))
            counter += 1
        except OSError:
            pass

    for f in glob.glob(base_path + "imdb_reviews-unsupervised.*"):
        os.remove(f)
        counter += 1
    print(f"Deleted {counter} files")


def get_dataset(name='imdb_reviews', version="1.0.0"):

    base_data_dir = "/content/tfds/"
    config="plain_text"
    version="1.0.0"

    clean_before_download(base_data_dir)
    tfds.disable_progress_bar()
    builder = tfds.text.IMDBReviews(data_dir=base_data_dir, 
                                    config=config, 
                                    version=version)
    download_config = tfds.download.DownloadConfig(
        download_mode=tfds.GenerateMode.FORCE_REDOWNLOAD)
    builder.download_and_prepare(download_config=download_config)

    base_tfrecords_filename = os.path.join(base_data_dir, "imdb_reviews", config, version, "")
    train_tfrecords_filename = base_tfrecords_filename + "imdb_reviews-train*"
    test_tfrecords_filename = base_tfrecords_filename + "imdb_reviews-test*"
    label_filename = os.path.join(base_tfrecords_filename, "label.labels.txt")
    labels = [label.rstrip('\n') for label in open(label_filename)]
    delete_unnecessary_files(base_tfrecords_filename)
    return (train_tfrecords_filename, test_tfrecords_filename), labels

tfrecords_filenames, labels = get_dataset()

# Commented out IPython magic to ensure Python compatibility.
# %%skip_for_export
# %%writefile albert.py
# 
# import tensorflow_hub as hub
# 
# ALBERT_TFHUB_URL = "https://tfhub.dev/tensorflow/albert_en_base/2"
# 
# def load_albert_layer(model_url=ALBERT_TFHUB_URL):
#     # Load the pre-trained ALBERT model as layer in Keras
#     albert_layer = hub.KerasLayer(
#         handle=model_url,
#         trainable=False)
#     return albert_layer

context = InteractiveContext()

output = example_gen_pb2.Output(
             split_config=example_gen_pb2.SplitConfig(splits=[
                 example_gen_pb2.SplitConfig.Split(name='train', hash_buckets=45),
                 example_gen_pb2.SplitConfig.Split(name='eval', hash_buckets=5)
             ]))
# Load the data from our prepared TFDS folder
examples = external_input("/content/tfds/imdb_reviews/plain_text/1.0.0")
example_gen = ImportExampleGen(input=examples, output_config=output)

context.run(example_gen)

# Commented out IPython magic to ensure Python compatibility.
# %%skip_for_export
# 
# for artifact in example_gen.outputs['examples'].get():
#     print(artifact.uri)

# Commented out IPython magic to ensure Python compatibility.
# %%skip_for_export
# 
# statistics_gen = StatisticsGen(
#     examples=example_gen.outputs['examples'])
# context.run(statistics_gen)
# 
# # context.show(statistics_gen.outputs['statistics'])

# Commented out IPython magic to ensure Python compatibility.
# %%skip_for_export
# 
# schema_gen = SchemaGen(
#     statistics=statistics_gen.outputs['statistics'],
#     infer_feature_shape=True)
# context.run(schema_gen)
# 
# context.show(schema_gen.outputs['schema'])

# Commented out IPython magic to ensure Python compatibility.
# %%skip_for_export
# 
# # Check the data schema for the type of input tensors
# tfdv.load_schema_text(schema_gen.outputs['schema'].get()[0].uri + "/schema.pbtxt")

# Commented out IPython magic to ensure Python compatibility.
# %%skip_for_export
# 
# example_validator = ExampleValidator(
#     statistics=statistics_gen.outputs['statistics'],
#     schema=schema_gen.outputs['schema'])
# context.run(example_validator)
# 
# context.show(example_validator.outputs['anomalies'])

# Commented out IPython magic to ensure Python compatibility.
# %%skip_for_export
# %%writefile transform.py
# 
# import tensorflow as tf
# import tensorflow_text as text
# 
# from tensorflow.python.platform import gfile
# 
# from albert import load_albert_layer
# 
# MAX_SEQ_LEN = 512  # Max number is 512
# 
# layer = load_albert_layer()
# model_file = layer.resolved_object.sp_model_file.asset_path.numpy().decode()
# del layer
# 
# def preprocessing_fn(inputs):
#     """Preprocess input column of text into transformed columns of.
#         * input token ids
#         * input mask
#         * input type ids
# 
#       Important ALBERT token IDs
#       '<pad>': 0,
#       '<unk>': 1,
#       '[CLS]': 2,
#       '[SEP]': 3,
#       '[MASK]': 4,
#     """
# 
#     CLS_ID = tf.constant(2, dtype=tf.int64)
#     SEP_ID = tf.constant(3, dtype=tf.int64)
#     PAD_ID = tf.constant(0, dtype=tf.int64)
#     
#     sentence_piece_model = gfile.GFile((model_file), 'rb').read()
#     sentencepiece = text.SentencepieceTokenizer(model=sentence_piece_model, 
#                                                 out_type=tf.int32) 
#     
#     def tokenize_text(text, sequence_length=MAX_SEQ_LEN):
#         """
#         Perform the ALBERT preprocessing from text -> input token ids
#         """
# 
#         # Convert text into token ids
#         tokens = sentencepiece.tokenize(text)
#         # The sentencepiece tokenizer provides token ids as tf.int32
#         # Need to cast to tf.int64 due to the TFT requirement
#         tokens = tf.cast(tokens, tf.int64)
# 
#         # Add start and end token ids to the id sequence
#         start_tokens = tf.fill([tf.shape(text)[0], 1], CLS_ID)
#         end_tokens = tf.fill([tf.shape(text)[0], 1], SEP_ID)
#         tokens = tokens[:, :sequence_length - 2]
#     
#         tokens = tf.concat([start_tokens, tokens, end_tokens], axis=1)
# 
#         # Truncate sequences greater than MAX_SEQ_LEN
#         tokens = tokens[:, :sequence_length]
# 
#         # Pad shorter sequences with the pad token id
#         tokens = tokens.to_tensor(default_value=PAD_ID)
#         pad = sequence_length - tf.shape(tokens)[1]
#         tokens = tf.pad(tokens, [[0, 0], [0, pad]], constant_values=PAD_ID)
# 
#         # And finally reshape the word token ids to fit the output 
#         # data structure of TFT  
#         return tf.reshape(tokens, [-1, sequence_length])
# 
#     def preprocess_albert_input(text):
#         """
#         Convert input text into the input_word_ids, input_mask, input_type_ids
#         """
#         input_word_ids = tokenize_text(text)
#         input_mask = tf.cast(input_word_ids > 0, tf.int64)
#         input_mask = tf.reshape(input_mask, [-1, MAX_SEQ_LEN])
#         
#         zeros_dims = tf.stack(tf.shape(input_mask))
#         input_type_ids = tf.fill(zeros_dims, 0)
#         input_type_ids = tf.cast(input_type_ids, tf.int64)
# 
#         return (
#             input_word_ids, 
#             input_mask,
#             input_type_ids
#         )
# 
#     input_word_ids, input_mask, input_type_ids = \
#         preprocess_albert_input(tf.squeeze(inputs['text'], axis=1))
# 
#     return {
#         'input_word_ids': input_word_ids,
#         'input_mask': input_mask,
#         'input_type_ids': input_type_ids,
#         'label': inputs['label']
#     }

transform = Transform(
    examples=example_gen.outputs['examples'],
    schema=schema_gen.outputs['schema'],
    module_file=os.path.abspath("transform.py"))
context.run(transform)

from tfx_bsl.coders.example_coder import ExampleToNumpyDict

pp = pprint.PrettyPrinter()

# Get the URI of the output artifact representing the transformed examples, which is a directory
train_uri = transform.outputs['transformed_examples'].get()[0].uri

print(train_uri)

# Get the list of files in this directory (all compressed TFRecord files)
tfrecord_folders = [os.path.join(train_uri, name) for name in os.listdir(train_uri)]
tfrecord_filenames = []
for tfrecord_folder in tfrecord_folders:
    for name in os.listdir(tfrecord_folder):
        tfrecord_filenames.append(os.path.join(tfrecord_folder, name))


# Create a TFRecordDataset to read these files
dataset = tf.data.TFRecordDataset(tfrecord_filenames, compression_type="GZIP")

for tfrecord in dataset.take(1):
    serialized_example = tfrecord.numpy()
    example = ExampleToNumpyDict(serialized_example)
    pp.pprint(example)

# Commented out IPython magic to ensure Python compatibility.
# %%skip_for_export
# %%writefile trainer.py
# 
# import tensorflow as tf
# import tensorflow_hub as hub
# import tensorflow_model_analysis as tfma
# import tensorflow_transform as tft
# from tensorflow_transform.tf_metadata import schema_utils
# 
# from typing import Text
# 
# import absl
# import tensorflow as tf
# from tensorflow import keras
# import tensorflow_transform as tft
# from tfx.components.trainer.executor import TrainerFnArgs
# 
# 
# _LABEL_KEY = 'label'
# ALBERT_TFHUB_URL = "https://tfhub.dev/tensorflow/albert_en_base/2"
# 
# 
# def _gzip_reader_fn(filenames):
#     """Small utility returning a record reader that can read gzip'ed files."""
#     return tf.data.TFRecordDataset(filenames, compression_type='GZIP')
# 
# def load_albert_layer(model_url=ALBERT_TFHUB_URL):
#     # Load the pre-trained BERT model as layer in Keras
#     albert_layer = hub.KerasLayer(
#         handle=model_url,
#         trainable=False)  # Model can be fine-tuned 
#     return albert_layer
# 
# def get_model(tf_transform_output, max_seq_length=512):
# 
#     # Dynamically create inputs for all outputs of our transform graph
#     feature_spec = tf_transform_output.transformed_feature_spec()  
#     feature_spec.pop(_LABEL_KEY)
# 
#     inputs = {
#         key: tf.keras.layers.Input(shape=(max_seq_length), name=key, dtype=tf.int64)
#             for key in feature_spec.keys()
#     }
# 
#     input_word_ids = tf.cast(inputs["input_word_ids"], dtype=tf.int32)
#     input_mask = tf.cast(inputs["input_mask"], dtype=tf.int32)
#     input_type_ids = tf.cast(inputs["input_type_ids"], dtype=tf.int32)
# 
#     albert_layer = load_albert_layer()
#     encoder_inputs = dict(
#         input_word_ids=tf.reshape(input_word_ids, (-1, max_seq_length)),
#         input_mask=tf.reshape(input_mask, (-1, max_seq_length)),
#         input_type_ids=tf.reshape(input_type_ids, (-1, max_seq_length)),
#     )
#     outputs = albert_layer(encoder_inputs)
#     
#     # Add additional layers depending on your problem
#     x = tf.keras.layers.Dense(256, activation='relu')(outputs["pooled_output"])
#     dense = tf.keras.layers.Dense(64, activation='relu')(x)
#     pred = tf.keras.layers.Dense(1, activation='sigmoid')(dense)
# 
#     keras_model = tf.keras.Model(
#         inputs=[
#                 inputs['input_word_ids'], 
#                 inputs['input_mask'], 
#                 inputs['input_type_ids']], 
#         outputs=pred)
#     keras_model.compile(loss='binary_crossentropy', 
#                         optimizer=tf.keras.optimizers.Adam(learning_rate=0.001), 
#                         metrics=['accuracy']
#                         )
#     return keras_model
# 
# 
# def _get_serve_tf_examples_fn(model, tf_transform_output):
#     """Returns a function that parses a serialized tf.Example and applies TFT."""
# 
#     model.tft_layer = tf_transform_output.transform_features_layer()
# 
#     @tf.function
#     def serve_tf_examples_fn(raw_features):
#         # Conversion from raw_features to features only needed to adjust 
#         # the Tensor shape to fit Keras' inputs
#         features = dict()
#         features['text'] = tf.reshape(raw_features['text'], [-1, 1])
#         transformed_features = model.tft_layer(features)
#         outputs = model(transformed_features)
#         return {'outputs': outputs}
# 
#     return serve_tf_examples_fn
# 
# def _input_fn(file_pattern: Text,
#               tf_transform_output: tft.TFTransformOutput,
#               batch_size: int = 32) -> tf.data.Dataset:
#     """Generates features and label for tuning/training.
# 
#     Args:
#       file_pattern: input tfrecord file pattern.
#       tf_transform_output: A TFTransformOutput.
#       batch_size: representing the number of consecutive elements of returned
#         dataset to combine in a single batch
# 
#     Returns:
#       A dataset that contains (features, indices) tuple where features is a
#         dictionary of Tensors, and indices is a single Tensor of label indices.
#     """
#     transformed_feature_spec = (
#         tf_transform_output.transformed_feature_spec().copy())
# 
#     dataset = tf.data.experimental.make_batched_features_dataset(
#         file_pattern=file_pattern,
#         batch_size=batch_size,
#         features=transformed_feature_spec,
#         reader=_gzip_reader_fn,
#         label_key=_LABEL_KEY)
# 
#     return dataset
# 
# # TFX Trainer will call this function.
# def run_fn(fn_args: TrainerFnArgs):
#     """Train the model based on given args.
# 
#     Args:
#       fn_args: Holds args used to train the model as name/value pairs.
#     """
#     tf_transform_output = tft.TFTransformOutput(fn_args.transform_output)
# 
#     train_dataset = _input_fn(fn_args.train_files, tf_transform_output, 32)
#     eval_dataset = _input_fn(fn_args.eval_files, tf_transform_output, 32)
# 
#     mirrored_strategy = tf.distribute.MirroredStrategy()
#     with mirrored_strategy.scope():
#         model = get_model(tf_transform_output=tf_transform_output)
# 
#     model.fit(
#         train_dataset,
#         steps_per_epoch=fn_args.train_steps,
#         validation_data=eval_dataset,
#         validation_steps=fn_args.eval_steps)
# 
#     features_spec = dict(
#         text=tf.TensorSpec(shape=(None), dtype=tf.string),
#     )
# 
#     signatures = {
#         'serving_default':
#             _get_serve_tf_examples_fn(model,
#                                       tf_transform_output).get_concrete_function(
#                                           features_spec
#                                       ),
#     }
#     model.save(fn_args.serving_model_dir, save_format='tf', signatures=signatures)

# NOTE: Adjust the number of training and evaluation steps
TRAINING_STEPS = 5000
EVALUATION_STEPS = 1000

trainer = Trainer(
    module_file=os.path.abspath("trainer.py"),
    custom_executor_spec=executor_spec.ExecutorClassSpec(GenericExecutor),
    examples=transform.outputs['transformed_examples'],
    transform_graph=transform.outputs['transform_graph'],
    schema=schema_gen.outputs['schema'],
    train_args=trainer_pb2.TrainArgs(num_steps=TRAINING_STEPS),
    eval_args=trainer_pb2.EvalArgs(num_steps=EVALUATION_STEPS))
context.run(trainer)

model_resolver = ResolverNode(
    instance_name='latest_blessed_model_resolver',
    resolver_class=latest_blessed_model_resolver.LatestBlessedModelResolver,
    model=Channel(type=Model),
    model_blessing=Channel(type=ModelBlessing))

context.run(model_resolver)

eval_config = tfma.EvalConfig(
    model_specs=[tfma.ModelSpec(label_key='label')],
    slicing_specs=[tfma.SlicingSpec()],
    metrics_specs=[
        tfma.MetricsSpec(metrics=[
            tfma.MetricConfig(
                class_name='CategoricalAccuracy',
                threshold=tfma.MetricThreshold(
                    value_threshold=tfma.GenericValueThreshold(
                        lower_bound={'value': 0.5}),
                    change_threshold=tfma.GenericChangeThreshold(
                        direction=tfma.MetricDirection.HIGHER_IS_BETTER,
                        absolute={'value': -1e-2})))
        ])
    ]
)

evaluator = Evaluator(
    examples=example_gen.outputs['examples'],
    model=trainer.outputs['model'],
    baseline_model=model_resolver.outputs['model'],
    eval_config=eval_config
)

context.run(evaluator)

# Check the blessing
!ls {evaluator.outputs['blessing'].get()[0].uri}

!mkdir /content/serving_model_dir

serving_model_dir = "/content/serving_model_dir"

pusher = Pusher(
    model=trainer.outputs['model'],
    model_blessing=evaluator.outputs['blessing'],
    push_destination=pusher_pb2.PushDestination(
        filesystem=pusher_pb2.PushDestination.Filesystem(
            base_directory=serving_model_dir)))

context.run(pusher)

push_uri = pusher.outputs.model_push.get()[0].uri
latest_version_path = os.path.join(push_uri)
loaded_model = tf.saved_model.load(latest_version_path)

example_str = b"This is the finest show ever produced for TV. Each episode is a triumph. The casting, the writing, the timing are all second to none. This cast performs miracles."
f = loaded_model.signatures["serving_default"]
print(f(tf.constant([example_str])))

!zip -r /content/model.zip /content/serving_model_dir
