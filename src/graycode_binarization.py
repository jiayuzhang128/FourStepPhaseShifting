import cv2 as cv
import numpy as np
import math
from wrapped_phase_algorithm import WrappedPhase

class Binariization():

    def __init__(self,n:int=5):
        self.n = n

    def get_threshold(self,m:int = 4):
        '''利用四幅相移图计算阈值'''
        wp = WrappedPhase()
        I = wp.getImageData(m)
        i = []
        for k in range(m):
            i.append(I[k].astype(np.float32))
        I_th = np.rint((i[0]+i[1]+i[2]+i[3])/m)  #np.rint()四舍五入取整
        TH = I_th.astype(np.uint8)
        cv.imshow('th', TH)
        key1 = cv.waitKey(0)
        if key1 == ord("s"):
            cv.imwrite('TH_img.png',TH)
        cv.destroyAllWindows()
        return TH

    def get_GC_images(self):
        '''读取格雷码图片'''
        J = []
        for i in range(5):
            filename = r"D:\研一文件\其他\structual_light_project\left\I" + str(i) + ".png"
            file_img = np.fromfile(filename,dtype = np.uint8)
            img = cv.imdecode(file_img,-1)
            J.append(img)
        return J

    def getBinaryGrayCode(self):
        '''将格雷码图像二值化处理'''
        b = Binariization()
        threshold = b.get_threshold()
        graycodes = b.get_GC_images()
        rows,cols = threshold.shape
        for a in graycodes:
            for b in range(rows):
                for c in range(cols):
                    if a[b,c] <= threshold[b,c]:
                        a[b,c] = 0
                    else:
                        a[b,c] = 255
        return graycodes
if __name__ == "__main__":
    bgc = Binariization()
    gc = bgc.getBinaryGrayCode()
    for u in range(5):
        gc[u].astype(np.uint8)
        cv.imshow('Binarized_GC-' + str(u),gc[u])
        key2 = cv.waitKey(0)
        if key2 == ord('s'):
            cv.imwrite('Binarized_GC-' + str(u) + ".png",gc[u])
        cv.destroyAllWindows()