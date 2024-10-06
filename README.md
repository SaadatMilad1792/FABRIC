# FABRIC
Fatigue and Balance Relationship Interaction Computation (F.A.B.R.I.C)

### Table of content

|     | Section                                                                 | Description                                         | Last updated   |
| --- | ----------------------------------------------------------------------- | --------------------------------------------------- | -------------- |
|  1  | [Getting Started With FABRIC](#Getting-Started-With-FABRIC)             | Instructions on getting started with FABRIC         | 10/06/2024     |
|  2  | [Parameter Manipulation](#Parameter-Manipulation)                       | Instructions on changing the parameters accordingly | 10/06/2024     |
|  3  | [FABRIC Processing Tools](#FABRIC-Processing-Tools)                     | FABRIC Guide on available processing tools          | 10/06/2024     |
|  4  | [FABRIC Analytic Tools](#FABRIC-Analytic-Tools)                         | FABRIC Guide on available analytic tools            | 10/06/2024     |
|  5  | [References And Acknowledgement](#References-And-Acknowledgement)       | FABRIC References And Acknowledgement               | 10/06/2024     |

### Getting Started With FABRIC
FABRIC is a package designed to assist with preprocessing tasks and is equipped with multiple analytical and visualization 
tools to streamline data preparation. This facilitates greater uniformity for researchers working on the relationship between
fatigue and balance. FABRIC utilizes [AMTIbsf](https://github.com/BMClab/BMC/blob/master/functions/AMTIbsf.py), developed by
[Renato Naville Watanabe](https://github.com/rnwatanabe), to extract data from .bsf files and creates a more comprehensive 
pandas DataFrame that is readily available for analysis.

Each .bsf file contains 30 seconds of data from a subject, sampled at a rate of 1000 frames per second. This results in a 
total of 30,000 rows in the DataFrame for specific conditions pertaining to each subject. By convention, the files are named
to convey all the necessary information related to the experiments:

```
FILE NAME: {subject ID}_{experiment Type}_{experiment Stage}_{experiment Conditions}.bsf
```

In order to get started with FABRIC, clone this repository on your machine, adequetly change the input and output directories
and make sure the input directory is where your input data is, the orientation of input directory must be like the following:

```
├── input/
│   ├── experiment Type 1/
│   │   ├── 1000_expType1_expStage1_expCondition1.bsf
│   │   ├── 1000_expType1_expStage1_expCondition2.bsf
│   │   ├── 1001_expType1_expStage1_expCondition1.bsf
│   │   ├── ...
│
│   ├── experiment Type 2/
│   │   ├── 1000_expType2_expStage1_expCondition1.bsf
│   │   ├── 1000_expType2_expStage1_expCondition2.bsf
│   │   ├── 1001_expType2_expStage1_expCondition1.bsf
│   │   ├── ...
│
│   ├── ...
```

### Parameter Manipulation


### FABRIC Processing Tools


### FABRIC Analytic Tools