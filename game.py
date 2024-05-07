import random
import pygame
pygame.init()
import sys
from network import Network


class Player():
    width = height = 40

    def __init__(self, startx, starty, color=(0,0,255), id=0):
        self.x = startx
        self.y = starty
        self.velocity = 2
        self.color = color if id == 0 else (255,0,0)

    def draw(self, g):
        pygame.draw.rect(g, self.color ,(self.x, self.y, self.width, self.height), 0)

    def move(self, dirn):
        """
        :param dirn: 0 or 1 (up, down)
        :return: None
        """

        if dirn == 0:
            self.y -= self.velocity
        else:
            self.y += self.velocity

class Obstacle():
    width = height = 20

    def __init__(self, startx, starty, color=(0,0,0)):
        self.x = startx
        self.y = starty
        self.velocity = 5
        self.color = color

    def draw(self, g):
        pygame.draw.rect(g, self.color ,(self.x, self.y, self.width, self.height), 0)

    def move(self):
        self.x -= self.velocity


class Game:

    def __init__(self, w, h):
        self.net = Network()
        self.obstacleCount = 2
        self.seed = 0
        self.playerId = int(self.net.id)
        self.playerReady = 0
        self.opponentReady = 0
        self.width = w
        self.height = h
        if (int(self.net.id) == 0):
            self.player = Player(0, 0, id=self.playerId) # Player 1 is blue
            self.player2 = Player(0, 300, id=1-self.playerId) # Player 2 is red
        else:
            self.player = Player(0, 300, id=self.playerId) # Player 1 is blue
            self.player2 = Player(0, 0, id=1-self.playerId) # Player 2 is red 
        
        self.obstacles = []
        for i in range(self.obstacleCount):
            y = random.randint(100, self.height)
            # print("rand y: " + y)
            self.obstacles.append(Obstacle(400, y))

        self.canvas = Canvas(self.width, self.height, "You are " + ("blue" if self.playerId == 0 else "red") )

    def start(self, run=True):
        buttonW, buttonH = 100, 50

        clock = pygame.time.Clock()
        while run:
            clock.tick(60)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                # check if button is pressed    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.width/2 <= mouse[0] <= self.width/2+buttonW and self.height/2 <= mouse[1] <= self.height/2+buttonH: 
                        self.playerReady = 1
                        print(self.playerReady)
                        
            # get mouse position
            mouse = pygame.mouse.get_pos()

            # draw white background
            self.canvas.draw_background()

            # draw mouse position at top corner of screen
            self.canvas.draw_text(str(mouse), 10, 0, 0)

            # check if player is ready
            if self.playerReady == 0:
                # check if player is hovering on the button, if so change color
                if self.width/2 <= mouse[0] <= self.width/2+buttonW and self.height/2 <= mouse[1] <= self.height/2+buttonH: 
                    pygame.draw.rect(self.canvas.get_canvas(), (170, 170, 170), [self.width/2, self.height/2, buttonW, buttonH], 0) 
                else: 
                    pygame.draw.rect(self.canvas.get_canvas(), (100, 100, 100), [self.width/2, self.height/2, buttonW, buttonH], 0) 
                self.canvas.draw_text("start", 35, self.width/2 + 10, self.height/2)
            else:
                # remove button and darken background
                self.canvas.draw_background((200, 200, 200))
                # display waiting for opponent
                self.canvas.draw_text("waiting for opponent...", 20, self.width/2 - 100, self.height/2)
                
            # send network stuff
            self.opponentReady, x, y = self.parse_data(self.send_data()) 

            if self.opponentReady == 1 and self.playerReady == 1:
                run = False
                self.run()

            # update canvas  
            self.canvas.update()

    def run(self):
        clock = pygame.time.Clock()
        run = True
        
        while run:
            clock.tick(60)
            print(len(self.obstacles))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.K_ESCAPE:
                    run = False

            keys = pygame.key.get_pressed()


            if keys[pygame.K_UP]:
                if self.player.y >= self.player.velocity:
                    self.player.move(0)

            if keys[pygame.K_DOWN]:
                if self.player.y <= self.height - self.player.velocity:
                    self.player.move(1)

            # Send Network Stuff
            self.opponentReady, self.player2.x, self.player2.y = self.parse_data(self.send_data())

           
            # Update Canvas
            self.canvas.draw_background()

            # Move obstacles
            for obstacle in self.obstacles:
                obstacle.move()

            # Draw obstacles
            for obstacle in self.obstacles:
                obstacle.draw(self.canvas.get_canvas())

            self.player.draw(self.canvas.get_canvas())
            self.player2.draw(self.canvas.get_canvas())
            self.canvas.update()

        pygame.quit()

    def send_data(self):
        """
        Send position to server
        :return: None
        """
        data = str(self.net.id) + "," + str(self.playerReady) + "-" + str(self.seed) + ":" + str(self.player.x) + "," + str(self.player.y)
        reply = self.net.send(data)
        return reply

    @staticmethod
    def parse_data(data):
        try:
            pos = data.split(":")[1].split(",")
            r = data.split(":")[0].split(",")
            return int(r, pos[0]), int(pos[1])
        except:
            return 0,0,0


class Canvas:

    def __init__(self, w, h, name="None"):
        self.width = w
        self.height = h
        self.screen = pygame.display.set_mode((w,h))
        pygame.display.set_caption(name)

    @staticmethod
    def update():
        pygame.display.update()

    def draw_text(self, text, size, x, y):
        pygame.font.init()
        font = pygame.font.SysFont("comicsans", size)
        render = font.render(text, 1, (0,0,0))

        self.screen.blit(render, (x,y))

    def get_canvas(self):
        return self.screen

    def draw_background(self, color=(255, 255, 255)):
        self.screen.fill(color)
