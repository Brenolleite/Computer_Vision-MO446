import numpy as np
import cv2
import keypoint

def KLT(video_path, type):
    # Get video length
    video = cv2.VideoCapture(video_path)
    length = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    # Parameters for lucas kanade optical flow
    lk_params = dict(winSize  = (15,15),
                     maxLevel = 2,
                     criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

    # Get frames
    ret, frame1 = video.read()

    # Transform frame to grayscale
    frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)

    # Get keypoints
    kps = []
    if type == "sift":
        kp = np.float32(keypoint.sift(frame1))
    else:
        kp = np.float32(keypoint.harris(frame1))

    kps.append(kp)

    for i in range(1, length - 1):
        # Get frames
        ret, frame2 = video.read()

        # Transform frame to grayscale
        frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

        # Calculate optical flow
        kp, st, err = cv2.calcOpticalFlowPyrLK(frame1, frame2, kps[i-1], None, **lk_params)

        # Add new points to matrix of frames
        kps.append(kp.squeeze())

        # Search index of bad kp
        st = np.array(st)
        index = np.where(st==0)

        # Delete bad keypoints
        np.delete(kps, index, axis=1)

        # update frame
        frame1 = frame2

        i += 1

    video.release()

    return np.array(kps)