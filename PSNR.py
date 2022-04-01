# PSNR.py

from skimage import measure

def psnr(img1, img2):
    # 一般，对于第三个参数，针对 uint8 数据，最大像素值为 255，而针对浮点型数据，最大像素值为 1
    return measure.compare_psnr(img1, img2, 255)

if __name__=="__main__":
    import cv2
    img1=cv2.imread('img1.png')
    img2=cv2.imread('img2.png')
    print('PSNR: ', psnr(img1,img2))