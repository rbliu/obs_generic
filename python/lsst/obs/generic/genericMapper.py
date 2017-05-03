#
# LSST Data Management System
# Copyright 2012 LSST Corporation.
#
# This product includes software developed by the
# LSST Project (http://www.lsst.org/).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the LSST License Statement and
# the GNU General Public License along with this program.  If not,
# see <http://www.lsstcorp.org/LegalNotices/>.
#

# This file was originally copied from obs_cfht.
import os

import pyfits

import lsst.afw.geom as afwGeom
import lsst.afw.image as afwImage
import lsst.afw.image.utils as afwImageUtils

from lsst.obs.base import CameraMapper, exposureFromImage
import lsst.pex.policy as pexPolicy
from lsst.daf.persistence import ButlerLocation, Policy

# Solely to get boost serialization registrations for Measurement subclasses
import lsst.meas.algorithms  # flake8: noqa

class GenericMapper(CameraMapper):
    packageName = "obs_generic"

    def __init__(self, **kwargs):
        policyFile = Policy.defaultPolicyFile("obs_generic", "GenericMapper.yaml", "policy")
        #policy = pexPolicy.Policy(policyFile)
        policy = Policy(policyFile)
        
        #super(GenericMapper, self).__init__(policy, policyFile.getRepositoryPath(), **kwargs)
        super(GenericMapper, self).__init__(policy, os.path.dirname(policyFile), **kwargs)

        # The "ccd" provided by the user is translated through the registry into an extension name for the "raw"
        # template.  The template therefore doesn't include "ccd", so we need to ensure it's explicitly included
        # so the ArgumentParser can recognise and accept it.

        self.exposures['raw'].keyDict['ccd'] = int

        # define filters?
        #self.filterIdMap = dict(u=0, g=1, r=2, i=3, z=4, i2=5)
        self.filterIdMap = dict(u=0, g=1, r=2, i=3, z=4)
        
        afwImageUtils.defineFilter('u',  lambdaEff=380)
        afwImageUtils.defineFilter('g',  lambdaEff=450)
        afwImageUtils.defineFilter('r',  lambdaEff=600)
        afwImageUtils.defineFilter('i',  lambdaEff=770)
        #afwImageUtils.defineFilter('i2', lambdaEff=750)
        afwImageUtils.defineFilter('z',  lambdaEff=900)
        afwImageUtils.defineFilter('decam_u', lambdaEff=350, alias=['u DECam c0006 3500.0 1000.0', 'u'])
        
        

        # Ensure each dataset type of interest knows about the full range of keys available from the registry
        keys = {'source': str,
                'visit': int,
                'ccd': int,
                #'filter': str,
                }
        for name in ("raw", "calexp", "postISRCCD", "src", "icSrc", "icMatch"):
            self.mappings[name].keyDict.update(keys)


    def _extractDetectorName(self, dataId):
        return "ccd%02d" % dataId['ccd']
    
    def _computeCcdExposureId(self, dataId):
        """Compute the 64-bit (long) identifier for a CCD exposure.
            
        @param dataId (dict) Data identifier with source, visit, ccd
        """
        pathId = self._transformId(dataId)
        telescope = {'lsstSim':'0', 'lsst':'1', 'cfht':'2', 'decam':'3', 'hsc':'4', 'suprime':'5', 'sdss':'6', 'ctio':'7', 'wiyn':'8', 'kpno':'9', 'comCam':'10', 'dls':'11',  'monocam':'12'}
        source = long(telescope[pathId['source']])
        visit = long(pathId['visit'])
        ccd = long(pathId['ccd'])
        return source * 1000000000000 + visit * 1000 + ccd

    def bypass_ccdExposureId(self, datasetType, pythonType, location, dataId):
        """Hook to retrieve identifier for CCD"""
        return self._computeCcdExposureId(dataId)

    def bypass_ccdExposureId_bits(self, datasetType, pythonType, location, dataId):
        """Hook to retrieve number of bits in identifier for CCD"""
        return 43
    
    def _computeCoaddExposureId(self, dataId, singleFilter):
        """Compute the 64-bit (long) identifier for a coadd.

        @param dataId (dict)       Data identifier with tract and patch.
        @param singleFilter (bool) True means the desired ID is for a single-
                                   filter coadd, in which case dataId
                                   must contain filter.
        """
        tract = long(dataId['tract'])
        if tract < 0 or tract >= 128:
            raise RuntimeError('tract not in range [0,128)')
        patchX, patchY = map(int, dataId['patch'].split(','))
        for p in (patchX, patchY):
            if p < 0 or p >= 2**13:
                raise RuntimeError('patch component not in range [0, 8192)')
        id = (tract * 2**13 + patchX) * 2**13 + patchY
        if singleFilter:
            return id * 8 + self.filterIdMap[dataId['filter']]
        return id

    def bypass_CoaddExposureId_bits(self, datasetType, pythonType, location, dataId):
        return 1 + 7 + 13*2 + 3

    def bypass_CoaddExposureId(self, datasetType, pythonType, location, dataId):
        return self._computeCoaddExposureId(dataId, True)

    bypass_deepCoaddId = bypass_CoaddExposureId

    bypass_deepCoaddId_bits = bypass_CoaddExposureId_bits

    def bypass_deepMergedCoaddId(self, datasetType, pythonType, location, dataId):
        return self._computeCoaddExposureId(dataId, False)

    bypass_deepMergedCoaddId_bits = bypass_CoaddExposureId_bits

    def _makeCamera(self, policy, repositoryDir):
        return None

    def _setAmpDetector(self, item, dataId, trimmed):
        return None

    def _setCcdDetector(self, item, dataId, trimmed):
        return None

    def _setFilter(self, mapping, item, dataId):
#        filter_header_string = item.getMetadata().get("FILTER")
#        import pdb
#        pdb.set_trace()
        return None

#   The mapperClass cannot be a 'NoneType' object
    @classmethod
    def getCameraName(cls):
        return "generic"


def removeKeyword(md, key):
    """Remove a keyword from a header without raising an exception if it doesn't exist"""
    if md.exists(key):
        md.remove(key)
