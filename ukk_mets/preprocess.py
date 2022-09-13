from nipype import config
cfg = dict(logging=dict(workflow_level='DEBUG', utils_level='DEBUG', interface_level='DEBUG'),
           execution={'stop_on_first_crash': False})
config.update_config(cfg)

from pathlib import Path
from ukk_mets.util import convert_to_nii, registration, brain_segmentation, crop_to_mask, n4_bias_field_correction


def run_preprocess(input_path):
    base = Path(input_path)
    pid = base.name

    print(f'Start preprocessing for patient: {pid}')

    # 1) Convert to Nifti
    sequences = ['T1C', 'T2', 'FLAIR']
    for sequence in sequences:
        dicom_dir = base.joinpath('DICOM', sequence)
        out_dir = base.joinpath('NIFTI', sequence)
        out_file = f'{sequence}'

        if not out_dir.is_dir():
            out_dir.mkdir(parents=True)

        print(f'PID: {pid} | Convert {sequence} to nifti')
        convert_to_nii(dicom_dir, out_dir, out_file)

        try:
            files = [x for x in out_dir.glob(f'{sequence}*')]
            if len(files) > 1:
                # multiple = True
                print(f'Warning! More than one file were generated for patient: {pid} | sequence: {sequence}')
            file = files[0]
        except IndexError:
            print(f'Error! Files not converted for patient: {pid} | sequence: {sequence}')
            continue

        file.rename(out_dir.joinpath(f'{pid}_{sequence}.nii.gz'))

        # if multiple:
        #     file = files[1]
        #     file.rename(out_dir.joinpath(f'{pid}_{sequence}_2.nii.gz'))

    print('All sequences were converted to nifti files!')

    # 2) Registration
    sequences = ['T2', 'FLAIR']

    for sequence in sequences:
        print(f'PID: {pid} | Registration {sequence} to T1C')

        in_file = base.joinpath('NIFTI', sequence, f'{pid}_{sequence}.nii.gz')
        ref_file = base.joinpath('NIFTI', 'T1C', f'{pid}_T1C.nii.gz')
        out_file = base.joinpath('NIFTI', sequence, f'{pid}_{sequence}_co.nii.gz')
        registration(str(in_file), str(ref_file), str(out_file))

    print('All sequences were registered to T1C!')

    # 3) Brain Segmentation
    print(f'PID: {pid} | Brain segmentation T1C')

    in_file = base.joinpath('NIFTI', 'T1C', f'{pid}_T1C.nii.gz')
    out_file = base.joinpath('NIFTI', 'T1C', f'{pid}_T1C_hdbet.nii.gz')
    brain_segmentation(str(in_file), str(out_file), device=0)

    out_file.parent.joinpath(f'{pid}_T1C_hdbet_mask.nii.gz').rename(
        out_file.parent.joinpath(f'{pid}_brain_segmentation.nii.gz'))

    print(f'PID: {pid} | Brain segmentation done.')

    # 4) Multiply brain segmentation with images
    print(f'PID: {pid} | Apply brain segmentation mask to other sequences')

    for sequence in sequences:
        mask_file = base.joinpath('NIFTI', 'T1C', f'{pid}_brain_segmentation.nii.gz')
        in_file = base.joinpath('NIFTI', sequence, f'{pid}_{sequence}_co.nii.gz')
        out_file = base.joinpath('NIFTI', sequence, f'{pid}_{sequence}_hdbet.nii.gz')
        crop_to_mask(in_file, mask_file, out_file)

    print(f'PID: {pid} | Application of brain segmentation mask done')

    # 5) N4-BiasField Correction

    print(f'PID: {pid} | Perform N4BiasFieldCorrection')

    sequences = ['T1C', 'T2', 'FLAIR']

    for i, sequence in enumerate(sequences):
        in_file = base.joinpath('NIFTI', sequence, f'{pid}_{sequence}_hdbet.nii.gz')
        out_file = base.joinpath('NIFTI', sequence, f'{pid}_{sequence}_hdbet_n4.nii.gz')
        brain_mask = str(base.joinpath('NIFTI', 'T1C', f'{pid}_brain_segmentation.nii.gz'))
        n4_bias_field_correction(in_file, str(out_file), brain_mask)

        # 6) Rename files to nnU-Net format
        out_file.rename(out_file.parent.joinpath(f'{pid}_000{i +1}.nii.gz'))

    print(f'PID: {pid} | N4BiasFieldCorrection done')