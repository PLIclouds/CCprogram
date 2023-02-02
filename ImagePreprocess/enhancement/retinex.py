import cv2
import numpy as np

class Retinex:
    """

    All supported type of request are listed below:

    1. Single Scale Retinex(SSR)

        Retinex is a theory raised in 1960s that improves the brightness, contrast and sharpness of an image. Here are some important
        views about it:

        ` The color of an object is determined by the reflection ability to the light, but has no relationship with the light 
          intensity.

        ` Picture S, which is the color that observer get, is determined by the reflection rate of the object R, and the incident light
          L. The mathematical form of SSR is given by S(x,y) = R(x,y) * L(x,y) (Here "*" means multiply). So if we can estimate L, we know R.

        ` But L is too hard to know precisely. We use the convolution of S(x,y) and a Gaussian kernel G(x,y) to express L(x,y).Plus, 
          I don't understand why lol.

    2. Multi-Scale Retinex(MSR)

        It's a algorithm developed by SSR, which use multiple size of Gaussian kernels to calculate L(x,y).

    Check more information about these algorithm by searching on the Internet!

    """

    def __init__(self, img):
        self.img = img

    def replaceZeroes(self, data):
        min_nonzero = min(data[data != 0])
        data[data == 0] = min_nonzero
        return data

    def cut_layer(self, img):
        return img[:, :, 0], img[:, :, 1] , img[:, :, 2] 

    def SSR_one_layer(self, img, size = 3):
        L_blur = cv2.GaussianBlur(img, (size, size), 0)
        img = self.replaceZeroes(img)
        L_blur = self.replaceZeroes(L_blur)

        dst_Img = cv2.log(img/255.0)
        dst_Lblur = cv2.log(L_blur/255.0)
        dst_IxL = cv2.multiply(dst_Img,dst_Lblur)
        log_R = cv2.subtract(dst_Img, dst_IxL)

        dst_R = cv2.normalize(log_R,None,0,255,cv2.NORM_MINMAX)
        log_uint8 = cv2.convertScaleAbs(dst_R)
        return log_uint8

    def SSR_r(self, size = 3):

        # size is for Gaussian kernel, not for the image. size must > 0 and size % 2 == 1 because of the usage of cv2.GaussianBlur

        img0, img1, img2 = self.cut_layer(self.img.astype(np.float32))
        
        dst_img0 = self.SSR_one_layer(img0, size)
        dst_img1 = self.SSR_one_layer(img1, size)
        dst_img2 = self.SSR_one_layer(img2, size)

        dst_img = cv2.merge((dst_img0, dst_img1, dst_img2))
        return dst_img

    def SSR(self, img_path, size = 3):
        # This is only used for COVERING !!! Make sure you know that before using it. 
        dst_img = self.SSR_r(size)
        cv2.imwrite(img_path,dst_img)
        
    def MSR_one_layer(self, img, scales = [15, 101, 301]):
        weight = 1 / 3.0
        scales_size = len(scales)
        h, w = img.shape[:2]
        log_R = np.zeros((h, w), dtype=np.float32)

        for i in range(scales_size):
            img = self.replaceZeroes(img)
            L_blur = cv2.GaussianBlur(img, (scales[i], scales[i]), 0)
            L_blur = self.replaceZeroes(L_blur)
            dst_Img = cv2.log(img/255.0)
            dst_Lblur = cv2.log(L_blur/255.0)
            dst_Ixl = cv2.multiply(dst_Img, dst_Lblur)
            log_R += weight * cv2.subtract(dst_Img, dst_Ixl)

        dst_R = cv2.normalize(log_R, None, 0, 255, cv2.NORM_MINMAX)
        log_uint8 = cv2.convertScaleAbs(dst_R)
        return log_uint8
    
    def MSR_r(self, scales = [15, 101, 301]):

        img0, img1, img2 = self.cut_layer(self.img.astype(np.float32))
        
        dst_img0 = self.MSR_one_layer(img0, scales)
        dst_img1 = self.MSR_one_layer(img1, scales)
        dst_img2 = self.MSR_one_layer(img2, scales)

        dst_img = cv2.merge((dst_img0, dst_img1, dst_img2))
        return dst_img

    def MSR(self, img_path, scales = [15, 101, 301]):
        # This is only used for COVERING !!! Make sure you know that before using it. 
        dst_img = self.MSR_r(scales)
        cv2.imwrite(img_path,dst_img)