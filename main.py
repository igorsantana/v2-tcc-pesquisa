""" Python 2.6+"""
from __future__ import print_function 
from HelperClasses.Config import Config
from HelperClasses.Cluster import cluster_to_file
from HelperClasses.CarskitConfigurator import create_config, rec_cfg
import argparse
import os
import shutil
import pandas as pd

dataset_help        = 'The dataset used to perform the datamine process. It must be a .csv file in the following format: [USERID][OBJID][RATING][LATITUDE][LONGITUDE]'
baseline_help       = 'The baseline algorithm that will be used to compare the results.'
config_help         = 'Configuration file that will contain the configuration for the datamine algorithms'
recommender_help    = 'Recommender system that will be used to compare with the baseline'
metrics_help        = 'Metrics that will be used.'

shutil.rmtree('Temporary Files')

parser = argparse.ArgumentParser(description="Datamine data and process it to be used with recommender systems.")
parser.add_argument('dataset', type=str, nargs=1, help=dataset_help)
parser.add_argument('baseline', type=str, nargs=1, help=baseline_help)
parser.add_argument('config', type=str, nargs=1, help=config_help)
parser.add_argument('recommender', type=str, nargs=1, help=recommender_help)
parser.add_argument('metrics', type=str, nargs='*', help=metrics_help, default='prec,rec,f1')
args = parser.parse_args()
conf = Config(args)

def get_results(rec_cfg):
    df = pd.read_csv('datasets/CARSKit.Workspace/' + rec_cfg + '_evalfolds.csv')
    df.drop(df.columns[[1, 2, 5, 6, 9, 10, 13, 14]], axis=1, inplace=True)
    return df

dataset_path = os.path.normpath(os.getcwd() + os.sep + 'datasets' + os.sep + conf.get_dataset())
print('Creating temporary files.')
os.makedirs('Temporary Files')
cluster_to_file(conf.get_config(), dataset_path)
print('Clustering done.')

for file in os.listdir('Temporary Files'):
    if file.endswith('.csv'):
        f = open('Temporary Files/'+file.split('.')[0] + '.conf', 'w')
        f.write(create_config(conf.get_recommender(), conf.get_baseline(), dataset_path))
        f.close()

values = {}
print('Starting the baseline algorithm')
f = open('Temporary Files/baseline.conf', 'w')
f.write(create_config(conf.get_baseline(), conf.get_baseline(), dataset_path))
f.close()
os.system('java -Xmx6G -jar jar/carskit.jar -c Temporary\ Files/baseline.conf > /dev/null')
values['baseline'] = get_results(rec_cfg(conf.get_baseline(), conf.get_baseline()))
values['data'] = []

print('Finished baseline algorithm')
print('Starting the recommendation process.')
i = 1
for file in os.listdir('Temporary Files'):
    if file.endswith('.conf'):
        os.system('java -Xmx6G -jar jar/carskit.jar -c Temporary\ Files/' + file + '> /dev/null')
        values['data'].append(get_results(rec_cfg(conf.get_recommender(), conf.get_baseline())))
        print('Algorithm ' + str(i) + ' done.')
        i += 1

print(values)