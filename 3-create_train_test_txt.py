# 3-create_train_test_txt.py
# encoding:utf-8

# Convert cityscape dataset to pascal voc format dataset

# 3. make train.txt/val.txt/city2pascal.txt for training and evaluation

import pdb  
import glob  
import os  
import random  
import math  
  
def get_sample_value(txt_name, category_name):  
    # label_path = '/home/lujialin/data/KITTI/training/label_2car/'
    label_path = '/home/ubuntu/codes/city2pascal/source/trainvaltxt/'  #txtfile folder
    txt_path = label_path + txt_name+'.txt'
    try:  
        with open(txt_path) as r_tdf:  
            if category_name in r_tdf.read():  
                return ' 1'  
            else:  
                return '-1'  
    except IOError as ioerr:  
        print('File error:'+str(ioerr))  


# txt_list_path = glob.glob('/home/lujialin/data/KITTI/training/label_2car/*.txt')
txt_list_path = glob.glob('/home/ubuntu/codes/city2pascal/source/trainvaltxt/*.txt')
txt_list = []
  
for item in txt_list_path:  
    temp1,temp2 = os.path.splitext(os.path.basename(item))  
    txt_list.append(temp1)  
txt_list.sort()  
print("txt_list, end = '\n\n'")
  
# 有博客建议train:val:city2pascal=8:1:1，先尝试用一下
num_trainval = random.sample(txt_list,int(math.floor(len(txt_list)))) # 可修改百分比  
num_trainval.sort()  
print("num_trainval, end = '\n\n'")
  
num_train = random.sample(num_trainval,int(math.floor(len(num_trainval)*8/9.0))) # 可修改百分比  
num_train.sort()  
print("num_train, end = '\n\n'")
  
num_val = list(set(txt_list).difference(set(num_train)))  
num_val.sort()  
print("num_val, end = '\n\n'")
  
#num_test = list(set(txt_list).difference(set(num_trainval)))  
#num_test.sort()  
#print "num_test, end = '\n\n'"
  
# pdb.set_trace()
  
Main_path = '/home/ubuntu/codes/city2pascal/source/Main/'
train_test_name = ['trainval','train','val']  
category_name = ['pedestrian']#修改类别
  
# 循环写trainvl train val city2pascal
for item_train_test_name in train_test_name:  
    list_name = 'num_'  
    list_name += item_train_test_name  
    train_test_txt_name = Main_path + item_train_test_name + '.txt'   
    try:  
        # 写单个文件  
        with open(train_test_txt_name, 'w') as w_tdf:  
            # 一行一行写  
            for item in eval(list_name):  
                w_tdf.write(item+'\n')  
        # 循环写Car Pedestrian Cyclist  
        for item_category_name in category_name:  
            category_txt_name = Main_path + item_category_name + '_' + item_train_test_name + '.txt'  
            with open(category_txt_name, 'w') as w_tdf:  
                # 一行一行写  
                for item in eval(list_name):  
                    w_tdf.write(item+' '+ get_sample_value(item, item_category_name)+'\n')  
    except IOError as ioerr:  
        print('File error:'+str(ioerr))  
