import random
import pygame
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
        self.difficulty = 2
        self.net = Network()
        self.playerId = int(self.net.id)
        self.width = w
        self.height = h
        if (int(self.net.id) == 0):
            self.player = Player(0, 0, id=self.playerId) # Player 1 is blue
            self.player2 = Player(0, 300, id=1-self.playerId) # Player 2 is red
        else:
            self.player = Player(0, 300, id=self.playerId) # Player 1 is blue
            self.player2 = Player(0, 0, id=1-self.playerId) # Player 2 is red 
        
        self.obstacles = []
        for i in range(self.difficulty):
            y = random.randint(100, self.height)
            self.obstacles.append(Obstacle(400, y))


        self.canvas = Canvas(self.width, self.height, "You are " + ("blue" if self.playerId == 0 else "red") )

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
            self.player2.x, self.player2.y = self.parse_data(self.send_data())

           
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
        data = str(self.net.id) + ":" + str(self.player.x) + "," + str(self.player.y)
        reply = self.net.send(data)
        return reply

    @staticmethod
    def parse_data(data):
        try:
            d = data.split(":")[1].split(",")
            return int(d[0]), int(d[1])
        except:
            return 0,0


class Canvas:

    def __init__(self, w, h, name="None"):
        self.width = w
        self.height = h
        self.screen = pygame.display.set_mode((w,h))
        pygame.display.set_caption(name)

    @staticmethod
    def update():
        pygame.display.update()

    # def draw_text(self, text, size, x, y):
    #     pygame.font.init()
    #     font = pygame.font.SysFont("comicsans", size)
    #     render = font.render(text, 1, (0,0,0))

    #     self.screen.draw(render, (x,y))

    def get_canvas(self):
        return self.screen

    def draw_background(self):
        self.screen.fill((255,255,255))
