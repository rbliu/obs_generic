# obs_generic

Things We would Like obs_generic to do, but are hard with current packages:

Simulated images:

Read in images with arbitrary footprint (within limits, but NXM basically)

Deal with the lack of astrometry and photometry references (i.e. deal with a missing WCS, arbitrary zeropoint, no HDU/CCD keyword)

Perform psf mapping(?), source detection, deblending, shape measurement as if the sim is a coadd, but without having to go through multiband (at the moment we pretend identical instances are different filters).
