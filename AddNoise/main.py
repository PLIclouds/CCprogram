# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# Press the green button in the gutter to run the script.

import os
import imghdr
from skimage import io
from skimage import util


def is_float_num(tmp):
    s = tmp.split('.')
    if len(s) > 2:
        return False
    else:
        for si in s:
            if not si.isdigit():
                return False
        return True


def legal_num(tmp, lower, upper):
    if not is_float_num(tmp):
        return 0
    tmp = float(tmp)
    if (tmp < lower) or (tmp > upper):
        return 0
    return 1


class Request:
    """
    The struct of Request class is sooooo bad that I don't want to rewrite it QAQ and don't want to consider any possibility of coding in the future.
    So I don't put any explanation here. Just treat it as a simple tool written by a noob.

    First try so ... not good enough.
    """
    def __init__(self):
        self.path = None
        self.noise_type = None

    def info(self):
        print("程序有bug才会跑到这来")

    def init_by_user(self):
        self.path = input("请输入要处理的图片所在文件夹的绝对路径：")
        while not os.path.exists(self.path):
            self.path = input("输入有误！请输入要处理的图片所在文件夹的绝对路径：")
        self.noise_type = input("请输入噪声类型：（G/I，代表高斯或椒盐噪声）")
        while (self.noise_type != "G") and (self.noise_type != "I"):
            self.noise_type = input("输入有误！请重新输入噪声类型：（G/I）")
        if self.noise_type == 'G':
            self.noise_type = 'Gaussian'
        else:
            self.noise_type = 'S&P'
        if self.noise_type == "Gaussian":
            b = GaussianRequest(a)
            b.subclass_set()
        else:
            b = SPRequest(a)
            b.subclass_set()
        if b.confirm():
            return b
        else:
            return self.init_by_user()

    def confirm(self):
        self.info()
        conf = input("该目录下图片将全部被处理，请确认已做好备份，是否继续？(Y/N)")
        while (conf != "Y") and (conf != "N"):
            conf = input("输入有误！请重新确认：(Y/N)")
        if conf == "N":
            return 0
        else:
            return 1

    def action(self, img, abspath, file):
        print("程序有bug才会跑到这来")

    def answer(self):
        print("开始处理图片")
        files = os.listdir(self.path)
        for file in files:
            abspath = os.path.join(self.path, file)
            if imghdr.what(abspath):
                img = io.imread(abspath)
                self.action(img, abspath, file)


class GaussianRequest(Request):

    mean = 0
    var = 0.01

    def __init__(self, father):
        self.path = father.path
        self.noise_type = father.noise_type

    def info(self):
        print("请确认信息:\n\n",
              "   噪声类型为：%s\n" % "高斯噪声",
              "   噪声强度为：%.2f%%\n" % (self.mean*100),
              "   噪声方差为：%.2f\n" % self.var,
              "   文件路径为：%s \n" % self.path)

    def subclass_set(self):
        self.mean = input("请输入噪声均值（0-100，代表0%-100%的噪声强度）或按下回车选择默认值：")
        while (not legal_num(self.mean, 0, 100)) and self.mean != '':
            self.mean = input("输入有误！请重新输入噪声均值（0-100，代表0%-100%的噪声强度）或按下回车选择默认值：")
        if self.mean == '':
            self.mean = 0
        self.mean = float(self.mean)/100

        self.var = input("请输入噪声方差或按下回车选择默认值：")
        while (not is_float_num(self.var)) and self.var != '':
            self.var = input("输入有误，请重新输入噪声方差或按下回车选择默认值：")
        if self.var == '':
            self.var = 0.01
        self.var = float(self.var)

    def action(self, img, abspath, file):
        img = util.random_noise(img, mean=self.mean, var=self.var)
        img = (img * 255.0).astype('uint8')
        io.imsave(abspath, img)


class SPRequest(Request):

    prob = 0.01

    def __init__(self, father):
        self.path = father.path
        self.noise_type = father.noise_type

    def info(self):
        print("请确认信息:\n\n",
              "   噪声类型为：%s\n" % "椒盐噪声",
              "   像素替换程度为：%.2f%%\n" % (self.prob*100),
              "   文件路径为：%s\n" % self.path)

    def subclass_set(self):
        self.prob = input("请输入像素替换程度（0-100，代表替换0%-100%的像素 ）或按下回车选择默认值：")
        while (not legal_num(self.prob, 0, 100)) and self.prob != '':
            self.prob = input("输入有误！请重新输入像素替换程度（0-100，代表替换0%-100%的像素）或按下回车选择默认值：")
        if self.prob == '':
            self.prob = 5
        self.prob = float(self.prob) / 100

    def action(self, img, abspath, file):
        img = util.random_noise(img, mode='s&p', amount=self.prob)
        img = (img * 255.0).astype('uint8')
        io.imsave(abspath, img)


if __name__ == '__main__':
    print("预处理程序")
    a = Request()
    a = a.init_by_user()
    a.answer()
    input("按回车结束程序")
