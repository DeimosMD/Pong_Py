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
isUpPressed = False
isDownPressed = False
isWPressed = False
isSPressed = False
score1 = 0
score2 = 0
loops = 0
loopsSinceScore = 9999
fontSize = 250
fontSize2 = 100
font = pygame.font.SysFont('pixeloidsans', fontSize)
font2 = pygame.font.SysFont('pixeloidsans', fontSize2)
gameOver = False
currentServer = round(random.randint(1,2))
serverServes = 0

class Ball:

        x = paddleWidth+50
        y = canvasHeight/2 + paddleHeight/2
        velocityX = 5
        velocityY = 0
        color = (round(random.randint(80,255)),round(random.randint(80,255)),round(random.randint(80,255)))
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
                        Ball.color = (round(random.randint(80,255)),round(random.randint(80,255)),round(random.randint(80,255)))
                if Ball.y <= 0:
                        Ball.velocityY *= -1
                        Ball.color = (round(random.randint(80,255)),round(random.randint(80,255)),round(random.randint(80,255)))
                if Paddle1.x + paddleWidth > Ball.x > Paddle1.x - ballWidth and Paddle1.y - ballHeight <= Ball.y <= Paddle1.y + paddleHeight:
                        Ball.velocityX *= -1
                        Ball.velocityY += Paddle1.velocityY
                        Ball.x = Paddle1.x + paddleWidth
                if Paddle2.x - ballWidth < Ball.x < Paddle2.x + paddleWidth and Paddle2.y - ballHeight <= Ball.y <= Paddle2.y + paddleHeight:
                        Ball.velocityX *= -1
                        Ball.velocityY += Paddle2.velocityY
                        Ball.x = Paddle2.x-ballWidth

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

class Paddle1:

        x = 50
        y = canvasHeight/2
        velocityY = 0

        @staticmethod
        def Update():
                if isWPressed:
                        Paddle1.velocityY -= paddleAcceleration
                if isSPressed:
                        Paddle1.velocityY += paddleAcceleration
                Paddle1.velocityY *= 1 - paddleProportionalDeceleration
                Paddle1.y += Paddle1.velocityY
                if Paddle1.y < 0:
                        Paddle1.y = 0
                if Paddle1.y > canvasHeight - paddleHeight:
                        Paddle1.y = canvasHeight - paddleHeight
                pygame.draw.rect(canvas, (255,255,255), pygame.Rect(Paddle1.x, Paddle1.y, paddleWidth, paddleHeight))

class Paddle2:

        x = canvasWidth - 50
        y = canvasHeight/2
        velocityY = 0

        @staticmethod
        def Update():
                if isUpPressed:
                        Paddle2.velocityY -= paddleAcceleration
                if isDownPressed:
                        Paddle2.velocityY += paddleAcceleration
                Paddle2.velocityY *= 1 - paddleProportionalDeceleration
                Paddle2.y += Paddle2.velocityY
                if Paddle2.y < 0:
                        Paddle2.y = 0
                if Paddle2.y > canvasHeight - paddleHeight:
                        Paddle2.y = canvasHeight - paddleHeight
                pygame.draw.rect(canvas, (255,255,255), pygame.Rect(Paddle2.x, Paddle2.y, paddleWidth, paddleHeight))

def updateScoring():
        global loopsSinceScore
        global gameOver
        global currentServer
        global serverServes
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
        if loopsSinceScore < 600 or gameOver == True:
                scoreText = font.render(str(score1)+" - "+str(score2), True, (255,255,255))
                canvas.blit(scoreText, (canvasWidth/2-fontSize-75, canvasHeight/2-fontSize+75))
                if not gameOver:
                        startTimerText = font2.render(str(math.ceil(5 - loopsSinceScore / 120)), True, (255, 255, 255))
                        canvas.blit(startTimerText, (canvasWidth / 2 - 25, canvasHeight / 2 + 200))
                        if currentServer == 1:
                            Ball.x = Paddle1.x + paddleWidth
                            Ball.y = Paddle1.y + paddleHeight/2
                            Ball.velocityY = Paddle1.velocityY
                        else:
                            Ball.x = Paddle2.x - ballWidth
                            Ball.y = Paddle2.y + paddleHeight/2
                            Ball.velocityY = Paddle2.velocityY

while not exit: 
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        exit = True
                if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                                isUpPressed = True
                        if event.key == pygame.K_DOWN:
                                isDownPressed = True
                        if event.key == pygame.K_w:
                                isWPressed = True
                        if event.key == pygame.K_s:
                                isSPressed = True
                if event.type == pygame.KEYUP:
                        if event.key == pygame.K_UP:
                                isUpPressed = False
                        if event.key == pygame.K_DOWN:
                                isDownPressed = False
                        if event.key == pygame.K_w:
                                isWPressed = False
                        if event.key == pygame.K_s:
                                isSPressed = False

        canvas.fill((0,0,0))
        Paddle1.Update()
        Paddle2.Update()
        Ball.Update()
        if loops < 1200:
                timerText = font.render(str(math.ceil(10-loops/120)), True, (255,255,255))
                canvas.blit(timerText, (canvasWidth/2-50, canvasHeight/2-fontSize+75))
                if currentServer == 1:
                    Ball.x = Paddle1.x + paddleWidth
                    Ball.y = Paddle1.y + paddleHeight/2
                    Ball.velocityY = Paddle1.velocityY
                else:
                    Ball.x = Paddle2.x - ballWidth
                    Ball.y = Paddle2.y + paddleHeight/2
                    Ball.velocityY = Paddle2.velocityY
        else:
                updateScoring()
        loops+=1
        pygame.display.update()
