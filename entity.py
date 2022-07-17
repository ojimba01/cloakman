import pygame
# Entinties are the objects that are drawn on the screen.
# They are also the objects that are updated with the scroll.
class entity():
#Enintity for set location sprites
#-------------------------------------------------------------------------------
    def __init__(self, location, rect):
        self.rect = rect
        self.location = location
    def render(self, surface, scroll):
        surface.blit(self.rect, (self.location[0] - scroll[0], self.location[1] - scroll[1]))
    def get_rect(self):
        return pygame.Rect(self.location[0], self.location[1], 8, 9)
    def collision_test(self, rect):
        jumper_rect = self.get_rect()
        return jumper_rect.colliderect(rect)

class entitym():
#Enintity for mouse location sprites
#-------------------------------------------------------------------------------
    def __init__(self):
        pass
    def render(self, surface, scroll, rect, location):
        self.location = location
        surface.blit(rect, (location[0] - scroll[0], location[1] - scroll[1]))
    def get_rect(self):
        return pygame.Rect(self.location[0], self.location[1], 8, 9)
    def collision_test(self, rect):
        jumper_rect = self.get_rect()
        return jumper_rect.colliderect(rect)

        
    
    


        

