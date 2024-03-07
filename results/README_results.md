To view the results of our project directly, please refer to the [link](https://drive.google.com/drive/folders/1-5dNveVGMdo6cYSLOfDXQnluGyOjEEjo?usp=sharing). Note that the files are large.

For each subject, the data is structured as follows:


    np.savez(os.path.join(save_location, "layer_%s%s%s" % (str(args.layer+1), "_area_", args.area)), 
        weights = weights, noise_model = noise_model, alphas = alphas, voxels = vox, stories = stories,
        tr_stats = np.array(tr_stats), word_stats = np.array(word_stats), explained_variance=bscorrs)
    with open(os.path.join(save_location, "layer_%s%s%s" % (str(args.layer+1), "_area_", args.area)), 'w') as file:
        data = {
            'max_r2': max(bscorrs),
            'args': vars(args) 
        }

subject/
├── brain area/
│   ├── layer1 (file with a dictionary describing arguments used when running train_EM.py-like files)
│   ├── layer1.npz (file with numpy arrays. keys: weights (best regression weights for each voxel), noise_model, alphas (penalty scores for ridge regression), voxels, stories (stories numbers),
        tr_stats, word_stats, explained_variance (best R2 scores)).
│   ├── layer_1_random (file with a dictionary describing arguments used when running train_EM_random.py)
│   ├── layer_1_random.npz (same as above .npz file but for random baseline)
│   └── ...
│   └── ...
├── brain area 2/
├── brain area 3/
└── ...

best_r2_scores.json containes best scores for each layer for each region for each participant.

Below is the information on brain regions data available for each subject:

- Subject 01: AC, ATFP, Broca, cIPL, hMT, IPS, LO, OFA, OPA, pSTS, sPMv, VO
- Subject 02: AC, ATFP, Broca, cIPL, hMT, IPS, LO, OFA, OPA, sPMv, VO
- Subject 03: AC, ATFP, Broca, hMT, IPS, LO, OFA, OPA, sPMv
- Subject 05: AC, Broca, IPS, LO, OFA, OPA, sPMv
- Subject 07: AC, Broca, cIPL, hMT, IPS, LO, OFA, OPA, sPMv
- Subject 08: AC, Broca, cIPL, hMT, IPS, LO, OFA, OPA, sPMv

*The deciphering of the abbreviations is provided in the appendix. 

[2] BOLD fMRI responses in human subjects reading and listening to a set of natural stories. More information can be found in: Deniz, F., Nunez-Elizalde, A.O., Huth, A.G. and Gallant, J.L., 2019. The representation of semantic information across human cerebral cortex during listening versus reading is invariant to stimulus modality. Journal of Neuroscience, 39(39), pp.7722-7736.
Dataset: https://gin.g-node.org/denizenslab/narratives_reading_listening_fmri