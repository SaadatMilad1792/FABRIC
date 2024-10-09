#######################################################################################################################
## -- necessary libraries -- ##########################################################################################
#######################################################################################################################
import os
import pandas as pd
from ..FILE import *
import matplotlib.pyplot as plt

#######################################################################################################################
## -- binary stream object generator -- ###############################################################################
#######################################################################################################################
def analytic(params):
  
  subParamObject = params["visytic"]
  inpPickleName, funcStat = subParamObject["inpPickleName"], subParamObject["funcStat"]
  inpDirectory, inpFolder = subParamObject["inpDirectory"], subParamObject["inpFolder"]
  outDirectory, outFolder = subParamObject["outDirectory"], subParamObject["outFolder"]
  
  if not funcStat:
    print(f"[+] FABRIC: analytic marked as deactive, modify param.yaml for activation.")
    return
  
  dataFrame = pd.read_pickle(os.path.join(inpDirectory, inpFolder, f"{inpPickleName}.pkl.gz"), compression = "gzip")
  
  PRE = dataFrame[dataFrame["expStage"] == "PRE"]["mean_value_ML"].mean()
  PST = dataFrame[dataFrame["expStage"] == "POST"]["mean_value_ML"].mean()
  print(PRE, PST)
  plt.plot([PRE, PST])
  
  return dataFrame