# ukk_mets

## Introduction
This repository predicts the genotype and histology of brain metastases

## Installation
Clone this repository:
`git clone https://github.com/rgutsche/ukk_mets.git`

## How to use it

### Prerequisites

##### For Preprocessing
Data should be in the following structure:
```
└── PID_1
    ├── T1C
    │   ├── IM-0305-0001.dcm
    │   ├── IM-0305-0002.dcm
    │   └── IM-0305-0003.dcm
    ├── T2
    │   ├── IM-0309-0001.dcm
    │   ├── IM-0309-0002.dcm
    │   └── IM-0309-0003.dcm
    ├── FLAIR
    │   ├── IM-0307-0001.dcm
    │   ├── IM-0307-0002.dcm
    │   └── IM-0307-0003.dcm
└── PID_2
      ├── T1C
      ├── T2
      └── FLAIR
└── ...
```

##### Tumor Segmentation
Please create your segmentation according to the following format:
- Label 1: Contrast enhancing tumor
- Label 2: Non-enhancingT2/FLAIR abnormalities (Edema)
- Label 3: Necrotic like parts

##### For prediction
Data should be in the following structure (IMPORTANT! Add tumor segmentation in nifti format!):
```
└── PID_1
    ├── IMG_DATA
    │   ├── PID_1_0001.nii.gz
    │   ├── PID_1_0002.nii.gz
    │   ├── PID_1_0003.nii.gz
    │   └── PID_1_tum_seg.nii.gz
└── ...
```

### Terminal commands
Terminal arguments:

- "-preprocess" must be 'Y' or 'N' if dicom files should be converted to nifti, registered and n4-bias-field corrected
- "-input_path" must be the path to the patient folder 

Example:

##### Only preprocess 
``` main.py -preprocess Y -input /Users/robin/data/PID ```

##### Only prediction
``` main.py -preprocess N -input /Users/robin/data/PID ```

### Output
##### Final output
The final output will create feature folder containing radiomics features as Excel file and the prediction with a preview of the tumor and an Excel file with the predictions.
```
└── PID_1
    ├── IMG_DATA
    ├── FEATURES
            ├── PID_1_features.xlsx
    ├── PREDICTION
            ├── PID_1_preview_tumor.png
            ├── PID_1_prediction.xlsx
└── ...
```

