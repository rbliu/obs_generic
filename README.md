# obs_generic

Things We would Like obs_generic to do, but are hard with current packages:

## Simulated images:

* Read in images with arbitrary footprint (within limits, but NXM basically)

* Deal with the lack of astrometry and photometry references (i.e. deal with a missing WCS, arbitrary zeropoint, no HDU/CCD keyword)

* Perform psf mapping(?), source detection, deblending, shape measurement as if the sim is a coadd, but without having to go through multiband (at the moment we pretend identical instances are different filters).

* Notes to selves:  as  process, using obs_file is preferable.  We might get away with not having any stack/multiband, and getting the shapes out of something like processCCD?


## Outside-Processed data

* Read in pixel-level corrected images (i.e. bias, flats, non-linearity, cross-talk, BFE have been corrected already)

* Perform psf mapping(?), coaddition (possibly handling different coadds for depth/shape stability?)

* Perform source detection, deblending, shape measurement, forced photometry, masking

* Determine the starflat from reference catalog + dithers; write out the starflat as a fits image 

* Do joint astrometry across multiple bands


## DM-Stack Processed Data

* Run multi-band processing on coadds from images from different cameras

* Run exposure-level forced photometry on images from different cameras


## Tasks

* Straightforward renaming

* What fields should go in registry (and which are required vs optional): visit, sensor, source, filter,date/time,

* Function to add something to registry

* Update mapper policy to use new keys

* Write dummy ISR Task(s) that mangles actually-processed "raw" images into the postIsrCcd Exposures the stack expects.

* Fix up configuration defaults.

* Remove the CameraGeom; see what breaks
