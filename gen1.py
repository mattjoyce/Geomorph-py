#!/usr/bin/env python
import os
import random
import Image

class map:
    def __init__(self, sizex=1, sizey=1, stroutfile):
        self.tx = sizex
        self.ty = sizey
        self.tilespath="/home/matt/projects/mapgen/tiles"
        self.corner=[]
        self.edge=[]
        self.base=[]
        self.im = Image.new("RGB", ((sizex+1)*500, (sizey+1)*500), "white")
        print self.im.size

    def randtile(self,element):
        # 0,1,2
        # 3,4,5
        # 6,7,8
        tile=""
        if element == 0:  #top left corner
            tile=self.corner[random.randint(0,len(self.corner)-1)]
            rotate=2
        elif element == 1:  #top centre edge
            tile=self.edge[random.randint(0,len(self.edge)-1)]
            rotate=3
        elif element == 2:  #top right
            tile=self.corner[random.randint(0,len(self.corner)-1)]
            rotate=3
        elif element == 3:  # left edge
            tile=self.edge[random.randint(0,len(self.edge)-1)]
            rotate=2
        elif element ==4:  # centre
            tile=self.base[random.randint(0,len(self.base)-1)]
            rotate=random.randint(0,4);
        elif element == 5:  # right edge
            tile=self.edge[random.randint(0,len(self.edge)-1)]
            rotate=0
        elif element == 6:  # bottom left corner
            tile=self.corner[random.randint(0,len(self.corner)-1)]
            rotate=0
        elif element == 7:  # bottom edge
            tile=self.edge[random.randint(0,len(self.edge)-1)]
            rotate=1
        elif element == 8: #bottom right corner
            tile=self.corner[random.randint(0,len(self.corner)-1)]
            rotate=0
        return (tile,rotate)
    
    
    def build(self):
        #top row
        strfile=self.tilespath+"/"+self.randtile(i)[0] #tl
        im_element=Image.open(strfile)
        self.im.paste(im,(0,0))
        
        self.im.save(self.stroutfile)
            
        
    def loadtiles(self):
        os.chdir(self.tilespath)
        for file in os.listdir(self.tilespath):
            if file.endswith(".jpg") and file.find("Corner")>-1:
                self.corner.append(file)
            elif file.endswith(".jpg") and file.find("Edge")>-1:
                self.edge.append(file)
            elif file.endswith(".jpg") and file.find("Base")>-1:
                self.base.append(file)

map1=map("/home/matt/projects/mapgen/test.jpg")
map1.loadtiles()
map1.build()