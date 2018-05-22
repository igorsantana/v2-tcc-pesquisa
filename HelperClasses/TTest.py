import os
import pandas as pd
import numpy as np
from scipy import stats

file_base = os.path.normpath(os.getcwd() + os.sep + 'resultados' + os.sep + 'bpr_foursquare.tsv')
file_test = os.path.normpath(os.getcwd() + os.sep + 'resultados' + os.sep + 'combined_reduction_foursquare.tsv')
sep       ='\t'
base_data = pd.read_csv(file_base, sep)
alte_data = pd.read_csv(file_test, sep)

for run in [0, 13, 26, 39, 52, 65, 78, 91, 104]:
  base_matrix = [[0 for x in range(9)] for y in range(10)] 
  cmpr_matrix = [[0 for x in range(9)] for y in range(10)] 
  a = 0
  for i in range(run+1, run + 11):
    for j in range (1, 10):
      base_matrix[a][j - 1] = float(base_data.values[i][j])
      cmpr_matrix[a][j - 1] = float(alte_data.values[i][j])
    a += 1

  base_cmp = [[0 for x in range(9)] for y in range(10)]
  alte_cmp = [[0 for x in range(9)] for y in range(10)]
  pvalues  = [0 for x in range(9)]
  for i in range(0, 9):
    a = 0
    for j in range(0,10):
      base_cmp[a] = base_matrix[j][i]
      alte_cmp[a] = cmpr_matrix[j][i]
      a+= 1
    pvalues[i] = stats.ttest_rel(np.array(base_cmp), np.array(alte_cmp)).pvalue
  print('\t'.join(str(x) for x in pvalues))
