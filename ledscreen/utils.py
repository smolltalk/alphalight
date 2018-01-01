import numpy
import PIL

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import numpy as np
    
def text_to_image(text, fontpath, fontsize):
    font = ImageFont.truetype(fontpath, fontsize) 
    w, h = font.getsize(text)  
    h *= 2
    image = Image.new('L', (w, h), 1)  
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), text, font=font) 
    arr = np.asarray(image)
    arr = arr[(arr != 1).any(axis=1)]
    result = Image.fromarray(arr)
    return result
