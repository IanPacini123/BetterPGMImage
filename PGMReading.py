import numpy as np
import math

class ImageManager:

    def __init__(self, name):
        self.image_Name = name


    def readImage(self):
        with open(f"PGMReading\{self.image_Name}.pgm") as read_Image:
            self.magic_Number = read_Image.readline()
            self.image_Width, self.image_Height = list(map(int, read_Image.readline().split(" ")))
            self.maxGray = read_Image.readline()
            self.image_Values = read_Image.read().split(" ")

        self.width_WBorder = self.image_Width + 2
        self.height_WBorder = self.image_Height + 2

        return 0

    def valuesToBorderMatrix(self):
        aux = 0
        self.image_MatrixWBorder = np.zeros( (self.height_WBorder, self.width_WBorder) )

        for i in range(1, self.height_WBorder - 1):
            for j in range(1, self.width_WBorder - 1):
                self.image_MatrixWBorder[i][j] = self.image_Values[aux]
                aux += 1

        return 0
    
    def treatBorder(self):
        image_Matrix = self.image_MatrixWBorder
        for indexes, _ in np.ndenumerate(image_Matrix):
            Y, X = indexes
            if Y == 0:
                image_Matrix[Y][X] = image_Matrix[Y+2][X]
            elif Y == self.height_WBorder - 1:
                image_Matrix[Y][X] = image_Matrix[Y-2][X]
            elif X == 0:
                image_Matrix[Y][X] = image_Matrix[Y][X+2]
            elif X == self.width_WBorder - 1:
                image_Matrix[Y][X] = image_Matrix[Y][X-2]

            image_Matrix[0][0] = image_Matrix[2][2]
            image_Matrix[0][self.width_WBorder - 1] = image_Matrix[2][self.width_WBorder - 3]

        self.image = image_Matrix

        return 0
    
    def makeImageBigger(self):
        self.previous_Image = self.image
        previous_Height, previous_Width = self.previous_Image.shape
        new_Image = np.zeros( (previous_Height * 3, previous_Width * 3) )
        for indices, value in np.ndenumerate(self.previous_Image):
            Y, X = indices
            newY = Y * 3
            newX = X * 3

            new_Image[newY][newX] = new_Image[newY][newX+1] = new_Image[newY][newX+2] = new_Image[newY+1][newX] = new_Image[newY+1][newX+1] = new_Image[newY+1][newX+2] = new_Image[newY+2][newX] = new_Image[newY+2][newX+1] = new_Image[newY+2][newX+2] = value

        self.image = new_Image

    def blurImage(self):
        #this method assumes the image already has a border
        self.previous_Image = self.image
        previous_Height, previous_Width = self.previous_Image.shape
        new_Image = np.zeros( (previous_Height - 2, previous_Width - 2) )
        auxY = auxX = 0
        for i in range(1, previous_Height-1):
            for j in range(1, previous_Width-1):
                new_Image[auxY][auxX] = math.trunc((self.previous_Image[i-1][j-1] + self.previous_Image[i-1][j] + self.previous_Image[i-1][j+1] +
                                         self.previous_Image[i][j-1] + self.previous_Image[i][j] + self.previous_Image[i][j+1] +
                                         self.previous_Image[i+1][j-1] + self.previous_Image[i+1][j] + self.previous_Image[i+1][j+1])/9)
                auxX+= 1
            auxX = 0
            auxY+=1
        self.image = new_Image
        
    def writeImage(self):
        image_height, image_width = self.image.shape
        with open(f"new{self.image_Name}.pgm", "x") as write_Image:
            write_Image.write(f"{self.magic_Number}{image_width} {image_height}\n{self.maxGray}")

            for index, value in np.ndenumerate(self.image.astype(int)):
                write_Image.write(f"{value} ")
                if index[1] == image_width:
                    write_Image.write("\n")



        





catImage = ImageManager("cat")
catImage.readImage()
catImage.valuesToBorderMatrix()
catImage.treatBorder()
print(catImage.image)
catImage.makeImageBigger()
print(catImage.image)
catImage.blurImage()
print(catImage.image)
catImage.writeImage()