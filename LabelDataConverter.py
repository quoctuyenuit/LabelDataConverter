import glob
import argparse
import shutil
import os
from PIL import Image
import sys
from DataSet import DataSet
from FunctionMode import FunctionMode

class Converter:
    imageExtensions = ['.tif', '.jpg', '.png', '.jpeg']
    def __init__(self, path, outputDirectoryPath, mode):
        #Tiền xử lý path để hàm glob có thể tìm file đệ quy.
        if path[-1] != '/':
            path += '/'

        if outputDirectoryPath[-1] != '/':
            outputDirectoryPath += '/'
        
        self.outputPath = outputDirectoryPath
        self.mode = mode

        #Make directory if not exists output path
        if not os.path.exists(self.outputPath):
            os.mkdir(self.outputPath)
        
        data_extension = ".json" if mode == FunctionMode.CONVERTER else ".txt"
        self.__retrieve_raw_data(path, data_extension)

        if mode == FunctionMode.CONVERTER:
            self.__retrieve_images(path)
    
    def __retrieve_raw_data(self, path, data_extension):
        self.data_paths = [f for f in glob.glob(path + "**/*" + data_extension, recursive=True)]
    
    def __retrieve_images(self, path):
        images_path = []
        for extension in self.imageExtensions:
            lower_format = path + "**/*" + extension.lower()
            upper_format = path + "**/*" + extension.upper()
            images_path.extend([f for f in glob.glob(lower_format, recursive=True)])
            images_path.extend([f for f in glob.glob(upper_format, recursive=True)])

        self.image_paths = []
        for image in images_path:
            for data in self.data_paths:
                if self.__compare(data, image):
                    self.image_paths.append(image)

    #=====================================================
    #Kiểm tra file json và image 
    #=====================================================
    def __compare(self, json_path, image_path):
        json_name = json_path.split("/")[-1].split(".")[0]
        image_name = image_path.split("/")[-1].split(".")[0]
        return json_name == image_name

    def __find_image_file(self, json_path):
        name = json_path.split("/")[-1].split(".")[0]
        for img in self.image_paths:
            if name in img:
                return img
        return ''
    
    def convert_label_data(self):
        for json in self.data_paths:
            if self.mode == FunctionMode.CONVERTER:
                image_path = self.__find_image_file(json)
                img = Image.open(image_path)
                max_size = img.size
            else:
                max_size = (sys.maxsize, sys.maxsize)
            data = DataSet(json, max_size, self.outputPath, self.mode)
            data.export_file()

    def copy_images(self):
        for json in self.data_paths:
            for img in self.image_paths:
                if self.__compare(json, img):
                    shutil.copy(img, self.outputPath)

parser = argparse.ArgumentParser("Convert Data")
parser.add_argument('-i', dest='inputpath', help="Nhập đường dẫn folder chứa source", type=str)
parser.add_argument('-o', dest='outputpath', help="Nhập đường dẫn folder muốn để output", type=str)
parser.add_argument('-m', dest='mode', help="Chọn loại chức năng, 1 ==> Convert json file to txt; 2 ==> Filter txt data", type=int)
args = parser.parse_args()
inputPath = args.inputpath
outputPath = args.outputpath

if args.mode == 2:
    mode = FunctionMode.FILTER
else:
    mode = FunctionMode.CONVERTER

#===========================================================
#Debug mode
#===========================================================
# inputPath = '../waste/'
# outputPath = '../test'
# mode = FunctionMode.FILTER
#===========================================================
converter = Converter(inputPath, outputPath, mode)
converter.convert_label_data()
print("Number of files:", len(converter.data_paths))
if mode == FunctionMode.CONVERTER:
    converter.copy_images()
    print("Number of image file:", len(converter.image_paths))
