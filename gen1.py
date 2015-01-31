#!/usr/bin/env python
import os
import random
import Image, ImageEnhance
import operator
random.seed()

class map:
    def __init__(self, stroutfile,sizex=1, sizey=1):
        self.tx = sizex
        self.ty = sizey
        self.tilespath="/home/matt/projects/mapgen/tiles"
        self.stroutfile=stroutfile
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
            rotate=180
        elif element == 1:  #top centre edge
            tile=self.edge[random.randint(0,len(self.edge)-1)]
            rotate=0
        elif element == 2:  #top right corner
            tile=self.corner[random.randint(0,len(self.corner)-1)]
            rotate=90
        elif element == 3:  # left edge
            tile=self.edge[random.randint(0,len(self.edge)-1)]
            rotate=90
        elif element ==4:  # centre
            tile=self.base[random.randint(0,len(self.base)-1)]
            rotate=random.randint(0,4)*90;
        elif element == 5:  # right edge
            tile=self.edge[random.randint(0,len(self.edge)-1)]
            rotate=270
        elif element == 6:  # bottom left corner
            tile=self.corner[random.randint(0,len(self.corner)-1)]
            rotate=270
        elif element == 7:  # bottom edge
            tile=self.edge[random.randint(0,len(self.edge)-1)]
            rotate=180
        elif element == 8: #bottom right corner
            tile=self.corner[random.randint(0,len(self.corner)-1)]
            rotate=0
        
        im1=Image.open(self.tilespath+"/"+tile).rotate(rotate)
        
        # flip side edges and base vertically, maybe
        if element in [3,4,5] and random.random()>0.5:
            im2=im1.transpose(Image.FLIP_TOP_BOTTOM)
        elif element in [1,4,7] and random.random()>0.5:
            im2=im1.transpose(Image.FLIP_LEFT_RIGHT)
        else:
            im2=im1
              
        return(self.equalize(im2))
        
    
    
    def build(self):
        #top row
        im_tile=self.randtile(0)
        self.im.paste(im_tile,(0,0))
        
        for i in range(0,self.tx):
            im_tile=self.randtile(1)
            self.im.paste(im_tile,(250+(i*500),0))
          
        im_tile=self.randtile(2)
        self.im.paste(im_tile,(250+(self.tx*500),0))
        
        # mid rows
        for y in range(0,self.ty):
            im_tile=self.randtile(3)
            self.im.paste(im_tile,(0,250+(y*500)))
            
            for x in range(0,self.tx):
                im_tile=self.randtile(4)
                self.im.paste(im_tile,(250+(x*500),250+(y*500)))
        
            im_tile=self.randtile(5)
            self.im.paste(im_tile,(250+(self.tx*500),250+(y*500)))
            
            
        #bottom
        im_tile=self.randtile(6)
        self.im.paste(im_tile,(0,250+(self.ty*500)))
        
        for i in range(0,self.tx):
            im_tile=self.randtile(7)
            self.im.paste(im_tile,(250+(i*500),250+(self.ty*500)))
          
        im_tile=self.randtile(8)
        self.im.paste(im_tile,(250+(self.tx*500),250+(self.ty*500)))
       
        # filename=self.stroutfile[:-4]
        # enhancer = ImageEnhance.Brightness(self.im)
        # for k in range(1, 9):
            # factor = k / 4.0
            # print(factor),  # 0.25 0.5 0.75 1.0 1.25 1.5 1.75 2.0
            # img_enhanced = enhancer.enhance(factor)
            # img_enhanced.save(filename+"_%03d.jpg" % (int(factor*100)) )
        self.im.save(self.stroutfile)

    def equalize(self,im):
        h = im.convert("L").histogram()
        lut = []
        for b in range(0, len(h), 256):
            # step size
            step = reduce(operator.add, h[b:b+256]) / 255
            # create equalization lookup table
            n = 0
            for i in range(256):
                lut.append(n / step)
                n = n + h[i+b]
        # map image through lookup table
        return im.point(lut*3)     
        
    def loadtiles(self):
        os.chdir(self.tilespath)
        for file in os.listdir(self.tilespath):
            if file.endswith(".jpg") and file.find("Corner")>-1:
                self.corner.append(file)
            elif file.endswith(".jpg") and file.find("Edge")>-1:
                self.edge.append(file)
            elif file.endswith(".jpg") and file.find("Base")>-1:
                self.base.append(file)

map1=map("/home/matt/projects/mapgen/test.jpg",5,5)
map1.loadtiles()
map1.build()