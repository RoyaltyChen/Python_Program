import random

import pygame

# 屏幕大小的常量
SCREEN_RECT = pygame.Rect(0, 0, 288, 512)
# 刷新帧率
FRAME_PER_SECOND = 60

# 创建管道的定时器常量
CREATE_PIPELINE_EVENT = pygame.USEREVENT


class GameSprite(pygame.sprite.Sprite):
    """精灵类"""

    def __init__(self, image_name, speed):
        """
        其它类的父类
        :param image_name: 图像名称
        :param speed: 移动速度
        """
        super(GameSprite, self).__init__()
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.speed = speed

    def update(self):
        self.rect.x -= self.speed


class Background(GameSprite):
    """背景类"""

    def __init__(self, is_alt=False):
        """
        初始化背景
        :param is_alt: 判断是否是第一张背景图像。因为小鸟向右运动的画面，是由背景交替移动的错觉实现的。此时需要两张图像交替
        """
        super(Background, self).__init__("./images/background-day.png", speed=1)

        if is_alt:
            self.rect.x = self.rect.width

    def update(self):
        super(Background, self).update()

        if self.rect.x < - self.rect.width:
            self.rect.x = self.rect.width


class Base(GameSprite):
    """地面类"""

    def __init__(self, is_alt=False):
        """
        初始化地面图像。
        :param is_alt: 判断是否是第一张地面图像，因为地面图像与背景处理方式相同，需要两张图像不停交替
        """
        super(Base, self).__init__("./images/base.png", speed=1)
        self.rect.y = SCREEN_RECT.height - self.rect.height + 50

        if is_alt:
            self.rect.x = self.rect.width

    def update(self):
        super(Base, self).update()

        if self.rect.x < - self.rect.width:
            self.rect.x = self.rect.width


class Bird(GameSprite):
    """主角类"""

    def __init__(self):
        """初始化小鸟"""

        super(Bird, self).__init__("./images/bluebird-midflap.png", speed=0)
        self.rect.centery = SCREEN_RECT.centery
        self.rect.x = 50

    def update(self):
        # super(Bird, self).update()
        self.rect.y += self.speed
        # 下降的速度可以进阶
        ## 加入重力因素，下降速度会越来越快


class Pipeline(GameSprite):
    """管道类"""

    def __init__(self, is_alt=False, rect=None):
        """
        初始化 管道 图像
        :param is_alt: 判断是否是需要旋转的管道图像
        :param rect:  不需要旋转的图像 Rect 对象
        """
        super(Pipeline, self).__init__("./images/pipe-green.png", speed=1)

        self.rect.x = SCREEN_RECT.width
        self.rect.y = SCREEN_RECT.height - random.randint(int(self.rect.height * 2 / 5), int(self.rect.height))
        if is_alt:
            self.image = pygame.transform.rotate(self.image, 180)
            self.rect.y = rect.y - 150 - self.rect.height

    def update(self):
        super(Pipeline, self).update()

        # 管道移动超出屏幕，则销毁
        if self.rect.x < - self.rect.width:
            self.kill()


class Score(GameSprite):
    """分数类"""

    def __init__(self, value, score=0, is_first=True, pre_rect=None):
        """
        显示数值图像
        :param value: 此数值对应图像名称
        :param score: 当前游戏获得的分数
        :param is_first: 此数值图像是否处于第一个位置
        :param pre_rect: 前一个数值图像Rect对象
        """

        super(Score, self).__init__("./images/%d.png" % value, speed=0)
        self.n = len(str(score))
        self.is_first = is_first
        self.pre_rect = pre_rect

        # 如果 is_first = False, 那么初始化Score对象时，参数pre_rect必须赋值
        if not self.is_first:
            if not self.pre_rect:
                print("参数 pre_rect 不能为 NoneType")

        self.rect.y = 100
        self.__position_x()

    def __position_x(self):
        """计算出score图像的X坐标值"""

        if self.is_first:
            self.rect.x = SCREEN_RECT.centerx - self.n / 2 * self.rect.width
        else:
            self.rect.x = self.pre_rect.x + self.pre_rect.width

    def update(self):
        super(Score, self).update()
