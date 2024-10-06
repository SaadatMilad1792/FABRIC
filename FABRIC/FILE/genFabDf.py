#######################################################################################################################
## -- necessary libraries -- ##########################################################################################
#######################################################################################################################
import os
import sys
from ..FILE import *

#######################################################################################################################
## -- binary stream object generator -- ###############################################################################
#######################################################################################################################
def genFabDf(params):
  
  subParamObject = params["process"]
  inpDirectory, inpFolder = subParamObject["inpDirectory"], subParamObject["inpFolder"]
  outDirectory, outFolder = subParamObject["outDirectory"], subParamObject["outFolder"]
  experimentTypes, dfType = subParamObject["experimentTypes"], subParamObject["dfType"]
    
  expTypes = dirSweep(os.path.join(inpDirectory, inpFolder))
  if not set(expTypes).issubset(set(experimentTypes)):
    sys.exit(f"Unknown Experiment Type Detected, Process Terminated. Allowed Types: {experimentTypes}")

  if os.path.isdir(outDirectory):
    outFullPath = os.path.join(outDirectory, outFolder)
    if not os.path.exists(outFullPath):
      os.makedirs(outFullPath)
  else:
    sys.exit(f"Directory '{outDirectory}' is invalid. Add a valid directory in 'params -> process -> outDirectory'")
    
  DataFrame = []
  for expType in expTypes:
    dataFiles = dirSweep(os.path.join(inpDirectory, inpFolder, expType))
    dataFiles = [f for f in dataFiles if f.split(".")[1] == dfType]
    for fc, dataFile in enumerate(dataFiles):
      print(f"Processing: {expType} -> {dataFile}: [{(100 * (fc + 1) / len(dataFiles)):.3f} %]", end = " " * 20 + "\r")
      DataFrame.append(bsObject(params, os.path.join(inpDirectory, inpFolder, expType), dataFile))
  
  DataFrame = pd.concat(DataFrame).reset_index(drop = True)
  DataFrame.to_pickle(os.path.join(outDirectory, outFolder, 'UNIVERSAL_FABRIC.pkl.gz'), compression = 'gzip')
  return DataFrame