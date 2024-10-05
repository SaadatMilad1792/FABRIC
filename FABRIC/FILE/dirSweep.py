#######################################################################################################################
## -- necessary libraries -- ##########################################################################################
#######################################################################################################################
import os

#######################################################################################################################
## -- directory sweep -- ##############################################################################################
#######################################################################################################################
def dirSweep(directory):
  return [entry.name for entry in os.scandir(directory) if entry.name != ".ipynb_checkpoints"]