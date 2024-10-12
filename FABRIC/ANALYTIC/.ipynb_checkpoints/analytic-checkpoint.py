#######################################################################################################################
## -- necessary libraries -- ##########################################################################################
#######################################################################################################################
import os
import pandas as pd
import matplotlib.pyplot as plt
from ..ANALYTIC import *

#######################################################################################################################
## -- binary stream object generator -- ###############################################################################
#######################################################################################################################
def analytic(params):
  
  subParamObject = params["visytic"]
  inpPickleName, funcStat = subParamObject["inpPickleName"], subParamObject["funcStat"]
  inpDirectory, inpFolder = subParamObject["inpDirectory"], subParamObject["inpFolder"]
  outDirectory, outFolder = subParamObject["outDirectory"], subParamObject["outFolder"]
  groupFilter = subParamObject["groupFilter"]
  
  if not funcStat:
    print(f"[+] FABRIC: analytic marked as deactive, modify param.yaml for activation.")
    return
  
  dataFrame = pd.read_pickle(os.path.join(inpDirectory, inpFolder, f"{inpPickleName}.pkl.gz"), compression = "gzip")
  
  groups = dataFrame.groupby(groupFilter)
  for gpFilter, groupDat in groups:
    if not "Unknown" in gpFilter:
      plotList = featPlot(params, gpFilter, groupDat)
      plotList[0].savefig(os.path.join(outDirectory, outFolder, f"{'boxPlt_' + '_'.join(gpFilter)}.png"))
      plotList[1].savefig(os.path.join(outDirectory, outFolder, f"{'hstPlt_' + '_'.join(gpFilter)}.png"))
    else:
      pass
    
  return True