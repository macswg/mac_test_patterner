# mac_rep_town

This is a pixel map generator for creating custom .png images with pixel-accurate test patterns for LED walls and projection surfaces.

As of Jan 2022 the software is command line interface only and because it is python code, it requires python to be installed. 

The program is writted in Python 3.9

There are four scripts:
1) TestPatternMakerX.py - this is the main script. Running this script allows you to enter the pixelspace and resolution information. This main script calls the 'raster_maker.py' script to generate the individual rasters. 
2) raster_maker.py - meant to be called my the main script.
3) greyStepsPatternMaker.py - creates a test pattern for identifying issues with limited vs full color space.
4) SgLedTestPattern_v9_1.py - this is an old script that will be archived off eventually. 
