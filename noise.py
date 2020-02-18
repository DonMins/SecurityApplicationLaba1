import numpy as np
import cv2

def add(image_name, mode):
    image_name.rfind('.')
    im = cv2.imread(image_name)
    s_vs_p = 0.5
    amount = 0.03
    out = np.copy(im)
    if mode == "salt":
        # Salt mode
        num_salt = np.ceil(amount * im.size * s_vs_p)
        coords = [np.random.randint(0, i - 1, int(num_salt))  for i in im.shape]
        out[coords] = 255
    elif mode == "pepper":
        num_pepper = np.ceil(amount * im.size * (1. - s_vs_p))
        coords = [np.random.randint(0, i - 1, int(num_pepper))
                  for i in im.shape]
        out[coords] = 0
    temp_name = image_name[0:image_name.rfind('.')] + '_temp' + image_name[image_name.rfind('.'):len(image_name)]
    cv2.imwrite(image_name[0:image_name.rfind('.')]+'_temp'+image_name[image_name.rfind('.'):len(image_name)],out)
    return temp_name
