import random

import pygame


def main():
    pygame.init()

    bg = pygame.image.load("./images/background-day.png")
    bg_rect = bg.get_rect()
    screen = pygame.display.set_mode(bg_rect.size)

    pipeline = pygame.image.load("./images/pipe-green.png")

    screen.blit(bg, (0, 0))
    screen.blit(pipeline, (288, 0))
    # 初始化时钟对象
    clock = pygame.time.Clock()

    pipeline_rect = pipeline.get_rect()
    pipeline_rect.x = 288
    pipeline_rect.y = bg_rect.height - random.randint(int(pipeline_rect.height * 1 / 4), int(pipeline_rect.height * 9/10))

    # t_pipeline = pipeline
    t_pipeline = pygame.transform.rotate(pipeline, 180)
    screen.blit(t_pipeline, (288, 0))
    t_pipeline_rect = t_pipeline.get_rect()
    t_pipeline_rect.x = 288
    t_pipeline_rect.y = pipeline_rect.y - 150 - t_pipeline_rect.height
    while True:

        # 设置时钟频率
        clock.tick(60)

        pipeline_rect.x -= 1
        t_pipeline_rect.x -= 1
        if pipeline_rect.x < - pipeline_rect.width:
            pipeline_rect.x = bg_rect.width
            t_pipeline_rect.x = bg_rect.width
        screen.blit(bg, bg_rect)

        screen.blit(pipeline, pipeline_rect)
        screen.blit(t_pipeline, t_pipeline_rect)
        print(pipeline_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("退出游戏")
                pygame.quit()
                exit()


if __name__ == '__main__':
    main()
