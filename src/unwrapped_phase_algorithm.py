import numpy as np
import cv2 as cv
import math
from wrapped_phase_algorithm import WrappedPhase
from graycode_binarization import Binariization
from generate_graycode_map import GrayCode

class UnwrappedPhase():
    '''获得解包裹相位'''
    def __init__(self,n:int = 5):
        self.n = n
    def getBinarizedGrayCodes(self,m:int = 5):
        '''获得二值化后的格雷码图像，m为格雷码位数'''
        BGC = []
        for i in range(self.n):
            filename = "binarized_GC-" + str(i) + ".png"
            img = np.array(cv.imread(filename, 0), np.uint8)
            img_scaled = img/255
            BGC.append(img_scaled.astype(np.uint8))
        return BGC

    def get_k1_k2(self):
        '''获得k1和k2矩阵'''
        BCG = self.getBinarizedGrayCodes()
        rows,cols = BCG[0].shape
        k1 = np.zeros((rows,cols),np.uint8)
        k2 = np.zeros((rows,cols),np.uint8)
        g_k1 = GrayCode(4)                                 #调用格雷码生成模块的GrayCode()类
        g_k2 = GrayCode(5)
        for a in range(rows):
            for b in range(cols):
                code1 = ""
                code_k1 = code1 + str(BCG[0][a,b]) + str(BCG[1][a,b]) + str(BCG[2][a,b]) + str(BCG[3][a,b])
                code_k2 = code1 + str(BCG[0][a,b]) + str(BCG[1][a,b]) + str(BCG[2][a,b]) + str(BCG[3][a,b]) + str(BCG[4][a,b])
                k1[a,b] = g_k1.code2k[code_k1]             #查询字典，将格雷码转换为对应的十进制数
                k2[a,b] = math.floor((g_k2.code2k[code_k2]+1)/2)
        return k1,k2


    def computeUnwrappedPhase(self):
        '''计算解包裹相位'''
        WP = WrappedPhase()
        wrapped_pha = WP.computeWrappedphase(WP.getImageData())
        k1,k2 = self.get_k1_k2()
        rows,cols = k1.shape
        unwrapped_pha = np.zeros((rows,cols),np.float16)
        for c in range(rows):
            for d in range(cols):
                if wrapped_pha[c,d] <= math.pi/2:
                    unwrapped_pha[c,d] = wrapped_pha[c,d] + k2[c,d]*2*math.pi
                elif wrapped_pha[c, d] > math.pi / 2 and wrapped_pha[c, d] < 3*math.pi / 2 :
                    unwrapped_pha[c, d] = wrapped_pha[c, d] + k1[c, d] * 2 * math.pi
                elif wrapped_pha[c, d] >= 3*math.pi / 2 :
                    unwrapped_pha[c, d] = wrapped_pha[c, d] + (k2[c, d]-1) * 2 * math.pi
        return unwrapped_pha

    def showUnwrappedPhase(self):
        '''显示解包裹相位'''
        upha = self.computeUnwrappedPhase()
        upha_scaled = np.rint(upha*255/(32*math.pi))
        upha_scaled_uint = upha_scaled.astype(np.uint8)
        cv.imshow("Absolute_pha.png",upha_scaled_uint)
        key = cv.waitKey(0)
        if key == ord("s"):
            cv.imwrite("Absolute_pha.png",upha_scaled_uint)
        cv.destroyAllWindows()

if __name__ == "__main__":
    u = UnwrappedPhase()
    u.showUnwrappedPhase()
