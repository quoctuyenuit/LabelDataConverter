import glob
import argparse
import shutil
import os
from module.DataSet import DataSet

class Converter:
    imageExtensions = ['.tif', '.jpg', '.png', '.jpeg']
    def __init__(self, path, outputDirectoryPath):
        #Tiền xử lý path để hàm glob có thể tìm file đệ quy.
        if path[-1] != '/':
            path += '/'

        if outputDirectoryPath[-1] != '/':
            outputDirectoryPath += '/'
        
        self.outputPath = outputDirectoryPath

        if not os.path.exists(self.outputPath):
            os.mkdir(self.outputPath)


        self.jsonData = [f for f in glob.glob(path + "**/*.json", recursive=True)]
        imagesPath = []
        for extension in self.imageExtensions:
            formatPath = path + "**/*" + extension.lower()
            upperFormat = path + "**/*" + extension.upper()
            imagesPath.extend([f for f in glob.glob(formatPath, recursive=True)])
            imagesPath.extend([f for f in glob.glob(upperFormat, recursive=True)])
        
        self.images = []
        for image in imagesPath:
            for json in self.jsonData:
                if self.checkData(json, image):
                    self.images.append(image)

    def convert_label_data(self):
        for json in self.jsonData:
            data = DataSet(json, self.find_image_file(json),self.outputPath)
            data.export_file()
    
    def find_image_file(self, json_path):
        name = json_path.split("/")[-1].split(".")[0]
        for img in self.images:
            if name in img:
                return img
        return ''
    # #=====================================================
    # #Kiểm tra file json và image 
    #=====================================================
    def checkData(self, jsonPath, imagePath):
        jsonName = jsonPath.split("/")[-1].split(".")[0]
        imageName = imagePath.split("/")[-1].split(".")[0]
        return jsonName == imageName

    def copyImages(self):
        for json in self.jsonData:
            for img in self.images:
                if self.checkData(json, img):
                    shutil.copy(img, self.outputPath)

parser = argparse.ArgumentParser("Convert Data")
parser.add_argument('-i', dest='inputpath', help="Nhập đường dẫn folder chứa source", type=str)
parser.add_argument('-o', dest='outputpath', help="Nhập đường dẫn folder muốn để output", type=str)
args = parser.parse_args()
inputPath = args.inputpath
outputPath = args.outputpath

#===========================================================
#Debug mode
#===========================================================
# inputPath = '/home/tuyenqn/Documents/data'
# outputPath = '/home/tuyenqn/Documents/ConvertLabelData/test'
#===========================================================

converter = Converter(inputPath, outputPath)
converter.convert_label_data()
converter.copyImages()
print("Number of json file:", len(converter.jsonData))
print("Number of image file:", len(converter.images))