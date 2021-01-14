# Obstacle avoidance algorithm
This algorithm is used to avoid incoming obstacles given by a Li-Dar.

## Usage
Use the obstacleAvoidance class with the following:
 - LidarHalfApertureAngle: With this value you can control which of the given lidar points are used in the algortithm.
 - Pid: This is used to control the steering angle.
 
 After the initialisation you can use the calculateSteeringAngle method.
 This method expects the following:
 - driveEnabled: boolean -> if the car is drving.
 - lidarDistances: A list of [distancepoints](#distancepoints) of the road borders.
 - obstacleDistances: An extra list of distancepoints from certain objects.
 - steeringAngle: The current steering angle of the car.
 
 This algorithm works via the following principle:
 
 It calculates the four closests points of the lidarDistances tuple consisting of:
 - Left point
 - Next left point
 - Right point
 - Next right point
 
 
 Then calculates the closest object if any.
 
 From these distances and the angle which accomodates these distances we can calculate the coordinates.
 This is done via the Pythagoras Theorem.
 
 Then we check if the obstacle is within our driving area.
 If there are no obstacles near we calculate the coordinates of the middle of the road (X).
   ```
    NL --- NR                  NL --- NR 
    ---------                  ---------
    ---------      ----->      ----X----
    ---------                  ---------
    L-------R                  L-------R
        ^                          ^
        |                          |
 driving direction
  ```

 But if there is an obstacle, this is used to calculate a safe steering angle.
 Let say we have an obstacle on the left side of the middle of the road.
 Then we use L + O + NR + R to calculate the middle (X)
  ```
 NL --- NR                  NL --- NR 
 ---------                  ---------
 -O-------      ----->      -O-------
 ---------                  -----X---
 L-------R                  L-------R
      ^                          ^
      |                          |
 driving direction
  ```
 With the middle coordinates we again use the Pythagoras Theorem the calculate the desired steering angle
 With the current steering angle and the desired steering angle we use the PID to calculate the next steering angle which is our output.
 
# distancepoints
The so called 'distancepoints' are points detected by an Li-Dar.
These points consist of a distance(between the Li-Dar and the object) and the angle.

If your Li-Dar does not output these variables, you can still use this algorithm. 
Instead of using the current for loop and calculate the coordinates you can also calculate the four closest coordinates and use these as input.
Change line 55 -> 74 with code that does the following: 

```     
       for lidarCoordinate in range (0, len(lidarCoordinates)):
        distance = math.sqrt(mat.pow(abs(lidarCoordinate.x), 2) + mat.pow(abs(lidarCoordinate.y), 2))
            if(lidarCoordinate.x < 0):
               if(distance < self.rightRoadBorder):
                  self.rightRoadBorder = distance
                  self.coordinatesR = lidarCoordinate
               elif (distance < self.nextRightRoadBorder):
                  self.nextRightRoadBorder = distance
                  self.coordinatesNR = lidarCoordinate
            else:
              if(distance < self.leftRoadBorder):
                  self.leftRoadBorder = distance
                  self.coordinatesL = lidarCoordinate
               elif (distance < self.nextLeftRoadBorder):
                  self.nextLeftRoadBorder = distance
                  self.coordinatesNL = lidarCoordinate
                  
```
