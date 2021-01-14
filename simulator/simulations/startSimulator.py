#! /usr/bin/python

# ====== Legal notices
#
# Copyright (C) 2013  - 2020 GEATEC engineering
#
# This program is free software.
# You can use, redistribute and/or modify it, but only under the terms stated in the QQuickLicence.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY, without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the QQuickLicence for details.
#
# The QQuickLicense can be accessed at: http://www.qquick.org/license.html
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
from __future__ import print_function, unicode_literals
from PyInquirer import prompt, print_json
import os
import sys as ss

ss.path.append (os.path.abspath ('../../..')) # If you want to store your simulations somewhere else, put SimPyLC in your PYTHONPATH environment variable

import simpylc as sp
from utils import control as ct
import keyboard_pilot as kp
import lidar_pilot as lp
import camera_pilot as cp
from utils import physics as ps
import visualisation as vs
from utils import timing as tm

questions = [
    {
        'type': 'list',
        'name': 'sensor',
        'message': 'Which sensor do you want to simulate?',
        'choices': [ 'Camera','Li-Dar', 'Keyboard']
    }
]

answers = prompt(questions)

if (answers['sensor'] == 'Camera'):
    sp.World (
        cp.CameraPilot,
        ps.Physics,
        vs.Visualisation,
        tm.Timing
    )  

elif(answers['sensor'] == 'Li-Dar'):
    sp.World (
        lp.LidarPilot,
        ps.Physics,
        vs.Visualisation,
        tm.Timing
    )  
elif(answers['sensor'] == 'Keyboard'):
    sp.World (
        ct.Control,
        kp.KeyboardPilot,
        ps.Physics,
        vs.Visualisation,
        tm.Timing,
    )
