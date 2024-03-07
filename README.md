# Preprocessing Pipe Line Neurodot -Container 

## Introduction

> This container runs the neurodot preprocesisng pipleline via papermill, by mounting the subject data from the scan resources folder and then exports and saves every figure into an output folder called savedFigures, and the output notebook (a fully run version of the notebook) is saved under outputNotebook filder. 

##  Design: 
  * Used python 
  * full list of packages needed: (listed within the Dockerfile.base)
    * deepdiff
    * matplotlib 
    * normalize_easy 
    * numpy 
    * scipy 
    * pyvista
    * sympy
    * papermill  
    
   
##  How to use:
  > All the scripts are located within the "workspace/neuro_dot" dir - any edits you will need to make for your specific use case will be with "NeuroDOT_PreProcessing_Script_dynamicFilterMode.ipynb". Once edits are done run ./build.sh to build your docker container. Specifics to edit within docker are the Dockerfile.base file for naming the container, pushing to git and libraries used. If you want integration with XNAT navigate to the "xnat" folder and edit the command.json documentation available at @ https://wiki.xnat.org/container-service/making-your-docker-image-xnat-ready-122978887.html#MakingyourDockerImage%22XNATReady%22-installing-a-command-from-an-xnat-ready-image

  * NOTE this was designed to be generalized to the mat type data. If you would like to just use the notebook or just the library it is recommend you visit: https://github.com/ythackerCS/NURO_DOT_py_dev which has the library files, and the same files for you to get started with creating your own pipleines.  

## Running (ON XNAT): 
  * Navigate to a Subject
  * Click on Run Containers and then click "Run presprocessing pipleine with subject data mounted" 
  * Select the folder with the data in it and hit run 

## Running in general: 
  * NeuroDOT_PreProcessing_Script_dynamicFilterMode.ipynb will read the RTStruct create a copy and then search through it for given filters, then scale the given ROI(s)
  * There are arguments needed to run this pipline which can be found within the scale.py script 
  * There is an upload componenet unique to XNAT if you just want to run it without uploading you can comment out that component. 

## NOTES: 
  * This was a test method container to see how well papermill works and to try a different form of running scripts typically you would convert your work to a .py file 
  * Parts of the scripts within workspace were written with project specificity in mind so please keep that in mind as you use this code 
  * It is recommended that you have some experience working with docker and specficially building containers for xnat for this to work for your use cases 
  * If you just want to use the code for your own work without docker stuff just navigate the original Neurodot library @ https://github.com/ythackerCS/NURO_DOT_py_dev which has the library files, and the same files for you to get started with creating your own pipleines.  
  
## Future: 
  
