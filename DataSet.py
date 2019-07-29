import json
import os
import operator
import base64
import sys
import numpy as np
from WordData import WordData
from FunctionMode import FunctionMode
from PIL import Image

class DataSet:
    def __init__(self, path, image_path, output_path, mode):
        self.data_path = path
        self.output_path = output_path
        self.image_path = image_path
        try:
            img = Image.open(self.image_path)
            self.max_size = img.size
        except:
            self.max_size = (sys.maxsize, sys.maxsize)

        self.is_valid = True
        self.mode = mode
        self.__retrieve_data(mode)
    
    def __retrieve_data(self, mode):
        if mode == FunctionMode.CONVERTER:
           self.__retrieve_json_data()
        else:
            self.__retrieve_txt_data()

    def __retrieve_txt_data(self):
        self.word_datas = []
        with open(self.data_path, "r") as txt_file:
            line = txt_file.readline()
            line_number = 1
            while line:
                line_data = self.__parse_line(line, line_number)
                if line_data[0]:
                    self.word_datas.append(line_data[1])
                else:
                    self.is_valid = False
                    return

                line = txt_file.readline()
                line_number += 1
    
    def __parse_line(self, line, line_number):
        line_data = line.split(",")
        if len(line_data) == 10:
            label = line_data[-2]
            line_data = line_data[:-2]
        else:
            label = line_data[-1][:-1]
            line_data = line_data[:-1]
        
        if len(line_data) != 8:
            print("[Error] Wrong data at line: ", line_number, "\nLine data: ", line, "at path:", self.data_path)
            return (False, None)
            
        points_data = []
        for num_str in line_data:
            try:
                points_data.append(int(num_str))
            except:
                print("[Error] cannot convert to number: ", num_str, " at line:", line, "\nLine number: ", line_number, "\nfile: ", self.data_path)
                return (False, None)
        
        arr_points = np.array(points_data)
        return (True, WordData(label, arr_points.reshape(-1, 2), self.data_path, self.max_size))


    def __retrieve_json_data(self):
        with open(self.data_path) as json_file:
            data = json.load(json_file)
            self.word_datas = []
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
                    word_data = WordData(label, [p1, p2, p3, p4], self.data_path, self.max_size)
                    self.word_datas.append(word_data)
                else:
                    word_data = WordData(label, raw_points, self.data_path, self.max_size)
                    self.word_datas.append(word_data)


    def export_file(self):
        if self.mode == FunctionMode.REVERSE:
            self.__export_json_file()
        else:
            self.__export_txt_file()
    
    def __export_txt_file(self):
        path = self.output_path + self.data_path.split("/")[-1].split(".")[0] + ".txt"
        txtFiles = open(path, "w")
        for data in self.word_datas:
            txtFiles.write("%s\n" %data.to_string())
        
        txtFiles.close()
    
    #Export jsonfile to open in LabelMe
    def __export_json_file(self):
        data = {}
        data['version'] = "3.16.2"
        data['flags'] = {}
        data['shapes'] = []
        for shape in self.word_datas:
            data['shapes'].append(shape.to_json_object())
        data['lineColor'] = [0, 255, 0, 128]
        data['fillColor'] = [255, 0, 0, 128]
        data['imagePath'] = self.image_path.split('/')[-1]
        
        with open(self.image_path, "rb") as image_file:
            imageData = base64.b64encode(image_file.read()).decode('utf-8')
            data['imageData'] = str(imageData)

        img = Image.open(self.image_path)
        data['imageHeight'] = img.size[1]
        data['imageWidth'] = img.size[0]

        path = self.output_path + self.data_path.split("/")[-1].split(".")[0] + ".json"
        with open(path, 'w') as outfile:
            json.dump(data, outfile, ensure_ascii=False, indent=2)

        




# # ==========================================================================    
# # Debug mode
# # ==========================================================================    
# path = '/home/tuyenqn/Documents/data/phandong_68.json'
# imagePath = '/home/tuyenqn/Documents/data/phandong_68.jpg'
# data = DataSet(path, imagePath, '/home/tuyenqn/Documents/waste')
# data.export_file()
# print(len(data.word_datas))

