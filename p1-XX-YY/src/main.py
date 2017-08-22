import cv2
import copy as cp
import numpy as np
import utils as ut

import masks as mask
import convolution as cv

# Python uses the BGR color scheme
input = cv2.imread('../input/p1-1-2.jpg')

<<<<<<< HEAD
<<<<<<< HEAD
# Gaussian Mask 3X3
g_mask_3 = np.matrix([
    [1, 2, 1],
    [2, 4, 2],
    [1, 2, 1]
    ])

# Gaussian Mask 7X7
g_mask_7 = np.matrix([
    [1, 1, 2, 2, 2, 1, 1],
    [1, 3, 4, 5, 4, 3, 1],
    [2, 4, 7, 8, 7, 4, 2],
    [2, 5, 8, 10, 8, 5, 2],
    [2, 4, 7, 8, 7, 4, 2],
    [1, 3, 4, 5, 4, 3, 1],
    [1, 1, 2, 2, 2, 1, 1]
    ])

# Gaussian Mask 15X15
g_mask_15 = np.matrix([
    [2, 2, 3, 4, 5, 5, 6, 6, 6, 5, 5, 4, 3, 2, 2],
    [2, 3, 4, 5, 7, 7, 8, 8, 8, 7, 7, 5, 4, 3, 2],
    [3, 4, 6, 7, 9, 10, 10, 11, 10, 10, 9, 7, 6, 4, 3],
    [4, 5, 7, 9, 10, 12, 13, 13, 13, 12, 10, 9, 7, 5, 4],
    [5, 7, 9, 11, 13, 14, 15, 16, 15, 14, 13, 11, 9, 7, 5],
    [5, 7, 10, 12, 14, 16, 17, 18, 17, 16, 14, 12, 10, 7, 5],
    [6, 8, 10, 13, 15, 17, 19, 19, 19, 17, 15, 13, 10, 8, 6],
    [6, 8, 11, 13, 16, 18, 19, 20, 19, 18, 16, 13, 11, 8, 6],
    [6, 8, 10, 13, 15, 17, 19, 19, 19, 17, 15, 13, 10, 8, 6],
    [5, 7, 10, 12, 14, 16, 17, 18, 17, 16, 14, 12, 10, 7, 5],
    [5, 7, 9, 11, 13, 14, 15, 16, 15, 14, 13, 11, 9, 7, 5],
    [4, 5, 7, 9, 10, 12, 13, 13, 13, 12, 10, 9, 7, 5, 4],
    [3, 4, 6, 7, 9, 10, 10, 11, 10, 10, 9, 7, 6, 4, 3],
    [2, 3, 4, 5, 7, 7, 8, 8, 8, 7, 7, 5, 4, 3, 2],
    [2, 2, 3, 4, 5, 5, 6, 6, 6, 5, 5, 4, 3, 2, 2]
    ])

# Gaussian pyramid

def pyrDown(img, lvls):
    for i in range(0, lvls):
        i_height, i_width, i_channels = img.shape
        height = math.floor(i_height / 2)
        width = math.floor(i_width / 2)
        newImg = np.zeros((height, width, 3), np.uint8)

        for j in range(0, height):
            for l in range(0, width):
                newImg.itemset((j, l, 0), img.item(j * 2, l * 2, 0))
                newImg.itemset((j, l, 1), img.item(j * 2, l * 2, 1))
                newImg.itemset((j, l, 2), img.item(j * 2, l * 2, 2))

        cv2.imwrite('../output/p1-2-2-{}.jpg'.format(i), newImg)
        img = newImg

def pyrUp(img, lvls):
    print("Pyramid UP not implemented yet")

def pyrAccLvl(pyrImg, lvl):
    print("Access to individual lvls not implemented yet")

# Convolute a linear filter to an image
def filter2d(img, kernel, anchor):
    # Image dimensions
    i_height, i_width, i_channels = img.shape
    print(i_height, " Image Size")

    # Kernel dimensions
    k_height, k_width = kernel.shape

    # Anchor distance to border
    anchor_distance = math.floor(k_height / 2)

    newImg = np.zeros((i_height, i_width, 3), np.uint8)

    # Apply the filter in every pixel
    for i in range(0, i_height):
        for j in range(0, i_width):
            
            # Kernel factor
            k_weight = 0
            sum = 0
            channel_0 = 0
            channel_1 = 0
            channel_2 = 0

            # print("Velho ", i, "-", j, ": ", newImg.item((i, j, 0)))

            # Operate with kernel
            for g in range(0, k_height):
                for h in range (0, k_width):
                    k_weight = 0

                    if i - abs(g - anchor_distance) >= 0 and j - abs(h - anchor_distance) >= 0:
                        # print("[", i,"-", j,"] With [", g,"-", h,"]")
                        k_weight = kernel.item((g, h))
                    if i + (g - anchor_distance) < i_height and j + (h - anchor_distance) < i_width:
                        k_weight = kernel.item((g, h))

                    channel_0 += k_weight * img.item((i, j, 0))
                    channel_1 += k_weight * img.item((i, j, 1))
                    channel_2 += k_weight * img.item((i, j, 2))
                    sum += k_weight

            print("Channel_0 Value ", channel_0, sum)
            newImg.itemset((i, j, 0), channel_0 / sum)
            newImg.itemset((i, j, 1), channel_1 / sum)
            newImg.itemset((i, j, 2), channel_2 / sum)

            print("Sum: ", sum)

            # print("Novo ", i, "-", j, ": ", newImg.item((i, j, 0)))

    cv2.imwrite('../output/TESTE.jpg', newImg)
    print(kernel)
    # print("Begin\n", newImg, "\nEnd")

def gaussianSomething():
    # Usar a função filter2D para gerar o kernel, http://docs.opencv.org/2.4/doc/tutorials/imgproc/imgtrans/filter_2d/filter_2d.html
    gaussian = cv2.getGaussianKernel(9, 1.7)
    cv2.imwrite('../output/gaussian.jpg', gaussian)
=======
||||||| merged common ancestors
=======
time = ut.time()
>>>>>>> 7921378064647595ea7b18009c0d23ca7f566658
output = cv.convolve(cp.copy(input), mask.g_3)
<<<<<<< HEAD
>>>>>>> ee4d5feeed70e0d7718031c53b3cd2263a45df19
||||||| merged common ancestors
=======
print("Convolution time:" + time.elapsed())
>>>>>>> 7921378064647595ea7b18009c0d23ca7f566658

cv2.imwrite('../output/p1-1-0.png', output)


time = ut.time()
cv2.filter2D(cp.copy(input), -1, np.flip(np.flip(mask.g_3, 0), 1), output)
print("OpenCV Convolution time:" + time.elapsed())

cv2.imwrite('../output/p1-1-1.png', output)
