import numpy as np
import cv2

def add(image_name):
    image_name.rfind('.')
    im = cv2.imread(image_name)
    amount = 0.03
    out = np.copy(im)
    num_salt = np.ceil(amount * im.size )
    coords = [np.random.randint(0, i - 1, int(num_salt)) for i in im.shape]
    out[coords] = 255

    temp_name = image_name[0:image_name.rfind('.')] + '_temp' + image_name[image_name.rfind('.'):len(image_name)]
    cv2.imwrite(image_name[0:image_name.rfind('.')]+'_temp'+image_name[image_name.rfind('.'):len(image_name)],out)
    return temp_name
