from PIL import Image
import numpy as np
from Point import Point

class WordData:
    __distance_ = 10
    __area = 300
    __default_str = "###"

    def __init__(self, label, points, path, max_size):
        self.label = label
        self.path = path
        self.max_size = max_size
        
        self.points = []
        for point in points:
            self.points.append(Point(point, self.max_size))
        
        self.__order_points()

        # if not self.__check_shape():
        #     self.label = self.__default_str

    def __order_points(self):
        points_ordered_x = self.points.copy()
        #Sort tăng dần theo y
        #Sau khi sort ta tách được 2 điểm trên và 2 điểm dưới
        points_ordered_x.sort()
        ad = points_ordered_x[:-2]
        bc = points_ordered_x[2:]
        #Sort tăng dần theo y
        #Sau khi sort ta tách được điểm trái và điểm phải
        ad.sort(key = lambda p: p.y)
        bc.sort(key = lambda p: p.y)
        a = ad[0]
        d = ad[1]
        b = bc[0]
        c = bc[1]
        self.points = [a, b, c, d]

    def __area_shape(self):
        s_x = 0
        s_y = 0
        for i in range(len(self.points) - 1):
            s_x += self.points[i].x * self.points[i+1].y
            s_y += self.points[i].y * self.points[i+1].x
        s_x += self.points[-1].x * self.points[0].y
        s_y += self.points[-1].y * self.points[0].x
        return (s_x - s_y) / 2

    def __distance(self, p1, p2):
        p1_a = np.array(p1.to_array())
        p2_a = np.array(p2.to_array())

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
            result += point.to_string() + ","

        result += self.label
        return result
    
    def to_json_object(self):
        data = {}
        data['label'] = self.label
        data['line_color'] = None
        data['fill_color'] = None
        data['points'] = []

        p1 = self.points[0]
        p2 = self.points[1]
        p3 = self.points[2]
        if p1.x == p2.x:
            data['points'].append([p1.to_array(), p3.to_array()])
            shape_type = "rectangle"
        else:
            for p in self.points:
                data['points'].append(p.to_array())
            shape_type = "polygon"

        data['shape_type'] = shape_type
        data["flags"] = {}

        return data
    
# # ==========================================================================    
# # Debug mode
# # ==========================================================================   
# w = WordData("av", [[0,5], [10, 0], [10,20], [20,5]], '/home/tuyenqn/Documents/data/phandong_68.json', '/home/tuyenqn/Documents/data/phandong_68.jpg')
# print(w.to_string())