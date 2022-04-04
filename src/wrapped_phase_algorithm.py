import numpy as np
import cv2 as cv
import math

class WrappedPhase():
    def __init__(self,n:int = 4):
        self.n = n
    @staticmethod
    def getImageData(m:int = 4,):
        '''获取相机拍摄的n幅相移图'''
        I = []
        for i in range(m):
            filename = r"D:\研一文件\其他\structual_light_project\left\I" + str(i+5) + ".png"
            img_file = np.fromfile(filename, dtype=np.uint8)  # 以dtype形式读取文件
            img = cv.imdecode(img_file, -1)  # 从指定的内存缓存中读取数据，并把数据转换(解码)成图像格式；主要用于从网络传输数据中恢复出图像。
            I.append(img)
        return I

    def computeWrappedphase(self,I,width:int = 1280,hight:int = 720):
        '''计算包裹相位'''
        i0 = I[0].astype(np.float32)
        i1 = I[1].astype(np.float32)
        i2 = I[2].astype(np.float32)
        i3 = I[3].astype(np.float32)
        pha = np.zeros((hight,width),np.float32)
        for a in range(hight):
            for b in range(width):
                if i0[a,b] == i2[a,b] and i3[a,b] < i1[a,b]:        #四个特殊位置
                    pha[a,b] = 3*math.pi/2
                elif i0[a,b] == i2[a,b] and i3[a,b] > i1[a,b]:      #四个特殊位置
                    pha[a,b] = math.pi/2
                elif i3[a, b] == i1[a, b] and i0[a, b] < i2[a, b]:  #四个特殊位置
                    pha[a, b] = math.pi
                elif i3[a, b] == i1[a, b] and i0[a, b] > i2[a, b]:  #四个特殊位置
                    pha[a, b] = 0
                elif i0[a, b] > i2[a, b] and i1[a,b] < i3[a,b]:     # 第一象限
                    pha[a,b] = math.atan((i3[a,b] - i1[a, b])/ (i0[a, b] - i2[a, b]))
                elif i0[a, b] < i2[a, b] and i1[a,b] < i3[a,b]:     # 第二象限
                    pha[a,b] = math.pi-math.atan((i3[a,b] - i1[a, b])/ (i2[a, b] - i0[a, b]))
                elif i0[a, b] < i2[a, b] and i1[a,b] > i3[a,b]:     # 第三象限
                    pha[a,b] = math.pi + math.atan((i3[a,b] - i1[a, b])/ (i0[a, b] - i2[a, b]))
                elif i0[a, b] > i2[a, b] and i1[a,b] > i3[a,b]:     # 第四象限
                    pha[a,b] = 2*math.pi - math.atan((i1[a,b] - i3[a, b])/ (i0[a, b] - i2[a, b]))
        pha_scaled = pha*255/(2*math.pi)
        pha_scaled1 = pha_scaled.astype(np.uint8)
        if __name__ == "__main__":
            cv.imshow("Wrapped_Phase",pha_scaled1)
            key = cv.waitKey(0)
            if key == ord("s"):
                cv.imwrite("Wrapped_Phase.png",pha_scaled1)
            cv.destroyAllWindows()
        return pha

if __name__ == "__main__":
    w = WrappedPhase()
    w.computeWrappedphase(w.getImageData())