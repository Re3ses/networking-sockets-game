import math
import random
import pygame
pygame.init()
import sys
from network import Network


class Player():
    width = height = 40

    def __init__(self, startx=10, starty=10, color=(0,0,255), id=0):
        self.id = id
        self.x = startx
        self.y = starty if id == 0 else 300 + 10
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

    def __init__(self, startx, starty, distance_to_next=700, color=(0,0,0)):
        self.x = startx + distance_to_next
        self.y = starty
        self.velocity = 2
        self.color = color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color ,(self.x, self.y, self.width, self.height), 0)

    def move(self):
        # start moving to the right
        self.x -= self.velocity

class ObstacleList():

    def __init__(self, obstacle_count, surface, w, h):
        self.width = w
        self.height = h
        self.surface = surface
        self.obstacles = []
        self.obstacle_count = obstacle_count

        for i in range(obstacle_count):
            random.seed(i)
            y = random.randint(10, (self.height // 2) - 10 )
            x = random.randint(10, self.width)
            # print("rand y: " + y)
            self.obstacles.append(Obstacle(700, y, x))

    def animate_obstacles(self):
        for obs in self.obstacles:
            # draw 
            obs.draw(self.surface)
            # move
            obs.move()
            


class Game:

    def __init__(self, w, h):
        self.net = Network()
        self.obstacleCount = 5
        self.seed = 0
        self.playerId = int(self.net.id)
        self.playerReady = 0
        self.opponentReady = 0
        self.width = w
        self.height = h
        if (int(self.net.id) == 0):
            self.player = Player(id=self.playerId) # Player 1 is blue
            self.player2 = Player(id=1-self.playerId) # Player 2 is red
        else:
            self.player = Player(id=self.playerId) # Player 1 is blue
            self.player2 = Player(id=1-self.playerId) # Player 2 is red 
        
        self.canvas = Canvas(self.width, self.height, "You are " + ("blue" if self.playerId == 0 else "red") )
        self.obstacles = ObstacleList(self.obstacleCount, self.canvas.get_canvas(), self.width, self.height)

    def start_screen(self):
        buttonW, buttonH = 100, 50
        run = True

        clock = pygame.time.Clock()
        while run:
            print("running start_screen()")
            clock.tick(60)
            print("player ready: " + str(self.playerReady) + " opponent ready: " + str(self.opponentReady))

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
            self.opponentReady, x, y = self.parse_data(self.send_data(), self.playerId) 

            if self.opponentReady == 1 and self.playerReady == 1:
                print("both ready")
                run = False

            # update canvas  
            self.canvas.update()
        print("returning to run()")
        return

    def run(self):
        clock = pygame.time.Clock()
        start = False

        if not start:
            self.start_screen()
            start = True

        while start:
            print("running run()")
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    start = False

                if event.type == pygame.K_ESCAPE:
                    start = False

            keys = pygame.key.get_pressed()

            if keys[pygame.K_UP]:
                if self.player.y >= self.player.velocity:
                    if self.playerId == 0 and self.player.y >= 10 + self.player.velocity:
                        self.player.move(0)
                    elif self.playerId == 1 and self.player.y >= self.height//2 + 10 + self.player.velocity:
                        self.player.move(0)

            if keys[pygame.K_DOWN]:
                if self.player.y <= (self.height - 40) - self.player.velocity:
                    if self.playerId == 0 and self.player.y <= self.height//2 - 40 - 10 - self.player.velocity:
                        self.player.move(1)
                    elif self.playerId == 1 and self.player.y <= 600 - 40 - 10 - self.player.velocity:
                        self.player.move(1)

            # Send Network Stuff
            self.opponentReady, self.player2.x, self.player2.y = self.parse_data(self.send_data(), self.playerId)

            # generate obstacles
            self.obstacles = ObstacleList(self.obstacleCount, self.canvas.get_canvas(), self.width, self.height)
            
            # Update Canvas
            self.canvas.draw_background()
            # Draw line
            self.canvas.draw_line()

            # move obstacles
            self.obstacles.animate_obstacles()

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
    def parse_data(data, id):
        if data:
            pos = data.split(":")[1].split(",")
            ready = data.split(":")[0].split(",")[1].split("-")
            return int(ready[0]), int(pos[0]), int(pos[1])
        else:   
            print("failed to parse data")
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

    def draw_line(self, color=(0,0,0), start=(0, 300), end=(600, 300), width=3):
        pygame.draw.line(self.screen, color, start, end, width)

    def draw_text(self, text, size, x, y):
        pygame.font.init()
        font = pygame.font.SysFont("comicsans", size)
        render = font.render(text, 1, (0,0,0))

        self.screen.blit(render, (x,y))

    def get_canvas(self):
        return self.screen

    def draw_background(self, color=(255, 255, 255)):
        self.screen.fill(color)
