
import os
import cv2
import numpy as np

class Request(object):
    """
    All supported type of request are listed below:

    1. Single Scale Retinex(SSR)

        Retinex is a theory raised in 1960s that improves the brightness, contrast and sharpness of an image. Here are some important
        views about it:

        ` The color of an object is determined by the reflection ability to the light, but has no relationship with the light 
          intensity.

        ` Picture S, which is the color that observer get, is determined by the reflection rate of the object R, and the incident light
          L. The mathematical form of SSR is given by S(x,y) = R(x,y) * L(x,y) (Here "*" means multiply). So if we can estimate L, we know R.

        ` But L is too hard to know precisely. We use the convolution of S(x,y) and a Gaussain kernel G(x,y) to express L(x,y).Plus, 
          I don't understand why lol.


    Attributes:

        path: All picture in the targeted folder
        type: the way that picture is processed
    """
    def __init__(self):
        self.path = None   
        self.type = None  

    def init_by_user(self):
        self.path = input("请输入要处理的图片所在文件夹的绝对路径：")
        while not os.path.exists(self.path):
            self.path = input("输入有误！请输入要处理的图片所在文件夹的绝对路径：")

    def read_image(image_path):
        img = cv2.imread(image_path)
        if img != None:
            return img
        else:
            input("路径错误或图片无法处理，该文件路径为\n%s\n请确认输入路径下仅有可处理文件后，重新输入路径"%image_path)
            return 0
    
    def replaceZeroes(data):
        min_nonzero = min(data[data != 0])
        data[data == 0] = min_nonzero
        return data

    def SSR(self,img):  # Single Scale Retinex

        L_blur = cv2.GaussianBlur(img,img.shape[:2],0)
        eps = float(1e-10)
    
        h,w = img.shape[:2]
        dst_img = np.zeros((h,w),dtype = np.float32)
        dst_Lblur = np.zeros((h, w),dtype= np.float32)
        dst_R = np.zeros((h, w), dtype= np.float32)
    
        img = self.replaceZeroes(img)
        L_blur = self.replaceZeroes(L_blur)
        cv2.log(img,dst_img)
        cv2.log(L_blur,dst_Lblur)
        log_R = cv2.subtract(dst_img,dst_Lblur)
    
        cv2.normalize(log_R,dst_R,0,255,cv2.NORM_MINMAX)
        log_uint8 = cv2.convertScaleAbs(dst_R)
    
    
        minvalue,maxvalue,minloc,maxloc = cv2.minMaxLoc(log_R)
        for i in range(h):
            for j in range(w):
                log_R[i,j] = (log_R[i,j]-minvalue)*255.0/(maxvalue-minvalue)
        log_uint8 = cv2.convertScaleAbs(log_R)
        return log_uint8

        
