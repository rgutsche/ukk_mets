import argparse

parser = argparse.ArgumentParser(description="Test Feature Extraction")
parser.add_argument('-path', type=str, required=True, help='Path to Patient Folder')
parser.add_argument('-pid', type=str, required=True, help='Patient ID')
args = parser.parse_args()

user_input_path = args.path
pid = args.pid


#%%
from pathlib import Path
import pandas as pd
import SimpleITK as sitk
from radiomics import featureextractor
import logging
logger = logging.getLogger("radiomics.glcm")
logger.setLevel(logging.ERROR)

# 1) Define paths
# base = Path('/Volumes/btu-ai/data/test')
base = Path(user_input_path)
# pid = 'FE1BP454M-BI'
img_path = base.joinpath(pid, f'{pid}_0001.nii.gz')
mask_path = base.joinpath(pid, f'{pid}_mr_segmentation.nii.gz')

sitk_img = sitk.ReadImage(str(img_path))
sitk_mask = sitk.ReadImage(str(mask_path), sitk.sitkUInt8)

# 2) Feature Extractor Settings
settings = {'normalize': True,
            'resample': [1, 1, 1],
            'binWidth': 0.1,
            'preCrop': True,
            'correctMask': True}

extractor = featureextractor.RadiomicsFeatureExtractor(**settings)
# extractor.enableFeatureClassByName('shape', enabled=False)
extractor.enableImageTypes(Wavelet={}, LoG={'sigma': [ 1, 2, 3, 4, 5 ]})


def remove_diagnostic_features(feature_dic):
    for x in [key for key, value in feature_dic.items() if key.startswith('diagnostics_')]:
        feature_dic.pop(x)
    return feature_dic

# 3) Extract Features
extracted_features = extractor.execute(sitk_img, sitk_mask, label=1)

extracted_features = remove_diagnostic_features(extracted_features)
extracted_features = dict(['T1KM_' + key, float(value) ] for key, value in extracted_features.items())
extracted_features = pd.DataFrame().from_dict(extracted_features, orient='index').T

extracted_features.to_excel(base.joinpath(pid, f'{pid}_features_v2.xlsx'))