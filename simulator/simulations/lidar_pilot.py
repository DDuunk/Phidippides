# ====== Legal notices
#
# Copyright (C) 2013 - 2020 GEATEC engineering
#
# This program is free software.
# You can use, redistribute and/or modify it, but only under the terms stated in the QQuickLicence.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY, without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the QQuickLicence for details.
#
# The QQuickLicense can be accessed at: http://www.geatec.com/qqLicence.html
#
# __________________________________________________________________________
#
#
#  THIS PROGRAM IS FUNDAMENTALLY UNSUITABLE FOR CONTROLLING REAL SYSTEMS !!
#
# __________________________________________________________________________
#
# It is meant for training purposes only.
#
# Removing this header ends your licence.
#
import sys
sys.path.append('../../')
import time as tm
import traceback as tb
import math
import simpylc as sp
from utils import pid as pid
from lidar_algorithm import obstacleAvoidance as oa

class LidarPilot:
    def __init__ (self):
        print ('Use up arrow to start, down arrow to stop')
        
        self.driveEnabled = False
        sp.world.physics.proportional.set(0.40)
        sp.world.physics.intergral.set(20)
        sp.world.physics.differential.set(15)
        self.steeringPID = pid.Pid(sp.world.physics.proportional,sp.world.physics.intergral, sp.world.physics.differential)
        sp.world.physics.velocity.set(0)
        sp.world.physics.positionX.set(-6)
        sp.world.physics.positionY.set(6)
        avoider = oa.obstacleAvoidance(sp.world.visualisation.lidar.halfApertureAngle, self.steeringPID)
        while True:
            key = sp.getKey ()
            if key == 'KEY_UP':
                self.driveEnabled = True
            elif key == 'KEY_DOWN':
                self.driveEnabled = False

            values = avoider.calculateSteeringAngle (self.driveEnabled,sp.world.visualisation.lidar.roadDistances, sp.world.visualisation.lidar.distances, sp.world.physics.steeringAngle)
            sp.world.physics.steeringAngle.set (values[0])
            sp.world.physics.targetVelocity.set (values[1])
            tm.sleep (0.02)
        