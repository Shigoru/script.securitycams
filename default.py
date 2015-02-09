'''
This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0) License.


To view a copy of this license, visit

German version:  http://creativecommons.org/licenses/by-nc-sa/4.0/deed.de
English version: http://creativecommons.org/licenses/by-nc-sa/4.0/

or send a letter to Creative Commons, 171 Second Street, Suite 300, San Francisco, California, 94105, USA.
'''


import xbmc
import xbmcgui
import xbmcvfs
import xbmcaddon
import urllib
import os
import time
from PIL import Image


addon   = xbmcaddon.Addon()
addonid = addon.getAddonInfo('id')


# ATTENTION
# You must use MJPEG Streams for the URL DefinitionURL1 =  addon.getSetting('Camera_URL1')
URL2 =  addon.getSetting('Camera_URL2')
URL3 =  addon.getSetting('Camera_URL3')
URL4 =  addon.getSetting('Camera_URL4')
URL5 =  addon.getSetting('Camera_URL5')
URL6 =  addon.getSetting('Camera_URL6')


# Test URLs with Webcams#URL1='http://62.157.185.131/record/current.jpg'#URL2='http://62.157.185.131/record/current.jpg'#URL3='http://62.157.185.131/record/current.jpg'#URL4='http://62.157.185.131/record/current.jpg'#URL5='http://62.157.185.131/record/current.jpg'#URL6='http://62.157.185.131/record/current.jpg'#URL1='http://webcams.passau.de/cam-rathaus-huge-aktuell.jpg'#URL2='http://www.mediac2.de/projekte/webcam/wallstrasse/aktuell/aktuell.jpg'#URL3='http://www.cityscope.de/bmw/current_pano.jpg'#URL4='http://www.goldbeck.de/uploads/webcam/df0691/current.jpg'#URL5='http://62.157.185.131/record/current.jpg'#URL6='http://webcams.passau.de/cam-rathaus-huge-aktuell.jpg'


class CamWindow(xbmcgui.WindowDialog):
    def __init__(self):
        path = xbmc.translatePath('special://profile/addon_data/%s' %addonid )
        if not xbmcvfs.exists(path):
            xbmcvfs.mkdir(path)

        IMAGEFILE1 = os.path.join(path, 'cam1.jpg')
        IMAGEFILE2 = os.path.join(path, 'cam2.jpg')
        IMAGEFILE3 = os.path.join(path, 'cam3.jpg')
        IMAGEFILE4 = os.path.join(path, 'cam4.jpg')
        IMAGEFILE5 = os.path.join(path, 'cam5.jpg')
        IMAGEFILE6 = os.path.join(path, 'cam6.jpg')

        self.isRunning = True
        
        # set the initial image before the window is shown
	# aspectRatio: integer - (values 0 = stretch (default), 1 = scale up (crops), 2 = scale down (black bars)
        urllib.urlretrieve(URL1, IMAGEFILE1)        
        self.resizeImg(IMAGEFILE1)
        self.image1 = xbmcgui.ControlImage(12, 360, 205, 160, IMAGEFILE1, aspectRatio = 0)
        self.addControl(self.image1)

        urllib.urlretrieve(URL2, IMAGEFILE2)
        self.resizeImg(IMAGEFILE2)
        self.image2 = xbmcgui.ControlImage(222, 360, 205, 160, IMAGEFILE2, aspectRatio = 0)
        self.addControl(self.image2)

        urllib.urlretrieve(URL3, IMAGEFILE3)
        self.resizeImg(IMAGEFILE3)
        self.image3 = xbmcgui.ControlImage(432, 360, 205, 160, IMAGEFILE3, aspectRatio = 0)
        self.addControl(self.image3)

        urllib.urlretrieve(URL4, IMAGEFILE4)
        self.resizeImg(IMAGEFILE4)
        self.image4 = xbmcgui.ControlImage(642, 360, 205, 160, IMAGEFILE4, aspectRatio = 0)
        self.addControl(self.image4)

        urllib.urlretrieve(URL5, IMAGEFILE5)
        self.resizeImg(IMAGEFILE5)
        self.image5 = xbmcgui.ControlImage(852, 360, 205, 160, IMAGEFILE5, aspectRatio = 0)
        self.addControl(self.image5)

        urllib.urlretrieve(URL6, IMAGEFILE6)
        self.resizeImg(IMAGEFILE6)
        self.image6 = xbmcgui.ControlImage(1062, 360, 205, 160, IMAGEFILE6, aspectRatio = 0)
        self.addControl(self.image6)

        self.show()
        
        past = time.time()        
        while (not xbmc.abortRequested) and (self.isRunning):
            if (time.time() - past > 0.1):
                urllib.urlretrieve(URL1, IMAGEFILE1)
                self.resizeImg(IMAGEFILE1)
                self.image1.setImage("")
                self.image1.setImage(IMAGEFILE1)        
                
                urllib.urlretrieve(URL2, IMAGEFILE2)
                self.resizeImg(IMAGEFILE2)
                self.image2.setImage("")
                self.image2.setImage(IMAGEFILE2)
                
                urllib.urlretrieve(URL3, IMAGEFILE3)
                self.resizeImg(IMAGEFILE3)
                self.image3.setImage("")
                self.image3.setImage(IMAGEFILE3)
                
                urllib.urlretrieve(URL4, IMAGEFILE4)
                self.resizeImg(IMAGEFILE4)
                self.image4.setImage("")
                self.image4.setImage(IMAGEFILE4)

                urllib.urlretrieve(URL5, IMAGEFILE5)
                self.resizeImg(IMAGEFILE5)
                self.image5.setImage("")
                self.image5.setImage(IMAGEFILE5)

                urllib.urlretrieve(URL6, IMAGEFILE6)
                self.resizeImg(IMAGEFILE6)
                self.image6.setImage("")
                self.image6.setImage(IMAGEFILE6)

                past = time.time()

            xbmc.sleep(1)
            

    def onAction(self, action):
        if (action == 10) or (action == 92):
            self.isRunning = False
            self.close()


    def resizeImg(self, IMAGEFILE):
        if xbmcvfs.exists(IMAGEFILE):
            img = Image.open(IMAGEFILE)
            img = img.resize((1280, 720))
            img.save(IMAGEFILE)
            

CW = CamWindow()
del CW
