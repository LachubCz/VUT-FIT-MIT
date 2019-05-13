from image import Image

class Fake(Image):
    def __init__(self, image, path, augmentation, x, y, w, h):
        super().__init__(image, path, augmentation)
        self.bbox =  {
          "x": x,
          "y": y,
          "w": w,
          "h": h
        }
