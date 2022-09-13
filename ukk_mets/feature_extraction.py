from pathlib import Path
import pandas as pd
import numpy as np
import SimpleITK as sitk
from tqdm import tqdm
from radiomics import featureextractor
import logging

logger = logging.getLogger("radiomics.glcm")
logger.setLevel(logging.ERROR)

#%%


def remove_diagnostic_features(feature_dic):
    for x in [key for key, value in feature_dic.items() if key.startswith('diagnostics_')]:
        feature_dic.pop(x)
    return feature_dic


def insert_meta(df, pid, bw, label):
    df.insert(0, 'pid', pid)
    df.insert(1, 'bin_width', bw)
    df.insert(2, 'Label', label)


def calculate_features(sitk_image, sitk_mask, label=1, sequence='T1C', bw=0.1):

    settings = {'normalize': True,
                'resample': [1, 1, 1],
                'binWidth': bw,
                'preCrop': True,
                'correctMask': True}

    extractor = featureextractor.RadiomicsFeatureExtractor(**settings)
    extractor.enableImageTypes(Wavelet={}, LoG={'sigma': [1, 2, 3, 4, 5]})
    extracted_features = extractor.execute(sitk_image, sitk_mask, label=label)
    extracted_features = remove_diagnostic_features(extracted_features)
    extracted_features = dict([f'{sequence}_' + key, float(value)] for key, value in extracted_features.items())
    features = pd.DataFrame().from_dict(extracted_features, orient='index').T
    return features


# input_path = '/Users/robin/data/UKK_METS'
# pid = '5704938'

def run_extraction(input_path):
    base = Path(input_path)
    pid = base.name

    segmentation = base.joinpath('IMG_DATA', f'{pid}_tum_seg.nii.gz')
    sitk_seg = sitk.ReadImage(str(segmentation))

    segmentation_array = sitk.GetArrayFromImage(sitk_seg)
    labels = list(np.unique(segmentation_array)[1:])
    if len(labels) > 1:
        labels.insert(len(labels), 4)
        for label in labels[:-1]:
            segmentation_array[segmentation_array == label] = 4
        combined_seg = sitk.GetImageFromArray(segmentation_array)
        combined_seg.CopyInformation(sitk_seg)

    sequences = ['T1C', 'T2', 'FLAIR']

    dfs_features = []
    for label in labels:
        calculated_features = []
        for i, sequence in tqdm(enumerate(sequences)):
            image = base.joinpath('IMG_DATA', f'{pid}_000{i+1}.nii.gz')
            sitk_img = sitk.ReadImage(str(image))

            if label == 4:
                orig_features = calculate_features(sitk_img, combined_seg, label=label, sequence=sequence, bw=0.1)
            else:
                orig_features = calculate_features(sitk_img, sitk_seg, label=label, sequence=sequence, bw=0.1)
            insert_meta(orig_features, pid, bw=0.1, label=label)
            calculated_features.append(orig_features)

        temp_df = pd.concat(calculated_features, axis=0).reset_index(drop=True)
        dfs_features.append(temp_df)
    final_df = pd.concat(dfs_features, axis=0).reset_index(drop=True)

    features_dir = base.joinpath('FEATURES')
    if not features_dir.is_dir():
        features_dir.mkdir(parents=True)

    final_df.to_excel(features_dir.joinpath(f'{pid}_features.xlsx'))


# PATH = Path('/Volumes/Gutsche/data')
# PATH_IMAGES = PATH.joinpath('intermediate', 'BRAF', 'BRAF_cropped')
# PATH_OUTPUT = PATH.joinpath('processed', 'BRAF')
# PATH_STATUS = PATH.joinpath('raw', 'patient_lists', 'BRAF', 'BRAF_test_set.xlsx')
#
# #%%
# df_status = pd.read_excel(PATH_STATUS, dtype=str)
# pids = df_status['Forget'].dropna().reset_index(drop=True)
#
#

#
#
# dfs = []
#
# # pid = pids[0]
# for i, pid in tqdm(enumerate(pids)):
#     t1_path = str(PATH_IMAGES.joinpath(f'{pid}_T1_image.nii.gz'))
#     mask_path = str(PATH_IMAGES.joinpath(f'{pid}_T1_mask.nii.gz'))
#
#     sitk_t1 = sitk.ReadImage(t1_path)
#     sitk_mask = sitk.ReadImage(mask_path, sitk.sitkUInt8)
#     resample = tio.Resample(1)
#
#     sitk_t1_res = resample(sitk_t1)
#     sitk_mask_res = resample(sitk_mask)
#
#     layer = int(sitk_t1_res.GetDepth()/2)
#     fig, axs = plt.subplots(nrows=1, ncols=2)
#     axs[0].imshow(sitk.GetArrayFromImage(sitk_t1_res)[:, :, layer], cmap='gray')
#     axs[0].set_title('t1_orig')
#     axs[1].imshow(sitk.GetArrayFromImage(sitk_mask_res)[:, :, layer], cmap='gray')
#     axs[1].set_title('mask_orig')
#     plt.savefig(PATH_OUTPUT.joinpath('plots', 'cropped_transformed', f'{pid}.png'), dpi=300)
#
#     t1_features_orig = extract_features(sitk_t1_res, sitk_mask_res)
#     df_t1 = pd.DataFrame()
#     df_t1 = df_t1.from_dict(t1_features_orig, orient='index').T
#     df_t1.insert(0, 'pid', pid)
#     dfs.append(df_t1)
#
# final_df = pd.concat(dfs, ignore_index=True)
# final_df.to_excel(PATH_OUTPUT.joinpath('features', 'rsmp1mm_bw010_test_set_t1_lastpid.xlsx'))


