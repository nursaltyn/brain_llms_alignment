import os
import numpy as np
import h5py

import config

# def get_resp_orig(subject, stories, stack = True, vox = None):
#     """loads response data
#     """
#     subject_dir = os.path.join(config.DATA_TRAIN_DIR, "train_response", subject)
#     resp = {}
#     for story in stories:
#         resp_path = os.path.join(subject_dir, "%s.hf5" % story)
#         hf = h5py.File(resp_path, "r")
#         resp[story] = np.nan_to_num(hf["data"][:])
#         if vox is not None:
#             resp[story] = resp[story][:, vox]
#         hf.close()
#     if stack: return np.vstack([resp[story] for story in stories]) 
#     else: return resp
    
# edit

def get_resp(resp_path, subject, stories, area=None, stack = True, mode='reading', vox = None, shuffle=False, area_list=False):
    '''
    resp path (str): path to response
    subject (str): subject number in the format "01", "02", etc
    stories (str): list with story numbers
    '''
    path = os.path.join(resp_path, f"{mode}\subject{subject}_{mode}_fmri_data_trn.hdf")
   
    hf_resp = h5py.File(path, "r")
    resp = {}
    for story in stories:
        print("story", story)
        data = hf_resp[f'story_{story}']
        if shuffle == True:
            print("shuffling data")
            shuffled_array = np.random.permutation(hf_resp[f'story_{story}'])
            data = shuffled_array
            
        # trim first and last 10 elements
        resp[story] = data[10:-10]
        resp[story] = np.nan_to_num(resp[story][:])
        # TODO: try to normalize response (0-mean, st.d. 1)
        if area:
            mask = get_mask(area, subject, list=area_list)
            resp[story] = resp[story][:, mask]
    hf_resp.close()
    if stack: return np.vstack([resp[story] for story in stories]) 
    else: return resp
    
def get_resp_eval(resp_path, subject, area=None, stack = True, mode='reading', vox = None): 
    path = os.path.join(resp_path, f"{mode}\subject{subject}_{mode}_fmri_data_val.hdf")
    pass
    

## old function for only one separate brain area 
# def get_mask(area, subject):
#     resp_path = f"C:\\Users\\Nursulu_1\\Downloads\\semantic-decoding\\mappers\\subject{subject}_mappers.hdf"
#     hf = h5py.File(resp_path, "r")
#     dataset = hf[area]
#     mask = dataset[:]
#     hf.close()
#     return mask

def get_mask(areas, subject, list=False):
    '''
    areas :list: a list with the names of brain regions
    subject :str: the number of the subject in the format "01", ..., "09"
    '''
    resp_path = f"C:\\Users\\Nursulu_1\\Downloads\\semantic-decoding\\mappers\\subject{subject}_mappers.hdf"
    hf = h5py.File(resp_path, "r")
    areas_combined = []
    if list == True:
        for area in areas:
            print("getting", area)
            dataset = hf[area]
            mask = dataset[:]
            if len(areas) == 1:
                # take all non-0 values
                mask = [index for index, value in enumerate(mask) if value != 0]
                # mask = mask[mask!=0]
            # if we have a concatenation of areas, take only the most significant pixels
            else:
                # take all values that are 1
                mask = [index for index, value in enumerate(mask) if value == 1]
                # mask = mask[mask==1]
            areas_combined.extend(mask)
    else:
        print("getting", areas)
        dataset = hf[areas]
        mask = dataset[:]
        # take all non-0 values
        mask = [index for index, value in enumerate(mask) if value != 0]
        return mask
    hf.close()
    areas_combined = sorted(areas_combined)
    print("length total mask", len(areas_combined))
    return areas_combined
    