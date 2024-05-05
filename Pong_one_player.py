import pygame 
import random
import math
pygame.init() 
canvasWidth = 1920
canvasHeight = 1080
ballWidth = 20
ballHeight = 20
paddleWidth = 30
paddleHeight = 300
paddleAcceleration = 1
paddleProportionalDeceleration = 0.2
canvas = pygame.display.set_mode((canvasWidth, canvasHeight)) 
pygame.display.set_caption("My Board")
exit = False
isWPressed = False
isSPressed = False
score1 = 0
score2 = 0
loops = 0
loopsSinceScore = 9999
loopsToRestAfterScore = 600
loopsToRestAtStart = 1200
fontSize = 250
fontSize2 = 100
font = pygame.font.SysFont('pixeloidsans', fontSize)
font2 = pygame.font.SysFont('pixeloidsans', fontSize2)
gameOver = False
currentServer = random.randint(1,2)
serverServes = 0
inPlay = False
botAccuracy = 35

class Ball:

        x = paddleWidth+50
        y = canvasHeight/2 + paddleHeight/2
        velocityX = 5
        velocityY = 0
        color = (random.randint(80,255),random.randint(80,255),random.randint(80,255))
        isLost = False

        @staticmethod
        def Update():
                global score1
                global score2
                global loopsSinceScore
                global gameOver

                Ball.x+=Ball.velocityX
                Ball.y+=Ball.velocityY

                if Ball.y + ballHeight >= canvasHeight:
                        Ball.velocityY *= -1
                        Ball.color = (random.randint(80,255),random.randint(80,255),random.randint(80,255))
                if Ball.y <= 0:
                        Ball.velocityY *= -1
                        Ball.color = (random.randint(80,255),random.randint(80,255),random.randint(80,255))
                if PlayerPaddle.x+paddleWidth > Ball.x > PlayerPaddle.x-ballWidth and PlayerPaddle.y-ballHeight <= Ball.y <= PlayerPaddle.y+paddleHeight:
                        Ball.velocityX *= -1
                        Ball.velocityY += PlayerPaddle.velocityY
                        Ball.x = PlayerPaddle.x + paddleWidth
                if BotPaddle.x-ballWidth < Ball.x < BotPaddle.x+paddleWidth and BotPaddle.y-ballHeight <= Ball.y <= BotPaddle.y+paddleHeight:
                        Ball.velocityX *= -1
                        Ball.velocityY += BotPaddle.velocityY
                        Ball.x = BotPaddle.x - ballWidth

                if Ball.x < 0 and Ball.isLost == False and gameOver == False:
                        Ball.isLost = True
                        score2 += 1
                        loopsSinceScore = 0
                        print(str(score1)+" - "+str(score2))
                if Ball.x > canvasWidth and Ball.isLost == False and gameOver == False:
                        Ball.isLost = True
                        score1 += 1
                        loopsSinceScore = 0
                        print(str(score1)+" - "+str(score2))

                pygame.draw.rect(canvas, Ball.color, pygame.Rect(Ball.x, Ball.y, ballWidth, ballHeight))

class PlayerPaddle:

        x = 50
        y = canvasHeight/2
        velocityY = 0

        @staticmethod
        def Update():
                if isWPressed:
                        PlayerPaddle.velocityY -= paddleAcceleration
                if isSPressed:
                        PlayerPaddle.velocityY += paddleAcceleration
                PlayerPaddle.velocityY *= 1 - paddleProportionalDeceleration
                PlayerPaddle.y += PlayerPaddle.velocityY
                if PlayerPaddle.y < 0:
                        PlayerPaddle.y = 0
                if PlayerPaddle.y > canvasHeight - paddleHeight:
                        PlayerPaddle.y = canvasHeight - paddleHeight
                pygame.draw.rect(canvas, (255,255,255), pygame.Rect(PlayerPaddle.x, PlayerPaddle.y, paddleWidth, paddleHeight))

class BotPaddle:

        x = canvasWidth - 50
        y = canvasHeight/2
        velocityY = 0

        # bot specific fields
        directionGoing = 0

        @staticmethod
        def Update():
                if inPlay:
                        if Ball.velocityX < 0:
                                BotPaddle.directionGoing = 0
                        if random.randint(0, abs(BotPaddle.x - Ball.x)) < botAccuracy:
                                BotPaddle.directionGoing = BotPaddle.getDirectionToBall()
                        if BotPaddle.x - (Ball.x + ballWidth) < 50:
                                if Ball.velocityY == 0:
                                        BotPaddle.directionGoing = random.randint(-1, 1)
                                else:
                                        BotPaddle.directionGoing = -Ball.velocityY/abs(Ball.velocityY)
                elif currentServer == 2:
                        if loops <= loopsToRestAtStart:
                                if random.randint(0, loopsToRestAtStart - loops) == 0:
                                        dir = random.randint(0, 1)
                                        if dir == 0:
                                                dir = -1
                                        BotPaddle.directionGoing = dir
                        else:
                                if random.randint(0, loopsToRestAfterScore - loopsSinceScore) == 0:
                                        dir = random.randint(0, 1)
                                        if dir == 0:
                                                dir = -1
                                        BotPaddle.directionGoing = dir
                BotPaddle.goDirection(BotPaddle.directionGoing)
                BotPaddle.velocityY *= 1 - paddleProportionalDeceleration
                BotPaddle.y += BotPaddle.velocityY
                if BotPaddle.y < 0:
                        BotPaddle.y = 0
                if BotPaddle.y > canvasHeight - paddleHeight:
                        BotPaddle.y = canvasHeight - paddleHeight
                pygame.draw.rect(canvas, (255,255,255), pygame.Rect(BotPaddle.x, BotPaddle.y, paddleWidth, paddleHeight))

        @staticmethod
        def getDirectionToBall() -> int:
                if BotPaddle.y + paddleHeight/2 > Ball.y + ballHeight/2:
                        return 1
                if BotPaddle.y + paddleHeight/2 < Ball.y + ballHeight/2:
                        return -1
                return 0

        @staticmethod
        def goDirection(d: int):
                if d == 1:
                        BotPaddle.velocityY -= paddleAcceleration
                elif d == -1:
                        BotPaddle.velocityY += paddleAcceleration


def updateScoring():
        global loopsSinceScore
        global gameOver
        global currentServer
        global serverServes
        global inPlay
        loopsSinceScore+=1
        if score1 >= 11 or score2 >= 11:
                if abs(score1 - score2) >= 2:
                        gameOver = True
        if Ball.isLost:
                Ball.isLost = False
                Ball.color = (round(random.randint(80,255)),round(random.randint(80,255)),round(random.randint(80,255)))
                if serverServes > 0:
                    serverServes = 0
                    if currentServer == 1:
                        currentServer = 2
                    else:
                        currentServer = 1
                else:
                    serverServes += 1
        if loopsSinceScore < loopsToRestAfterScore or gameOver == True:
                scoreText = font.render(str(score1)+" - "+str(score2), True, (255,255,255))
                canvas.blit(scoreText, (canvasWidth/2-fontSize-75, canvasHeight/2-fontSize+75))
                if not gameOver:
                        startTimerText = font2.render(str(math.ceil(5 - loopsSinceScore / 120)), True, (255, 255, 255))
                        canvas.blit(startTimerText, (canvasWidth / 2 - 25, canvasHeight / 2 + 200))
                        if currentServer == 1:
                            Ball.x = PlayerPaddle.x + paddleWidth
                            Ball.y = PlayerPaddle.y + paddleHeight / 2
                            Ball.velocityY = PlayerPaddle.velocityY
                        else:
                            Ball.x = BotPaddle.x - ballWidth
                            Ball.y = BotPaddle.y + paddleHeight / 2
                            Ball.velocityY = BotPaddle.velocityY
                if loopsToRestAfterScore-loopsSinceScore < 5:
                        inPlay = True
                else:
                        inPlay = False
        else:
                inPlay = True

while not exit: 
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        exit = True
                if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_w:
                                isWPressed = True
                        if event.key == pygame.K_s:
                                isSPressed = True
                if event.type == pygame.KEYUP:
                        if event.key == pygame.K_w:
                                isWPressed = False
                        if event.key == pygame.K_s:
                                isSPressed = False

        canvas.fill((0,0,0))
        PlayerPaddle.Update()
        BotPaddle.Update()
        Ball.Update()
        if loops < loopsToRestAtStart:
                timerText = font.render(str(math.ceil(10-loops/120)), True, (255,255,255))
                canvas.blit(timerText, (canvasWidth/2-50, canvasHeight/2-fontSize+75))
                if currentServer == 1:
                    Ball.x = PlayerPaddle.x + paddleWidth
                    Ball.y = PlayerPaddle.y + paddleHeight / 2
                    Ball.velocityY = PlayerPaddle.velocityY
                else:
                    Ball.x = BotPaddle.x - ballWidth
                    Ball.y = BotPaddle.y + paddleHeight / 2
                    Ball.velocityY = BotPaddle.velocityY
        else:
                updateScoring()
        loops+=1
        pygame.display.update()
