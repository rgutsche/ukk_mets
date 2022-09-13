import SimpleITK as sitk
from radiomics import featureextractor
import logging

logger = logging.getLogger("radiomic.glcm")
logger.setLevel(logging.ERROR)

def run_extraction(input_path):
    pass

PATH = Path('/Volumes/Gutsche/data')
PATH_IMAGES = PATH.joinpath('intermediate', 'BRAF', 'BRAF_cropped')
PATH_OUTPUT = PATH.joinpath('processed', 'BRAF')
PATH_STATUS = PATH.joinpath('raw', 'patient_lists', 'BRAF', 'BRAF_test_set.xlsx')

#%%
df_status = pd.read_excel(PATH_STATUS, dtype=str)
pids = df_status['Forget'].dropna().reset_index(drop=True)


def extract_features(t1_array, mask_array):
    settings = {'normalize': False,
                'binWidth': 0.1,
                'preCrop': True,
                'correctMask': True}

    extractor = featureextractor.RadiomicsFeatureExtractor(**settings)

    extractor.enableImageTypes(Wavelet={}, LoG={'sigma': [1, 2, 3, 4, 5]})

    feats_t1 = extractor.execute(t1_array, mask_array, label=1)

    for x in [key for key, value in feats_t1.items() if key.startswith('diagnostics_')]:
        feats_t1.pop(x)

    t1_features = dict([f'T1_'+ key, float(value)] for key, value in feats_t1.items())

    return t1_features


dfs = []

# pid = pids[0]
for i, pid in tqdm(enumerate(pids)):
    t1_path = str(PATH_IMAGES.joinpath(f'{pid}_T1_image.nii.gz'))
    mask_path = str(PATH_IMAGES.joinpath(f'{pid}_T1_mask.nii.gz'))

    sitk_t1 = sitk.ReadImage(t1_path)
    sitk_mask = sitk.ReadImage(mask_path, sitk.sitkUInt8)
    resample = tio.Resample(1)

    sitk_t1_res = resample(sitk_t1)
    sitk_mask_res = resample(sitk_mask)

    layer = int(sitk_t1_res.GetDepth()/2)
    fig, axs = plt.subplots(nrows=1, ncols=2)
    axs[0].imshow(sitk.GetArrayFromImage(sitk_t1_res)[:, :, layer], cmap='gray')
    axs[0].set_title('t1_orig')
    axs[1].imshow(sitk.GetArrayFromImage(sitk_mask_res)[:, :, layer], cmap='gray')
    axs[1].set_title('mask_orig')
    plt.savefig(PATH_OUTPUT.joinpath('plots', 'cropped_transformed', f'{pid}.png'), dpi=300)

    t1_features_orig = extract_features(sitk_t1_res, sitk_mask_res)
    df_t1 = pd.DataFrame()
    df_t1 = df_t1.from_dict(t1_features_orig, orient='index').T
    df_t1.insert(0, 'pid', pid)
    dfs.append(df_t1)

final_df = pd.concat(dfs, ignore_index=True)
final_df.to_excel(PATH_OUTPUT.joinpath('features', 'rsmp1mm_bw010_test_set_t1_lastpid.xlsx'))


