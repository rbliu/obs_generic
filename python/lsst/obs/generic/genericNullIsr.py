#!/usr/bin/env python
#
# LSST Data Management System
# Copyright 2008-2015 AURA/LSST.
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
# see <https://www.lsstcorp.org/LegalNotices/>.
#
from __future__ import absolute_import, division, print_function

import lsst.pipe.base as pipeBase
import lsst.pex.config as pexConfig


class GenericNullIsrConfig(pexConfig.Config):
    pass

## \addtogroup LSST_task_documentation
## \{
## \page GenericNullIsrTask
## \ref GenericNullIsrTask_ "GenericNullIsrTask"
## \copybrief GenericNullIsrTask
## \}


class GenericNullIsrTask(pipeBase.Task):
    """!Load a post-ISR CCD exposure

    @anchor GenericNullIsrTask_

    @section pipe_tasks_genericNullIsr_Contents  Contents

     - @ref pipe_tasks_genericNullIsr_Purpose
     - @ref pipe_tasks_genericNullIsr_Initialize
     - @ref pipe_tasks_genericNullIsr_IO
     - @ref pipe_tasks_genericNullIsr_Config

    @section pipe_tasks_genericNullIsr_Purpose  Description

    Load a post-ISR exposure, and optionally persist it as a `postISRCCD`.

    This is used to retarget the `isr` subtask in `ProcessCcdTask` when you input a pre-processed image to LSST DMstack.

    @section pipe_tasks_genericNullIsr_Initialize  Task initialisation

    @copydoc \_\_init\_\_

    @section pipe_tasks_genericNullIsr_IO  Invoking the Task

    The main method is `runDataRef`.

    @section pipe_tasks_genericNullIsr_Config  Configuration parameters

    See @ref GenericNullIsrConfig
    """
    ConfigClass = GenericNullIsrConfig
    _DefaultName = "isr"

    @pipeBase.timeMethod
    def runDataRef(self, sensorRef):
        """!Load a post-ISR CCD exposure

        @param[in] sensorRef  butler data reference for post-ISR exposure
            (a daf.persistence.butlerSubset.ButlerDataRef)

        @return a pipeBase.Struct with fields:
        - exposure: exposure after application of ISR: the "postISRCCD" exposure, unchanged
        """
        self.log.info("Loading a post-ISR image file %s" % (sensorRef.dataId))

        exposure = sensorRef.get("postISRCCD", immediate=True)

        return pipeBase.Struct(
            exposure=exposure,
        )
