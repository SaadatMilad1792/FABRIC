#######################################################################################################################
## -- necessary libraries -- ##########################################################################################
#######################################################################################################################
import os
import sys
import pandas as pd
from ..SUPPORT import *

#######################################################################################################################
## -- binary stream object generator -- ###############################################################################
#######################################################################################################################
def bsObject(params, directory, fileName):
  
  subParamObject = params["process"]
  codeName = fileName.split(".")[0].split("_")
  framePerSecond = subParamObject["framePerSecond"]
  subId, expType, expStage, expCond = codeName[0], codeName[1], codeName[2], list(codeName[3])
  expName, stabilityStatus, eyeStatus, trial = expCond[0], expCond[1], expCond[2], expCond[3]
  data, _, _ = loadbsf(os.path.join(directory, fileName), plot = False)
  
  dataPacket = []
  for i in range(len(data)):
    dataPacket.append(pd.DataFrame({
      "subId": [subId], 
      "expType": [expType], 
      "expStage": [expStage], 
      "time (s)": (i + 1) / framePerSecond,
      "expTrial": [trial], 
      "expName": ["Balance" if expName == "B" else "Unknown"],  
      "stabilityStatus": ["Stable" if stabilityStatus == "S" else "Unstable" if stabilityStatus == "U" else "Unknown"],
      "eyeStatus": ["Closed" if eyeStatus == "C" else "Open" if eyeStatus == "O" else "Unknown"],
      "Fx": [data[i][0]], "Fy": [data[i][1]], "Fz": [data[i][2]], 
      "Mx": [data[i][3]], "My": [data[i][4]], "Mz": [data[i][5]],
    }))

  return pd.concat(dataPacket).reset_index(drop = True)