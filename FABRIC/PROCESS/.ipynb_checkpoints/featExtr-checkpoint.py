#######################################################################################################################
## -- necessary libraries -- ##########################################################################################
#######################################################################################################################
import numpy as np
import pandas as pd
# cite this at the end: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8623280/

#######################################################################################################################
## -- binary stream object generator -- ###############################################################################
#######################################################################################################################
def featExtr(params, dataFrame):
  
  subParamObject = params["featExt"]
  funcStat = subParamObject["funcStat"]
  if not funcStat:
    print(f"[+] FABRIC: featExtr marked as deactive, modify param.yaml for activation.")
    return
  
  grouped = dataFrame.groupby(['subId', 'expType', 'expStage', 'expTrial', 'expName', 'stabilityStatus', 'eyeStatus'])
  for name, group in grouped:
    COPx = group["My"] / group["Fz"]
    COPy = group["Mx"] / group["Fz"]

    COPx = 100 * (COPx - np.mean(COPx))
    COPy = 100 * (COPy - np.mean(COPy))
    
    dataFrame.loc[group.index, "COPx"] = COPx
    dataFrame.loc[group.index, "COPy"] = COPy
  
  return dataFrame
