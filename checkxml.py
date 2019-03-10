import os
import xml.dom.minidom
from xml.dom.minidom import Document
import shutil

def custombasename(fullname):
    return os.path.basename(os.path.splitext(fullname)[0])


def GetFileFromThisRootDir(dir, ext=None):
    allfiles = []
    needExtFilter = (ext != None)
    for root, dirs, files in os.walk(dir):  # files是文件夹下所有文件的名称
        for filespath in files:  # 依次取文件名
            filepath = os.path.join(root, filespath)  # 构成绝对路径
            extension = os.path.splitext(filepath)[1][
                        1:]  # os.path.splitext(path)  #分割路径，返回路径名和文件后缀 其中[1]为后缀.png，再取[1:]得到png
            if needExtFilter and extension in ext:
                allfiles.append(filepath)
            elif not needExtFilter:
                allfiles.append(filepath)
    return allfiles  # 返回dir中所有文件的绝对路径


def move_file(xmlpath):
    rootdir = '/home/ubuntu/Desktop/JPEGImages/'
    img_dir = os.path.join(rootdir)
    move_image_dir = os.path.join(rootdir, 'blank/', 'images/')
    move_xml_dir = os.path.join(rootdir, 'blank/', 'xml/')
    if not os.path.isdir(move_image_dir):
        os.makedirs(move_image_dir)
    if not os.path.isdir(move_xml_dir):
        os.makedirs(move_xml_dir)
    name = custombasename(xmlpath)
    print('name',name)
    oldxmlpath = xmlpath
    newxmloath = os.path.join(move_xml_dir + name +'.xml')

    oldimgpath = os.path.join(img_dir + name + '.jpg')
    newimgpath = os.path.join(move_image_dir + name + '.jpg')

    shutil.move(oldimgpath, newimgpath)
    shutil.move(oldxmlpath, newxmloath)


def readXml(xmlfile):
    DomTree = xml.dom.minidom.parse(xmlfile)
    annotation = DomTree.documentElement
    sizelist = annotation.getElementsByTagName('size')  # [<DOM Element: filename at 0x381f788>]
    heights = sizelist[0].getElementsByTagName('height')
    img_height = int(heights[0].childNodes[0].data)
    widths = sizelist[0].getElementsByTagName('width')
    img_width = int(widths[0].childNodes[0].data)
    depths = sizelist[0].getElementsByTagName('depth')
    depth = int(depths[0].childNodes[0].data)
    # if widths != heights:
        # print('width ~= height %s' % xmlfile)
    objectlist = annotation.getElementsByTagName('object')
    bboxes = []
    objnum = len(objectlist)
    # print('objnum',objnum)
    for objects in objectlist:
        namelist = objects.getElementsByTagName('name')
        class_label = namelist[0].childNodes[0].data
        bndbox = objects.getElementsByTagName('bndbox')[0]
        x1_list = bndbox.getElementsByTagName('xmin')
        x1 = float(x1_list[0].childNodes[0].data)
        y1_list = bndbox.getElementsByTagName('ymin')
        y1 = float(y1_list[0].childNodes[0].data)
        x2_list = bndbox.getElementsByTagName('xmax')
        x2 = float(x2_list[0].childNodes[0].data)
        y2_list = bndbox.getElementsByTagName('ymax')
        y2 = float(y2_list[0].childNodes[0].data)
        # 这里我box的格式【xmin，ymin，xmax，ymax，classname】
        bbox = [x1, y1, x2, y2, class_label]
        bboxes.append(bbox)
        minvalue = min(x1, y1, x2, y2)  # 最小值
        max_x_value = max(x1, x2)  # x的最大值
        max_y_value = max(y1, y2)  # y的最大值
        # if x1 > x2:
        #     print('Xmin>Xmax %s' % xmlfile)
        # if y1 > y2:
        #     print('Ymin>Ymax %s' % xmlfile)
        #
        # if minvalue <= 0:
        #     print('最小值有异常%s' % xmlfile)
        # if max_x_value > img_width:
        #     print('x最大值有异常%s' % xmlfile)
        # if max_y_value > img_height:
        #     print('y最大值有异常%s' % xmlfile)

        width = x2 - x1
        height = y2 - y1
        # if width == 0:
        #     print('width=0，图片路径为%s' % xmlfile)
        # elif height == 0:
        #     print('height=0，图片路径为%s' % xmlfile)
        # else:
        #     scale = float(height) / width
            # if scale > 4:
                # print('scale > 4，图片路径为%s' % xmlfile)
            # elif scale < 0.25:
                # print('scale <0.25，图片路径为%s' % xmlfile)

    # print(len(bboxes))
    if bboxes == []:  # xml中无目标
        # print('%s不存在目标' % xmlfile)
        move_file(xmlfile)
    return objnum

if __name__ == '__main__':
    xmldir = '/home/ubuntu/Desktop/Annotations'
    xmlpath = GetFileFromThisRootDir(xmldir)
    nummax = 0
    name = ''
    for xmldir in xmlpath:
        num = readXml(xmldir)
        if num > 50:
            name = xmldir
            move_file(name)
            print('move',num,name)
