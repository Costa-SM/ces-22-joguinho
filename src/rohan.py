from resources import load_sprite

class Rohan():
    def __init__(self):
        image, image_rect = load_sprite('rohan.png')
        self.surface = image
        self.rect = image_rect
        self.position = (0, 0)

    def get_surface(self):
        return self.surface

    def get_rect(self):
        return self.rect