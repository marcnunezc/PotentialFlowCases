# PotentialFlowCases

Usage of `PotentialAnalysisCustom.py`:


`python3 PotentialAnalysisCustom.py ProjectParameters.json` to run body-fitted cases (this is the default .json).

`python3 PotentialAnalysisCustom.py RefineProjectParameters.json` to run body-fitted cases with adaptive refinement.

The refined mesh will be stored in Meshes/ directory in order to be used in a new analysis.

`python3 PotentialAnalysisCustom.py Parameters_LevelSet.json` to run embedded cases.

