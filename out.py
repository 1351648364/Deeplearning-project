import cv2
from PIL import Image
import numpy as np


class UnsupportedFormat(Exception):
    def __init__(self, input_type):
        self.t = input_type

    def __str__(self):
        return "不支持'{}'模式的转换，请使用为图片地址(path)、PIL.Image(pil)或OpenCV(cv2)模式".format(self.t)


class MatteMatting():
    def __init__(self, original_graph, mask_graph, input_type='path'):

        if input_type == 'path':
            self.img1 = cv2.imread(original_graph)
            self.img2 = cv2.imread(mask_graph)
        elif input_type == 'pil':
            self.img1 = self.__image_to_opencv(original_graph)
            self.img2 = self.__image_to_opencv(mask_graph)
        elif input_type == 'cv2':
            self.img1 = original_graph
            self.img2 = mask_graph
        else:
            raise UnsupportedFormat(input_type)

    @staticmethod
    def __transparent_back(img):
        """
        :param img: 传入图片地址
        :return: 返回替换白色后的透明图
        """
        img = img.convert('RGBA')
        L, H = img.size
        color_0 = (255, 255, 255, 255)  # 要替换的颜色
        for h in range(H):
            for l in range(L):
                dot = (l, h)
                color_1 = img.getpixel(dot)
                if color_1 == color_0:
                    color_1 = color_1[:-1] + (0,)
                    img.putpixel(dot, color_1)
        return img

    def save_image(self, path, mask_flip=False):

        if mask_flip:
            img2 = cv2.bitwise_not(self.img2)  # 黑白翻转
        image = cv2.add(self.img1, img2)
        image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))  # OpenCV转换成PIL.Image格式
        img = self.__transparent_back(image)
        img.save(path)


    @staticmethod
    def __image_to_opencv(image):
        """
        PIL.Image转换成OpenCV格式
        """
        img = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)
        return img


mm = MatteMatting("image.jpg", "output.jpg")
mm.save_image("thing.png", mask_flip=True)