import os
import numpy as np
import json
import torch
import config
from utils_ridge.stimulus_utils import TRFile, load_textgrids, load_simulated_trfiles, load_textgrids_eval
from utils_ridge.dsutils import make_word_ds
from utils_ridge.interpdata import lanczosinterp2D
from utils_ridge.util import make_delayed

# This code was mostly taken from Tang et al. (2023). Some edits are marked by "edit" comment
def get_story_wordseqs(stories):
    """loads words and word times of stimulus stories
    """
    grids = load_textgrids(stories, config.DATA_TRAIN_DIR)
    with open(os.path.join(config.DATA_TRAIN_DIR, "respdict.json"), "r") as f:
        respdict = json.load(f)
    trfiles = load_simulated_trfiles(respdict)
    wordseqs = make_word_ds(grids, trfiles)
    return wordseqs

# edit (new function)
def get_story_wordseqs_eval(stories):
    """loads words and word times of stimulus stories
    """
    grids = load_textgrids_eval(stories, config.DATA_TEST_DIR)
    with open(os.path.join(config.DATA_TRAIN_DIR, "respdict.json"), "r") as f:
        respdict = json.load(f)
    trfiles = load_simulated_trfiles(respdict)
    wordseqs = make_word_ds(grids, trfiles)
    return wordseqs


def get_stim_eval(stories, features, tr_stats = None, make_delay=True, segment=True, context=None):
    """extract quantitative features of stimulus stories
    """
    word_seqs = get_story_wordseqs_eval(stories)
    #edit
    word_vecs = {story : features.make_stim(word_seqs[f"story_{story}"].data, segment=segment, context=context) for story in stories}
    word_mat = np.vstack([word_vecs[story] for story in stories])
    word_mean, word_std = word_mat.mean(0), word_mat.std(0)
    
    ds_vecs = {story : lanczosinterp2D(word_vecs[story], word_seqs[f"story_{story}"].data_times, word_seqs[f"story_{story}"].tr_times) 
               for story in stories}
    story_shapes = [ds_vecs[story][5+config.TRIM:-config.TRIM].shape for story in stories]
    story_shapes = [(shape[0], shape[1]) for shape in story_shapes]
    ds_mat = np.vstack([ds_vecs[story][5+config.TRIM:-config.TRIM] for story in stories])
    # normalize to 0 mean and unit variance
    if tr_stats is None: 
        r_mean, r_std = ds_mat.mean(0), ds_mat.std(0)
        r_std[r_std == 0] = 1
    else: 
        r_mean, r_std = tr_stats
    ds_mat = np.nan_to_num(np.dot((ds_mat - r_mean), np.linalg.inv(np.diag(r_std))))
    
    # edit: try without delay mat
    if make_delay == True:
        del_mat = make_delayed(ds_mat, config.STIM_DELAYS)
    else:
        del_mat = ds_mat
            
    if tr_stats is None: return del_mat, (r_mean, r_std), (word_mean, word_std)
    else: return del_mat
    
def get_stim(stories, features, tr_stats = None, make_delay=True, segment=True, context=None):
    """extract quantitative features of stimulus stories
    """
    word_seqs = get_story_wordseqs(stories)
    word_vecs = {story : features.make_stim(word_seqs[f"story_{story}"].data, segment=segment, context=context) for story in stories}
    word_mat = np.vstack([word_vecs[story] for story in stories])
    word_mean, word_std = word_mat.mean(0), word_mat.std(0)
    
    ds_vecs = {story : lanczosinterp2D(word_vecs[story], word_seqs[f"story_{story}"].data_times, word_seqs[f"story_{story}"].tr_times) 
               for story in stories}
    story_shapes = [ds_vecs[story][5+config.TRIM:-config.TRIM].shape for story in stories]
    story_shapes = [(shape[0], shape[1]) for shape in story_shapes]
    ds_mat = np.vstack([ds_vecs[story][5+config.TRIM:-config.TRIM] for story in stories])
    # normalize to 0 mean and unit variance
    if tr_stats is None: 
        r_mean, r_std = ds_mat.mean(0), ds_mat.std(0)
        r_std[r_std == 0] = 1
    else: 
        r_mean, r_std = tr_stats
    ds_mat = np.nan_to_num(np.dot((ds_mat - r_mean), np.linalg.inv(np.diag(r_std))))
    
    # edit: try without delay mat
    if make_delay == True:
        del_mat = make_delayed(ds_mat, config.STIM_DELAYS)
    else:
        del_mat = ds_mat
            
    if tr_stats is None: return del_mat, (r_mean, r_std), (word_mean, word_std)
    else: return del_mat

def predict_word_rate(resp, wt, vox, mean_rate):
    """predict word rate at each acquisition time
    """
    delresp = make_delayed(resp[:, vox], config.RESP_DELAYS)
    rate = ((delresp.dot(wt) + mean_rate)).reshape(-1).clip(min = 0)
    return np.round(rate).astype(int)

def predict_word_times(word_rate, resp, starttime = 0, tr = 2):
    """predict evenly spaced word times from word rate
    """
    half = tr / 2
    trf = TRFile(None, tr)
    trf.soundstarttime = starttime
    trf.simulate(resp.shape[0])
    tr_times = trf.get_reltriggertimes() + half

    word_times = []
    for mid, num in zip(tr_times, word_rate):  
        if num < 1: continue
        word_times.extend(np.linspace(mid - half, mid + half, num, endpoint = False) + half / num)
    return np.array(word_times), tr_times