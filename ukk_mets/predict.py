from pathlib import Path
import pandas as pd
import pickle
import os
import numpy as np

# pid = '5704938'
# input_path = '/Users/robin/data/ukk_mets/5704938'
# age = 70


def run_prediction(input_path, age):
    base = Path(input_path)
    pid = base.name
    age = int(age)

    clf = pickle.load(open(Path(os.getcwd()).joinpath('models', 'braf_model.sav'), 'rb'))

    df = pd.read_excel(base.joinpath('FEATURES', f'{pid}_features.xlsx')).drop(columns='Unnamed: 0')

    feature_names = ['T1C_original_firstorder_Uniformity',
                     'T1C_wavelet-LLL_ngtdm_Contrast',
                     'T1C_log-sigma-3-mm-3D_glcm_DifferenceAverage',
                     'T1C_log-sigma-3-mm-3D_glcm_Idm',
                     'T1C_log-sigma-5-mm-3D_glcm_InverseVariance']

    features = df[feature_names].iloc[-1:]
    features.insert(0, 'age', age)

    mean_vals = np.array([59.866, 0.0450, 0.246, 1.290, 0.543, 0.455])
    sd_vals = np.array([12.228, 0.020, 0.179, 0.542, 0.113, 0.052])

    features = (features - mean_vals)/sd_vals
    predictions = clf.predict(features)
    probabilities = clf.predict_proba(features)

    dic = {'pid': pid, 'pred': int(predictions.item()), 'prob_wt': probabilities[0][0], 'prob_mut': probabilities[0][1]}

    output = base.joinpath('PREDICTION')
    if not output.is_dir():
        output.mkdir(parents=True)

    pd.DataFrame(dic).to_excel(output.joinpath(f'{pid}_prediction.xlsx'))

