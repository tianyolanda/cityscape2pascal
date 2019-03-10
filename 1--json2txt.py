# convert cityscape dataset to pascal voc format dataset

# 1. convert every cityscape image label '.json' to '.txt'

import json
import os
from os import listdir, getcwd
from os.path import join
import os.path



rootdir = '/home/ubuntu/codes/city2pascal/source/JPEGImages'  # 写自己存放图片的数据地址

def position(pos):
    # 该函数用来找出xmin,ymin,xmax,ymax即bbox包围框
    x = []
    y = []
    nums = len(pos)
    for i in range(nums):
        x.append(pos[i][0])
        y.append(pos[i][1])
    x_max = max(x)
    x_min = min(x)
    y_max = max(y)
    y_min = min(y)
    # print(x_max,y_max,x_min,y_min)
    b = (float(x_min), float(y_min), float(x_max), float(y_max))
    # print(b)
    return b

# pascal voc 标准格式
# < xmin > 174 < / xmin >
# < ymin > 101 < / ymin >
# < xmax > 349 < / xmax >
# < ymax > 351 < / ymax >

def convert(size, box):
    # 该函数将xmin,ymin,xmax,ymax转为x,y,w,h中心点坐标和宽高
    dw = 1. / (size[0])
    dh = 1. / (size[1])
    x = (box[0] + box[1]) / 2.0 - 1
    y = (box[2] + box[3]) / 2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    print((x, y, w, h))
    return (x, y, w, h)


def convert_annotation(image_id):
    # load_f = open("/home/ubuntu/PycharmProjects/city2pascal/source/train/tubingen/%s_gtFine_polygons.json" % (image_id), 'r')  # 导入json标签的地址
    load_f = open("/home/ubuntu/codes/city2pascal/source/trainvaljson/%s_gtFine_polygons.json" % (image_id), 'r')  # 导入json标签的地址
    load_dict = json.load(load_f)
    out_file = open('/home/ubuntu/codes/city2pascal/source/trainvaltxt/%s_leftImg8bit.txt' % (image_id), 'w')  # 输出标签的地址
    # keys=tuple(load_dict.keys())
    w = load_dict['imgWidth']  # 原图的宽，用于归一化
    h = load_dict['imgHeight']
    # print(h)
    objects = load_dict['objects']
    nums = len(objects)
    # print(nums)
    # object_key=tuple(objects.keys()
    cls_id = ''
    for i in range(0, nums):
        labels = objects[i]['label']
        # print(i)
        if (labels in ['person', 'rider']):
            # print(labels)
            pos = objects[i]['polygon']
            bb = position(pos)
            # bb = convert((w, h), b)
            cls_id = 'pedestrian'  # 我这里把行人和骑自行车的人都设为类别pedestrian
            out_file.write(cls_id + " " + " ".join([str(a) for a in bb]) + '\n')
            # print(type(pos))
        elif (labels in ['car', 'truck', 'bus', 'caravan', 'trailer']):
            # print(labels)
            pos = objects[i]['polygon']
            bb = position(pos)
            # bb = convert((w, h), b)
            cls_id = 'car'  # 我这里把各种类型的车都设为类别car
            out_file.write(cls_id + " " + " ".join([str(a) for a in bb]) + '\n')

    if cls_id == '':
        print('no label json:',"%s_gtFine_polygons.json" % (image_id))


def image_id(rootdir):
    a = []
    for parent, dirnames, filenames in os.walk(rootdir):
        for filename in filenames:
            # print(filename)

            filename = filename[:-16]
            # filename = filename.strip('_leftImg8bit.png')
            a.append(filename)
    return a



if __name__ == '__main__':
    names = image_id(rootdir)
    for image_id in names:
        convert_annotation(image_id)