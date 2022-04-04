import cv2
import numpy as np
#k:把格雷码直接当初二进制对应的十进制数
#v：格雷码实际对应的十进制数
class GrayCode():
    codes = np.array([])
    code2k = {}
    k2v = {}
    v2k = {}
    def __init__(self, n: int = 3):
        self.n = n
        self.codes = self.__formCodes(self.n)
        # 从格雷码转换到k
        for k in range(2 ** n):
            self.code2k[self.__code2k(k)] = k
        # 从格雷码转换到v
        for k in range(2 ** n):
            self.k2v[k] = self.__k2v(k)
        # 从v转换到k（idx）
        for k, v in self.k2v.items():
            self.v2k[v] = k

    @staticmethod            #不需要实例化直接像函数一样调用（类名.方法名()来调用），定义时也不需要self，cls参数
    def __createGrayCode(n: int):
        '''生成n位格雷码'''
        if n < 1:
            print("输入数字必须大于0")
            # assert (0);
        #        elif n == 1:                                      #代码较长
        #            code = ["0", "1"]
        #            return code
        #        else:
        #            code = []
        #            code_pre = GrayCode.__createGrayCode(n - 1)   #递归嵌套
        #            code.append("0" + idx for idx in code_pre)    #解析法写for循环
        #            code.append("1" + idx for idx in code_pre(::-1))
        #            return code
        else:
            code = ["0", "1"]
            for i in range(1, n):  # 循环递归
                code_lift = ["0" + idx for idx in code]  # 解析法写for循环
                code_right = ["1" + idx for idx in code[::-1]]
                code = code_lift + code_right
            return code

    def __formCodes(self, n: int):
        '''生成codes矩阵'''
        code_temp = GrayCode.__createGrayCode(n)       # 首先生成n位格雷码储存在code_temp中
        codes = []
        for row in range(len(code_temp[0])):           #n位格雷码循环n次，
            c = []
            for idx in range(len(code_temp)):          #循环2**n次
                c.append(int(code_temp[idx][row]))     #将code_temp中第idx个元素中的第row个数添加到c中
            codes.append(c)
        return np.array(codes, np.uint8)

    def toPattern(self, idx: int, cols: int = 1920, rows: int = 1080):
        '''生成格雷码光栅图'''
        #assert (idx >= 0) #断言用法，确保idx >= 0
        row = self.codes[idx, :]                                #idx表示codes的行索引
        one_row = np.zeros((cols), np.uint8)                    #np.zeros((5),np.uint8)=array([0,0,0,0,0])一个参数是行向量，两个参数是矩阵
        #assert (cols % len(row) == 0)
        per_col = int(cols / len(row))                          #将1280个像素分成256份，每份per_col=5个像素
        for i in range(len(row)):
            one_row[i * per_col: (i + 1) * per_col] = row[i]
        pattern = np.tile(one_row, (rows, 1)) * 255             #np.tile(a，(b,c))函数用a来重构b行c列
        return pattern


    def __code2k(self, k):
        '''将k映射到对应的格雷码'''
        col = self.codes[:, k]
        code = ""
        for i in col:
            code += str(i)
        return code

    def __k2v(self, k):
        '''将k映射为v'''
        col = list(self.codes[:, k])           #将第k列格雷码储存在col中
        col = [str(i) for i in col]
        code = "".join(col)                    #将列表中的元素整合到一起
        v = int(code,2)
        return v


    def store_gray_code_map_value(self):
        '''将8幅256列的格雷码编码图的码值列表储存在'格雷光栅码值.txt'文件中'''
        filename = '格雷光栅码值.txt'
        with open(filename,'w') as fob1:
            fob1.write("codes\n")
            for i in g.codes:
                fob1.write('长度：' + str(len(i))+ '\n')
                fob1.write(str(i) + '\n')

if __name__ == '__main__':
    n =  5
    g = GrayCode(n)
    print("codes")
    print(g.codes)
    print("\ncode -> k")
    print(g.code2k)
    print("\nk -> v")
    print(g.k2v)
    print("\nv -> k")
    print(g.v2k)
    g.store_gray_code_map_value()
    for i in range(n):
        pattern = g.toPattern(i)
        title ='Pattern-' + str(i)
        cv2.namedWindow(title, cv2.WINDOW_NORMAL)
        '''使窗口正常显示'''
        cv2.imshow(title, pattern)
        key = cv2.waitKey(0)
        if key == ord('s'):
            cv2.imwrite(title + '.png', pattern)
        cv2.destroyWindow(title)