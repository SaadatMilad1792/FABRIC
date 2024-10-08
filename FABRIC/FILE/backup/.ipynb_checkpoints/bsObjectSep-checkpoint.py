#######################################################################################################################
## -- necessary libraries -- ##########################################################################################
#######################################################################################################################
import os
import pandas as pd
from ..SUPPORT import *

# cite this at the end: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8623280/
from FABRIC.SUPPORT.code_descriptors_postural_control.stabilogram.stato import Stabilogram
from FABRIC.SUPPORT.code_descriptors_postural_control.descriptors import compute_all_features

#######################################################################################################################
## -- binary stream object generator -- ###############################################################################
#######################################################################################################################
def bsObject(params, directory, fileName):
  subParamObject = params["process"]
  featExtr = subParamObject["featExtr"]
  framePerSecond, verbose = subParamObject["framePerSecond"], subParamObject["verbose"]

  codeName = fileName.split(".")[0].split("_")
  subId, expType, expStage, expCond = codeName[0], codeName[1], codeName[2], list(codeName[3])
  expName, stabilityStatus, eyeStatus, trial = expCond[0], expCond[1], expCond[2], expCond[3]
  
  data, _, _ = loadbsf(os.path.join(directory, fileName), plot=False)
  
  dataPacket = pd.DataFrame([{
    "subId": subId,
    "expType": expType,
    "expStage": expStage,
    "expTrial": trial,
    "expName": "Balance" if expName == "B" else "Unknown",
    "stabilityStatus": "Stable" if stabilityStatus == "S" else "Unstable" if stabilityStatus == "U" else "Unknown",
    "eyeStatus": "Closed" if eyeStatus == "C" else "Open" if eyeStatus == "O" else "Unknown",
    "time (s)": (i + 1) / framePerSecond,
    "Fx": data[i][0], "Fy": data[i][1], "Fz": data[i][2],
    "Mx": data[i][3], "My": data[i][4], "Mz": data[i][5],
  } for i in range(len(data))])

  COPx = 100 * ((dataPacket["My"] / dataPacket["Fz"]) - np.mean(dataPacket["My"] / dataPacket["Fz"]))
  COPy = 100 * ((dataPacket["Mx"] / dataPacket["Fz"]) - np.mean(dataPacket["Mx"] / dataPacket["Fz"]))

  dataPacket["COPx"], dataPacket["COPy"] = COPx, COPy

  featurePacket = pd.DataFrame([{
    "subId": subId,
    "expType": expType,
    "expStage": expStage,
    "expTrial": trial,
    "expName": "Balance" if expName == "B" else "Unknown",
    "stabilityStatus": "Stable" if stabilityStatus == "S" else "Unstable" if stabilityStatus == "U" else "Unknown",
    "eyeStatus": "Closed" if eyeStatus == "C" else "Open" if eyeStatus == "O" else "Unknown",
  }])

  if featExtr:
    try:
      stato = Stabilogram()
      stato.from_array(array = np.column_stack((COPx, COPy)), original_frequency=framePerSecond)
      features = compute_all_features(stato, params_dic={"sway_density_radius": 0.3})

      for key, value in features.items():
        featurePacket[key] = value

    except Exception as e:
      print(f"[-] Failed to extract features due to invalid values: {fileName}")
      print(str(e))
      return

  return [dataPacket, featurePacket]