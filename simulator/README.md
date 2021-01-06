# Simulator
A simulator to simulate an autonomous car driving by camera or lidar input.

## Installation
- Python 3.x. 
- Install SimPyLC according to https://github.com/QQuick/SimPyLC
- Install other dependencies: 
```
    pip install PyInquirer
```
- Clone this repository.

## Usage
```Shell
cd simulator\simulations
python startSimulator.py
```
## PID
The vehicle uses a PID to steer smoothly accros the track.
- It is possible to change the parameters realtime within the gui.
- You can also change the default values within utils.pid.py

## Camera pilot
The camera pilot simulates using the steering module by using a mp4 video feed. 
- The input consists of a video feed with already segmented road surface.
- It is recommended to choose for "No.track"

## Lidar pilot
The lidar pilot is used to simulate a lidar which detects obstacles.
Within the tracks are several obstacles placed:
    - '$' water
    - '*' road surface
    - '^' cones
    - '#' car
 You can use the gui to change parameters. 


