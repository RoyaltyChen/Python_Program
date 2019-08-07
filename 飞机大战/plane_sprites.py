import random

import pygame

# 屏幕大小的常量
SCREEN_RECT = pygame.Rect(0, 0, 480, 700)
# 刷新帧率
FRAME_PER_SECOND = 60
# 创建敌机的定时器常量
CREATE_ENEMY_EVENT = pygame.USEREVENT
# 创建子弹的定时器常量
HERO_FIRE_EVENT = pygame.USEREVENT + 1

# 定义字体大小以及字体类型常量
FONT_SIZE = 50
FONT_FAMILY = u"微软雅黑"


class GameSprite(pygame.sprite.Sprite):
    """飞机大战游戏精灵"""

    def __init__(self, image_name, speed=1):
        # 调用父类的初始化方法
        super().__init__()

        # 定义对象的属性
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.speed = speed

    def update(self):
        # 在屏幕的垂直方向上移动(向下移动)
        self.rect.y += self.speed

    def boom(self):
        self.speed = 0


class Background(GameSprite):
    """游戏背景精灵"""
    """
    思路：
        1. 利用两张图片交替进行
        2. 先将两张图片直接合成一张图片，然后当图像移动到 -height/2 时，
            重新切换到初始位置。
    """

    def __init__(self, is_alt=False):
        """
        背景精灵初始化
        :param is_alt:表示是否是第二张图片
        """
        super().__init__('./素材/images/bg.png')
        if is_alt:
            self.rect.y = -self.rect.height
        pass

    def update(self):

        # 1. 调用父类的方法实现
        super().update()
        # 2. 判断是否移出屏幕,如果移出屏幕，将图像设置到屏幕的上方,
        if self.rect.y >= SCREEN_RECT.height:
            self.rect.y = -self.rect.height
        pass


class Start_End_Screen(GameSprite):
    """启动界面以及结束界面"""

    def __init__(self):
        super(Start_End_Screen, self).__init__('./素材/images/again.png', speed=0)
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.centery = SCREEN_RECT.centery


class Enemy(GameSprite):
    def __init__(self):
        # 1. 调用父类方法，创建敌机精灵，同时指定敌机图片
        super(Enemy, self).__init__("./素材/images/enemy1.png")
        # 2. 指定敌机的初始随机速度
        self.speed = random.randint(1, 3)
        # 3. 指定敌机的初始随机位置
        self.rect.bottom = 0
        max_x = SCREEN_RECT.width - self.rect.width
        self.rect.x = random.randint(0, max_x)

        # 自身分数
        self.value = 1
        # 爆炸效果
        self.hit = False  # 被击中
        self.bomb_list = [pygame.image.load(path) for path in
                          ["./素材/images/enemy1_down1.png", "./素材/images/enemy1_down2.png",
                           "./素材/images/enemy1_down3.png", "./素材/images/enemy1_down4.png"]]  # 爆炸分帧图片组
        self.image_num = 0  # 显示刷新多少次换一张图片
        self.image_index = 0  # 当前显示图片的index

    def update(self):
        if self.hit:
            self.boom()
        else:
            # 1. 调用父类方法，保持垂直方向的飞行
            super(Enemy, self).update()
            # 2. 判断是否飞出屏幕，如果是，需要从精灵组删除。
            if self.rect.y >= SCREEN_RECT.height:
                # print("飞出屏幕，需要从精灵组删除....")
                self.kill()

    def __del__(self):
        # print("敌机挂了 %s" % self.rect)
        pass

    def boom(self):
        super(Enemy, self).boom()
        # self.screen.blit(self.bomb_list[self.image_index], (self.rect.x, self.rect.y))
        self.image = self.bomb_list[self.image_index]
        self.image_num += 1
        if self.image_num == 8:  # 刷新10次切换1张图
            self.image_num = 0
            self.image_index += 1
        if self.image_index > len(self.bomb_list) - 1:
            self.kill()
            # self.hit = False  # 爆炸动画播放完成，再修改标记
            self.image_num = 1
            self.image_index = 1


class Hero(GameSprite):
    """英雄精灵"""

    def __init__(self):

        # 1. 调用父类方法，设置image & speed
        super(Hero, self).__init__("./素材/images/me1.png", speed=0)
        # 2. 初始化英雄飞机位置
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.bottom = SCREEN_RECT.bottom - 120

        # 3. 创建子弹精灵组
        self.bullets = pygame.sprite.Group()

        # 爆炸效果
        self.hit = False  # 被击中
        self.bomb_list = [pygame.image.load(path) for path in
                          ["./素材/images/me_destroy_1.png", "./素材/images/me_destroy_2.png",
                           "./素材/images/me_destroy_3.png", "./素材/images/me_destroy_4.png"]]  # 爆炸分帧图片组
        self.image_num = 0  # 显示刷新多少次换一张图片
        self.image_index = 0  # 当前显示图片的index

    def update(self):
        if self.hit:
            self.boom()
        else:
            # 英雄在水平方向移动
            self.rect.x += self.speed

            # 控制英雄不能离开屏幕
            if self.rect.x < 0:
                self.rect.x = 0
            if self.rect.right > SCREEN_RECT.right:
                self.rect.right = SCREEN_RECT.right

    def fire(self):
        if self.hit:
            return
        print("发射子弹...")
        for i in range(3):
            # 1. 创建子弹精灵
            bullet = Bullet()

            # 2. 设置精灵的位置
            bullet.rect.bottom = self.rect.y - 20 * i
            bullet.rect.centerx = self.rect.centerx

            # 3. 将精灵添加到精灵组
            self.bullets.add(bullet)

    def boom(self):
        """爆炸动画"""
        super(Hero, self).boom()
        self.speed = 4
        self.rect.y += self.speed
        # self.screen.blit(self.bomb_list[self.image_index], (self.rect.x, self.rect.y))
        self.image = self.bomb_list[self.image_index]
        self.image_num += 1
        if self.image_num == 12:  # 刷新10次切换1张图
            self.image_num = 0
            self.image_index += 1
        if self.image_index > len(self.bomb_list) - 1:
            if self.rect.y > SCREEN_RECT.height:
                self.kill()
            # self.hit = False  # 爆炸动画播放完成，再修改标记
            self.image_num = 1
            self.image_index = 1


class Bullet(GameSprite):
    """子弹精灵"""

    def __init__(self):
        # 调用父类方法，设置子弹图片 & 初始速度
        super(Bullet, self).__init__("./素材/images/bullet1.png", speed=-2)

    def update(self):
        # 调用父类方法，让子弹沿垂直方向飞行
        super(Bullet, self).update()

        # 判断子弹是否飞出屏幕
        if self.rect.bottom < 0:
            self.kill()

    def __del__(self):
        print("子弹被销毁...")

"""
class GameFont(object):
    def __init__(self, content):
        #self.font = pygame.font.SysFont(FONT_FAMILY, FONT_SIZE)
        pygame.font.init()
        font = pygame.font.SysFont(FONT_FAMILY, FONT_SIZE)
        self.font = font.render(str(content).encode('utf-8'),True,(10,10,10))
        self.rect = self.font.get_rect()

        # 设置字体位置
        self.rect.x = SCREEN_RECT.width - self.rect.width -10
        self.rect.y = SCREEN_RECT.y + 10

"""
