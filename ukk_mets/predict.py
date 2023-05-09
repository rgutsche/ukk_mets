from pathlib import Path
import pandas as pd
import pickle
import os
import numpy as np


#%% Old Version
# def run_prediction(input_path, age):
#
#     # Set some variables
#     base = Path(input_path)
#     pid = base.name
#     age = int(age)
#
#     # Load BRAF and PD-L1 classifiers
#     clf_BRAF = pickle.load(open(Path(os.getcwd()).joinpath('models', 'braf_model.sav'), 'rb'))
#     clf_PDL1 = pickle.load(open(Path(os.getcwd()).joinpath('models', 'pdl1_model.sav'), 'rb'))
#
#     # Load Features
#     df = pd.read_excel(base.joinpath('FEATURES', f'{pid}_features.xlsx')).drop(columns='Unnamed: 0')
#
#
#
#     feature_names_BRAF = ['T1C_original_firstorder_Uniformity',
#                           'T1C_wavelet-LLL_ngtdm_Contrast',
#                           'T1C_log-sigma-3-mm-3D_glcm_DifferenceAverage',
#                           'T1C_log-sigma-3-mm-3D_glcm_Idm',
#                           'T1C_log-sigma-5-mm-3D_glcm_InverseVariance']
#
#     feature_names_PDL1 = ['T1C_original_shape_MeshVolume',
#                           'T1C_original_firstorder_Energy',
#                           'T1C_original_ngtdm_Coarseness',
#                           'T1C_wavelet-LLL_glcm_MCC']
#
#     features_BRAF = df[feature_names_BRAF].iloc[-1:]
#     features_BRAF.insert(0, 'age', age)
#
#     features_PDL1 = df[feature_names_PDL1].iloc[-1:]
#
#     # Standardize Features
#     mean_vals_BRAF = np.array([59.866, 0.0450, 0.246, 1.290, 0.543, 0.455])
#     sd_vals_BRAF = np.array([12.228, 0.020, 0.179, 0.542, 0.113, 0.052])
#
#     mean_vals_PDL1 = np.array([24626.260, 86706.990, 0.001143, 0.864755])
#     sd_vals_PDL1 = np.array([29142.058, 75423.971, 0.000706, 0.067249])
#
#     features_BRAF = (features_BRAF - mean_vals_BRAF)/sd_vals_BRAF
#     features_PDL1 = (features_PDL1 - mean_vals_PDL1)/sd_vals_PDL1
#
#     # Prediction
#     predictions_BRAF = clf_BRAF.predict(features_BRAF)  # threshold 0.5
#     probabilities_BRAF = clf_BRAF.predict_proba(features_BRAF)
#
#     threshold_BRAF = 0.6
#     if probabilities_BRAF[0][1] < threshold_BRAF:
#         prediction_BRAF_2 = 0
#     else:
#         prediction_BRAF_2 = 1
#
#     predictions_PDL1 = clf_PDL1.predict(features_PDL1)  # threshold 0.5
#     probabilities_PDL1 = clf_PDL1.predict_proba(features_PDL1)
#
#     threshold_PDL1 = 0.73109
#     if probabilities_PDL1[0][1] < threshold_PDL1:
#         prediction_PDL1_2 = 0
#     else:
#         prediction_PDL1_2 = 1
#
#     dic = {'pid': pid,
#            'BRAF_pred_thresh_default': int(predictions_BRAF.item()),
#            'BRAF_pred_thresh_best': int(prediction_BRAF_2),
#            'BRAF_prob_wt': probabilities_BRAF[0][0], 'BRAF_prob_mut': probabilities_BRAF[0][1],
#            'PDL1_pred_thresh_default': int(predictions_PDL1.item()),
#            'PDL1_pred_thresh_best': int(prediction_PDL1_2),
#            'PDL1_prob_wt': probabilities_PDL1[0][0], 'PDL1_prob_mut': probabilities_PDL1[0][1]}
#
#     # Save output
#     output = base.joinpath('PREDICTION')
#     if not output.is_dir():
#         output.mkdir(parents=True)
#
#     pd.Series(dic).to_excel(output.joinpath(f'{pid}_prediction.xlsx'))


#%% New Version

base = Path('/Users/robin/Desktop')
pid = '5704938'
age = 60

def run_prediction(input_path, age):

    # Set some variables
    base = Path(input_path)
    pid = base.name
    age = int(age)

    # Load BRAF and PD-L1 classifiers
    clf_BRAF = pickle.load(open(Path(os.getcwd()).joinpath('models', 'braf_model.sav'), 'rb'))
    clf_PDL1 = pickle.load(open(Path(os.getcwd()).joinpath('models', 'pdl1_model.sav'), 'rb'))

    # Load Features and Feature Names
    feature_names = {
        'BRAF': ['T1C_original_firstorder_Uniformity',
                 'T1C_wavelet-LLL_ngtdm_Contrast',
                 'T1C_log-sigma-3-mm-3D_glcm_DifferenceAverage',
                 'T1C_log-sigma-3-mm-3D_glcm_Idm',
                 'T1C_log-sigma-5-mm-3D_glcm_InverseVariance'],

        'PDL1': ['T1C_original_shape_MeshVolume',
                 'T1C_original_firstorder_Energy',
                 'T1C_original_ngtdm_Coarseness',
                 'T1C_wavelet-LLL_glcm_MCC']
    }

    mean_vals = {
        'BRAF': np.array([59.866, 0.0450, 0.246, 1.290, 0.543, 0.455]),
        'PDL1': np.array([24626.260, 86706.990, 0.001143, 0.864755])
    }

    sd_vals = {
        'BRAF': np.array([12.228, 0.020, 0.179, 0.542, 0.113, 0.052]),
        'PDL1': np.array([29142.058, 75423.971, 0.000706, 0.067249])
    }

    # Load Features
    df = pd.read_excel(base.joinpath('FEATURES', f'{pid}_features.xlsx')).drop(columns='Unnamed: 0')

    # Extract Features
    result = []
    features = {}
    for cancer_type in ['BRAF', 'PDL1']:
        feature_names_cancer = feature_names[cancer_type]
        features_cancer = df[feature_names_cancer].iloc[-1:]
        if cancer_type == 'BRAF':
            features_cancer.insert(0, 'age', age)
        features_cancer = (features_cancer - mean_vals[cancer_type]) / sd_vals[cancer_type]
        features[cancer_type] = features_cancer

        # Prediction
        clf_cancer = clf_BRAF if cancer_type == 'BRAF' else clf_PDL1
        predictions = clf_cancer.predict(features_cancer)  # threshold 0.5
        probabilities = clf_cancer.predict_proba(features_cancer)
        threshold = 0.56638 if cancer_type == 'BRAF' else 0.73109
        if probabilities[0][1] < threshold:
            prediction_2 = 0
        else:
            prediction_2 = 1

        # Build dictionary

        if cancer_type == 'BRAF':
            dic = {'pid': pid,
                   f'{cancer_type}_pred_thresh_default': int(predictions.item()),
                   f'{cancer_type}_pred_thresh_best': int(prediction_2),
                   f'{cancer_type}_prob_wt': probabilities[0][0],
                   f'{cancer_type}_prob_mut': probabilities[0][1]}
        else:
            dic = {f'{cancer_type}_pred_thresh_default': int(predictions.item()),
                   f'{cancer_type}_pred_thresh_best': int(prediction_2),
                   f'{cancer_type}_prob_wt': probabilities[0][0],
                   f'{cancer_type}_prob_mut': probabilities[0][1]}
        result.append(pd.Series(dic))

    output = base.joinpath('PREDICTION')
    if not output.is_dir():
        output.mkdir(parents=True)

    pd.concat(result, axis=0).to_excel(output.joinpath(f'{pid}_prediction.xlsx'))

