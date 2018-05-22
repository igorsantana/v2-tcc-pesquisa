"""Clustering"""
import json
import sys
import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN, KMeans, AgglomerativeClustering

def cluster_task(cluster):
    if not cluster.get('config'):
        cluster['config'] = {}
    cfg = cluster.get('config')
    if cluster.get('name') == "KMeans":
        return KMeans(  n_clusters=cfg.get("num_clusters") or 5,
                        init=cfg.get("init") or "k-means++",
                        max_iter=cfg.get('max_iterations') or 300,
                        precompute_distances= "auto")
    if cluster.get('name') == "DBSCAN":
        return DBSCAN(  eps=cfg.get('eps') or 0.5,
                        min_samples=cfg.get('min_pts') or 1, 
                        metric=cfg.get('distance') or 'haversine')
    if cluster.get('name') == "HierarchicalClusterer":
        return AgglomerativeClustering( n_clusters=cfg.get("num_clusters") or 5,
                                        affinity=cfg.get("distance") or "manhattan",
                                        linkage="average")

def print_pretty(cluster, num):
    if cluster.get('name') == "KMeans":
        return ("Kmeans_num" + str(cluster["config"].get("num_clusters")))
    if cluster.get('name') == "DBSCAN":
        return ("DBSCAN_eps" + str(cluster["config"].get("eps")) + "_minpts" + str(cluster["config"].get("min_pts")) + "_num" + str(num))
    if cluster.get('name') == "HierarchicalClusterer":
        return ("HierarchicalClusterer_num" + str(cluster["config"].get("num_clusters")))

def cluster_to_file(json_file, input_file):
    with open(json_file) as data_file:
        json_data = json.load(data_file)
    
    attr_to_cluster = json_data["attributesToCluster"].split(',')
    df              = pd.read_csv(input_file, header = 0)
    coords          = df.as_matrix(columns=attr_to_cluster)
    x = 0
    for cluster in json_data["clustering"]:
        task = cluster_task(cluster)
        if cluster.get('name') == 'DBSCAN':
            task.fit(np.radians(coords))    
        else:
            task.fit(coords)
        lbls = task.labels_
        n_clusters_ = len(set(lbls)) - (1 if -1 in lbls else 0)
        copy = df.copy()
        for i in range(0, len(attr_to_cluster)):
            copy.drop(attr_to_cluster[i], axis=1, inplace=True)
        copy['REGION'] = task.labels_
        copy.to_csv('Temporary Files/' + print_pretty(cluster, n_clusters_) + ".csv", index = False)
        x+=1
1