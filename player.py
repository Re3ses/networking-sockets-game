import pygame

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

    def increase_vel(self):
        self.velocity += .5

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