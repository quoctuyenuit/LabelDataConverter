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
    def __init__(self, path, outputDirectoryPath, wrong_directory, mode):
        #Tiền xử lý path để hàm glob có thể tìm file đệ quy.
        if path[-1] != '/':
            path += '/'

        if outputDirectoryPath[-1] != '/':
            outputDirectoryPath += '/'
        
        self.output_path = outputDirectoryPath
        self.wrong_directory = wrong_directory
        self.mode = mode
        self.wrong_files = []

        #Make directory if not exists output path
        if not os.path.exists(self.output_path):
            os.mkdir(self.output_path)
        if not os.path.exists(self.wrong_directory):
            os.mkdir(self.wrong_directory)
        
        data_extension = ".json" if mode == FunctionMode.CONVERTER else ".txt"
        self.__retrieve_raw_data(path, data_extension)
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
            data = DataSet(json, max_size, self.output_path, self.mode)
            
            if data.is_valid:
                data.export_file()
            else:
                self.wrong_files.append(json)
        
        self.__process_wrong_data()

    def copy_images(self):
        self.__copy_images(self.data_paths, self.output_path)
    
    def __copy_images(self, files, output):
        for file in files:
            for img in self.image_paths:
                if self.__compare(file, img):
                    shutil.copy(img, output)

    def __process_wrong_data(self):
        print("======================================================")
        self.__copy_images(self.wrong_files, self.wrong_directory)
        for file in self.wrong_files:
            img = self.__find_image_file(file)
            os.remove(file)
            os.remove(img)
            self.data_paths.remove(file)
            self.image_paths.remove(self.__find_image_file(file))
            print("[Wrong] ", file)
        print("Number of wrong file: ", len(self.wrong_files))
        print("======================================================")

parser = argparse.ArgumentParser("Convert Data")
parser.add_argument('-i', dest='input_path', help="Nhập đường dẫn folder chứa source", type=str)
parser.add_argument('-o', dest='output_path', help="Nhập đường dẫn folder muốn để output", type=str)
parser.add_argument('-wd', dest='wrong_directory', help="Nhập đường dẫn folder muốn để output", type=str)
parser.add_argument('-m', dest='mode', help="Chọn loại chức năng, 1 ==> Convert json file to txt; 2 ==> Filter txt data", type=int)
args = parser.parse_args()
input_path = args.input_path
output_path = args.output_path
wrong_directory = args.wrong_directory

if args.mode == 2:
    mode = FunctionMode.FILTER
else:
    mode = FunctionMode.CONVERTER

#===========================================================
#Debug mode
#===========================================================
# input_path = '/home/tuyenqn/Downloads/dataset_train_v1_anh_mang'
# output_path = '../DataSetCheck'
# wrong_directory = './wrong_directory'
# mode = FunctionMode.FILTER
#===========================================================
converter = Converter(input_path, output_path, wrong_directory, mode)
converter.convert_label_data()
converter.copy_images()
print("Number of files are done:", len(converter.data_paths))
print("Number of image file done:", len(converter.image_paths))