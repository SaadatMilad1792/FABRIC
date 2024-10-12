#######################################################################################################################
## -- necessary libraries -- ##########################################################################################
#######################################################################################################################
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import textwrap

#######################################################################################################################
## -- binary stream object generator -- ###############################################################################
#######################################################################################################################
def featPlot(params, gpFilter, groupDat):
  
  PRE = groupDat[groupDat["expStage"] == "PRE"]
  POST = groupDat[groupDat["expStage"] == "POST"]
  features = groupDat.iloc[:, groupDat.columns.get_loc("mean_value_ML"):].keys()

  sns.set(style = "whitegrid", context = "talk")
  fig, axes = plt.subplots(nrows = 8, ncols = 9, figsize = (9 * 10, 8 * 10), dpi = 100, facecolor = "white")
  axes, plotList = axes.flatten(), []

  for fIndex, feat in enumerate(features):
    featPre, featPost = np.array(list(PRE[feat])), np.array(list(POST[feat]))
    zsFeatPre, zsFeatPost, threshold = np.abs(stats.zscore(featPre)), np.abs(stats.zscore(featPost)), 2
    idxPre, idxPost = np.where(zsFeatPre > threshold)[0], np.where(zsFeatPost > threshold)[0]

    featPre, featPost = np.delete(featPre, idxPre), np.delete(featPost, idxPost)

    sns.boxplot(data = [featPre, featPost], palette = "pastel", ax = axes[fIndex])
    axes[fIndex].set_xticks([0, 1])
    axes[fIndex].set_xticklabels(["PRE", "POST"])

    avgPre, stdPre = np.mean(featPre), np.std(featPre)
    avgPost, stdPost = np.mean(featPost), np.std(featPost)
    medPre, medPost = np.median(featPre), np.median(featPost)

    avgChange = ((avgPost - avgPre) / avgPre) * 100
    stdChange = ((stdPost - stdPre) / stdPre) * 100
    medChange = ((medPost - medPre) / medPre) * 100

    avgArr = '↑' if avgChange > 0 else '↓'
    stdArr = '↑' if stdChange > 0 else '↓'
    medArr = '↑' if medChange > 0 else '↓'

    legendText = [
      f"PRE: (Mean: {avgPre:.3e}, Std: {stdPre:.3e}, Median: {medPre:.3e})",
      f"POST: (Mean: {avgPost:.3e}, Std: {stdPost:.3e}, Median: {medPost:.3e})",
      f"Change: (Mean: {avgArr} {avgChange:.2f}%, Std: {stdArr} {stdChange:.2f}%, Median: {medArr} {medChange:.2f}%)"
    ]

    legendColors = ["#ABC9EA", "#EFB792", (1, 1, 1, 0)]
    handles = [plt.Line2D([0], [0], color = color, lw = 4) for color in legendColors]

    axes[fIndex].legend(handles, legendText, loc = 'lower right', fontsize = 12, frameon = True)
    wrappedTitle = "\n".join(textwrap.wrap(f"{feat.replace('_', ' ')}", width = 32))
    axes[fIndex].set_title(wrappedTitle, fontsize = 36, pad = 16)
    axes[fIndex].set_xlabel("PRE vs POST", fontsize = 28, labelpad = 16)
    wrappedYlabel = "\n".join(textwrap.wrap(f"{feat.replace('_', ' ')}", width = 32))
    axes[fIndex].set_ylabel(wrappedYlabel, fontsize = 28, labelpad = 16)

    axes[fIndex].grid(True, axis = "y", linestyle = "--", alpha = 0.7)

  plt.tight_layout(pad = 2.0)
  plotList.append(fig)
  plt.close(fig)
  
  sns.set(style = "whitegrid", context = "talk")
  fig, axes = plt.subplots(nrows = 8, ncols = 9, figsize = (9 * 10, 8 * 10), dpi = 100, facecolor = "white")
  axes = axes.flatten()

  for fIndex, feat in enumerate(features):
    featPre, featPost = np.array(list(PRE[feat])), np.array(list(POST[feat]))
    zsFeatPre, zsFeatPost, threshold = np.abs(stats.zscore(featPre)), np.abs(stats.zscore(featPost)), 2
    idxPre, idxPost = np.where(zsFeatPre > threshold)[0], np.where(zsFeatPost > threshold)[0]

    featPre, featPost = np.delete(featPre, idxPre), np.delete(featPost, idxPost)
    sns.histplot(featPre, bins = 20, color = "#ABC9EA", kde = True, stat = 'density', ax = axes[fIndex], label = "PRE", alpha = 0.6)
    sns.histplot(featPost, bins = 20, color = "#EFB792", kde = True, stat = 'density', ax = axes[fIndex], label = "POST", alpha = 0.6)

    legendText = [f"PRE", f"POST"]

    legendColors = ["#ABC9EA", "#EFB792", (1, 1, 1, 0)]
    handles = [plt.Line2D([0], [0], color = color, lw = 4) for color in legendColors]

    axes[fIndex].legend(handles, legendText, loc = 'lower right', fontsize = 12, frameon = True)
    wrappedTitle = "\n".join(textwrap.wrap(f"{feat.replace('_', ' ')}", width = 32))
    axes[fIndex].set_title(wrappedTitle, fontsize = 36, pad = 16)
    axes[fIndex].set_xlabel("Values", fontsize = 28, labelpad = 16)
    wrappedYlabel = "\n".join(textwrap.wrap(f"Density", width = 32))
    axes[fIndex].set_ylabel(wrappedYlabel, fontsize = 28, labelpad = 16)

    axes[fIndex].grid(True, axis = "y", linestyle = "--", alpha = 0.7)

  plt.tight_layout(pad = 2.0)
  plotList.append(fig)
  plt.close(fig)
  
  return plotList