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

#Class stores data from csv and image itself
class Image(object):
    def __init__(self, image, path, x, y, w, h):
        self.image = image
        self.path = path
        self.bbox =  {
          "x": x,
          "y": y,
          "w": w,
          "h": h
        }
        self.width = self.image.shape[0]
        self.height = self.image.shape[1]
        self.augmentation = True

    #def get_first_im(self):
    #    parametres = self.path.split('_')
    #    os.path.join(ground_truths_path, "Au_"+parametres[4][:3]+"_"+parametres[4][3:]+".jpg")
    #    parametres
#
    #def get_second_im(self):