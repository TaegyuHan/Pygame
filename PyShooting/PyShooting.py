import pygame
import sys
import random
from time import sleep

padWidth = 480
padHeight = 640
rockImage = [
    "image/rock01.png",
    "image/rock02.png",
    "image/rock03.png",
    "image/rock04.png",
    "image/rock05.png",
    "image/rock06.png",
    "image/rock07.png",
    "image/rock08.png",
    "image/rock09.png",
    "image/rock10.png",
    "image/rock11.png",
    "image/rock12.png",
    "image/rock13.png",
    "image/rock14.png",
    "image/rock15.png",
    "image/rock16.png",
    "image/rock17.png",
    "image/rock18.png",
    "image/rock19.png",
    "image/rock20.png",
    "image/rock21.png",
    "image/rock22.png",
    "image/rock23.png",
    "image/rock24.png",
    "image/rock25.png",
    "image/rock26.png",
    "image/rock27.png",
    "image/rock28.png",
    "image/rock29.png",
    "image/rock30.png",
]

explosionSound = [
    "music/explosion01.wav",
    "music/explosion02.wav",
    "music/explosion03.wav",
    "music/explosion04.wav",
]


def writeScore(count):
    global gamePad
    font = pygame.font.Font("font/NanumGothic.ttf", 20)
    text = font.render("파괴한 운석 수: " + str(count), True, (255, 255, 255))
    gamePad.blit(text, (10, 0))


def writePassed(count):
    global gamePad
    font = pygame.font.Font("font/NanumGothic.ttf", 20)
    text = font.render("놓친 운석 수: " + str(count), True, (255, 0, 0))
    gamePad.blit(text, (350, 0))


# 게임 메시지 출력
def writeMessage(text):
    global gamePad, gameOverSound
    textfont = pygame.font.Font("font/NanumGothic.ttf", 60)
    text = textfont.render(text, True, (255, 0, 0))
    textpos = text.get_rect()
    textpos.center = (padWidth / 2, padHeight / 2)
    gamePad.blit(text, textpos)
    pygame.display.update()
    pygame.mixer.music.stop()
    gameOverSound.play()
    sleep(2)
    pygame.mixer.music.play(-1)
    runGame()


def crash():
    global gamePad
    writeMessage("전투기 파괴!")


def gameOver():
    global gamePad
    writeMessage("게임 오버!")


def drawObject(obj, x, y):
    global gamePad
    gamePad.blit(obj, (x, y))


def initGame():
    global gamePad, clock, background, fighter, missile, explosion, missileSound, gameOverSound
    pygame.init()
    gamePad = pygame.display.set_mode((padWidth, padHeight))
    pygame.display.set_caption("PyShooting")  # 게임 이름
    background = pygame.image.load("image/background.png")  # 배경 그림
    fighter = pygame.image.load("image/fighter.png")  # 전투기 그림
    missile = pygame.image.load("image/missile.png")  # 미사일 그림
    explosion = pygame.image.load("image/explosion.png")  # 폭발 그림
    pygame.mixer.music.load("music/music.wav")  # 배경음악
    pygame.mixer.music.play(-1)
    missileSound = pygame.mixer.Sound("music/missile.wav")
    gameOverSound = pygame.mixer.Sound("music/gameover.wav")
    clock = pygame.time.Clock()


def runGame():
    global gamePad, clock, background, fighter, missile, explosion, missileSound, gameOverSound

    # 무기 좌표 리스트
    missileXY = []

    # 운석 랜덤 생성
    rock = pygame.image.load(random.choice(rockImage))
    rockSize = rock.get_rect().size  # 운석크기
    rockWidth = rockSize[0]
    rockHeight = rockSize[1]
    destroySound = pygame.mixer.Sound(random.choice(explosionSound))

    # 운석 초기 위치 설정
    rockX = random.randrange(0, padWidth - rockWidth)
    rockY = 0
    rockSpeed = 2

    # 전투기 크기
    fighterSize = fighter.get_rect().size
    fighterWidth = fighterSize[0]
    fighterHeight = fighterSize[1]

    # 전투기 초기 위치
    x = padWidth * 0.45
    y = padHeight * 0.9
    fighterX = 0

    isShot = False
    shotCount = 0
    rockPassed = 0

    onGame = False
    while not onGame:
        for event in pygame.event.get():
            if event.type in [pygame.QUIT]:  # 게임 프로그램 종료
                pygame.quit()
                sys.exit()

            if event.type in [pygame.KEYDOWN]:
                if event.key == pygame.K_LEFT:  # 전투기 왼쪽으로 이동
                    fighterX -= 5

                elif event.key == pygame.K_RIGHT:  # 전투기 오른쪽으로 이동
                    fighterX += 5

                elif event.key == pygame.K_SPACE:  # 미사일 발사
                    missileSound.play()
                    missileX = x + fighterWidth / 2
                    missileY = y - fighterHeight
                    missileXY.append([missileX, missileY])

            if event.type in [pygame.KEYUP]:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    fighterX = 0

        drawObject(background, 0, 0)

        drawObject(fighter, x, y)

        # 미사일 발사 화면에 그리기
        if len(missileXY) != 0:
            for i, bxy in enumerate(missileXY):  # 미사일 요소에 대해 반복함
                bxy[1] -= 10  # 총알의 y좌표 -10 (위로 이동)
                missileXY[i][1] = bxy[1]

                # 미사일이 운석을 맞추었을 경우
                if bxy[1] < rockY:
                    if bxy[0] > rockX and bxy[0] + rockX + rockWidth:
                        missileXY.remove(bxy)
                        isShot = True
                        shotCount += 1

                if bxy[1] <= 0:  # 미사일이 화면 밖을 벗어나면
                    try:
                        missileXY.remove(bxy)  # 미사일 제거
                    except:
                        pass

        if len(missileXY) != 0:
            for bx, by in missileXY:
                drawObject(missile, bx, by)

        writeScore(shotCount)

        rockY += rockSpeed  # 운석 아래로 움직임

        # 운석이 지구로 떨어진 경우
        if rockY > padHeight:
            rock = pygame.image.load(random.choice(rockImage))
            rockSize = rock.get_rect().size
            rockWidth = rockSize[0]
            rockHeight = rockSize[1]
            rockX = random.randrange(0, padWidth - rockWidth)
            rockY = 0
            rockPassed += 1

        if rockPassed == 3:
            gameOver()

        writePassed(rockPassed)

        if isShot:
            drawObject(explosion, rockX, rockY)
            destroySound.play()

            rock = pygame.image.load(random.choice(rockImage))
            rockSize = rock.get_rect().size
            rockWidth = rockSize[0]
            rockHeight = rockSize[1]
            rockX = random.randrange(0, padWidth - rockWidth)
            rockY = 0
            destroySound = pygame.mixer.Sound(random.choice(explosionSound))
            isShot = False

            rockSpeed += 0.2
            if rockSpeed >= 10:
                rockSpeed = 10

        drawObject(rock, rockX, rockY)

        # 전투기 위치 재조정
        x += fighterX
        if x < 0:
            x = 0
        elif x > padWidth - fighterWidth:
            x = padWidth - fighterWidth

        # 전투기가 운석과 충돌했는지 체크
        if y < rockY + rockHeight:
            if (rockX > x and rockX < x + fighterWidth) or (
                rockX + rockWidth > x and rockX + rockWidth < x + fighterWidth
            ):
                crash()

        pygame.display.update()  # 게임화면을 다시 그림

        clock.tick(60)

    pygame.quit()


initGame()
runGame()
