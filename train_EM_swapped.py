import os
import numpy as np
import json
import argparse

import config
from GPT import GPT
from StimulusModel import LMFeatures
from utils_stim import get_stim
from utils_resp.utils_resp import get_resp, get_mask
from utils_ridge.ridge import ridge, bootstrap_ridge
np.random.seed(42)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--subject", type = str, required = True) #'01' to '09'
    # edit: somehow need to work with other models
    parser.add_argument("--gpt", type = str, default = "perceived")
    parser.add_argument("--layer", type = int) #layer from 0 to 11
    parser.add_argument("--area", type = list, default=None) #layer from 0 to 11
    parser.add_argument("--num_stories", type = int, default=10) #number of stories to consider
    parser.add_argument("--mode", type = str, default = "reading")
    # parser.add_argument("--split", type = str, default = "train")
    # TODO: add a full list of available brain regions 
    # TODO: add a list of stories and corresponding names
    args = parser.parse_args()
    
    stories = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10"]
    stories = stories[:args.num_stories]
    resp_path = r"C:\Users\Nursulu_1\Downloads\semantic-decoding\data_train\train_response"
    print("Subject", args.subject)
    print("Layer", args.layer)
    print("Loading GPT")
    # load gpt
    with open(os.path.join(config.DATA_LM_DIR, args.gpt, "vocab.json"), "r") as f:
        gpt_vocab = json.load(f)
    gpt = GPT(path = os.path.join(config.DATA_LM_DIR, args.gpt, "model"), vocab = gpt_vocab, device = config.GPT_DEVICE)
    # can change the layer manually, also context size
    features = LMFeatures(model = gpt, layer = args.layer, context_words = config.GPT_WORDS)
    print("Areas:", args.area)
    print("Estimating Encoding model")    
    # estimate encoding model
    rstim, tr_stats, word_stats = get_stim(stories, features)
    # rresp = get_resp(args.subject, stories, stack = True)
    rresp = get_resp(resp_path, args.subject, stories, stack=True, area=args.area, mode=args.mode)
    # TODO: shapes are different from stimuli. try trimming for now, then figure out why the difference is there.
    # rresp = rresp[:rstim.shape[0], :]
    # swap
    nchunks = int(np.ceil(rstim.shape[0] / 5 / config.CHUNKLEN))
    # swapped response and stimulus
    print("Starting bootstrap ridge regression")
    weights, alphas, bscorrs = bootstrap_ridge(rresp, rstim, use_corr = False, alphas = config.ALPHAS,
        nboots = config.NBOOTS, chunklen = config.CHUNKLEN, nchunks = nchunks)        
    bscorrs = bscorrs.mean(2).max(0)
    # TODO: use logger instead of print
    print("max(bscorrs) is ", max(bscorrs))
    vox = np.sort(np.argsort(bscorrs)[-config.VOXELS:])
    del rstim, rresp
    
    print("Estimating model noise...")
    # estimate noise model. swapped stim and resp
    resp_dict = {story : get_stim([story], features, tr_stats = tr_stats) for story in stories}
    stim_dict = get_resp(resp_path, args.subject, stories, area=args.area, stack = False, vox = vox)
    noise_model = np.zeros([len(vox), len(vox)])
    for hstory in stories:
        # at each iteration, our story stimula becomes test
        tstim, hstim = np.vstack([stim_dict[tstory][:resp_dict[tstory].shape[0]] for tstory in stories if tstory != hstory]), stim_dict[hstory][:resp_dict[hstory].shape[0]]
        # at each iteration, our brain response becomes test
        tresp, hresp = np.vstack([resp_dict[tstory] for tstory in stories if tstory != hstory]), resp_dict[hstory]
        # we build a model (weights) trained on all other stum-resp pairs
        bs_weights = ridge(tstim, tresp, alphas[vox])
        # then we test how well it generalizes to our story
        resids = hresp - hstim.dot(bs_weights)
        # the residuals are added, and then we iterate again through other models
        bs_noise_model = resids.T.dot(resids)
        noise_model += bs_noise_model / np.diag(bs_noise_model).mean() / len(stories)
    del stim_dict, resp_dict
        
    print("Saving the results")
    # save
    # save_location = os.path.join("C:/Users/Nursulu_1/Downloads/semantic-decoding/trim_like_stim/", args.subject)
    save_location = os.path.join(config.MODEL_DIR, args.subject, "_".join(args.area))
    os.makedirs(save_location, exist_ok = True)
    np.savez(os.path.join(save_location, "layer_%s%s%s" % (str(args.layer+1), "_area_", args.area)), 
        weights = weights, noise_model = noise_model, alphas = alphas, voxels = vox, stories = stories,
        tr_stats = np.array(tr_stats), word_stats = np.array(word_stats), explained_variance=bscorrs)
    with open(os.path.join(save_location, "layer_%s%s%s" % (str(args.layer+1), "_area_", args.area)), 'w') as file:
        data = {
            'max_r2': max(bscorrs),
            'args': vars(args)  # Assuming 'args' is an argparse.Namespace object
        }
        json.dump(data, file, indent=4)
    # else:
    #     save_location = os.path.join(config.MODEL_DIR, args.subject, "_".join(args.area))
    #     os.makedirs(save_location, exist_ok = True)
    #     np.savez(os.path.join(save_location, "layer_%s%s%s" % (str(args.layer+1), "_area_", args.area)), 
    #         weights = weights, alphas = alphas, voxels = vox, stories = stories,
    #         tr_stats = np.array(tr_stats), word_stats = np.array(word_stats), explained_variance=bscorrs)
    #     with open(os.path.join(save_location, "layer_%s%s%s" % (str(args.layer+1), "_area_", args.area)), 'w') as file:
    #         data = {
    #             'max_r2': max(bscorrs),
    #             'args': vars(args)  # Assuming 'args' is an argparse.Namespace object
    #         }
    #         json.dump(data, file, indent=4)