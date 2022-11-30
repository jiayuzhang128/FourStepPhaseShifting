import cv2
import numpy as np

class GrayCode():
    codes = np.array([])
    code2k = {}
    k2v = {}
    v2k = {}
    def __init__(self, n: int = 3):
        self.n = n
        self.codes = self.__creatCode(self.n)
        # 从k（idx）转换到格雷码
        for k in range(2 ** n):
            self.code2k[self.__k2code(k)] = k
        # 从格雷码转换到v
        for k in range(2 ** n):
            self.k2v[k] = self.__k2v(k)
        # 从v转换到k（idx）
        for k, v in self.k2v.items():
            self.v2k[v] = k

    def toPattern(self, idx: int, cols: int = 1280, rows: int = 800):
        assert (idx >= 0) #断言用法，确保idx >= 0
        row = self.codes[idx, :]
        one_row = np.zeros([cols], np.uint8)
        assert (cols % len(row) == 0)
        per_col = int(cols / len(row))

        for i in range(len(row)):
            one_row[i * per_col: (i + 1) * per_col] = row[i]
        pattern = np.tile(one_row, (rows, 1)) * 255
        return pattern

    def __creatCode(self, n: int):
        code_temp = GrayCode.__createGrayCode(n)
        codes = []
        for row in range(len(code_temp[0])):
            c = []
            for idx in range(len(code_temp)):
                c.append(int(code_temp[idx][row]))
            codes.append(c)
        return np.array(codes, np.uint8)

    def __k2code(self, k):
        col = self.codes[:, k]
        code = ""
        for i in col:
            code += str(i)
        return code

    def __k2v(self, k):
        col = list(self.codes[:, k])
        col = [str(i) for i in col]
        code = "".join(col)
        return int(code, 2)

    @staticmethod
    def __createGrayCode(n: int):
        if n < 1:
            print("输入数字必须大于0")
            assert (0);
        elif n == 1:
            code = ["0", "1"]
            return code
        else:
            code = []
            code_pre = GrayCode.__createGrayCode(n - 1)
            for idx in range(len(code_pre)):
                code.append("0" + code_pre[idx])
            for idx in range(len(code_pre) - 1, -1, -1):
                code.append("1" + code_pre[idx])
            return code


if __name__ == '__main__':
    n = 5
    g = GrayCode(n)
    print("code")
    print(g.codes)
    print("\ncode -> k")
    print(g.code2k)
    print("\nk -> v")
    print(g.k2v)
    print("\nv -> k")
    print(g.v2k)
    for i in range(n):
        pattern = g.toPattern(i)
        title ='Pattern-' + str(i)
        cv2.imshow(title, pattern)
        cv2.waitKey()
        cv2.destroyWindow(title)