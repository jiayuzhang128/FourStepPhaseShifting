import cv2
import numpy as np
import math

class PhaseShiftingCode():
    def __init__(self,n: int = 4):
        self.n = n

    def toPhasePattern(self,j:int,freq:int=16,width:int=1920,hight:int=1080):
        '''生成'''
        col = np.zeros((width),np.uint8)       #生成一个维数为width的行向量
        for i in range(width):
            col[i] = 128 + 127 * math.cos(2 * math.pi *( i * freq / width + j/ self.n))
        pattern = np.tile(col,(hight,1))
        return pattern

if __name__ == '__main__':                                      #只在当前模块执行，其他模块导入本模块时不执行
    n = 4
    p = PhaseShiftingCode(n)
    for k in range(n):
        pattern = p.toPhasePattern(k)
        title ='PhaseShifting-' + str(k)
        cv2.imshow(title, pattern)
        key = cv2.waitKey(0)
        if key == ord('s'):
            cv2.imwrite(title + '.png', pattern)
        cv2.destroyWindow(title)