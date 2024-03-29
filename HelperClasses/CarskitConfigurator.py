setting_stuff = """evaluation.setup=cv -k 10 -p on --rand-seed 1 --test-view all
item.ranking=on -topN 10
guava.cache.spec=maximumSize=200,expireAfterAccess=2m

################################################### Model-based Methods ##########################################
num.factors=10
num.max.iter=200

learn.rate=2e-3 -max -1 -bold-driver

reg.lambda=0.0001 -c 0.001
pgm.setup=-alpha 2 -beta 0.5 -burn-in 300 -sample-lag 10 -interval 100

################################################### Memory-based Methods #########################################
# similarity method: PCC, COS, COS-Binary, MSD, CPC, exJaccard; -1 to disable shrinking;
similarity=cos
num.shrinkage=-1

num.neighbors=10

################################################### Method-specific Settings #######################################
CAMF_CU_domEmo=-k 50
CAMF_CU_domEmo2=-k 40
CAMF_CU_endEmo=-k 40
CAMF_CU_endEmo2=-k 50
AoBPR=-lambda 0.3
BUCM=-gamma 0.5
BHfree=-k 10 -l 10 -gamma 0.2 -sigma 0.01
FISM=-rho 100 -alpha 0.4
Hybrid=-lambda 0.5
LDCC=-ku 20 -kv 19 -au 1 -av 1 -beta 1
PD=-sigma 2.5
PRankD=-alpha 20
RankALS=-sw on
RSTE=-alpha 0.4
# note: lp+lg>4, options: -sol 1;0;0;1;etc
DCR=-wt 0.9 -wd 0.4 -p 5 -lp 2.05 -lg 2.05
# note: lp+lg>4, options: -sol 0.5;0.01;0.02;etc
DCW=-wt 0.9 -wd 0.4 -p 5 -lp 2.05 -lg 2.05 -th 0.8
SPF=-i 0 -b 5 -th 0.9 -f 10 -t 100 -l 0.02 -r 0.001
SLIM=-l1 1 -l2 1 -k 1
CAMF_LCS=-f 10
CSLIM_C=-lw1 1 -lw2 5 -lc1 1 -lc2 5 -k 3 -als 0
CSLIM_CI=-lw1 1 -lw2 5 -lc1 1 -lc2 1 -k 1 -als 0
CSLIM_CU=-lw1 1 -lw2 0 -lc1 1 -lc2 5 -k 10 -als 0
CSLIM_CUCI=-lw1 1 -lw2 5 -lc1 1 -lc2 5 10 -1 -als 0
GCSLIM_CC=-lw1 1 -lw2 5 -lc1 1 -lc2 5 -k -1 -als 0
CSLIM_ICS=-lw1 1 -lw2 5 -k 1 -als 0
CSLIM_LCS=-lw1 1 -lw2 5 -k 1 -als 0
CSLIM_MCS=-lw1 -20000 -lw2 100 -k 3 -als 0
GCSLIM_ICS=-lw1 1 -lw2 5 -k 10 -als 0
GCSLIM_LCS=-lw1 1 -lw2 5 -k -1 -als 0
GCSLIM_MCS=-lw1 1 -lw2 5 -k -1 -als 0
FM=-lw 0.01 -lf 0.02"""

def create_config(rec, baseline, dataset):
    config = 'dataset.ratings.lins=' + dataset + '\n' \
             'dataset.social.lins=-1' + '\n' \
             'ratings.setup=-threshold -1 -datatransformation 1 -fullstat -1' + '\n'\
             'recommender=' + rec_cfg(rec, baseline) + '\n'
    return config + setting_stuff


def rec_cfg(rec, baseline):
    if rec == 'davi':
        return 'davibest -traditional ' + baseline
    if rec == 'combinedreduction':
        return 'combinedreduction -tp 5 -innerfolds 5 -traditional' + baseline
    if rec == 'usersplitting':
        return 'usersplitting -traditional ' + baseline
    if rec == 'itemsplitting':
        return 'itemsplitting -traditional ' + baseline
    if rec == 'uisplitting':
        return 'uisplitting -traditional ' + baseline
    if rec == 'bpr':
        return 'bpr'
    print('Erro')
