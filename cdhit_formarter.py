#!/usr/bin/python3
# -*- coding: utf-8 -*-
###############################>GENERAL-INFORMATIONS<###############################
"""
Build in Python 3.6
Author:
Yago Dias
yag.dias@gmail.com
Script Repository:
https://github.com/yagdias/handfull_bioinfo_scripts
"""
###############################>LIBRARIES<###############################

import pandas as pd
import argparse
import csv
import re

###############################>ARGUMENTS<###############################
parser = argparse.ArgumentParser(
    description='This scripts receives a cdhit output formats it to csv, displaying the representative in the first column and the second column all the sequences that clusterized with the representative, in a single cell.', formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument(
    "-in", "--input", help="clstr file, from cd-hit", required=True)
# Storing argument on variables
args = parser.parse_args()
input_file = args.input
###############################>EXECUTION<###############################
with open(input_file, 'r') as cluster_file, open(input_file+'.cd.clstr.tsv', 'w') as cluster_formated:
    cluster_file_reader = cluster_file.readlines()
    cluster_formated_writer = csv.writer(cluster_formated, delimiter='\t')
    cluster_formated_writer.writerow(['Sequence', 'Cluster', 'Representative'])
    cluster_list = []
    for line in cluster_file_reader:
        line = line.rstrip('\n')
        if 'Cluster' in line:
            cluster_number = re.sub(r'>Cluster ', '', line)
        else:
            if 'at ' in line:
                representative = 'FALSE'
            else:
                representative = 'TRUE'
            sequence_name = re.sub(r'.*>', '', line)
            sequence_name = re.sub(r'\.\.\..*', '', sequence_name)
            cluster_list.append(
                [sequence_name, cluster_number, representative])
    cluster_formated_writer.writerows(cluster_list)
df = pd.read_csv(input_file+'.cd.clstr.tsv', sep='\t')
concat = df.groupby(['Cluster', 'Representative']).transform(
    lambda x: ','.join(x)).drop_duplicates()
concat.columns = ['Representative']
concat['Sequence'] = concat.shift(-1)
concat['Sequence'][concat.Representative.str.contains(
    'Aag') == concat['Sequence'].str.contains('Aag')] = ''
concat = concat[concat.Representative.str.contains('Aag')]
concat.to_csv(input_file+".csv", index=False)
