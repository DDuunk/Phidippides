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

import time as tm
import traceback as tb
import math

class obstacleAvoidance:
    def __init__ (self, lidarHalfApertureAngle, pid):
        self.steeringPID = pid
        self.lidarHalfApertureAngle = lidarHalfApertureAngle
        
    def calculateSteeringAngle (self, driveEnabled, lidarDistances, obstacleDistances, steeringAngle):   # Control algorithm to be tested
        self.driveEnabled = driveEnabled
        self.lidarDistances = lidarDistances
        self.obstacleDistances = obstacleDistances

        self.leftRoadBorder = 1e20
        self.leftRoadBorderAngle = 0
        
        self.nextLeftRoadBorder = 1e20
        self.nextLeftRoadBorderAngle = 0

        self.rightRoadBorder = 1e20
        self.rightRoadBorderAngle = 0
        
        self.nextRightRoadBorder = 1e20
        self.nextRightRoadBorderAngle = 0
        self.alternativeCoordinates = (0,0)
        self.closestObstacleDistance = 1e20
        self.closestObstacleAngle = 0
        for lidarAngle in range (-self.lidarHalfApertureAngle, self.lidarHalfApertureAngle):
            lidarDistance = self.lidarDistances [lidarAngle]
            obstacleDistance = self.obstacleDistances [lidarAngle]
            
            # Detect 4 closest points of road borders
            self.calculateFourClosestPoints(lidarAngle,lidarDistance)
            # Detect closest obstacle
            self.calculateClosestObstacle(obstacleDistance, lidarAngle)

        #check if obstacle within current direction
        #and calculate coordinates for middle point with or without obstacle
        self.coordinatesNR = self.calculateCoordinates(self.nextRightRoadBorderAngle, self.nextRightRoadBorder)
        self.coordinatesR = self.calculateCoordinates(self.rightRoadBorderAngle, self.rightRoadBorder)
        self.coordinatesNL = self.calculateCoordinates(self.nextLeftRoadBorderAngle, self.nextLeftRoadBorder)
        self.coordinatesL = self.calculateCoordinates(self.leftRoadBorderAngle, self.leftRoadBorder)
        self.coordinatesO = self.calculateCoordinates(self.closestObstacleAngle, self.closestObstacleDistance)
        
        #if obstacle within reach avoid
        if(self.closestObstacleAngle > -30 and self.closestObstacleAngle < 30 and self.isObstacleWithinDirection()):
            self.avoidObstacleCollision()
       
        self.xMiddle = self.coordinatesL[0] + self.coordinatesNL[0] + self.coordinatesR[0] + self.coordinatesNR[0]
        self.yMiddle = self.coordinatesL[1] + self.coordinatesNL[1] + self.coordinatesR[1] + self.coordinatesNR[1]

        #set steering angle
        self.steeringAngle = steeringAngle
        self.controlSteeringAngle()
        #set velocity
        self.targetVelocity = (90 - abs (self.steeringAngle))/75 if self.driveEnabled else 0
        
        return (self.steeringAngle, self.targetVelocity)

    def calculateClosestObstacle(self,distance, angle):
        if(self.closestObstacleDistance > distance):
            self.closestObstacleDistance = distance
            self.closestObstacleAngle = angle

    #check if obstacle closer than road borders
    def isObstacleWithinDirection(self):
        if(self.nextRightRoadBorder < self.closestObstacleDistance and
         self.rightRoadBorder < self.closestObstacleDistance and
         self.nextLeftRoadBorder < self.closestObstacleDistance and
         self.leftRoadBorder < self.closestObstacleDistance ):
            return False
        return True

    def avoidObstacleCollision(self):
        distanceL = math.sqrt(math.pow(abs(self.coordinatesO[0] - self.coordinatesL[0]),2) +  math.pow(abs(self.coordinatesO[1] - self.coordinatesL[1]),2))
        distanceR = math.sqrt(math.pow(abs(self.coordinatesO[0] - self.coordinatesR[0]),2) +  math.pow(abs(self.coordinatesO[1] - self.coordinatesR[1]),2))
        distanceNL = math.sqrt(math.pow(abs(self.coordinatesO[0] - self.coordinatesNL[0]),2) +  math.pow(abs(self.coordinatesO[1] - self.coordinatesNL[1]),2))
        distanceNR = math.sqrt(math.pow(abs(self.coordinatesO[0] - self.coordinatesNR[0]),2) +  math.pow(abs(self.coordinatesO[1] - self.coordinatesNR[1]),2))
        if(distanceL < distanceR and distanceL < distanceNL and distanceL < distanceNR):
            self.coordinatesL = (self.coordinatesO[0], self.coordinatesO[1] )
        elif(distanceR < distanceNL and distanceR < distanceNR):
            self.coordinatesR = (self.coordinatesO[0], self.coordinatesO[1] )
        elif(distanceNL < distanceNR):
            self.coordinatesNL = (self.coordinatesO[0], self.coordinatesO[1] )
        else:
            self.coordinatesNR = (self.coordinatesO[0], self.coordinatesO[1] )

    def calculateFourClosestPoints(self, lidarAngle, lidarDistance):
        # discard points within 25 degrees to avoid a head on collision  
        if lidarDistance < self.leftRoadBorder and lidarAngle < -25:
            self.nextLeftRoadBorder =  self.leftRoadBorder
            self.nextLeftRoadBorderAngle = self.leftRoadBorderAngle 
            self.leftRoadBorder = lidarDistance 
            self.leftRoadBorderAngle = lidarAngle
        elif lidarDistance < self.rightRoadBorder and lidarAngle > 25: 
            self.nextRightRoadBorder =  self.rightRoadBorder
            self.nextRightRoadBorderAngle = self.rightRoadBorderAngle
            self.rightRoadBorder = lidarDistance 
            self.rightRoadBorderAngle = lidarAngle
        elif lidarDistance < self.nextLeftRoadBorder and lidarAngle < -25:
            self.nextLeftRoadBorder = lidarDistance
            self.nextLeftRoadBorderAngle = lidarAngle
        elif lidarDistance < self.nextRightRoadBorder and lidarAngle > 25:
            self.nextRightRoadBorder = lidarDistance
            self.nextRightRoadBorderAngle = lidarAngle

    def calculateCoordinates(self, angle, distance):
        x = math.cos(math.radians(angle)) * distance
        y = math.sin(math.radians(angle)) * distance
        return (x,y)

    def controlSteeringAngle(self): 
        soughtAfterAngle = math.degrees(math.atan((self.yMiddle / self.xMiddle)))
        currentAngle = self.steeringAngle
        self.steeringAngle = self.steeringPID.control(currentAngle, soughtAfterAngle, 0.02)
