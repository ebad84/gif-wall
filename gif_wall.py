from time import sleep
import os

import ctypes,requests



import os
from PIL import Image

############################################
'''
I searched high and low for solutions to the "extract animated GIF frames in Python"
problem, and after much trial and error came up with the following solution based
on several partial examples around the web (mostly Stack Overflow).
There are two pitfalls that aren't often mentioned when dealing with animated GIFs -
firstly that some files feature per-frame local palettes while some have one global
palette for all frames, and secondly that some GIFs replace the entire image with
each new frame ('full' mode in the code below), and some only update a specific
region ('partial').
This code deals with both those cases by examining the palette and redraw
instructions of each frame. In the latter case this requires a preliminary (usually
partial) iteration of the frames before processing, since the redraw mode needs to
be consistently applied across all frames. I found a couple of examples of
partial-mode GIFs containing the occasional full-frame redraw, which would result
in bad renders of those frames if the mode assessment was only done on a
single-frame basis.
Nov 2012
'''


def analyseImage(path):
    '''
    Pre-process pass over the image to determine the mode (full or additive).
    Necessary as assessing single frames isn't reliable. Need to know the mode 
    before processing all frames.
    '''
    im = Image.open(path)
    results = {
        'size': im.size,
        'mode': 'full',
    }
    try:
        while True:
            if im.tile:
                tile = im.tile[0]
                update_region = tile[1]
                update_region_dimensions = update_region[2:]
                if update_region_dimensions != im.size:
                    results['mode'] = 'partial'
                    break
            im.seek(im.tell() + 1)
    except EOFError:
        pass
    return results


def processImage(path):
    directory = path.split(".")[:-1][0]
    try:
        os.mkdir(directory)
    except:
        pass
    '''
    Iterate the GIF, extracting each frame.
    '''
    mode = analyseImage(path)['mode']
    
    im = Image.open(path)

    i = 0
    p = im.getpalette()
    last_frame = im.convert('RGB')
    
    try:
        while True:            
            '''
            If the GIF uses local colour tables, each frame will have its own palette.
            If not, we need to apply the global palette to the new frame.
            '''
            if not im.getpalette():
                im.putpalette(p)
            
            new_frame = Image.new('RGB', im.size)
            
            '''
            Is this file a "partial"-mode GIF where frames update a region of a different size to the entire image?
            If so, we need to construct the new frame by pasting it on top of the preceding frames.
            '''
            if mode == 'partial':
                new_frame.paste(last_frame)
            
            new_frame.paste(im, (0,0), im.convert('RGBA'))
            new_frame.save(directory+'/%s-%d.jpg' % (''.join(os.path.basename(path).split('.')[:-1]), i), 'JPEG')

            i += 1
            last_frame = new_frame
            im.seek(im.tell() + 1)
    except EOFError:
        pass
#spliting image
############################################################

############################################################
def ch_background(url=None,path=None):
    if path != None:
        #ctypes.windll.user32.SystemParametersInfoA(20, 0, path, 3)
        change_wallpaper()
    elif url != None:
        open("downloaded_pic.jpg","wb").write(requests.get(url).content)
        #ctypes.windll.user32.SystemParametersInfoW(20, 0, "downloaded_pic.jpg", 3)
        WALLPAPER_PATH = "downloaded_pic.jpg"
        change_wallpaper()

def set_wall(gif_name,addrs,sleep_time=1/34):
    for wall_addr in addrs:
        wall_addr = gif_name.split(".")[:-1][0]+"\\"+wall_addr
        ctypes.windll.user32.SystemParametersInfoW(20 , 0 , wall_addr,3)
        #ch_background(path=wall_addr)
        print(wall_addr)
        #sleep(sleep_time)

def gif_frames(gif_name):
    directory = gif_name.split(".")[:-1][0]
    return os.listdir(directory)

#changing background wallpaper
############################################################

name = input("file_path: ")#"0f47de6c60b9533c0fdebcd6ba8c2936.gif"
processImage(name)


addresses = gif_frames(name)
while True:
    #break
    set_wall(name,addresses)

#ch_background(url="https://files.virgool.io/upload/users/201480/posts/novq0myni9rh/q0d7ui576uld.jpeg")
