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
    if sequence != 'T1C':
        extractor.enableFeatureClassByName('shape', enabled=False)
    extractor.enableImageTypes(Wavelet={}, LoG={'sigma': [1, 2, 3, 4, 5]})
    extracted_features = extractor.execute(sitk_image, sitk_mask, label=label)
    extracted_features = remove_diagnostic_features(extracted_features)
    extracted_features = dict([f'{sequence}_' + key, float(value)] for key, value in extracted_features.items())
    features = pd.DataFrame().from_dict(extracted_features, orient='index').T
    return features


def save_preview():
    pass

# input_path = '/Users/robin/data/UKK_METS'
# pid = '5704938'

#%%
def run_extraction(input_path):
    base = Path(input_path)
    pid = base.name

    segmentation = base.joinpath('IMG_DATA', f'{pid}_tum_seg.nii.gz')
    sitk_seg = sitk.ReadImage(str(segmentation),  sitk.sitkUInt8)

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
            print('Bis hierhin ok!')
            sitk_img = sitk.ReadImage(str(image), sitk.sitkUInt8)
            if label == 4:
                orig_features = calculate_features(sitk_img, combined_seg, label=int(label), sequence=sequence, bw=0.1)
            else:
                print('Bis hier auch ok!')
                orig_features = calculate_features(sitk_img, sitk_seg, label=int(label), sequence=sequence, bw=0.1)
                print('Extraction klappt')

            calculated_features.append(orig_features)
        temp_df = pd.concat(calculated_features, axis=1).reset_index(drop=True)
        insert_meta(temp_df, pid, bw=0.1, label=label)
        dfs_features.append(temp_df)
    final_df = pd.concat(dfs_features, axis=0).reset_index(drop=True)

    features_dir = base.joinpath('FEATURES')
    if not features_dir.is_dir():
        features_dir.mkdir(parents=True)

    final_df.to_excel(features_dir.joinpath(f'{pid}_features.xlsx'))