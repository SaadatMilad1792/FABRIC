#######################################################################################################################
## -- necessary libraries -- ##########################################################################################
#######################################################################################################################
import os
import sys
import threading
from ..FILE import *
from concurrent.futures import ThreadPoolExecutor

#######################################################################################################################
## -- binary stream object generator -- ###############################################################################
#######################################################################################################################
def genFabDf(params):
  
  subParamObject = params["process"]
  outPickleName = subParamObject["outPickleName"]
  parallelProc, maxWorker = subParamObject["parallelProc"], subParamObject["maxWorker"]
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
  if not parallelProc:
    for expType in expTypes:
      dataFiles = dirSweep(os.path.join(inpDirectory, inpFolder, expType))
      dataFiles = [f for f in dataFiles if f.split(".")[1] == dfType]
      for fc, dataFile in enumerate(dataFiles):
        print(f"Process: {dataFiles[fc]}: [{(fc + 1):04} / {len(dataFiles):04} %]")
        DataFrame.append(bsObject(params, os.path.join(inpDirectory, inpFolder, expType), dataFile))
   
  elif parallelProc:
    lock = threading.Lock()
    def bsObjectCompact(expType, dataFile):
      result = bsObject(params, os.path.join(inpDirectory, inpFolder, expType), dataFile)
      with lock:
        DataFrame.append(result)
        print(f"{dataFile} [STATUS: DONE]")

    with ThreadPoolExecutor(max_workers=maxWorker) as executor:
      for expType in expTypes:
        dataFiles = dirSweep(os.path.join(inpDirectory, inpFolder, expType))
        dataFiles = [f for f in dataFiles if f.split(".")[1] == dfType]
        futures = [executor.submit(bsObjectCompact, expType, dataFile) for dataFile in [dataFiles[0]]]
        for fc, future in enumerate(futures):
          print(f"Process: {dataFiles[fc]}: [{(fc + 1):04} / {len(dataFiles):04} %]")

      for future in futures:
        future.result()
  
  else:
    sys.exit(f"Invalid parallel type. Valid choices: ['True', 'False']")
  
  print(f"FABRIC [STATUS: DONE] -> Generated f'{outPickleName}.pkl.gz")
  DataFrame = pd.concat(DataFrame).reset_index(drop = True)
  DataFrame.to_pickle(os.path.join(outDirectory, outFolder, f'{outPickleName}.pkl.gz'), compression = 'gzip')
  return DataFrame