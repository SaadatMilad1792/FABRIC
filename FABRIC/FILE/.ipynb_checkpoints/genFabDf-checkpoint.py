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
  outPickleName, funcStat = subParamObject["outPickleName"], subParamObject["funcStat"]
  parallelProc, maxWorker = subParamObject["parallelProc"], subParamObject["maxWorker"]
  inpDirectory, inpFolder = subParamObject["inpDirectory"], subParamObject["inpFolder"]
  outDirectory, outFolder = subParamObject["outDirectory"], subParamObject["outFolder"]
  experimentTypes, dfType = subParamObject["experimentTypes"], subParamObject["dfType"]
  
  if not funcStat:
    print(f"[+] FABRIC: genFabDf marked as deactive, modify param.yaml for activation.")
    return
    
  expTypes = dirSweep(os.path.join(inpDirectory, inpFolder))
  if not set(expTypes).issubset(set(experimentTypes)):
    print(f"[-] Unknown Experiment Type Detected, Process Terminated. Allowed Types: {experimentTypes}")
    sys.exit(f"Unknown Experiment Type Detected, Process Terminated. Allowed Types: {experimentTypes}")

  if os.path.isdir(outDirectory):
    outFullPath = os.path.join(outDirectory, outFolder)
    if not os.path.exists(outFullPath):
      os.makedirs(outFullPath)
  else:
    print(f"[-] Directory '{outDirectory}' is invalid. Add a valid directory in 'params > process > outDirectory'")
    sys.exit(f"[-] Directory '{outDirectory}' is invalid. Add a valid directory in 'params > process > outDirectory'")
    
  dataFrame = []
  if not parallelProc:
    for expType in expTypes:
      dataFiles = dirSweep(os.path.join(inpDirectory, inpFolder, expType))
      dataFiles = [f for f in dataFiles if f.split(".")[1] == dfType]
      for fc, dataFile in enumerate(dataFiles):
        print(f"{dataFiles[fc]}".ljust(24), f" | Progress: ".ljust(12),
              f"[{(fc + 1):04} / {len(dataFiles):04}] -> ({(100 * (fc + 1) / len(dataFiles)):.3f} %)".ljust(16))
        dataFrame.append(bsObject(params, os.path.join(inpDirectory, inpFolder, expType), dataFile))
   
  elif parallelProc:
    def bsObjectCompact(expType, dataFile):
      result = bsObject(params, os.path.join(inpDirectory, inpFolder, expType), dataFile)
      print(f"{dataFile}".ljust(24), "-> [STATUS: DONE]".ljust(16))
      return result

    allResults = []
    with ThreadPoolExecutor(max_workers = maxWorker) as executor:
      futures = []
      for expType in expTypes:
        dataFiles = dirSweep(os.path.join(inpDirectory, inpFolder, expType))
        dataFiles = [f for f in dataFiles if f.split(".")[1] == dfType]

        for fc, dataFile in enumerate(dataFiles):
          futures.append(executor.submit(bsObjectCompact, expType, dataFile))
          print(f"{dataFiles[fc]}".ljust(24), f" | Progress: ".ljust(12),
                f"[{(fc + 1):04} / {len(dataFiles):04}] -> ({(100 * (fc + 1) / len(dataFiles)):.3f} %)".ljust(16))

      for future in futures:
        result = future.result()
        allResults.append(result)

    dataFrame.extend(allResults)
  
  else:
    print(f"[-] Invalid parallel type. Valid choices: ['True', 'False']")
    sys.exit(f"[-] Invalid parallel type. Valid choices: ['True', 'False']")
  
  print(f"FABRIC [STATUS: DONE] -> Generated f'{outPickleName}.pkl.gz")
  dataFrame = pd.concat(dataFrame).reset_index(drop = True)
  dataFrame.to_pickle(os.path.join(outDirectory, outFolder, f'{outPickleName}.pkl.gz'), compression = 'gzip')
  return dataFrame