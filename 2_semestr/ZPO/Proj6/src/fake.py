#################################################################################
# Description:  Class stores data from csv and image itself
#               
# Authors:      Petr Buchal         <petr.buchal@lachub.cz>
#               Martin Ivanco       <ivancom.fr@gmail.com>
#               Vladimir Jerabek    <jerab.vl@gmail.com>
#
# Date:     2019/04/13
# 
# Note:     This source code is part of project created on UnIT extended 2019.
#################################################################################
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
