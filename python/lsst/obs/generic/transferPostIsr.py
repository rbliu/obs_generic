# obs_generic
#
# Before running processCcd.py with obs_generic, the post-ISR image must be put under the directory
# ./postISR/%(source)s/v%(visit)08d/postISR-%(visit)08d_%(ccd)03d.fits
#
# This piece of code aims to create a copy of the post-ISR image (ccd) with appropriate filename
# such that the pipeline can access to it.
#
# Usage:
# transferPostIsr.py <post-ISR image.fits> --source <source name> --visit <visit num> --ccd <ccd num>

from __future__ import absolute_import, division, print_function
import os
import pyfits
from past.builtins import basestring
from builtins import object
import shutil
import argparse
import tempfile
import string
import sys
import numpy as np

import lsst.afw.image as afwImg
import lsst.afw.image.utils as afwImageUtils
from lsst.pex.config import Config, Field, DictField, ListField, ConfigurableField
import lsst.pex.exceptions
from lsst.pipe.base import Task, InputOnlyArgumentParser
from lsst.daf.persistence import ButlerLocation, Policy



def transferPostIsr(file, source, visit, ccd):
    
    visit_str = str(visit).zfill(8)
    ccd_str = str(ccd).zfill(3)

    outpath = 'postISR/' + source + '/v' + visit_str
    outfile = os.getcwd() + '/' + outpath + '/postISR-' + visit_str + '_' + ccd_str + '.fits'
    
    if os.path.isfile(outfile):
        print("The post-ISR already exists: " + outfile + "\n")
    
    
    else:
    
        if not os.path.isdir(outpath):
            try:
                os.makedirs(outpath)
            except:
                if not os.path.isdir(outpath):
                    raise

        if source=='decam':

            #os.symlink(os.path.abspath(file), outfile)
            original_fits = pyfits.open(os.path.abspath(file))
            original_data = original_fits[1].data
        
            print(original_fits[0].header['FILTER'])

            def getVar(data):
            # estimate variance (read out noise + sky photon noise)
            # from edges of the frame
                pad = 10
                var = np.var(np.concatenate((
                                         data[:pad,:].flatten(),
                                         data[:,:pad].flatten(),
                                         data[-pad:,:].flatten(),
                                         data[:,-pad:].flatten() )))
                return var

            hdr = afwImg.readMetadata(file)
            wcs = afwImg.makeWcs(hdr)

            exposure = lsst.afw.image.ExposureF(original_data.shape[1], original_data.shape[0])
            exposure.getMaskedImage().getImage().getArray()[:,:] = original_data
            exposure.getMaskedImage().getVariance().getArray()[:,:] = getVar(original_data)
            exposure.setWcs(wcs)

            exposure.writeFits(outfile)
        
            out_fits = pyfits.open(outfile, mode='update')
            prihdr = out_fits[0].header
            prihdr['FILTER'] = 'decam_z'
            out_fits.flush()
            out_fits.close()

        elif source=='cfht':

            os.symlink(os.path.abspath(file), outfile)

        else:

            os.symlink(os.path.abspath(file), outfile)

        print(os.path.abspath(file) + '  <-->  ' + outfile + "\n")


#if __name__ == "__main__":
#    task = TransferPostIsrTask()
#    task.main()

