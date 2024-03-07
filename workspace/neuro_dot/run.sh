#!/bin/bash


die(){
    echo >&2 "$@"
    exit 1
}

echo $@

SUBJECT_MAT=$1
shift
PARAMS=$1

dt=`date --utc +%Y%m%d-%H%M%S`

echo dt 

OUTPUTFOLDER_NOTEBOOK="/outputfiles/${dt}_preprocessing_notebook"
OUTPUTFOLDER_IMAGES="/outputfiles/${dt}_images/"

mkdir $OUTPUTFOLDER_NOTEBOOK $OUTPUTFOLDER_IMAGES

echo 'papermill neuro_dot/NeuroDOT_PreProcessing_Notebook.ipynb $OUTPUTFOLDER_NOTEBOOK/output.ipynb -p patient_data /input/$SUBJECT_MAT -p params_file /input/$PARAMS -p saveImagePath $OUTPUTFOLDER_IMAGES'

papermill neuro_dot/NeuroDOT_PreProcessing_Notebook.ipynb $OUTPUTFOLDER_NOTEBOOK/output.ipynb -p participant_data /input/$SUBJECT_MAT -p params_file /input/$PARAMS -p saveImagePath $OUTPUTFOLDER_IMAGES