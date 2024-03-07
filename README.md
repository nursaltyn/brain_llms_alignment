This seminar project is dedicated to aligning brain activations during fMRI reading with hidden states of Large Language Models. In this project, the variance explained by different brain regions in different layers of GPT was estimated. 

# Usage

## 1. Getting data

1. Download [training and test](https://gin.g-node.org/denizenslab/narratives_reading_listening_fmri/src/master/responses) brain response data and save the files into  `data_train/train_response/reading` and `data_test/test_response/reading` directories, correspondingly. [2]

2. Download [train and test stimuli](https://drive.google.com/drive/folders/16_djOe_jhVRxXQieyBEN2pCgItwFYGQt?usp=drive_link) and save the files into `data_train/train_stimulus` and `data_test/test_stimulus` directories, correspondingly. [3]

3. Download [mappers](https://gin.g-node.org/denizenslab/narratives_reading_listening_fmri/src/master/mappers) files with voxel-wise brain regions data for participants and save them in the folder "mappers". [2]

4. Download [custom language model](https://utexas.box.com/shared/static/7ab8qm5e3i0vfsku0ee4dc6hzgeg7nyh.zip) data and extract contents into new data_lm/ directory. [1] 
In this project, we will only work with "perceived" model.

3. Download [test data](https://utexas.box.com/shared/static/ae5u0t3sh4f46nvmrd3skniq0kk2t5uh.zip) and extract contents into new `data_test/` directory. Stimulus data for `test_stimulus/[EXPERIMENT]` and response data for `test_response/[SUBJECT_ID]` can be downloaded from [OpenNeuro](https://openneuro.org/datasets/ds004510/). [3]


Note: the paths have to be adjusted to be run on your computer. This will soon be fixed.

## 2. Estimate the encoding model. 

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

The following .py files are provided:

--train_EM_swapped.py: to learn a linear map for the chosen combination of subject-brain region-layer.

--train_EM_speech_network.py: learn a map for speech network: Auditory Cortex (AC), Broca's area, Superior Ventral Premotor Speech Area (sPMv).

--train_EM_parietal_network.py: learn a map for parietal network: Intraparietal Sulcus (IPS), Caudal Inferior Parietal Lobe (cIPL).  

--train_EM_temporal_network.py: learn a map for temporal network: Human Middle Temporal Area (hMT), Anterior Temporal Face Patch (ATFP), Posterior Superior Temporal Sulcus (pSTS).  

--train_EM_occipital_network.py: learn a map for occipital network: Lateral Occipital Complex (LO), Occipital Face Area (OFA), Occipital Place Area (OPA).

The areas were chosen based on the availability of the data for voxels of the regions for each participant. Not all subject's mappers contain information about all the regions. Below is the information on brain regions data available for each subject:

- Subject 01: 

## Results

To view the results of our project directly, please refer to the link.

#### Data and code references:

[1] Tang, J., LeBel, A., Jain, S. et al. Semantic reconstruction of continuous language from non-invasive brain recordings. Nat Neurosci 26, 858–866 (2023). https://doi.org/10.1038/s41593-023-01304-9
Code: https://www.nature.com/articles/s41593-023-01304-9#data-availability

[2] BOLD fMRI responses in human subjects reading and listening to a set of natural stories. More information can be found in: Deniz, F., Nunez-Elizalde, A.O., Huth, A.G. and Gallant, J.L., 2019. The representation of semantic information across human cerebral cortex during listening versus reading is invariant to stimulus modality. Journal of Neuroscience, 39(39), pp.7722-7736.
Dataset: https://gin.g-node.org/denizenslab/narratives_reading_listening_fmri

[3] Amanda LeBel and Lauren Wagner and Shailee Jain and Aneesh Adhikari-Desai and Bhavin Gupta and Allyson Morgenthal and Jerry Tang and Lixiang Xu and Alexander G. Huth (2024). An fMRI dataset during a passive natural language listening task. OpenNeuro. [Dataset] doi: doi:10.18112/openneuro.ds003020.v2.2.0
Dataset: https://openneuro.org/datasets/ds003020/versions/2.2.0.


#### Appendix

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