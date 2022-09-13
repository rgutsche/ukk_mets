from pathlib import Path
import pandas as pd
import pickle
import os

pid = '5704938'


def run_prediction(input_path, age):
    base = Path(input_path)
    pid = base.name
    age = int(age)

    clf = pickle.load(open(Path(os.getcwd()).joinpath('models', 'braf_model.sav'), 'rb'))

    df = pd.read_excel(base.joinpath(pid, 'FEATURES', f'{pid}_features.xlsx')).drop(columns='Unnamed: 0')

    feature_names = ['T1C_original_firstorder_Uniformity',
                    'T1C_wavelet-LLL_ngtdm_Contrast',
                    'T1C_log-sigma-3-mm-3D_glcm_DifferenceAverage',
                    'T1C_log-sigma-3-mm-3D_glcm_Idm',
                    'T1C_log-sigma-5-mm-3D_glcm_InverseVariance']

    features = df[feature_names]

    clf =

    predictions = clf.predict(features)
    probabilities = clf.predict_proba(features)

    threshold = ?



    pass

