import pygame
from random import randint

class CherryRush:
    def __init__(self):
        pygame.init()

        self.height = 580
        self.width = 770
        self.screen = pygame.display.set_mode((self.width+170, self.height))
        pygame.display.set_caption("Cherry Rush")
        self.clock = pygame.time.Clock()
        self.font1 = pygame.font.SysFont("Arial", 30)
        self.font2 = pygame.font.SysFont("Arial", 24)

        self.directions = ["left", "up", "right", "down"]
        self.to_right = False
        self.to_left = False
        self.to_up = False
        self.to_down = False
        self.movement = 3
        self.points = 0
        self.seconds = 10
        self.intro = True

        self.load_img()
        self.new_game()

        self.loop()
    
    def load_img(self):
        self.pictures = {"ghost": None, "cherry": None, "mario": None, "background": None, "header": None}
        for pic in self.pictures:
            self.pictures[pic] = pygame.image.load(pic +".png")
    
    def generate_xy(self, name: str):
        x = randint(0, self.width-self.pictures[name].get_width())
        y = randint(0, self.height-self.pictures[name].get_height())
        return [x,y]

    def new_cherry(self):
        cherry = self.generate_xy("cherry")
        while not self.distance_ok(self.player, cherry, 250):
            cherry = self.generate_xy("cherry")
        return cherry

    def new_ghost(self):
        xy = self.generate_xy("ghost")
        direction = self.directions[randint(0,3)]
        ghost =  [xy[0], xy[1], direction]
        while not self.distance_ok(self.player, ghost, 100):
                ghost = self.new_ghost()
        return ghost
    
    def distance_ok(self, player: list, ghost: list, dist: int):
        if abs(ghost[0]-player[0]) < dist or abs(ghost[1]-player[1]) < dist:
            return False
        return True

    def new_game(self):
        self.player = self.generate_xy("mario")
        self.cherry = self.new_cherry()
        self.ghosts = []
        for i in range(3):
            self.ghosts.append(self.new_ghost())

    def loop(self):
        self.counter = 1
        while True:
            self.draw_screen()
            self.inspect_actions()
            self.ghosts_move()
            self.player_moves()
            self.add_ghost()
            self.clock.tick(60)
            self.counter += 1
            if self.counter == 1201:
                self.counter = 1

    def inspect_actions(self):
        for action in pygame.event.get():
            if action.type == pygame.QUIT:
                exit()
            if action.type == pygame.KEYDOWN:
                if action.key == pygame.K_LEFT:
                    self.to_left = True
                if action.key == pygame.K_RIGHT:
                    self.to_right = True
                if action.key == pygame.K_UP:
                    self.to_up = True
                if action.key == pygame.K_DOWN:
                    self.to_down = True
                if action.key == pygame.K_SPACE:
                    self.movement = 6
                if action.key == pygame.K_RETURN:
                    self.intro = False
                if action.key == pygame.K_ESCAPE:
                    exit()
                if action.key == pygame.K_F2:
                    CherryRush()
            if action.type == pygame.KEYUP:
                if action.key == pygame.K_LEFT:
                    self.to_left = False
                if action.key == pygame.K_RIGHT:
                    self.to_right = False
                if action.key == pygame.K_UP:
                    self.to_up = False
                if action.key == pygame.K_DOWN:
                    self.to_down = False
                if action.key == pygame.K_SPACE:
                    self.movement = 2

    def draw_screen(self):
        self.screen.fill((0,0,0))

        if self.intro:
            self.intro_page()
            pygame.display.flip()
            return

        self.screen.blit(self.pictures['background'], (0,0))

        self.instrictions()

        for ghost in self.ghosts:
            self.screen.blit(self.pictures['ghost'], (ghost[0], ghost[1]))

        self.screen.blit(self.pictures['mario'], (self.player[0], self.player[1]))

        self.screen.blit(self.pictures['cherry'], (self.cherry[0], self.cherry[1]))

        self.game_over()

        pygame.display.flip()

    def intro_page(self):
        self.screen.blit(self.pictures['header'], (0,0))
        start = self.font1.render("Press Enter to start", True, (255, 0, 0))
        self.screen.blit(start, ((self.width+170)/2-start.get_width()/2, self.height/2))
        hint = self.font2.render("HINT: Use boost at the start to get higher score", True, (0, 0, 255))
        self.screen.blit(hint, ((self.width+170)/2-hint.get_width()/2, self.height-hint.get_height()*2))


    def instrictions(self):
        score = self.font2.render(f"Points: {self.points}", True, (0, 255, 0))
        self.screen.blit(score, (self.width+15, score.get_height()))
        spawn = self.font2.render("Next Spawn in:", True, (255, 0, 255))
        self.screen.blit(spawn, (self.width+15, score.get_height()*3))
        spawn_time = self.font2.render(f"{self.seconds}", True, (255, 0, 255))
        self.screen.blit(spawn_time, (self.width+spawn.get_width()/2, score.get_height()*4))
        retry = self.font2.render(f"F2 = Restart", True, (255, 0, 0))
        self.screen.blit(retry, (self.width+15, self.height-(retry.get_height()*4)))
        esc = self.font2.render(f"ESC = Exit", True, (255, 0, 0))
        self.screen.blit(esc, (self.width+15, self.height-(retry.get_height()*2)))
        boost = self.font2.render(f"Space = BOOST", True, (0, 255, 0))
        self.screen.blit(boost, (self.width+15, self.height/2-(boost.get_height()/2)))

    def game_over(self):
        if self.lost():
            end = self.font1.render("GAME OVER", True, (255, 0, 0))
            end_score = self.font2.render(f"Points: {self.points}", True, (255, 0, 0))
            end_height = end.get_height()
            end_width = end.get_width()
            end_x = self.width/2 - end_width/2
            end_y = self.height/2 - end_height/2
            pygame.draw.rect(self.screen, (0, 0, 0), (end_x-5, end_y, end_width+10, end_height*2))
            self.screen.blit(end, (end_x, end_y))
            self.screen.blit(end_score, (end_x+end_width/2-end_score.get_width()/2, end_y+end_height))

    def ghosts_move(self):
        if self.lost() or self.intro:
            return
        for ghost in self.ghosts:
            if self.counter % 60 == 0:
                ghost[2] = self.directions[randint(0,3)]
            while True:
                if ghost[2] == "left" and ghost[0] > 0:
                    ghost[0] -= self.movement
                    break
                elif ghost[2] == "left":
                    ghost[2] = self.directions[randint(0,3)]
                if ghost[2] == "up" and ghost[1] > 0:
                    ghost[1] -= self.movement
                    break
                elif ghost[2] == "up":
                    ghost[2] = self.directions[randint(0,3)]
                if ghost[2] == "right" and ghost[0]+self.pictures["ghost"].get_width() < self.width:
                    ghost[0] += self.movement
                    break
                elif ghost[2] == "right":
                    ghost[2] = self.directions[randint(0,3)]
                if ghost[2] == "down" and ghost[1]+self.pictures["ghost"].get_height() < self.height:
                    ghost[1] += self.movement
                    break
                elif ghost[2] == "down":
                    ghost[2] = self.directions[randint(0,3)]
        

    def player_moves(self):
        if self.lost() or self.intro:
            return
        if self.to_right and self.player[0] < self.width-self.pictures['mario'].get_width():
            self.player[0] += self.movement
        if self.to_left and self.player[0] > 0:
            self.player[0] -= self.movement
        if self.to_up and self.player[1] > 0:
            self.player[1] -= self.movement
        if self.to_down and self.player[1] < self.height-self.pictures['mario'].get_height(): 
            self.player[1] += self.movement
        self.get_point()

    def get_point(self):
        if self.hit(self.cherry, "cherry", self.player, "mario"):
            self.cherry = self.new_cherry()
            self.points += 1

    def lost(self):
        for ghost in self.ghosts:
            if self.hit(self.player, "mario", ghost, "ghost"):
                return True
        return False

    def hit(self, obj1: list, name1: str, obj2: list, name2: str):
        obj1_width = self.pictures[name1].get_width()
        obj1_height = self.pictures[name1].get_height()
        obj2_width = self.pictures[name2].get_width()
        obj2_height = self.pictures[name2].get_height()
        if obj1[0] in range(obj2[0], obj2[0] + obj2_width) or obj1[0] + obj1_width in range(obj2[0], obj2[0] + obj2_width):
            if obj1[1] in range(obj2[1], obj2[1] + obj2_height) or obj1[1] + obj1_height in range(obj2[1], obj2[1] + obj2_height):
                return True
        return False

    def add_ghost(self):
        if self.lost() or self.intro:
            return
        if self.counter % 60 == 0:
            self.seconds -= 1
        if self.counter % 600 == 0:
            self.seconds = 10
            self.ghosts.append(self.new_ghost())
            while not self.distance_ok(self.player, self.ghosts[-1], 100):
                self.ghosts[-1] = self.new_ghost()

if __name__ == "__main__":
    CherryRush()
