# <p> <b>CrystalEyes</b></p>


<img src="/assets/splash.png" width="300" title="cellpose" alt="cellpose" align="right" vspace="50">



![version](https://img.shields.io/badge/release-v1.2.0-blue)
![python-versions](https://img.shields.io/badge/python-3.9_%7C_3.10_%7C_3.11_%7C_3.12-limegreen)
![cellpose-version](https://img.shields.io/badge/cellpose-3.0.10-red)
![cellpose-version](https://img.shields.io/badge/NumPy-1.26-yellow)
[![Licence: MIT](https://img.shields.io/github/license/i30101/CrystalEyes-v1.0.0)](https://github.com/i30101/CrystalEyes-v1.0.0/blob/master/LICENSE)
![issues](https://img.shields.io/github/issues/i30101/CrystalEyes-v1.0.0)
[![repo size](https://img.shields.io/github/repo-size/i30101/CrystalEyes-v1.0.0)](https://github.com/i30101/CrystalEyes-v1.0.0/)
<br><br>



A Python app for analyzing microscope images of nano-ice crystal growth using Python and machine learning.

### How it works
CrystalEyes uses Python and the Cellpose machine learning library to extract data from images of ice crystal growth. It processes binary Linkam Data Files to extract temperature data and images. These images are analyzed to extract values such as average area, density, and coverage of ice crystals. The GUI, made using Tkinter and Ttk, provides a simple user experience.
<br><br>




## Changelog

### Version 1.0.0: app rehaul
Version `1.0.0` introduces a new GUI and support for LDF files only. In contrast to versions `0.8.0` and `0.9.0`, LDF support enables instant processing of images. You do not have to export images and video files from Linkam manually; the built-in binary parser does that instead. 

> [!WARNING]
> Timestamp data is not available for this version. The app will not process timestamps from LDF files. The duration between each frame defaults to one minute.

### Version 1.2.0: what's new

This is the latest and fully functional version of CrystalEyes. Previous versions of CrystalEyes are in beta and not optimized for performance or user experience. The features newly added in this version are:

- Extraction of additional variables (see below for full list)
- Fixed debugging console
- Data boxes to quickly view temperature / rate / limit data along with interactive temperature graph
- Optimized data analysis and computer vision algorithms; average compute time on test machine (see below) ranges from 12-30 seconds, depending on the number of shapes present in a sample

### Full Release Schedule

| Version  | Description                                                    | 
|----------|----------------------------------------------------------------| 
| `v1.2.0` | Fully functioning user interface, parser, and analysis modules |
| `v1.0.0` | Non-functioning beta testing for new user interface            |
| `v0.9.0` | Non-functioning beta testing for Linkam Data File parser       |
| `v0.8.0` | Functioning and OCR-dependent, outdated                        |
<br>



## Dependencies
Unfortunately, CrystalEyes `v1.2.0` has highly specific dependencies. Most critical is Cellpose `3.0.10`, as the newer `4.0.6` is too-heavily GPU-reliant and requires Nvidia CUDA due to its larger neural network. The latest version of NumPy supported by Cellpose `3.0.10` is `1.26.4`, meaning Python versions `3.9`, `3.10`, `3.11`, or `3.12` are supported. 

> [!CAUTION]
> Python `3.13` does not support NumPy `1.26`. Please be aware of which Python version your system is using, as it may not support this software.

CrystalEyes `1.2.0` was primarily tested on a system with 32 GB RAM with an integrated Intel processor/graphics chip (the graphics card was not used). Expect 1.8-2.5 GB of RAM use during operation; CPU usage will spike for each frame analysis as well.

Microsoft's Redistributable C++ Compiler (often installed through [Visual Studio Build Tools](https://visualstudio.microsoft.com/downloads/?q=build+tools)) may be required to install NumPy `1.26`. If you are unable to download the C++ compiler, consider using an alternate Python interpreter and package manager (such as Miniconda). 

> [!NOTE]
> Python version `3.10.13` along with NumPy version `1.26.3` were used during testing, along with Miniconda3 as the interpreter.

A full list of 
<br>


## Setup

<br>


## Usage

<br>


### List of LDF variables
- File name
- Date
- Frame number
- Ramp number
- Temperature
- Temperature limit
- Temperature rate
- Raw images
- Processed images
- Processed data


### List of analysis variables
- Raw images
- Processed images
- Average areas (px^2)
- Average areas (um^2)
- Density (crystals per um^2)
- Coverage (ratio)