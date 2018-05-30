import numpy as np
import cv2
import time

######## README ########
# TODO: scaling is wrong AF. I just did it that way we see something in plot
# TODO: we need to edit the absolute distance function in visual_odometry.py
# TODO: "initial driving orientation" in plot should be downwards. If we stay still,
# data is bullshit (starts to drive in any direction) -> we should start using VO
# as soon as we drive, not before
# TODO: I think this only works if openCV v3+ and not Duckiebots version v2.5
# Maybe we should try to use older functions, or upgrade, I am not sure..
########################
from visual_odometry import PinholeCamera, VisualOdometry

# Sleep time for debugging
sleeptime = 0.3

# Cam: width, height, focal length x, focal length y, cam center x, cam center y
cam = PinholeCamera(640.0, 480.0, 1192, 1192, 320.0, 240.0)

# VO: cam, speed
vo = VisualOdometry(cam, 0.1)

# Some trajectory or so
traj = np.zeros((600,600,3), dtype=np.uint8)

# Loop through every image (gray scale) in our DB
for img_id in range(1,105):
	# Load image
	img = cv2.imread('DB_duckiebot/test_g_'+str(img_id).zfill(6)+'.png', 0)

	# Update odometry
	vo.update(img, img_id)
	# Obtain positions
	cur_t = vo.cur_t
	if(img_id > 2):
		x, y, z = cur_t[0], cur_t[1], cur_t[2]
	else:
		x, y, z = 0., 0., 0.

	# Obtain drawing pixels
	draw_x, draw_y = -int(x)*4+290, int(z)*4+290
	# Draw
	cv2.circle(traj, (draw_x,draw_y), 1, (img_id*255/4540,255-img_id*255/4540,0), 1)
	cv2.rectangle(traj, (10, 20), (600, 60), (0,0,0), -1)
	text = "Coordinates: x=%2fm y=%2fm z=%2fm"%(x,y,z)
	cv2.putText(traj, text, (20,40), cv2.FONT_HERSHEY_PLAIN, 1, (255,255,255), 1, 8)

	cv2.imshow('Road facing camera', img)
	cv2.imshow('Trajectory', traj)
	cv2.waitKey(1)
	time.sleep(sleeptime)

cv2.imwrite('map.png', traj)
