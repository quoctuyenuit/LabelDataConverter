class Point:
    def __init__(self, point, maxSize):
        self.x = point[0]
        self.y = point[1]
        self.__filter(maxSize)

    def __filter(self, maxSize):
        self.x = 0 if self.x < 0 else self.x
        self.y = 0 if self.y < 0 else self.y
        self.x = maxSize[0] if self.x > maxSize[0] else self.x
        self.y = maxSize[1] if self.y > maxSize[1] else self.y

    def __gt__(self, other):
        return (self.x > other.x) or (self.x == other.x and self.y < other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
            
    def __lt__(self, other):
        return (self.x < other.x) or (self.x == other.x and self.y > other.y)

    #============================================================================
    #Public function
    #============================================================================
    def to_string(self):
        return str(int(round(self.x))) + "," + str(int(round(self.y)))

    def to_array(self):
        return [self.x, self.y]