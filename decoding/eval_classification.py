import os
import numpy as np
import json
import argparse

import config
from utils_resp.utils_resp import get_resp, get_mask, get_resp_eval
np.random.seed(42)

from GPT import GPT
from StimulusModel import LMFeatures
from utils_stim import get_stim, get_stim_eval
import random
from sklearn.metrics.pairwise import cosine_similarity


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--subject", type = str, required = True) #'01' to '09'
    parser.add_argument("--layer", type = int) #layer from 0 to 11
    parser.add_argument("--area", type = str) #brain area
    # parser.add_argument("--area_list", type = bool, default=True) #to list
    parser.add_argument("--mode", type = str, default = "reading")
    args = parser.parse_args()
    
    resp_path = r"C:\Users\Nursulu_1\Downloads\semantic-decoding\data_test\test_response"
    stories = ['11']
    
    resp_eval = get_resp_eval(resp_path, args.subject, area=args.area, stack = False, mode=args.mode, vox = None, area_list=False)
    # two validation stories, take average prediction
    resp_eval = sum([resp_eval[i] for i in resp_eval])/2
    
    # load weights
    weight_path = f"C:\\Users\\Nursulu_1\\Downloads\\semantic-decoding\\models\\{args.subject}\\{args.area}\layer_{args.layer+1}_area_{args.area}.npz"
    ws_data = np.load(weight_path)
    ws = ws_data['weights']
    ws.shape
    
    # prediction
    pred = resp_eval.dot(ws)
    
    gpt = "perceived"
    # load gpt
    with open(os.path.join(config.DATA_LM_DIR, gpt, "vocab.json"), "r") as f:
        gpt_vocab = json.load(f)
        
    gpt = GPT(path = os.path.join(config.DATA_LM_DIR, gpt, "model"), vocab = gpt_vocab, device = config.GPT_DEVICE)
    # can change the layer manually, also context size
    features = LMFeatures(model=gpt, layer=args.layer, context_words = config.GPT_WORDS)

    test, tr_stats, word_stats = get_stim_eval(stories, features, segment=True, context=5)
    
    acc_2v2 = []
    for i in range(test.shape[0]):
        # filter current row
        vals = [num for num in range(test.shape[0]) if num != i]
        # Choose a random integer from the filtered list
        random_int = np.random.choice(vals)
            
        rand_stim = test[random_int]
        sim_true = cosine_similarity(pred[i].reshape(1, -1), test[i].reshape(1, -1))
        sim_false = cosine_similarity(pred[i].reshape(1, -1), rand_stim.reshape(1, -1))
        # print("true", sim_true, "false", sim_false)
        if sim_true > sim_false:
            acc_2v2.append(1)
            
    avg_acc = sum(acc_2v2)/test.shape[0]
    print("2v2 accuracy", avg_acc)
    save_location = os.path.join(config.MODEL_DIR, "eval", args.mode, args.subject, args.area)
    os.makedirs(save_location, exist_ok = True)
    with open(os.path.join(save_location, "layer_%s" % (str(args.layer+1))), 'w') as file:
        data = {
            'acc_2v2': avg_acc,
            'args': vars(args)  
        }
        json.dump(data, file, indent=4)
