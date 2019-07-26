import json
import os
import numpy as np
from PIL import Image
import operator

class LabelData:
    __distance_ = 10
    __area = 300
    __default_str = "###"
    def __init__(self, label, points, path, imagePath):
        self.label = label
        self.path = path
        img = Image.open(imagePath)
        self.imageSize = img.size
        
        self.points = []

        for point in points:
            self.points.append(self.__filter_point(point))
        
        self.__order_points()

        if not self.__check_shape():
            self.label = self.__default_str

    def __order_points(self):
        points_ordered_x = self.points.copy()
        #Sort tăng dần theo y
        #Sau khi sort ta tách được 2 điểm trên và 2 điểm dưới
        points_ordered_x.sort(key = lambda x: x[0])
        ad = points_ordered_x[:-2]
        bc = points_ordered_x[2:]
        #Sort tăng dần theo y
        #Sau khi sort ta tách được điểm trái và điểm phải
        ad.sort(key = lambda x : x[1])
        bc.sort(key = lambda x : x[1])
        a = ad[0]
        d = ad[1]
        b = bc[0]
        c = bc[1]
        self.points = [a, b, c, d]

    def __filter_point(self, point):
        x = point[0]
        y = point[1]
        if x < 0:
            x = 0
        elif x > self.imageSize[0]:
            x = self.imageSize[0]
        
        if y < 0:
            y = 0
        elif y > self.imageSize[1]:
            y = self.imageSize[1]
        
        return (x, y)
    
    def __area_shape(self):
        s_x = 0
        s_y = 0
        for i in range(len(self.points) - 1):
            s_x += self.points[i][0] * self.points[i+1][1]
            s_y += self.points[i][1] * self.points[i+1][0]
        s_x += self.points[-1][0] * self.points[0][1]
        s_y += self.points[-1][1] * self.points[0][0]
        return (s_x - s_y) / 2

    def __distance(self, p1, p2):
        p1_a = np.array(p1)
        p2_a = np.array(p2)

        return np.linalg.norm(p1_a - p2_a)

    def __check_edge(self):
        for p1 in self.points:
            for p2 in self.points:
                if p1 != p2 and self.__distance(p1, p2) <= self.__distance_:
                    print("[Warning] discard shape with label: ", self.label, " path: ", self.path)
                    return True
        return False

    def __check_shape(self):
        return not (self.__area_shape() <= self.__area or self.__check_edge())
    
    def to_string(self):
        result = ""
        for point in self.points:
            result += str(int(round(point[0]))) + "," + str(int(round(point[1]))) + ","

        result += self.label
        return result
#=========================================================================================
#=========================================================================================
#=========================================================================================

class DataSet:
    def __init__(self, path, image_path, output_path):
        self.data_path = path
        self.output_path = output_path
        self.image_path = image_path
        self.__filterData()
    
    def __filterData(self):
        with open(self.data_path) as json_file:
            data = json.load(json_file)
            self.label_datas = []
            for shape in data['shapes']:
                #=============================================
                #get label
                #=============================================
                label = shape['label']
                #=============================================
                #get points
                #=============================================
                raw_points = shape['points']
                if len(raw_points) < 4:
                    p1 = raw_points[0]
                    p3 = raw_points[1]
                    p2 = [p3[0], p1[1]]
                    p4 = [p1[0], p3[1]]
                    points = [p1, p2, p3, p4]
                    self.label_datas.append(LabelData(label, points, self.data_path, self.image_path))
                else:
                    self.label_datas.append(LabelData(label, raw_points, self.data_path, self.image_path))
    def export_file(self):
        path = self.output_path + self.data_path.split("/")[-1][:-5] + ".txt"
        txtFiles = open(path, "w")
        for data in self.label_datas:
            txtFiles.write("%s\n" %data.to_string())
        
        txtFiles.close()

#==========================================================================    
#Debug mode
#==========================================================================    
# path = '/home/tuyenqn/Documents/data/phandong_68.json'
# imagePath = '/home/tuyenqn/Documents/data/phandong_68.jpg'
# data = DataSet(path, imagePath, '/home/tuyenqn/Documents/ConvertLabelData/module/test/')
# data.export_file()
# print(len(data.label_datas))
