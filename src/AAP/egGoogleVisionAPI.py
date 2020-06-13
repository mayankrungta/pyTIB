#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os, io
import re
from google.cloud import vision
from google.cloud import storage
from google.protobuf import json_format

""" 
 pip install --upgrade google-cloud-storage
"""
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'/home/mayank/libtech/src/scripts/bbmp_aap.json'

project = 'bbmp'
bucket_name = 'draft-rolls'
file_name = 'z.txt'

print(storage)
storage_client = storage.Client()
print(storage_client)
bucket = storage_client.get_bucket(bucket_name)
print(bucket)
blob = bucket.blob(file_name)
print(blob)
print(blob.upload_from_filename(file_name))

exit(0)

client = vision.ImageAnnotatorClient()

batch_size = 100
mime_type = 'application/pdf'
feature = vision.types.Feature(
    type=vision.enums.Feature.Type.DOCUMENT_TEXT_DETECTION)

gcs_source_uri = 'gs://aap-bbmp/bbmp-wards-2020.pdf'
gcs_source = vision.types.GcsSource(uri=gcs_source_uri)
input_config = vision.types.InputConfig(gcs_source=gcs_source, mime_type=mime_type)

gcs_destination_uri = 'gs://aap-bbmp/bbmp-wards-2020.pdf_'

gcs_destination = vision.types.GcsDestination(uri=gcs_destination_uri)
output_config = vision.types.OutputConfig(gcs_destination=gcs_destination, batch_size=batch_size)
async_request = vision.types.AsyncAnnotateFileRequest(
    features=[feature], input_config=input_config, output_config=output_config)

operation = client.async_batch_annotate_files(requests=[async_request])
operation.result(timeout=180)

storage_client = storage.Client()
match = re.match(r'gs://([^/]+)/(.+)', gcs_destination_uri)
bucket_name = match.group(1)
prefix = match.group(2)
bucket = storage_client.get_bucket(bucket_name)

# List object with the given prefix
blob_list = list(bucket.list_blobs(prefix=prefix))
print('Output files:')
for blob in blob_list:
    print(blob.name)

output = blob_list[0]
json_string = output.download_as_string()
response = json_format.Parse(json_string, vision.types.AnnotateFileResponse())

buffer = ''
for page_response in response.responses:
    annotation = page_response.full_text_annotation
    #print('Page text:')
    #print(annotation.text)
    buffer += annotation.text + '\n'

filename = 'bbmp-wards-2020.txt'
with open(filename, 'w') as html_file:
    print(f'Writing file[{filename}]')
    html_file.write(buffer)
