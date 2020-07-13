
import cv2
from skimage import feature
import numpy as np

class Descriptor:

    def color_history(image,histSize):
        image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        hist = cv2.calcHist(images=[image], channels=[0, 1, 2], mask=None, histSize=[histSize,histSize,histSize], ranges=[0, 256] * 3)
        hist = cv2.normalize(hist, dst=hist.shape)
        
        return hist.flatten()

    def lpb_history(image,numPoints,radius,eps=1e-7):
        # Chuyển ảnh sang đen trắng
        # đầu vào của local_binary_pattern image đen trắng
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        lbp = feature.local_binary_pattern(image, numPoints, radius, method="uniform")
        (hist, _) = np.histogram(lbp.ravel(),bins=np.arange(0,numPoints + 3),range=(0, numPoints + 2))

        hist = hist.astype("float")
        hist /= (hist.sum() + eps)
        return hist

    def hog(image,cell_size,block_size,bins):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image = cv2.resize(image, (200, 100))
        H = feature.hog(image, orientations=bins, pixels_per_cell=(cell_size, cell_size),
                        cells_per_block=(block_size, block_size), transform_sqrt=True, block_norm="L1")
        return H
    