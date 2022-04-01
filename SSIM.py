# SSIM.py

from skimage import measure

def ssim(img1, img2):
    # 彩色图像需要将参数multichannel的值设为true
    return measure.compare_ssim(img1, img2, multichannel=True)

if __name__=="__main__":
    import cv2
    img1=cv2.imread('img1.png')
    img2=cv2.imread('img2.png')
    print('SSIM: ', ssim(img1,img2))