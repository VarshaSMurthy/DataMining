from itertools import product
from PIL import Image
import cv2
import os
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import normalize
from sklearn.decomposition import PCA
import cv2

source_path = "./testData"


def brain_extraction(image, cluster_path, slice_path):
    mt = match_template(source_path + '/' + image)
    img = Image.open(source_path + '/' + image)
    w, h = img.size
    grid = product(range(mt[2], h - h % mt[0], mt[0]), range(mt[3], w - w % mt[1], mt[1]))
    #  create folders to slices and clusters
    create_dir(cluster_path, slice_path)
    # Slice the images in IC
    count = 0
    split_text = os.path.splitext(image)
    for i, j in grid:
        box = (j + 5.5, i, j + mt[1], i + mt[0])
        sliced = slice_path + '/' + f'{split_text[0]}_{count}_{split_text[1]}'
        img.crop(box).save(sliced)
        count = count + 1


def create_dir(cluster_path, slice_path):
    if not os.path.exists(slice_path):
        os.mkdir(slice_path)
    if not os.path.exists(cluster_path):
        os.mkdir(cluster_path)


def filterImage():
    os.chdir("./Slices/")
    # loop through the images in slice folder
    for files in os.listdir():
        print(files)
        os.chdir(files)
        for file in os.listdir():
            print(file)
            # convert to grey scale
            img = cv2.imread(file, 0)
            # print(img.shape)
            count = cv2.countNonZero(img)
            if count < 14:
                os.remove(file)
        os.chdir('..')
        print("Filetered images in " + files)
    os.chdir('..')


def match_template(image_path):
    template = cv2.imread('template.png', 0)
    img_rgb = cv2.imread(image_path)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    pix = np.where(res >= threshold)

    xcord = set()
    for i in pix[0]:
        xcord.add(i)
    ycord = set()
    for i in pix[1]:
        ycord.add(i)
    #  sort the x and y coordinates
    xcord = sorted(xcord)
    ycord = sorted(ycord)

    return [xcord[1] - xcord[0], ycord[1] - ycord[0], xcord[0], ycord[0]]


def clusters(path):
    print(os.getcwd())
    os.chdir(path)
    os.chdir('./Slices/')

    for files in os.listdir():
        # Check folder present or not to save the output
        if os.path.isdir(path + "/Clusters/" + files):
            pass
        else:
            os.mkdir(path + "/Clusters/" + files)
        os.chdir(files)

        # print(os.getcwd())
        for file in os.listdir():
            if file.endswith(".png"):
                image = cv2.imread(file)
                # convert to hsv
                hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

                # mask of blue
                mask1 = cv2.inRange(hsv, (90, 150, 50), (120, 255, 255))
                #  mask of red
                mask2 = cv2.inRange(hsv, (0, 50, 50), (36, 255, 255))

                # mask of yellow
                mask3 = cv2.inRange(hsv, (10, 0, 0), (40, 255, 255))

                # final mask and masked
                mask = cv2.bitwise_or(mask1, mask2, mask3)
                target = cv2.bitwise_and(image, image, mask=mask)

                dest = path + "/Clusters/" + files
                outfile = '%s/%s' % (dest, file)
                cv2.imwrite(outfile, target)
        os.chdir('..')
        print("Completed detecting Clusters in " + files)
    os.chdir('..')
    print(os.getcwd())
    countClusters()


def countClusters():
    os.chdir('./Clusters')
    for files in os.listdir():
        os.chdir(files)
        df = pd.DataFrame(columns=['SliceNumber', 'ClusterCount'])
        for file in os.listdir():
            image = cv2.imread(file,0)
            count = cv2.countNonZero(image)
            cluster = 0
            s = file.split("_")[3]
            if count < 14:
                pass
            else:
                img = np.array(image)
                x, y = np.where(img != 0)
                x = list(x)
                y = list(y)
                res = []
                [res.append([x[i], y[i]]) for i in range(len(x))]
                clustering = DBSCAN(eps=2, min_samples=2).fit(res)
                clustering.labels_
                l = set(clustering.labels_)
                labels = list(clustering.labels_)
                label_map = {i: labels.count(i) for i in l}
                for k, v in label_map.items():
                    if k != -1:
                        if v > 135:
                            cluster += 1
                # print(cluster)
            # Update the csv file with the cluster count
            data = [s, cluster]
            df.loc[len(df)]=data
        df.to_csv('Clusters.csv',index=False)
        os.chdir('..')
    os.chdir('..')
