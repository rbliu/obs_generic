import os.path
from lsst.utils import getPackageDir

from lsst.obs.generic.genericNullIsr import GenericNullIsrTask
config.isr.retarget(GenericNullIsrTask)

"""
config.isr.doBias = False
config.isr.doDark = False
config.isr.doFlat = False
config.isr.doFringe = False
config.isr.fringeAfterFlat = False
config.isr.doWrite = False
config.isr.setGainAssembledCcd = True
config.isr.assembleCcd.setGain = False
config.isr.fringe.filters = ['i', 'i2', 'z']
config.isr.fringe.pedestal = True
config.isr.fringe.small = 1
config.isr.fringe.large = 50
config.isr.doAssembleIsrExposures = True

config.charImage.repair.doCosmicRay=True
config.charImage.repair.cosmicray.cond3_fac=2.5
config.charImage.repair.cosmicray.cond3_fac2=0.4
config.charImage.repair.cosmicray.niteration=3
config.charImage.repair.cosmicray.nCrPixelMax=100000
config.charImage.repair.cosmicray.minSigma=6.0
config.charImage.repair.cosmicray.min_DN=150.0

try :
    # AstrometryTask, the default
    config.calibrate.refObjLoader.filterMap = {
        'i2': 'i',
    }
    config.calibrate.astrometry.wcsFitter.order = 3
    config.calibrate.astrometry.matcher.maxMatchDistArcSec=5
except :
    # ANetAstrometryTask
    config.calibrate.astrometry.solver.filterMap = {
        'i2': 'i',
    }

config.calibrate.photoCal.applyColorTerms = True
config.calibrate.photoCal.photoCatName="e2v"
"""
