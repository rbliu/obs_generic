import os.path

from lsst.utils import getPackageDir

config.processCcd.load(os.path.join(getPackageDir("obs_generic"), "config", "processCcd.py"))
config.ccdKey = 'ccd'
