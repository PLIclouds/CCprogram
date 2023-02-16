
import os
import cv2
import numpy as np
import enhancement as en

class Request(object):
    """

    This class can be easy to use for some people who don't like to make more complex choice on the parameters of the algorithm but want to have a try.
    Clearly, it still work but not good enough! I recommend everyone to use it by downloading the folder "enhancement" and use it as whatever you like!

    But if you still want to try it, you can use it by the fellow steps:
        
        1. First you will put in the path of the FOLDER, which includes the pictures you'd like to process. If you write a wrong path, you have to check
           it and try again. 
        2. Next put in the method you want to use. Also, If you write a wrong name, you have to check it and try again. (Currently only support SSR and 
           MSR, which is introduced in detail in enhancement/retinex.py)
        3. Finally press any buttons in your keyboard to continue. But make sure you know that your original pictures will be covered and can NOT be 
           found later!!!

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
        self.type = input("请输入处理类型：（目前仅支持SSR和MSR）")
        while(self.type != 'SSR' and self.type != 'MSR'):
            self.type = input("输入有误！请输入合法的处理类型：")
        input("请注意，被处理的文件将被覆盖且无法恢复！\n按任意键确认继续")

    def read_image(self, image_path):
        img = cv2.imread(image_path)
        return img

    def answer(self):
        files = os.listdir(self.path)
        for file in files:
            abspath = os.path.join(self.path, file)
            img = self.read_image(abspath) 
            if np.max(img) == None:
                continue
            match self.type:
                case 'SSR': 
                    ans = en.Retinex(img)
                    ans.SSR(img_path = abspath)
                case 'MSR':
                    ans = en.Retinex(img)
                    ans.MSR(img_path = abspath)
                case _:
                    input("fatal error!\n遇到此类错误请反馈给开发人员!")
                    return 1
        return 0
      

if __name__ == '__main__':
    re = Request()
    re.init_by_user()
    re.answer()