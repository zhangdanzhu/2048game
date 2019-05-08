# _*_ coding:UTF-8 _*_

import numpy, sys, random, pygame
from pygame.locals import *

SIZE = 4            # 4*4行列
BLOCK_WH = 110      # 每个块的长度宽度
BLOCK_SPACE = 10    # 两个块之间的间隙
BLOCK_SIZE = BLOCK_WH * SIZE + (SIZE + 1) * BLOCK_SPACE
MATRIX = numpy.zeros([SIZE, SIZE])              # 初始化矩阵4*4的0矩阵
SCREEN_SIZE = (BLOCK_SIZE, BLOCK_SIZE + 110)    # 屏幕尺寸
TITLE_RECT = pygame.Rect(0, 0, BLOCK_SIZE, 110) # 设置标题矩形的大小
Score = 0

Block_Color = {
    0: (150, 150, 150),
    2: (255, 255, 255),
    4: (255, 255, 128),
    8: (255, 255, 0),
    16: (255, 220, 128),
    32: (255, 220, 0),
    64: (255, 190, 0),
    128: (255, 160, 0),
    256: (255, 130, 0),
    512: (255, 100, 0),
    1024: (255, 70, 0),
    2048: (255, 40, 0),
    4096: (255, 10, 0),
}  # 数块颜色


# 基础类
class UpdateNew(object):
    """docstring for UpdateNew"""

    def __init__(self, matrix):
        super(UpdateNew, self).__init__()
        self.matrix = matrix
        self.score = 0
        self.zerolist = []

    def combineList(self, rowlist):
        '''
        合并相同的数字
        :param rowlist:
        :return:
        '''
        start_num = 0
        end_num = SIZE - rowlist.count(0) - 1
        while start_num < end_num:
            # 按照移动方向优先级（之前四个方向的按键已经弄好了顺序）
            if rowlist[start_num] == rowlist[start_num + 1]:
                rowlist[start_num] *= 2
                self.score += int(rowlist[start_num])  # 每次返回累加的分数
                rowlist[start_num + 1:] = rowlist[start_num + 2:]
                rowlist.append(0)
            start_num += 1
        return rowlist

    def removeZero(self, rowlist):
        '''
        根据空位移动
        :param rowlist:
        :return:
        '''
        while True:
            mid = rowlist[:]  # 拷贝一份list
            try:
                rowlist.remove(0)
                rowlist.append(0)
            except:
                pass
            if rowlist == mid:
                break;
        return self.combineList(rowlist)

    def toSequence(self, matrix):
        '''
        处理
        :param matrix:
        :return:
        '''
        lastmatrix = matrix.copy()
        m, n = matrix.shape  # 获得矩阵的行，列
        for i in range(m):
            newList = self.removeZero(list(matrix[i]))
            matrix[i] = newList
            for k in range(SIZE - 1, SIZE - newList.count(0) - 1, -1):  # 添加所有有0的行号列号
                self.zerolist.append((i, k))
        if matrix.min() == 0 and (matrix != lastmatrix).any():  # 矩阵中有最小值0且移动后的矩阵不同，才可以添加0位置处添加随机数
            GameInit.initData(SIZE, matrix, self.zerolist)
        return matrix


class LeftAction(UpdateNew):
    """docstring for LeftAction"""

    def __init__(self, matrix):
        super(LeftAction, self).__init__(matrix)

    def handleData(self):
        matrix = self.matrix.copy()  # 获得一份矩阵的复制
        newmatrix = self.toSequence(matrix)
        return newmatrix, self.score


class RightAction(UpdateNew):
    """docstring for RightAction"""

    def __init__(self, matrix):
        super(RightAction, self).__init__(matrix)

    def handleData(self):
        matrix = self.matrix.copy()[:, ::-1]
        newmatrix = self.toSequence(matrix)
        return newmatrix[:, ::-1], self.score


class UpAction(UpdateNew):
    """docstring for UpAction"""

    def __init__(self, matrix):
        super(UpAction, self).__init__(matrix)

    def handleData(self):
        matrix = self.matrix.copy().T
        newmatrix = self.toSequence(matrix)
        return newmatrix.T, self.score


class DownAction(UpdateNew):
    """docstring for DownAction"""

    def __init__(self, matrix):
        super(DownAction, self).__init__(matrix)

    def handleData(self):
        matrix = self.matrix.copy()[::-1].T
        newmatrix = self.toSequence(matrix)
        return newmatrix.T[::-1], self.score


class GameInit(object):
    """docstring for GameInit"""

    def __init__(self):
        super(GameInit, self).__init__()

    @staticmethod
    def getRandomLocal(zerolist=None):
        '''
        随机获取一个位置
        :param zerolist:
        :return:
        '''
        if zerolist == None:
            a = random.randint(0, SIZE - 1)
            b = random.randint(0, SIZE - 1)
        else:
            a, b = random.sample(zerolist, 1)[0]
        return a, b

    @staticmethod
    def getNewNum():
        '''
        随机返回2或者4
        :return: 2或者4
        '''
        n = random.random()
        if n > 0.8:
            n = 4
        else:
            n = 2
        return n

    @classmethod
    def initData(cls, Size,matrix = None,zerolist = None):
        '''
        初始化棋盘
        :return: 返回初始化任意位置为2或者4的矩阵
        '''
        if matrix is None:
            matrix = MATRIX.copy()
        a, b = cls.getRandomLocal(zerolist)  # zerolist空任意返回(x,y)位置，否则返回任意一个0元素位置
        n = cls.getNewNum()
        matrix[a][b] = n
        return matrix

    @classmethod
    def drawSurface(cls, screen, matrix, score):
        pygame.draw.rect(screen, (255, 255, 255), TITLE_RECT)  # 第一个参数是屏幕，第二个参数颜色，第三个参数rect大小，第四个默认参数
        font1 = pygame.font.SysFont('simsun', 48)
        font2 = pygame.font.SysFont(None, 32)
        screen.blit(font1.render('Score:', True, (255, 127, 0)), (20, 25))  # font.render第一个参数是文本内容，第二个参数是否抗锯齿，第三个参数字体颜色
        screen.blit(font1.render('%s' % score, True, (255, 127, 0)), (170, 25))
        screen.blit(font2.render('up', True, (255, 127, 0)), (360, 20))
        screen.blit(font2.render('left  down  right', True, (255, 127, 0)), (300, 50))
        a, b = matrix.shape
        for i in range(a):
            for j in range(b):
                cls.drawBlock(screen, i, j, Block_Color[matrix[i][j]], matrix[i][j])

    @staticmethod
    def drawBlock(screen, row, column, color, blocknum):
        font = pygame.font.SysFont('stxingkai', 80)
        w = column * BLOCK_WH + (column + 1) * BLOCK_SPACE
        h = row * BLOCK_WH + (row + 1) * BLOCK_SPACE + 110
        pygame.draw.rect(screen, color, (w, h, 110, 110))
        if blocknum != 0:
            fw, fh = font.size(str(int(blocknum)))
            screen.blit(font.render(str(int(blocknum)), True, (0, 0, 0)), (w + (110 - fw) / 2, h + (110 - fh) / 2))

    @staticmethod
    def keyDownPressed(keyvalue, matrix):
        if keyvalue == K_LEFT:
            return LeftAction(matrix)
        elif keyvalue == K_RIGHT:
            return RightAction(matrix)
        elif keyvalue == K_UP:
            return UpAction(matrix)
        elif keyvalue == K_DOWN:
            return DownAction(matrix)

    @staticmethod
    def gameOver(matrix):
        testmatrix = matrix.copy()
        a, b = testmatrix.shape
        # 如果存在一行或一列相邻两个数相同，则游戏没有结束
        for i in range(a):
            for j in range(b - 1):
                if testmatrix[i][j] == testmatrix[i][j + 1]:
                    print('游戏没有结束')
                    return False
        for i in range(b):
            for j in range(a - 1):
                if testmatrix[j][i] == testmatrix[j + 1][i]:
                    print('游戏没有结束')
                    return False
        # 否则数字已满且无法行动，游戏结束
        print('游戏结束')
        return True


def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)  # 屏幕设置，第一个参数分辨率，第二个参数模式(FULLSCREEN为全屏若不需要全屏则置0)，第三个参数色深
    # 初始化棋盘，获得最初的一个数
    matrix = GameInit.initData(SIZE)
    # 当前分数
    currentscore = 0
    # 画界面
    GameInit.drawSurface(screen, matrix, currentscore)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            # 退出
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            # 按键
            elif event.type == pygame.KEYDOWN:
                actionObject = GameInit.keyDownPressed(event.key, matrix)  # 创建各种动作类的对象
                matrix, score = actionObject.handleData()  # 处理数据
                currentscore += score
                GameInit.drawSurface(screen, matrix, currentscore)
                # 没有空位了则进行游戏是否结束的判断
                if matrix.min() != 0:
                    GameInit.gameOver(matrix)
        pygame.display.update()

if __name__ == '__main__':
    main()
