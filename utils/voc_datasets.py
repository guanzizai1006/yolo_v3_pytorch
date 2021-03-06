import torch
import torch.utils.data as data
from os.path import join, split
from os import listdir
import numpy as np 
import os
import torchvision
import torchvision.transforms as transforms
import xml.etree.ElementTree as ET 
from PIL import Image

classes = ["aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow", "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]
class_to_ind = dict(list(zip(classes, list(range(len(classes))))))

def readxml(infile):

	tree = ET.parse(infile)

	objs = tree.findall('object')

	boxes = []
	gt_classes = []

	for idx, obj in enumerate(objs):
		diffi = obj.find('difficult').text

		cls = obj.find('name').text
		if cls not in classes or int(diffi) == 1:
			continue

		cls_id = class_to_ind[cls]

		bbox = obj.find('bndbox')
		x1 = float(bbox.find('xmin').text) - 1
		y1 = float(bbox.find('ymin').text) - 1
		x2 = float(bbox.find('xmax').text) - 1
		y2 = float(bbox.find('ymax').text) - 1

		boxes.append([x1, y1, x2, y2])
		gt_classes.append([cls_id])

	boxes_np = np.array(boxes)
	gt_classes_np = np.array(gt_classes)

	return boxes_np, gt_classes_np


class VOC2007(data.Dataset):
    def __init__(self,dataPath='/media/data2/wb/VOCdevkit/VOC2007', \
    					transform=None, size = 416):
        super(VOC2007, self).__init__()
        # list all images into a list
        self.imgsize = size
        image_set_file = os.path.join(dataPath, 'ImageSets',\
        						 'Main', 'trainval.txt')
        assert os.path.exists(image_set_file),\
        		 'Path does not exist: {}'.format(image_set_file)

        with open(image_set_file) as f:
            self.image_index = [x.strip() for x in f.readlines()]

        self.dataPath = dataPath
        self.transform = transform

    def __getitem__(self, index):

        img_path = os.path.join(self.dataPath,'JPEGImages', \
        			self.image_index[index] + '.jpg')
        xml_path = os.path.join(self.dataPath,'Annotations', \
        			self.image_index[index] + '.xml')

        origin_img = Image.open(img_path).convert('RGB') 
        boxes, classes = readxml(xml_path)

        ## resize the img and boxes
        w, h = origin_img.size
        boxes = np.asarray(boxes, dtype=np.float)

        img = origin_img.resize((self.imgsize, self.imgsize), Image.ANTIALIAS)
        if len(boxes) > 0:
        	boxes[:, 1::2] *= float(self.imgsize) / float(h)
        	boxes[:, 0::2] *= float(self.imgsize) / float(w)
        gt_classes = np.zeros((len(classes), 20))
        for i in range(len(classes)):
        	gt_classes[i, classes[i, 0]] = 1.0

        if self.transform is not None:
            img = self.transform(img)

        gt_boxes = torch.from_numpy(boxes).float()
        gt_classes = torch.from_numpy(gt_classes).float()

        return img, gt_boxes, gt_classes

    def __len__(self):
        # You should change 0 to the total size of your dataset.
        return len(self.image_index)

class VOC2007_TEST(data.Dataset):
    def __init__(self,dataPath='/media/data2/wb/VOCdevkit/VOC2007', \
                        transform=None, size = 416):
        super(VOC2007_TEST, self).__init__()
        # list all images into a list
        self.imgsize = size
        image_set_file = os.path.join(dataPath, 'ImageSets',\
                                 'Main', 'test.txt')
        assert os.path.exists(image_set_file),\
                 'Path does not exist: {}'.format(image_set_file)

        with open(image_set_file) as f:
            self.image_index = [x.strip() for x in f.readlines()]

        self.dataPath = dataPath
        self.transform = transform

    def __getitem__(self, index):

        img_path = os.path.join(self.dataPath,'JPEGImages', \
                    self.image_index[index] + '.jpg')
        xml_path = os.path.join(self.dataPath,'Annotations', \
                    self.image_index[index] + '.xml')

        origin_img = Image.open(img_path).convert('RGB') 
        boxes, classes = readxml(xml_path)

        name = self.image_index[index]

        ## resize the img and boxes
        w, h = origin_img.size
        boxes = np.asarray(boxes, dtype=np.float)

        img = origin_img.resize((self.imgsize, self.imgsize), Image.ANTIALIAS)
        if len(boxes) > 0:
            boxes[:, 1::2] *= float(self.imgsize) / float(h)
            boxes[:, 0::2] *= float(self.imgsize) / float(w)
        gt_classes = np.zeros((len(classes), 20))
        for i in range(len(classes)):
            gt_classes[i, classes[i, 0]] = 1.0

        if self.transform is not None:
            img = self.transform(img)

        gt_boxes = torch.from_numpy(boxes).float()
        gt_classes = torch.from_numpy(gt_classes).float()

        return img, gt_boxes, gt_classes, name

    def __len__(self):
        # You should change 0 to the total size of your dataset.
        return len(self.image_index)

class VOC2007_Eval(data.Dataset):
    def __init__(self,dataPath='/media/data2/wb/VOCdevkit/VOC2007', \
                        transform=None, size = 416):
        super(VOC2007_Eval, self).__init__()
        # list all images into a list
        self.imgsize = size
        image_set_file = os.path.join(dataPath, 'ImageSets',\
                                 'Main', 'train.txt')
        assert os.path.exists(image_set_file),\
                 'Path does not exist: {}'.format(image_set_file)

        with open(image_set_file) as f:
            self.image_index = [x.strip() for x in f.readlines()]

        self.dataPath = dataPath
        self.transform = transform

    def __getitem__(self, index):

        img_path = os.path.join(self.dataPath,'JPEGImages', \
                    self.image_index[index] + '.jpg')
        xml_path = os.path.join(self.dataPath,'Annotations', \
                    self.image_index[index] + '.xml')

        origin_img = Image.open(img_path).convert('RGB') 
        boxes, classes = readxml(xml_path)

        ## resize the img and boxes
        w, h = origin_img.size
        boxes = np.asarray(boxes, dtype=np.float)

        img = origin_img.resize((self.imgsize, self.imgsize), Image.ANTIALIAS)
        gt_classes = classes

        if self.transform is not None:
            img = self.transform(img)

        gt_boxes = torch.from_numpy(boxes).float()
        gt_classes = torch.from_numpy(gt_classes).float()

        return img, gt_boxes, gt_classes, [h, w]

    def __len__(self):
        # You should change 0 to the total size of your dataset.
        return len(self.image_index)
