import cv2
import numpy as np


def motion_interchange_pattern(F_tD, F_t, x, y, theta):
    p_t = F_t[y-1:(y-1)+3, x-1:(x-1)+3]

    neighborhood_pattern = [(x-4, y), (x-3, y+3),
                            (x, y+4), (x+3, y+3),
                            (x+4, y), (x+3, y-3),
                            (x, y-4), (x-3, y-3)]

    patches = [F_tD[iy-1:(iy-1)+3, ix-1:(ix-1)+3]
               for ix, iy in neighborhood_pattern]

    descriptor, shift_bit = (0, 1)
    for p_i in patches:
        if sum([np.subtract(p_t[i, j], p_i[i, j])**2
                for i in range(3)
                for j in range(3)]) > theta:
            descriptor |= shift_bit
            shift_bit <<= 1
    return descriptor


def compute(previous_frame, frame, motion_descriptor_size=2,
            appearance_descriptor_size=8, theta=288):

    difference_image = cv2.absdiff(previous_frame, frame)

    keypoints = cv2.BRISK_create().detect(difference_image)
    keypoints, motion_descriptors = (cv2.xfeatures2d.FREAK_create()
                                     .compute(difference_image, keypoints))

    appearance_keypoints = []
    appearance_descriptors = []

    for keypoint in keypoints:
        rt = np.ceil(keypoint.size)
        rx, ry = np.array(keypoint.pt) - int(keypoint.size/2)

        F_t = cv2.resize(frame[ry:ry+rt, rx:rx+rt], (19, 19))
        F_tD = cv2.resize(previous_frame[ry:ry+rt, rx:rx+rt], (19, 19))

        center_MIP = motion_interchange_pattern(F_tD, F_t, 9, 9, theta)
        if bin(center_MIP).count('1') > 0:

            descriptor = [motion_interchange_pattern(F_tD, F_t, x, y, theta)
                          for x, y in [(5, 5), (5, 9), (5, 13), (9, 5),
                                       (9, 13), (13, 5), (13, 9), (13, 13)]]
            appearance_descriptors.append(descriptor)
            appearance_keypoints.append((rx, ry, rt))

    return (motion_descriptors[:motion_descriptor_size],
            appearance_descriptors[:appearance_descriptor_size],
            appearance_keypoints)
