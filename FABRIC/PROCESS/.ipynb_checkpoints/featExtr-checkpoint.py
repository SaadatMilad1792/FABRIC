#######################################################################################################################
## -- necessary libraries -- ##########################################################################################
#######################################################################################################################
import os
import numpy as np
import pandas as pd
from FABRIC.SUPPORT.code_descriptors_postural_control.stabilogram.stato import Stabilogram
from FABRIC.SUPPORT.code_descriptors_postural_control.descriptors import compute_all_features
# cite this at the end: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8623280/

#######################################################################################################################
## -- binary stream object generator -- ###############################################################################
#######################################################################################################################
def featExtr(params):
  
  subParamObject = params["featExt"]
  framePerSecond = subParamObject["framePerSecond"]
  outPickleName, funcStat = subParamObject["outPickleName"], subParamObject["funcStat"]
  inpDirectory, inpFolder = subParamObject["inpDirectory"], subParamObject["inpFolder"]
  outDirectory, outFolder = subParamObject["outDirectory"], subParamObject["outFolder"]
  
  if not funcStat:
    print(f"[+] FABRIC: featExtr marked as deactive, modify param.yaml for activation.", flush = True)
    return
  
  dataFrame = pd.read_pickle(os.path.join(inpDirectory, inpFolder, f'{outPickleName}.pkl.gz'), compression='gzip')
  print(f"[+] FABRIC Data Frame Successfully Loaded.", flush = True)
  
  currentGroup = 0
  grouped = dataFrame.groupby(['subId', 'expType', 'expStage', 'expTrial', 'expName', 'stabilityStatus', 'eyeStatus'])
  
  validGroups = []
  for name, group in grouped:
    currentGroup += 1
    
    try:
      group = group.copy()
      COPx = 100 * ((group["My"] / group["Fz"]) - np.mean(group["My"] / group["Fz"]))
      COPy = 100 * ((group["Mx"] / group["Fz"]) - np.mean(group["Mx"] / group["Fz"]))
      COP = np.array([np.array(COPx), np.array(COPy)]).T
      
      dataFrame.loc[group.index, "COPx"] = COPx
      dataFrame.loc[group.index, "COPy"] = COPy
      
      stato = Stabilogram()
      stato.from_array(array=COP, original_frequency=framePerSecond)
      features = compute_all_features(stato, params_dic={"sway_density_radius": 0.3})
      print("Extracted: ", "[", currentGroup, "/", len(grouped), "]", flush = True)
      
      for key, value in features.items():
        dataFrame.loc[group.index, key] = value
        
      validGroups.extend(group.index)
      
    except Exception as e:
      print(f"[!] Skipping group {name} due to error: {e}", flush = True)
      continue
  
  dataFrame = dataFrame.loc[validGroups]
  print(f"FABRIC [STATUS: DONE] -> Extracted Features '{outPickleName}_FT.pkl.gz'", flush = True)
  
  dataFrame = dataFrame.reset_index(drop=True)
  dataFrame.to_pickle(os.path.join(outDirectory, outFolder, f'{outPickleName}_FT.pkl.gz'), compression='gzip')
  
  return dataFrame