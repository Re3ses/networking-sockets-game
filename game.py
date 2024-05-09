import math
import random
import pygame
pygame.init()
import sys
from network import Network

random.seed(10)

class Player():
    width = height = 40

    def __init__(self, startx=10, starty=10, color=(0,0,255), id=0):
        self.id = id
        self.x = startx
        self.y = starty if id == 0 else 300 + 10
        self.velocity = 2
        self.color = color if id == 0 else (255,0,0)

        self.playerRect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update_pos(self, x, y):
        self.x = x
        self.y = y
        self.update_player_rect()

    def get_player_rect(self):
        return self.playerRect
    
    def update_player_rect(self):
        self.playerRect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color , self.playerRect)

    def move(self, dirn):
        """
        :param dirn: 0 or 1 (up, down)
        :return: None
        """
        if dirn == 0:
            self.y -= self.velocity
        else:
            self.y += self.velocity

        self.update_player_rect()

class Obstacle():
    width = height = 20

    def __init__(self, startx=600, starty=0, distance_to_next=300, color=(0,0,0)):
        self.x = startx + distance_to_next
        self.y = starty
        self.velocity = 2
        self.color = color
        self.rect1 = pygame.Rect(self.x, self.y, self.width, self.height)
        self.rect2 = pygame.Rect(self.x, self.y+300, self.width, self.height)

    def get_pos(self):
        return self.x, self.y
    
    def get_rect1(self):
        return self.rect1
    
    def get_rect2(self):
        return self.rect2
    
    def get_rects(self):
        return self.rect1, self.rect2
    
    def update_pos(self, x, y):
        self.x = x
        self.y = y
        self.update_rects()

    def update_rects(self):
        self.rect1 = pygame.Rect(self.x, self.y, self.width, self.height)
        self.rect2 = pygame.Rect(self.x, self.y+300, self.width, self.height)
    
    def draw(self, surface):
        """
        Draw the obstacle twice on the screen
        """
        pygame.draw.rect(surface, self.color , self.rect1)
        pygame.draw.rect(surface, self.color , self.rect2)

    def move(self):
        # start moving to the right
        self.x -= self.velocity
        self.update_rects()

class ObstacleList():

    def __init__(self, surface, w, h):
        self.width = w
        self.height = h
        self.surface = surface
        self.obstacles = []
        self.generate_obstacle()
    
    def get_obstacles(self):
        return self.obstacles

    def generate_obstacle(self):
        y = random.randint(10, ((self.height // 2) - 20) )
        self.obstacles.append(Obstacle(starty=y))
    
    def get_obstacle_rects(self):
        obstacleRects = []
        for obs in self.obstacles:
            obstacleRects.extend(obs.get_rects())
        return obstacleRects

    def delete_out_of_bounds(self):
        if self.obstacles[0].get_pos()[0] < 0 - 20:
            self.obstacles = self.obstacles[1:]

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
        self.selfReady = 0
        self.opponentReady = 0
        self.game_winner = None
        self.width = w
        self.height = h
        if (int(self.net.id) == 0):
            self.player = Player(id=self.playerId) # Player 1 is blue
            self.opponent = Player(id=1-self.playerId) # Player 2 is red
        else:
            self.player = Player(id=self.playerId) # Player 1 is blue
            self.opponent = Player(id=1-self.playerId) # Player 2 is red 
        
        self.canvas = Canvas(self.width, self.height, "You are " + ("blue" if self.playerId == 0 else "red") )
        self.obstacles = ObstacleList(self.canvas.get_canvas(), self.width, self.height)

    def start_screen(self):
        print("running start_screen()")
        buttonW, buttonH = 100, 50
        run = True

        clock = pygame.time.Clock()
        print("player ready: " + str(self.selfReady) + " opponent ready: " + str(self.opponentReady))
        while run:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                # check if button is pressed    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.width/2 <= mouse[0] <= self.width/2+buttonW and self.height/2 <= mouse[1] <= self.height/2+buttonH: 
                        self.selfReady = 1
                        print(self.selfReady)
                        
            # get mouse position
            mouse = pygame.mouse.get_pos()

            # draw white background
            self.canvas.draw_background()

            # draw mouse position at top corner of screen
            self.canvas.draw_text(str(mouse), 10, 0, 0)

            # check if player is ready
            if self.selfReady == 0:
                # check if player is hovering on the button, if so change color
                if self.width/2 <= mouse[0] <= self.width/2+buttonW and self.height/2 <= mouse[1] <= self.height/2+buttonH: 
                    pygame.draw.rect(self.canvas.get_canvas(), (170, 170, 170), [self.width/2, self.height/2, buttonW, buttonH], 0) 
                else: 
                    pygame.draw.rect(self.canvas.get_canvas(), (100, 100, 100), [self.width/2, self.height/2, buttonW, buttonH], 0) 
                self.canvas.draw_text("start", 35, self.width/2 + 10, self.height/2)
            else:
                print("player ready")
                # remove button and darken background
                self.canvas.draw_background((200, 200, 200))
                # display waiting for opponent
                self.canvas.draw_text("waiting for opponent...", 20, self.width/2 - 100, self.height/2)
                                
            # send network stuff
            self.opponentReady, x, y = self.parse_game_state(self.send_game_state(), self.playerId) 

            if self.opponentReady == 1 and self.selfReady == 1:
                print("both ready")
                run = False

            # update canvas  
            self.canvas.update()
        print("returning to run()")
        return

    def run(self):
        print("running run()")
        clock = pygame.time.Clock()
        start = False

        if not start:
            self.start_screen()
            start = True

        while start:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    start = False

                if event.type == pygame.K_ESCAPE:
                    start = False

            keys = pygame.key.get_pressed()

            if keys[pygame.K_UP]:
                print("pressed up")
                if self.player.y >= self.player.velocity:
                    if self.playerId == 0 and self.player.y >= 10 + self.player.velocity:
                        self.player.move(0)
                    elif self.playerId == 1 and self.player.y >= self.height//2 + 10 + self.player.velocity:
                        self.player.move(0)

            if keys[pygame.K_DOWN]:
                print("pressed down")
                if self.player.y <= (self.height - 40) - self.player.velocity:
                    if self.playerId == 0 and self.player.y <= self.height//2 - 40 - 10 - self.player.velocity:
                        self.player.move(1)
                    elif self.playerId == 1 and self.player.y <= 600 - 40 - 10 - self.player.velocity:
                        self.player.move(1)

            tempx = tempy = 0
            # Send Network Stuff
            self.opponentReady, tempx, tempy = self.parse_game_state(self.send_game_state(), self.playerId)
            self.opponent.update_pos(tempx, tempy)

            # generate obstacles
            if self.obstacles.get_obstacles()[-1].get_pos()[0] < 300:
                self.obstacles.generate_obstacle()
            
            # Update Canvas
            self.canvas.draw_background()
            # Draw line
            self.canvas.draw_line()

            # move obstacles
            self.obstacles.animate_obstacles()  

            # check for collision
            if self.check_for_collision() == 1:
                print("Player 1 collided with obstacle")
                self.lose_screen()
                start = False
            if self.check_for_collision() == 2:
                print("Player 2 collided with obstacle")
                self.win_screen()
                start = False

            # check if first obstacle is out of bounds
            self.obstacles.delete_out_of_bounds()
            
            self.player.draw(self.canvas.get_canvas())
            self.opponent.draw(self.canvas.get_canvas())
            self.canvas.update()
        pygame.quit()
        
    def check_for_collision(self):
        """
        Check for collision between players and obstacles.
        Returns:
            int: 1 if player 1 collides with an obstacle, 2 if player 2 collides with an obstacle, 0 otherwise.
        """
        # Get the obstacle rectangles
        rects = self.obstacles.get_obstacle_rects()
        # Get the player rectangles
        selfRect = self.player.get_player_rect()
        opponentRect = self.opponent.get_player_rect()

        # Check if player 1 collides with any obstacle
        if selfRect.collidelist(rects) > -1:
            return 1
        # Check if player 2 collides with any obstacle
        elif opponentRect.collidelist(rects) > -1:
            return 2
        # No collision
        else:
            return 0

    def send_game_state(self):
        """
        Send position to server
        :return: None
        """
        data = str(self.net.id) + "," + str(self.selfReady) + "-" + str(self.seed) + ":" + str(self.player.x) + "," + str(self.player.y)
        reply = self.net.send(data)
        return reply

    @staticmethod
    def parse_game_state(data, id):
        if data:
            pos = data.split(":")[1].split(",")
            ready = data.split(":")[0].split(",")[1].split("-")
            return int(ready[0]), int(pos[0]), int(pos[1])
        else:   
            print("failed to parse data")
            return 0,0,0 
        
    def win_screen(self):
        print("running win_screen()")
        run = True
        clock = pygame.time.Clock()
        while run:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            self.canvas.draw_background()
            self.canvas.draw_text("You Win!", 50, self.width//2 - 50, self.height//2)
            self.canvas.update()
        pygame.quit()

    def lose_screen(self):
        print("running lose_screen()")
        run = True
        clock = pygame.time.Clock()
        while run:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            self.canvas.draw_background()
            self.canvas.draw_text("You Lose!", 50, self.width//2 - 50, self.height//2)
            self.canvas.update()
        pygame.quit()


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
