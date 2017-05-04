# Before running processCcd.py with obs_generic, the post-ISR image must be put under the directory
# ./postISR/%(source)s/v%(visit)08d/postISR-%(visit)08d_%(ccd)03d.fits
# This piece of code aims to create a soft link of the post-ISR image such that the pipeline can access to it.
#
# Usage:
# python transferPostIsr.py <post-ISR image.fits> --source <source name> --visit <visit num> --ccd <ccd num>

import argparse
import string
import os
#from lsst.pipe.base import Task, InputOnlyArgumentParser

parser = argparse.ArgumentParser(description='transfer the image.')

parser.add_argument('file', metavar='file', type=str, help='give the image filename')
parser.add_argument('--source', metavar='source', type=str, help='name of telescope/camera')
parser.add_argument('--visit', metavar='visit', type=int, help='visit number must have no more than 8 digits')
parser.add_argument('--ccd', metavar='ccd', type=int, help='ccd number must have no more than 3 digits')

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

print(os.path.abspath(args.file) + '  <-->  ' + outfile)
