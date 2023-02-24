from ukk_mets.feature_extraction import run_extraction
from ukk_mets.preprocess import run_preprocess
from ukk_mets.predict import run_prediction
import argparse


def main():
    parser = argparse.ArgumentParser(description="Prediction of Metastases Genotype with Radiomics")
    parser.add_argument('-preprocess', type=str, required=True, help='"Y" or "N" if files need to be preprocessed')
    parser.add_argument('-feat_extract', type=str, required=True, help='"Y" or "N" if features need to be extracted')
    parser.add_argument('-age', type=str, required=True, help='patient age important for the prediction')
    parser.add_argument('-input_path', type=str, required=True, help='path to patient folder with dicom or nifti files')

    args = parser.parse_args()

    preprocess_user_input = args.preprocess
    input_path = args.input_path
    age = args.age
    extract = args.feat_extract

    if preprocess_user_input == 'Y' or preprocess_user_input == 'y':
        run_preprocess(input_path)
        return

    if extract == 'Y' or extract == 'y':
        run_extraction(input_path)

    run_prediction(input_path, age)


if __name__ == '__main__':
    main()
