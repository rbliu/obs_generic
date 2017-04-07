# This task aims to transfer the post-ISR images to a correct Butler-style path with an appropriate filename.
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

import lsst.afw.image as afwImage
import lsst.afw.image.utils as afwImageUtils
from lsst.pex.config import Config, Field, DictField, ListField, ConfigurableField
import lsst.pex.exceptions
from lsst.pipe.base import Task, InputOnlyArgumentParser
from lsst.daf.persistence import ButlerLocation, Policy



def transferPostIsr(parser.file, parser.source, parser.visit, parser.ccd):
        
    args = parser.parse_args()

    visit_str = str(args.visit).zfill(8)
    ccd_str = str(args.ccd).zfill(3)

    outpath = 'postISR/' + args.source + '/v' + visit_str
    outfile = os.getcwd() + '/' + outpath + '/postISR-' + visit_str + '_' + ccd_str + '.fits'

    if not os.path.isdir(outpath):
        try:
            os.makedirs(outpath)
        except:
            if not os.path.isdir(outpath):
                raise

    os.symlink(os.path.abspath(args.file), outfile)

    original_fits = pyfits.open(os.path.abspath(args.file))
    original_data = original_fits[0].data

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

    hdr = afwImg.readMetadata(args.file)
    wcs = afwImg.makeWcs(hdr)

    exposure = lsst.afw.image.ExposureF(original_data.shape[1], original_data.shape[0])
    exposure.getMaskedImage().getImage().getArray()[:,:] = data
    exposure.getMaskedImage().getVariance().getArray()[:,:] = getVar(data)
    exposure.setWcs(wcs)

    exposure.writeFits(outfile)



    print(os.path.abspath(args.file) + '  <-->  ' + outfile)


#if __name__ == "__main__":
#    task = TransferPostIsrTask()
#    task.main()

