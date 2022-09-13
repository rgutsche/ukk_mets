from nipype.interfaces import fsl
from nipype.interfaces.ants import N4BiasFieldCorrection
from nipype.interfaces.dcm2nii import Dcm2niix
from nipype.interfaces.fsl import ApplyMask
from HD_BET.run import run_hd_bet
from nipype import config
cfg = dict(logging=dict(workflow_level='DEBUG'),
           execution={'stop_on_first_crash': False})
config.update_config(cfg)


def convert_to_nii(dicom_dir_path, out_dir_path, out_path):
    """
    Convert dir containing dicom series to nifti file. File will be compressed (out_filename.nii.gz).
    dcm2niix tool is used.
    :param dicom_dir_path: str or pathlike object | dir containing single dicom series
    :param out_dir_path: str or pathlike object | output dir
    :param out_path: str or pathlike object | output file name (without .nii.gz suffix!)
    :return: nifti file
    """
    converter = Dcm2niix()
    converter.inputs.source_dir = dicom_dir_path
    converter.inputs.bids_format = False
    converter.inputs.compress = 'y'
    converter.inputs.output_dir = out_dir_path
    converter.inputs.out_filename = f'{out_path}'
    converter.inputs.verbose = False
    converter.run()


def registration(in_path, ref_path, out_path):
    """
    Registration image to another image (for example T1-km to T1-native)
    :param in_path: str or pathlike object | nifti file that should be registered
    :param ref_path: str or pathlike object | nifti file that should be registered to
    :param out_path: str or pathlike object | output file name (without .nii.gz suffix!)
    :return: registered nifti file
    """
    flt = fsl.FLIRT(cost_func='mutualinfo',
                    dof=7,
                    searchr_x=[180, 180],
                    searchr_y=[180, 180],
                    searchr_z=[180, 180],
                    interp='trilinear')

    flt.inputs.in_file = in_path  # File that should be registered
    flt.inputs.reference = ref_path  # File that should be registered to
    flt.inputs.output_type = 'NIFTI_GZ'
    flt.inputs.out_file = out_path
    flt.run()

def brain_segmentation(in_path, out_path, device=0):
    """
    Brain segmentation using HD-BET
    :param in_path: str |
    :param out_path: str |
    :param device_id: either int for device id or 'cpu'
    :return: image crop to brain mask, brain mask
    """
    run_hd_bet(in_path, out_path, device=device)

def crop_to_mask(in_path, mask_path, out_path):
    """
    Use HD-BET brain segmentation mask for all sequences
    :param in_path:
    :param mask_path:
    :param out_path:
    :return:
    """
    mask = ApplyMask()
    mask.inputs.in_file = in_path
    mask.inputs.mask_file = mask_path
    mask.inputs.out_file = out_path
    mask.run()


def n4_bias_field_correction(in_path, out_path, brain_mask_path):
    """
    N4-bias-field correction unsing ANTS
    :param in_path:
    :param out_path:
    :param brain_mask_path:
    :return:
    """
    n4 = N4BiasFieldCorrection()
    n4.inputs.input_image = in_path
    n4.inputs.mask_image = brain_mask_path
    n4.inputs.output_image = out_path
    n4.run()
