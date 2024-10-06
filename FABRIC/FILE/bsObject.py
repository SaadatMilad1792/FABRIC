#######################################################################################################################
## -- necessary libraries -- ##########################################################################################
#######################################################################################################################
import sys
from ..FILE import *

#######################################################################################################################
## -- binary stream object generator -- ###############################################################################
#######################################################################################################################
def bsObject(params):
  
  subParamObject = params["process"]
  inpDirectory, inpFolder = subParamObject["inpDirectory"], subParamObject["inpFolder"]
  outDirectory, outFolder = subParamObject["outDirectory"], subParamObject["outFolder"]
  experimentTypes = subParamObject["experimentTypes"]
    
  expType = dirSweep(inpDirectory + inpFolder)
  if not set(expType).issubset(set(experimentTypes)):
    sys.exit(f"Unknown Experiment Type Detected, Process Terminated. Allowed Types: {experimentTypes}")

  if os.path.isdir(outDirectory):
    outFullPath = os.path.join(outDirectory, outFolder)
    if not os.path.exists(outFullPath):
      os.makedirs(outFullPath)
  else:
    sys.exit(f"Directory '{outDirectory}' is invalid. Add a valid directory in 'params -> process -> outDirectory'")
    