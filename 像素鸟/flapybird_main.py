"""
    program: flapybird
    author: Mr Chen
    date: 2019-08-20
    version: v1

    Function: a bird is controlled
    Uncompleted: start and pause game

"""

import pygame
from flapybird_sprites import *


class FlapyBirdGame(object):
    """控制游戏整个流程"""

    def __init__(self):
        # 创建窗口
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)
        # 创建时钟对象
        self.clock = pygame.time.Clock()

        # 分数变量
        self.score = 0
        self.flag = False
        self.is_score_changing = False

        # 创建精灵和精灵组
        self.__create_sprites()

        # 4. 设置定时器事件 - 创建管道 1s
        pygame.time.set_timer(CREATE_PIPELINE_EVENT, 3500)

    def __create_sprites(self):
        """创建精灵以及精灵组"""
        # 创建背景精灵
        bg1 = Background()
        bg2 = Background(True)
        self.bg_group = pygame.sprite.Group(bg1, bg2)

        # 创建管道精灵组
        self.pipeline_group = pygame.sprite.Group()

        # 创建路面精灵
        base = Base()
        base1 = Base(True)
        self.base_group = pygame.sprite.Group(base, base1)

        # 创建小鸟
        self.bird = Bird()
        self.bird_group = pygame.sprite.Group(self.bird)

        # 创建数字
        score = Score(0)
        self.score_group = pygame.sprite.Group(score)

    def __update_sprite(self):
        """更新绘制精灵、精灵组"""
        self.bg_group.update()
        self.bg_group.draw(self.screen)

        # Pipeline
        self.pipeline_group.update()
        self.pipeline_group.draw(self.screen)

        # 绘制路面精灵
        self.base_group.update()
        self.base_group.draw(self.screen)

        # 绘制主角 - 小鸟
        self.bird_group.update()
        self.bird_group.draw(self.screen)

        # 绘制数字
        self.score_group.update()
        self.score_group.draw(self.screen)

    def __handle_event(self):
        """事件监听"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over()
            elif event.type == CREATE_PIPELINE_EVENT:
                p = Pipeline()
                p1 = Pipeline(True, p.rect)
                self.pipeline_group.add(p, p1)

        # 使用键盘提供的方法获取键盘按键 - 按键元组
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_SPACE]:
            self.bird.speed = -2
        else:
            self.bird.speed = 2

    def __collide_check(self):
        """碰撞检测"""
        # 小鸟撞击管道
        bird_hit_pipeline = pygame.sprite.spritecollide(self.bird, self.pipeline_group, False)
        if bird_hit_pipeline:
            self.game_over()

        # 小鸟撞击地面
        bird_hit_base = pygame.sprite.spritecollide(self.bird, self.base_group, False)
        if bird_hit_base:
            self.game_over()

        # 得分
        for p in self.pipeline_group:
            if p.rect.x == self.bird.rect.x + self.bird.rect.width:
                self.flag = True
            if p.rect.x + p.rect.width < self.bird.rect.x and self.flag:
                self.score += 1
                self.is_score_changing = True
                self.flag = False

        #self.score += n
        if self.is_score_changing:
            self.score_group.empty()
            for i, s in enumerate(str(self.score)):
                if i == 0:
                    sc = Score(int(s), score=self.score)
                else:
                    sc = Score(int(s), is_first=False, score=self.score, pre_rect=sc.rect)
                self.score_group.add(sc)
            self.is_score_changing = False
    def start_game(self):
        while True:
            self.clock.tick(FRAME_PER_SECOND)

            # 事件监听
            self.__handle_event()
            # 碰撞检测
            self.__collide_check()
            # 更新绘制精灵、精灵组
            self.__update_sprite()
            # 显示精灵、精灵组
            pygame.display.update()

    @staticmethod
    def game_over():
        """游戏退出"""
        # 卸载游戏模块
        pygame.quit()

        # 退出程序
        exit()


def main():
    """游戏开始"""
    game = FlapyBirdGame()

    game.start_game()


if __name__ == '__main__':
    main()
