from pathlib import Path
from ukk_mets.util import convert_to_nii
import logging


def run_preprocess(input_path):
    base = Path(input_path)
    pid = base.parent
    log_file = base.joinpath(f'{pid}.log')

    logging.basicConfig(filename=log_file,
                        filemode='w', format='%(name)s - %(levelname)s - %(message)s')

    logging.warning(f'Start preprocessing for patient: {pid}')

    sequences = ['T1C', 'T2', 'FLAIR']
    for sequence in sequences:
        dicom_dir = base.joinpath('DICOM', sequence)
        out_dir = base.joinpath('NIFTI', sequence)
        out_file = f'{sequence}'

        if not out_dir.is_dir():
            out_dir.mkdir(parents=True)

        logging.warning(f'PID: {pid}. convert {sequence} to nifti')

        convert_to_nii(str(dicom_dir), str(out_dir), str(out_file))

        try:
            file = [x for x in out_dir.glob(f'{sequence}*')][0]
        except IndexError:
            logging.error(f'Error! Files not converted for patient: {pid} | sequence: {sequence}')
            continue

        file.rename(out_dir.joinpath(f'{sequence}.nii.gz'))

    logging.warning('All sequences were converted to nifti files!')


