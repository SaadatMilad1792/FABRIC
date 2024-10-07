'''This code imports the .bsf files from the AMTI data collection software and exports a csv file with a large set of COP metrics.

Set the input and output directories as "input_path" and "output_path"

input_path: This should be the /FAB Data/Balance/ folder of the DARPA OneDrive. The code will iterate through each subfolder for each type of fatigue to extract metrics from those files

output_path: a file called "BalanceMetrics.csv" will be saved at this location. When running the code, it looks to see if this file already exists. If it does, it makes a list of which .bsf 
files have already been extracted and removes those from the list. This way, if you run the code and then add additional samples, you can run the code again and it will automatically find 
the ones that haven't been extracted and will extract just those and append them to the csv output file (it also saves the prior version of "BalanceMetrics.csv" as "BalanceMetrics_Backup.csv"). This saves time since the extraction can take a while. Expect it to take at least 
30 minutes the first time you run it.

The calculations for these metrics are described here:
https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8623280/

This is currently setup for 30 second reading, removing the first 2 and last 3 seconds (so using 25 seconds of data)

The code uses a "Try/Except" clause so that if there is an error with a specific file, it doesn't cause the code to stop. This is important bc the metrics are not exported until the end.
If there was a file that caused an error 45 minutes into running the code, you would have to rerun everything. In this case it will extract data from all the good files and anything that
throws an error you can check after.


'''

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os
import glob

from AMTIbsf import loadbsf

from code_descriptors_postural_control.stabilogram.stato import Stabilogram
from code_descriptors_postural_control.descriptors import compute_all_features


# set these to the correct input and output folders
input_path = "C:/Users/johnh/OneDrive - Texas A&M University/FAB Data/Balance/"
output_path = "C:/Users/johnh/OneDrive - Texas A&M University/DARPA Analysis/Balance/ExtractedData/"


#Go to the folder where you export the data
os.chdir(output_path)

#check if the output file exists (i.e. have you already run the code before to analyze some of the data)
if os.path.isfile('BalanceMetrics.csv'):
    # File exists, read it as DataFrame
    FinalData = pd.read_csv('BalanceMetrics.csv', index_col = 0)

    #make a backup copy
    pd.DataFrame(FinalData).to_csv('BalanceMetrics_Backup.csv', index = True)

    # Make a list of all the filenames that you have already processed
    PreviouslyProcessed = FinalData.index.tolist()
else:
    # File does not exist, create an empty DataFrame
    FinalData = pd.DataFrame()

    #also create empty list
    PreviouslyProcessed = []



# initialize a dataframe to store all of the new data before concatenating with old data
NewData = pd.DataFrame()

FatigueTypeList = ['M', 'P', 'MP', 'SM', 'SP']


for FatigueType in FatigueTypeList:

    FilePath = input_path + FatigueType + "/"
    print(FilePath)

    #import all bsf files within that directory
    os.chdir(FilePath)
    File_List = glob.glob('*.bsf')
    # File_List = glob.glob('*.txt')

    # Remove items from File_List that are also in PreviouslyProcessed
    File_List = [file for file in File_List if file not in PreviouslyProcessed]

    # Print the updated File_List
    print(File_List)





    for file in File_List:
        # print the name of the file
        print(file)
        ######################## import the data from the bsf file and extract center of pressure data (cop) #######################################
        data, mh, ih = loadbsf(filename=FilePath + file, plot=0)
        data = pd.DataFrame(data, columns = [' Fx', ' Fy', ' Fz', ' Mx', ' My', ' Mz'])

        # #This reads .txt file instead of .bsf
        # data = pd.read_csv(FilePath + file,header=None,sep=",",index_col=None)
        # data.columns = [' Fx', ' Fy', ' Fz', ' Mx', ' My', ' Mz']

        # #####################################################################################################################################
        # # https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8623280/

        # calculate COP
        X = data.get(" My")/data.get(" Fz")
        Y = data.get(' Mx')/ data.get(' Fz')
        X = X - np.mean(X)
        Y = Y - np.mean(Y)
        X = 100*X
        Y = 100*Y

        # cut off the first two seconds and the last 3 seconds to use the middle 25 seconds of data. Some participants noted that they jerked a little when we said start and some files have all 0s during the last second
        X = X.to_numpy()[2000:27000]
        Y= Y.to_numpy()[2000:27000]


        COP_data = np.array([X,Y]).T
        print(COP_data.shape)

        try:

            # Verif if NaN data
            valid_index = (np.sum(np.isnan(COP_data),axis=1) == 0)

            if np.sum(valid_index) != len(COP_data):
                raise ValueError("Clean NaN values first")



            stato = Stabilogram()
            stato.from_array(array=COP_data, original_frequency=1000)


            sway_density_radius = 0.3 # 3 mm

            params_dic = {"sway_density_radius": sway_density_radius}


            features = compute_all_features(stato, params_dic=params_dic)

            features = pd.DataFrame.from_dict(features, orient='index', dtype=None, columns=[file]).T
            features = features.assign(ID = mh.name)


            NewData = pd.concat([NewData, features])
        except:
            print('ERROR: ' + file + ' is invalid.')




print(NewData)
FinalData = pd.concat([FinalData, NewData])

os.chdir(output_path)
pd.DataFrame(FinalData).to_csv('BalanceMetrics.csv', index = True)