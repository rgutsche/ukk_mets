import argparse
from ukk_mets.preprocess import run_preprocess
from ukk_mets.feature_extraction import run_extraction
from ukk_mets.predict import run_prediction


def main():
    parser = argparse.ArgumentParser(description="Prediction of Metastases Genotype with Radiomics")
    parser.add_argument('-preprocess', type=str, required=True, help='"Y" or "N" if files need to be preprocessed')
    parser.add_argument('-input_path', type=str, required=True, help='path to patient folder with dicom or nifti files')

    args = parser.parse_args()

    preprocess_user_input = args.preprocess
    input_path = args.input_path

    if preprocess_user_input == 'Y' or preprocess_user_input == 'y':
        run_preprocess(input_path)
    else:
        print('| Skip preprocessing and start feature extraction |')
        run_extraction(input_path)
        # print(f'| Use this path for prediction: {input_path}')
        run_prediction(input_path)


# def predict():
#     parser = argparse.ArgumentParser(description="Test - Bla \n Bla Bla \n 12345")
#         #
#         # parser.add_argument('-input_t1c', type=str, required=True, help='path to patient folder with dicom files')
#         # parser.add_argument('-input_t2', type=str, required=True, help='path to patient folder with dicom files')
#         # parser.add_argument('-input_flair', type=str, required=True, help='path to patient folder with dicom files')
#         #
#
#     parser.add_argument('-input_nifties', type=str, required=True, help='path to patient folder with niftie files')
#
#
#     # parser.add_argument('-output', type=str, required=True, help='path to patient folder')
#     # Use a breakpoint in the code line below to debug your script.
#
#     args = parser.parse_args()
#     path_input = args.input
#
#     print(f'{path_input}')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # preprocess_user_input = input('Preprocess Y/N?')
    main()

    # if preprocess_user_input == 'Y' or preprocess_user_input == 'y':
    #     preprocess()
    # else:
    #     predict()
    # print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
