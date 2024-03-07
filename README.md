This seminar project is dedicated to aligning brain activations during fMRI reading with hidden states of Large Language Models. In this project, the variance explained by different brain regions in different layers of GPT was estimated. 

Note: the paths have to be adjusted to be run on your computer. This will soon be fixed.

# Usage

## 1. Getting data

1. Download [training and test](https://gin.g-node.org/denizenslab/narratives_reading_listening_fmri/src/master/responses) brain response data and save the files into  `data_train/train_response/reading` and `data_test/test_response/reading` directories, correspondingly. [2]

2. Download [train and test stimuli](https://drive.google.com/drive/folders/16_djOe_jhVRxXQieyBEN2pCgItwFYGQt?usp=drive_link) and save the files into `data_train/train_stimulus` and `data_test/test_stimulus` directories, correspondingly. [3]

3. Download [mappers](https://gin.g-node.org/denizenslab/narratives_reading_listening_fmri/src/master/mappers) files with voxel-wise brain regions data for participants and save them in the folder "mappers". [2]

4. Download [custom language model](https://utexas.box.com/shared/static/7ab8qm5e3i0vfsku0ee4dc6hzgeg7nyh.zip) data and extract contents into new data_lm/ directory. [1] 
In this project, we will only work with "perceived" model.

3. Download [test data](https://utexas.box.com/shared/static/ae5u0t3sh4f46nvmrd3skniq0kk2t5uh.zip) and extract contents into new `data_test/` directory. Stimulus data for `test_stimulus/[EXPERIMENT]` and response data for `test_response/[SUBJECT_ID]` can be downloaded from [OpenNeuro](https://openneuro.org/datasets/ds004510/). [3]

## 2. Estimating the encoding model 

In this step, we learn a linear map from brain activations to GPT layers using bootstrap ridge regression. 

Below is an example of a code to obtain a

```bash
python encoding/train_EM_swapped.py --subject '01' --layer '0' --area 'roi_mask_Broca'
```
--subject takes the number of a subject to estimate model for (str). Ranges from "01" to "09". 

Note: fine-grained brain regions data is provided only for subjects "01", "02", "03", "05", "07", "08".

--layer takes arguments from 0 to 11, corresponding to 12 layers of GPT model.

--area takes brain regions that should be mapped to the GPT layer. It can either take a string (for one individual region) or list (for a concatenation of regions).

We provide .bat scripts to run .py files automatically. 

### 2.1. Available .py files

The following .py files are provided:

--train_EM_swapped.py: to learn a linear map for the chosen combination of subject-brain region-layer.

--train_EM_speech_network.py: learn a map for speech network: Auditory Cortex (AC), Broca's area, Superior Ventral Premotor Speech Area (sPMv).

--train_EM_parietal_network.py: learn a map for parietal network: Intraparietal Sulcus (IPS), Caudal Inferior Parietal Lobe (cIPL).  

--train_EM_temporal_network.py: learn a map for temporal network: Human Middle Temporal Area (hMT), Anterior Temporal Face Patch (ATFP), Posterior Superior Temporal Sulcus (pSTS).  

--train_EM_occipital_network.py: learn a map for occipital network: Lateral Occipital Complex (LO), Occipital Face Area (OFA), Occipital Place Area (OPA).

--train_EM_random.py: learn a map while shuffling the vectors for brain response (random baseline)

--train_EM_no_delays.py: learn a map without delay matrices for text stimuli

### 2.2. Available brain regions

The areas were chosen based on the availability of the data for voxels of the regions for each participant. Not all subject's mappers contain information about all the regions. Below is the information on brain regions data available for each subject:

- Subject 01: AC, ATFP, Broca, cIPL, hMT, IPS, LO, OFA, OPA, pSTS, sPMv, VO
- Subject 02: AC, ATFP, Broca, cIPL, hMT, IPS, LO, OFA, OPA, sPMv, VO
- Subject 03: AC, ATFP, Broca, hMT, IPS, LO, OFA, OPA, sPMv
- Subject 05: AC, Broca, IPS, LO, OFA, OPA, sPMv
- Subject 07: AC, Broca, cIPL, hMT, IPS, LO, OFA, OPA, sPMv
- Subject 08: AC, Broca, cIPL, hMT, IPS, LO, OFA, OPA, sPMv

*The deciphering of the abbreviations is provided in the appendix. 

## 3. Results

To view the results of our project directly, please refer to the [link](https://drive.google.com/drive/folders/1-5dNveVGMdo6cYSLOfDXQnluGyOjEEjo?usp=sharing). Note that the files are large.

#### Data and code references:

[1] Tang, J., LeBel, A., Jain, S. et al. Semantic reconstruction of continuous language from non-invasive brain recordings. Nat Neurosci 26, 858–866 (2023). https://doi.org/10.1038/s41593-023-01304-9
Code: https://github.com/HuthLab/semantic-decoding

[2] BOLD fMRI responses in human subjects reading and listening to a set of natural stories. More information can be found in: Deniz, F., Nunez-Elizalde, A.O., Huth, A.G. and Gallant, J.L., 2019. The representation of semantic information across human cerebral cortex during listening versus reading is invariant to stimulus modality. Journal of Neuroscience, 39(39), pp.7722-7736.
Dataset: https://gin.g-node.org/denizenslab/narratives_reading_listening_fmri

[3] Amanda LeBel and Lauren Wagner and Shailee Jain and Aneesh Adhikari-Desai and Bhavin Gupta and Allyson Morgenthal and Jerry Tang and Lixiang Xu and Alexander G. Huth (2024). An fMRI dataset during a passive natural language listening task. OpenNeuro. [Dataset] doi: doi:10.18112/openneuro.ds003020.v2.2.0
Dataset: https://openneuro.org/datasets/ds003020/versions/2.2.0.


## Appendix

### Brain regions and their size (voxels)

    /roi_mask_AC: Auditory Cortex [2300]
    /roi_mask_ATFP: Anterior Temporal Face Patch [42]
    /roi_mask_Broca: Broca's Area [371]
    /roi_mask_EBA: Extrastriate Body Area [311]
    /roi_mask_FEF: Frontal Eye Fields [478]
    /roi_mask_FFA: Fusiform Face Area [327]
    /roi_mask_FO: Fusiform Gyrus [271]
    /roi_mask_IFSFP: Inferior Frontal Sulcus Face Patch [310]
    /roi_mask_IPS: Intraparietal Sulcus [1076]
    /roi_mask_LO: Lateral Occipital Complex [291]
    /roi_mask_M1F: Primary Motor Cortex - Feet Region [241]
    /roi_mask_M1H: Primary Motor Cortex - Hand Region [228]
    /roi_mask_M1M: Primary Motor Cortex - Mouth Region [339]
    /roi_mask_OFA: Occipital Face Area [167]
    /roi_mask_OPA: Occipital Place Area [219]
    /roi_mask_PMvh: Ventral Premotor Cortex - Hand Region [37]
    /roi_mask_PPA: Parahippocampal Place Area [178]
    /roi_mask_RSC: Retrosplenial Cortex [285]
    /roi_mask_S1F: Primary Somatosensory Cortex - Face Region [182]
    /roi_mask_S1H: Primary Somatosensory Cortex - Hand Region [497]
    /roi_mask_S1M: Primary Somatosensory Cortex - Mouth Region [459]
    /roi_mask_SEF: Supplementary Eye Fields [51]
    /roi_mask_SMFA: Supplementary Motor Foot Area [113]
    /roi_mask_SMHA: Supplementary Motor Hand Area [154]
    /roi_mask_V1: Primary Visual Cortex (Area 1) [674]
    /roi_mask_V2: Secondary Visual Cortex (Area 2) [613]
    /roi_mask_V3: Tertiary Visual Cortex (Area 3) [638]
    /roi_mask_V3A: Visual Area 3A [149]
    /roi_mask_V3B: Visual Area 3B [212]
    /roi_mask_V4: Visual Area 4 [471]
    /roi_mask_V7: Visual Area 7 [173]
    /roi_mask_VO: Ventral Occipital Cortex [157]
    /roi_mask_cIPL: Caudal Inferior Parietal Lobe[785]
    /roi_mask_hMT: Human Middle Temporal Area [129]
    /roi_mask_pIC: Posterior Insular Cortex [40]
    /roi_mask_pSTS: Posterior Superior Temporal Sulcus [426]
    /roi_mask_sPMv: Superior Ventral Premotor Speech Area [305]

* Please note that the ROI masks are taken from [2], but we haven't found their descriptions. Therefore, our deciphering might be misaligned with the actual meaning of the mask. We tried to proof-read the abbreviations in other neuroscience works.

### Story names 

The names of the stimulus data from [2] and correspondong story names from [3]:

- story_01 = alternateithicatom
- story_02 = avatar
- story_03 = howtodraw
- story_04 = legacy
- story_05 = life
- story_06 = myfirstdaywiththeyankees
- story_07 = naked
- story_08 = odetostepfather
- story_09 = souls
- story_10 = undertheinfluence
- story_11 = wheretheressmoke

