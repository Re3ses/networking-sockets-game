import pygame

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