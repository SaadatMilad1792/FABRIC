# FABRIC
Fatigue and Balance Relationship Interaction Computation (F.A.B.R.I.C)

### Table of content

|     | Section                                                                 | Description                                         | Last updated   |
| --- | ----------------------------------------------------------------------- | --------------------------------------------------- | -------------- |
|  1  | [Getting Started With FABRIC](#Getting-Started-With-FABRIC)             | Instructions on getting started with FABRIC         | 10/07/2024     |
|  2  | [Parameter Manipulation](#Parameter-Manipulation)                       | Instructions on changing the parameters accordingly | 10/08/2024     |
|  3  | [FABRIC Processing Tools](#FABRIC-Processing-Tools)                     | FABRIC Guide on available processing tools          | 10/06/2024     |
|  4  | [FABRIC Analytic Tools](#FABRIC-Analytic-Tools)                         | FABRIC Guide on available analytic tools            | 10/06/2024     |
|  5  | [References And Acknowledgement](#References-And-Acknowledgement)       | FABRIC References And Acknowledgement               | 10/06/2024     |

### Getting Started With FABRIC
FABRIC is a package designed to assist with preprocessing tasks and is equipped with multiple analytical and visualization 
tools to streamline data preparation. This facilitates greater uniformity for researchers working on the relationship between
fatigue and balance. FABRIC utilizes [AMTIbsf](https://github.com/BMClab/BMC/blob/master/functions/AMTIbsf.py), developed by
[Renato Naville Watanabe](https://github.com/rnwatanabe), to extract data from `.bsf` files and creates a more comprehensive 
pandas DataFrame that is readily available for analysis.

Each `.bsf` file contains 30 seconds of data from a subject, sampled at a rate of 1000 frames per second. This results in a 
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
│   ├── .../
│   │   ├── [...].bsf
│   │   ├── [...].bsf
```

Once the input and output directories are configured, you’re ready to use FABRIC. There are two ways to run this package without
making further changes. You’ll find two files provided: `FABRIC.py` and `FABRIC.ipynb`, each serving a different purpose. Given 
the large size of the data, it’s recommended to run `FABRIC.py` in the background using the `nohup` command in Linux to prevent 
disruptions. However, if you prefer a more interactive experience, the Jupyter Notebook (`FABRIC.ipynb`) is the better option. 
After setting up the input/output directories and activating the necessary functions in the parameter file, you can either run 
FABRIC within Jupyter Notebook or execute it in the background using the following `nohup` command:

```linux
nohup python FABRIC.py > output.log 2>&1 &
```

### Parameter Manipulation
In order to properly understand how FABRIC works, you need to be able to fully understand how the parameters are passed to 
FABRIC sub modules. All parameters are stored in a `.yaml` file called `params.yaml`. When passed to each sub module, the
sub module will select the parameters for that specific sub module, and then it will have accessm to them all. In order to 
load the params.yaml, simply create the parameters file, and load it with the following buildin function in FABRIC:

```python
# Ex. load the entire parameter .yaml file
params = FABRIC.loadArgs('./{directory to params}/params.yaml')

# Ex. select only the paremeters for process sub module
process_params = params["process"]
```

Here is the default values stored in the paremeter file, in this section we will provide in depth explanation for each and
everyone of them. Keep in mind that in order for this code to work on your machine, you need to properly adjust the input
and output directories, and activate tools by setting `funcStat` to `True`, which is always `False` by default.
```yaml
{
  ## -- 1.0: [generic: LAUNCH] generic globally shared information -- ##
  "generic": {
    
  },
  
  ## -- 2.0: [process: LAUNCH] process core parameters -- ##
  "process": {
    "inpDirectory": "/esplabdata/FABRIC", "inpFolder": "raw",
    "outDirectory": "/esplabdata/FABRIC", "outFolder": "prc",
    "experimentTypes": ["SM", "SP", "MP", "M", "P"],
    "outPickleName": "UNIVERSAL_FABRIC", "funcStat": True,
    "dfType": "bsf", "framePerSecond": 1000, "verbose": False,
    "parallelProc": True, "maxWorker": 48, "featExtr": True,
    "debuggingMode": True,
  },
}
```

The table below serves as a guide to help you understand the impact of each parameter on the code. It is recommended to set all
`funcStat` values to `False` by default and modify them only by overriding specific values directly in the code. Avoid 
altering these values in the `.yaml` file, unless you explicitly intend to do so, as it may overwrite your output files.

| Sub Module | Parameter                 | Description                                                                             |
| ---------- | ------------------------- | --------------------------------------------------------------------------------------  |
| generic    | N/A                       | N/A                                                                                     |
| process    | inpDirectory              | Path to input directory (NOTE: exclude the folder name)                                 |
| process    | inpFolder                 | Name of the input folder (NOTE: This is a name not a path                               |
| process    | outDirectory              | Path to output directory (NOTE: exclude the folder name)                                |
| process    | outFolder                 | Name of the output folder (NOTE: This is a name not a path                              |
| process    | experimentTypes           | Valid experiment types (Ex. `P - Physical Fatigue` , `M - Mental Fatigue`)              |
| process    | outPickleName             | Name of the output pickle file that is saved in the output directory                    |
| process    | funcStat                  | Enables or disables methods, always set to False initially, set to True for activation  |
| process    | dfType                    | Input file type (Since FABRIC is based on `.bsf`, there is no change necessary)         |
| process    | framePerSecond            | Number of frames in every second of experiment, similar to sampling rate                |
| process    | verbose                   | Provides details regarding threads for parallel debugging                               |
| process    | parallelProc              | Enables parallel `.bsf` loading, significantly enhancing the speed of the preprocessing |
| process    | maxWorker                 | Maximum number of workers (Only when parallelProc is set to True)                       |
| process    | featExtr                  | Enables or disables feature extraction on the data frame                                |
| process    | debuggingMode             | Limits the size of input files to a single `.bsf` file for debugging                    |

**NOTE:** FABRIC leverages parallelism to optimize performance. However, it’s essential to find the right balance in CPU allocation; having 
too few CPUs can be as detrimental as having too many due to the communication overhead between them. Carefully choose the `maxWorker` value 
to enhance stability. For an optimal experience, regularly monitor the `output.log` file to ensure that `.bsf` files are being loaded concurrently 
while others are processed. If you observe a high number of files loading but only a few marked as `DONE`, consider adjusting the `maxWorkers`. 
This hyperparameter is specific to your system configuration, so optimizing it is your responsibility as the user.


### FABRIC Processing Tools
FABRIC is equipped with a range of processing tools, integrating both established methods from previous studies and newly added 
functionalities. As an end-to-end pipeline, FABRIC is designed to handle large datasets efficiently, ultimately generating a standardized
dataset for further analysis. The process begins with FABRIC generating an initial dataset containing six raw measurements: 
`["Fx", "Fy", "Fz", "Mx", "My", "Mz"]`. These primary values are used to calculate the center of pressure (COP) in both the x and y directions. 
Once the COPx and COPy values are derived, they are passed into the feature extraction module from [stato](add-reference-fix-me), where balance
features are extracted for deeper insights.

Here is how the processing tool handles the raw `.bsf` files, and generates a pandas dataframe, and stores it at the output directory location.
The image below shows the information stored in each row of the dataframe:

![Example image of a single row, in the dataframe](./images/markdown/DataFrameStructure.png)




### FABRIC Analytic Tools


### References And Acknowledgement