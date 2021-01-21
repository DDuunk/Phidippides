# Lidar segmentator
This segmentator is used to remove unused cloud points from the lidar pointcloud. 

## Usage
```Shell
from read_json import read_json
import json as json
pointcloud = read_json()
seg = segmentator(11.1111111, 4,-0.9,1.5)
points = seg.segmentate(pointcloud)

file = open("segmentation.txt", "a")
for point in points:    
    file.write(str(point.get('x')) +" "+str(point.get('y'))+" "+str(point.get('z')) + "\n")
file.close()
```
