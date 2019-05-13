class Image(object):
    def __init__(self, image, path, augmentation):
        self.image = image
        self.path = path
        self.width = self.image.shape[0]
        self.height = self.image.shape[1]
        self.augmentation = augmentation
        self.bbox = None
