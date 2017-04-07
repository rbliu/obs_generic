#!/usr/bin/env python

import argparse
import string
import os
#from lsst.pipe.base import Task, InputOnlyArgumentParser

parser = argparse.ArgumentParser(description='transfer the image.')

parser.add_argument('file', metavar='file', type=str, help='give the image filename')
parser.add_argument('--source', metavar='source', type=str, help='name of telescope/camera')
parser.add_argument('--visit', metavar='visit', type=int, help='visit number must have no more than 8 digits')
parser.add_argument('--ccd', metavar='ccd', type=int, help='ccd number must have no more than 3 digits')


from lsst.obs.generic.transferPostIsr import transferPostIsr
transferPostIsr(parser.file, parser.source, parser.visit, parser.ccd)
