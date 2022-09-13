# ukk_mets

## Introduction
This repository predicts the genotype and histology of brain metastases

## Installation
Clone this repository:
`git clone https://github.com/rgutsche/ukk_mets.git`

## How to use it

### Prerequisites
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
    │   └── t2
└── PID_2
      ├── T1C
      ├── T2
      └── FLAIR
└── ...
```

### Terminal commands
Terminal arguments:

- "-preprocess" must be 'Y' or 'N' if dicom files should be converted to nifti, registered and n4-bias-field corrected
- "-input_path" must be the path to the patient folder 

Example:

##### Preprocess 
``` main.py -preprocess Y -input /Users/robin/data/PID ```