from future.builtins import next

import os
import pandas as pd
import csv
import logging
import pdb
import dedupe 

#These are different files that we use for our machine learning problem. 
input_file = 'Deduplication Problem - Sample Dataset.csv'
intermediate_output_file = 'Intermediate_Output.csv'
settings_file = 'duplication_example_learned_settings'
training_file = 'duplication_example_training.json'
input_file_with_ids = 'input_with_ids.csv'


def readData(filename):
    """
    Read in our data from a CSV file and create a dictionary of records, 
    where the key is a unique record ID and each value is dict
    """
    Id = 0
    data_d = {}
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            clean_row = []
            clean_row = [('Id',str(Id))]
            for (k, v) in row.items():
                clean_row.append((k,v))
            row_id = Id
            data_d[row_id] = dict(clean_row)
            Id=Id+1

    return data_d

print('importing data ...')
data_d = readData(input_file)
    
   
#    Now I am creating new input file with id's column added. We are doing this so that we can uniquely identify records which match to each other.

with open(input_file_with_ids, 'w') as f_input:
    write1 = csv.writer(f_input, lineterminator = '\n')
    headings = ['Id','ln','dob','gn','fn']
    write1.writerow(headings)
    for i in range(len(data_d)):
	    write1.writerow(data_d[i].values())




#	If a settings file already exists, we'll just load that and skip training.

if os.path.exists(settings_file):
    print('reading from', settings_file)
    with open(settings_file, 'rb') as f:
        deduper = dedupe.StaticDedupe(f)
else:
    # ## Training

    # Define the fields dedupe will pay attention to
    fields = [
        {'field' : 'ln', 'type': 'String'},
        {'field' : 'dob', 'type': 'String'},
        {'field' : 'gn', 'type': 'String'},
        {'field' : 'fn', 'type': 'String'},
        ]

    # Create a new deduper object and pass our data model to it.
    deduper = dedupe.Dedupe(fields)

    deduper.sample(data_d, 115)

    if os.path.exists(training_file):
        print('reading labeled examples from ', training_file)
        with open(training_file, 'rb') as f:
            deduper.readTraining(f)


    print('starting active labeling...')
    dedupe.consoleLabel(deduper)
    deduper.train()


    with open(training_file, 'w') as tf:
        deduper.writeTraining(tf)


    with open(settings_file, 'wb') as sf:
        deduper.writeSettings(sf)

# Find the threshold that will maximize a weighted average of our
# precision and recall.  When we set the recall weight to 2, we are
# saying we care twice as much about recall as we do precision.
#
# If we had more data, we would not pass in all the blocked data into
# this function but a representative sample.

threshold = deduper.threshold(data_d, recall_weight=1)

print('clustering...')

# match will return sets of record IDs that dedupe believes are all referring to the same entity.
clustered_dupes = deduper.match(data_d, threshold)

print('# duplicate sets', len(clustered_dupes))

## Writing Results

# Write our original data back out to a CSV with a new column called 
# 'Cluster ID' which indicates which records refer to each other.

cluster_membership = {}
cluster_id = 0
for (cluster_id, cluster) in enumerate(clustered_dupes):
    id_set, scores = cluster
    cluster_d = [data_d[c] for c in id_set]
    canonical_rep = dedupe.canonicalize(cluster_d)
    for record_id, score in zip(id_set, scores):
        cluster_membership[record_id] = {
            "cluster id" : cluster_id,
            "canonical representation" : canonical_rep,
            "confidence": score
        }

singleton_id = cluster_id + 1

with open(intermediate_output_file, 'w') as f_output, open(input_file_with_ids) as f_input:
    writer = csv.writer(f_output, lineterminator = '\n')
    reader = csv.reader(f_input)

    heading_row = next(reader)
    heading_row.insert(0, 'confidence_score')
    heading_row.insert(0, 'Cluster ID')
    canonical_keys = canonical_rep.keys()
    for key in canonical_keys:
        heading_row.append('canonical_' + key)

    writer.writerow(heading_row)

    for row in reader:
        row_id = int(row[0])
        if row_id in cluster_membership:
            cluster_id = cluster_membership[row_id]["cluster id"]
            canonical_rep = cluster_membership[row_id]["canonical representation"]
            row.insert(0, cluster_membership[row_id]['confidence'])
            row.insert(0, cluster_id)
            for key in canonical_keys:
                row.append(canonical_rep[key].encode('utf8'))
        else:
            row.insert(0, None)
            row.insert(0, singleton_id)
            singleton_id += 1
            for key in canonical_keys:
                row.append(None)
        writer.writerow(row)









