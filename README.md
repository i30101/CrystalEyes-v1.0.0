# CrystalEyes

TODO update these
![version](https://img.shields.io/badge/release-v1.0.0-blue)
![python-versions](https://img.shields.io/badge/python-3.11_%7C_3.12_%7C_3.13-limegreen)
![cellpose-version](https://img.shields.io/badge/cellpose-4.0.6-red)
[![Licence: MIT](https://img.shields.io/github/license/i30101/CrystalEyes-v1.0.0)](https://github.com/i30101/CrystalEyes-v1.0.0/blob/master/LICENSE)
![issues](https://img.shields.io/github/issues/i30101/CrystalEyes-v1.0.0)
[![repo size](https://img.shields.io/github/repo-size/i30101/CrystalEyes-v1.0.0)](https://github.com/i30101/CrystalEyes-v1.0.0/)




<br>
A Python app for analyzing microscope images of nano-ice crystal growth using Python and machine learning.

### How it works
CrystalEyes uses Python and the Cellpose machine learning library to extract data from images of ice crystal growth. It processes binary Linkam Data Files to extract temperature data and images. These images are analyzed to extract values such as average area, density, and coverage of ice crystals. The GUI, made using Tkinter and Ttk, provides a simple user experience.




## Changelog

### Version 1.0.0: app rehaul
Version `1.0.0` introduces a new GUI and support for LDF files only. In contrast to versions `0.8.0` and `0.9.0`, LDF support enables instant processing of images. You do not have to export images and video files from Linkam manually; the built-in binary parser does that instead. 

> [!WARNING]
> Timestamp data is not available for this version. The app will not process timestamps from LDF files.

### Version 1.2.0: what's new
- Extraction of additional variables (see below for full list)
- Fixed debugging console

### Full Release Schedule

| Version  | Description                                                 | 
|----------|-------------------------------------------------------------| 
| `v1.2.0` | Fully functioning user interface / LDF parser / CV analysis |
| `v1.0.0` | Beta testing for new UI                                     |
| `v0.9.0` | Beta testing for LDF parser                                 |
| `v0.8.0` | OCR-dependent, outdated                                     |




## Dependencies




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