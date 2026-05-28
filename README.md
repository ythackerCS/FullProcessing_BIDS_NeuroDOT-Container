# FullProcessing BIDS NeuroDOT Container

## Overview

`FullProcessing_BIDS_NeuroDOT-Container` is a Docker container for running a full NeuroDOT processing workflow on functional near-infrared spectroscopy (fNIRS) and diffuse optical tomography (DOT) data. The workflow combines preprocessing, quality control, reconstruction, spectroscopy, visualization, and output export into a single reproducible containerized pipeline.

The container uses Papermill to execute the notebook:

```text
workspace/neuro_dot/NeuroDot_FullProcessingPipeline.ipynb
```

This workflow was designed to support XNAT/OXI-based fNIRS data processing while also providing a reusable notebook-based pipeline for researchers working with NeuroDOT data.

## Motivation

Full fNIRS/DOT processing often requires multiple manual steps, including raw-data quality control, filtering, superficial signal regression, block averaging, image reconstruction, spectroscopy, and visualization. Running these steps manually can make results harder to reproduce across users, projects, and institutions.

This container packages the NeuroDOT full-processing workflow into a reproducible Docker environment so that the same processing steps can be run consistently through XNAT Container Service or adapted for local Docker use.

## Workflow Summary

The full-processing notebook performs the following major steps:

1. Loads fNIRS/DOT data and metadata from a `.mat` file.
2. Loads processing parameters from a JSON-style `params.txt` file.
3. Generates raw-data quality-control visualizations.
4. Applies logmean transformation.
5. Detects good and noisy measurements.
6. Visualizes measurement quality across source-detector distances.
7. Applies detrending and temporal filtering.
8. Performs superficial signal regression.
9. Applies additional low-pass filtering and resampling.
10. Performs block averaging based on paradigm synchronization points.
11. Loads the sensitivity matrix, extinction matrix, and MNI/anatomical files.
12. Performs image reconstruction using Tikhonov inversion.
13. Converts reconstructed absorption changes into hemoglobin measures.
14. Generates volumetric and surface-ready visualization outputs.
15. Saves derived matrices and outputs to a `.mat` file.

## Key Features

- Runs full NeuroDOT processing through a Papermill-executed Jupyter notebook
- Supports preprocessing and reconstruction in one workflow
- Generates raw-data QC plots and signal-quality visualizations
- Applies logmean transformation, detrending, filtering, resampling, and block averaging
- Performs superficial signal regression
- Runs DOT image reconstruction using sensitivity matrices
- Computes hemoglobin measures including HbO, HbR, and HbT
- Supports anatomical visualization using MNI and atlas resources
- Saves generated figures, executed notebooks, and derived `.mat` outputs
- Designed for XNAT Container Service and OXI-style workflows
- Can be adapted for project-specific NeuroDOT datasets

## Inputs

The notebook expects several input resources. Paths may be edited at the beginning of the notebook.

Example default paths include:

```text
participant_data = "./Data/NeuroDOT_Data_Sample_CCW1.mat"
params_file = "./Data/params.txt"
Emat = "/Project/E_matrices/E.mat"
MNI_file = "/Project/MNI_files/Segmented_MNI152nl_on_MNI111_py"
A_fn = "/Project/A_matrices/A_AdultV24x28.mat"
MNI_path = "NONE"
```

### Required Inputs

- fNIRS/DOT participant data in `.mat` format
- `params.txt` file containing processing parameters
- Sensitivity matrix, such as an `A` matrix
- Extinction matrix, such as an `E` matrix
- MNI or anatomical reference files for visualization
- NeuroDOT Python library files available inside the container

### Example Data

The notebook includes default references to sample NeuroDOT data:

```text
./Data/NeuroDOT_Data_Sample_CCW1.mat
```

This sample is intended for testing and demonstration. For project-specific use, edit the input paths at the beginning of the notebook.

## Outputs

The workflow saves outputs to the configured output directory.

Default output path:

```text
./outputfiles
```

Expected outputs may include:

- Executed full-processing notebook
- Saved QC and processing figures
- Reconstructed absorption matrices
- Hemoglobin matrices, including HbO, HbR, and HbT
- MNI-aligned visualization objects
- Reconstruction parameters
- Final `.mat` file containing derived matrices

The saved `.mat` file is named using the participant file name, parameter file name, and optional tag.

Example output naming logic:

```text
participant_used + "_" + params_used + "_" + optionalTag + ".mat"
```

## Saved Matrices

The notebook saves several derived outputs into the `savedMatricies` dictionary before exporting to `.mat`.

Common saved outputs include:

```text
cortex_mu_a
cortex_Hb
MNI_dim
Params_recon
```

These outputs can be used for downstream visualization, statistical analysis, or additional processing.

## Repository Structure

```text
FullProcessing_BIDS_NeuroDOT-Container/
|-- workspace/
|   |-- neuro_dot/
|   |   |-- NeuroDot_FullProcessingPipeline.ipynb
|   |   |-- NeuroDOT library files
|-- xnat/
|   |-- command.json
|-- Dockerfile.base
|-- build.sh
|-- README.md
```

Update this section if the local repository structure changes.

## Requirements

The required Python packages are defined in `Dockerfile.base`.

Core packages used by the notebook include:

- `numpy`
- `matplotlib`
- `scipy`
- `mat73`
- `json`
- `papermill`
- NeuroDOT Python modules

The notebook imports NeuroDOT modules including:

```text
Visualizations
Spatial_Transforms
Temporal_Transforms
Light_Modeling
File_IO
Analysis
Matlab_Equivalent_Functions
Reconstruction
```

Additional requirements:

- Docker
- XNAT Container Service, if running through XNAT
- NeuroDOT-compatible `.mat` data
- Sensitivity and extinction matrix resources
- MNI/anatomical resources for reconstruction visualization

## Installation and Build

Clone the repository:

```bash
git clone https://github.com/ythackerCS/FullProcessing_BIDS_NeuroDOT-Container.git
cd FullProcessing_BIDS_NeuroDOT-Container
```

Edit the notebook input paths and parameters as needed:

```text
workspace/neuro_dot/NeuroDot_FullProcessingPipeline.ipynb
```

Build the Docker container:

```bash
./build.sh
```

If deploying through XNAT, update the XNAT command configuration:

```text
xnat/command.json
```

XNAT Container Service documentation is available here:

```text
https://wiki.xnat.org/container-service/making-your-docker-image-xnat-ready-122978887.html
```

## Running on XNAT

1. Navigate to the relevant subject or session in XNAT.
2. Select **Run Containers**.
3. Choose the NeuroDOT full-processing container command.
4. Select the resource folder containing the fNIRS/DOT input data.
5. Confirm any required mounted project resources, such as A matrices, E matrices, MNI files, or parameter files.
6. Run the container.
7. Review outputs, including saved figures, executed notebook, and exported `.mat` files.

## Running Outside XNAT

This container can be adapted for local Docker execution by manually mounting input and output directories.

Example pattern:

```bash
docker run --rm \
  -v /path/to/data:/Data:ro \
  -v /path/to/project/resources:/Project:ro \
  -v /path/to/output:/outputfiles \
  fullprocessing-bids-neurodot:latest
```

The exact command may differ depending on the container entrypoint and local path structure.

If running outside XNAT, users may need to modify or remove XNAT-specific upload logic.

## Notebook Configuration

Most project-specific edits should be made near the beginning of:

```text
workspace/neuro_dot/NeuroDot_FullProcessingPipeline.ipynb
```

Common values to update include:

```python
saveImages = "yes"
saveMatPath = "./outputfiles"
saveImagePath = "./outputfiles"
saveNoteBookPath = "./outputfiles"

participant_data = "./Data/NeuroDOT_Data_Sample_CCW1.mat"
params_file = "./Data/params.txt"
Emat = "/Project/E_matrices/E.mat"
MNI_file = "/Project/MNI_files/Segmented_MNI152nl_on_MNI111_py"
A_fn = "/Project/A_matrices/A_AdultV24x28.mat"
MNI_path = "NONE"
optionalTag = ""
```

Processing parameters are loaded from:

```text
params.txt
```

Individual parameters may also be overwritten directly inside the notebook if needed.

## Processing Details

### Raw Data QC

The notebook generates several raw-data quality-control plots, including:

- Raw time trace overview
- Spectrum and falloff metrics
- Cap-level data quality views
- Source-detector distance visualizations

### Preprocessing

The preprocessing workflow includes:

- Logmean transformation
- Good-measurement detection
- Detrending
- High-pass filtering
- Low-pass filtering
- Superficial signal regression
- Resampling
- Block averaging

### Reconstruction

The reconstruction workflow includes:

- Loading an A matrix
- Inverting the A matrix using Tikhonov regularization
- Smoothing the inverted A matrix
- Reconstructing absorption changes
- Applying spectroscopy using an E matrix
- Computing HbO, HbR, and HbT

### Visualization

The workflow supports:

- Volumetric visualization
- Flat-field reconstruction visualization
- MNI-aligned visualization
- Block-averaged hemoglobin visualization
- Optional surface visualization

Some interactive plotting commands are included in the notebook but commented out by default.

## Customization

Users may need to customize:

- input `.mat` file paths
- parameter file paths
- A matrix path
- E matrix path
- MNI file path
- output folders
- block length and paradigm synchronization points
- visualization thresholds
- XNAT input and output resource names

This workflow was developed for NeuroDOT-compatible `.mat` data and may require adaptation for other data formats or study designs.

## Related Projects

- [NeuroDOT_py](https://github.com/WUSTL-ORL/NeuroDOT_py): Python toolbox for optical brain mapping
- [fNIRSPluginXNAT](https://github.com/ythackerCS/fNIRSPluginXNAT): XNAT plugin for organizing fNIRS data
- [Preprocessing_BIDS_NeuroDOT-Container](https://github.com/ythackerCS/Preprocessing_BIDS_NeuroDOT-Container): Containerized NeuroDOT preprocessing workflow
- [Reconstruction_BIDS_NeuroDOT-Container](https://github.com/ythackerCS/Reconstruction_BIDS_NeuroDOT-Container): Containerized NeuroDOT reconstruction workflow
- [OXI](https://oxi.wustl.edu): Optical-imaging XNAT-enabled Informatics platform

## Notes

This container was developed as research software for reproducible NeuroDOT processing in an XNAT/OXI environment. Some scripts and notebook cells may contain project-specific assumptions and may require modification for new datasets, acquisition structures, or deployment environments.

Users should have experience with Docker, XNAT Container Service, and NeuroDOT workflows before adapting this container for production use.

For users who only want to use NeuroDOT without Docker or XNAT integration, see:

```text
https://github.com/WUSTL-ORL/NeuroDOT_py
```

## Status

Research software. This container may require adaptation for specific fNIRS/DOT datasets, XNAT deployments, or NeuroDOT workflow updates.

## Future Work

Potential future improvements include:

- Generalizing input handling across more NeuroDOT-compatible datasets
- Improving BIDS compatibility and validation
- Adding clearer checks for required A, E, and MNI resources
- Improving error reporting for failed notebook execution
- Adding local Docker execution examples
- Adding sample test data and expected output structure
- Expanding XNAT deployment documentation
- Adding automated output validation and QC summaries
