import sys
import time
import cv2
import numpy as np
from PIL import Image


def viewImage(image, name_of_window):
    cv2.namedWindow(name_of_window, cv2.WINDOW_NORMAL)
    cv2.imshow(name_of_window, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def code():
    # 1 first open
    img = cv2.imread('assignment1.png')
    cv2.imshow("Image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    # bounding box
    bounded = img.copy()
    cv2.rectangle(bounded, (480, 17), (920, 720), (0, 255, 255), 5)
    # Viewing bounded image
    viewImage(bounded, "Bounded img")
    # blurred
    blurred = bounded.copy()[17:720, 460:920]
    blurred = cv2.GaussianBlur(blurred, (33, 33), 0)
    viewImage(blurred, "Blurred img")
    # final image
    result_image = img.copy()
    result_image[17:17 + blurred.shape[0], 480:480 + blurred.shape[1]] = blurred
    viewImage(result_image, 'result')


# code()


class Image:
    def __init__(self, name):
        self.name = name

    def read(self):
        read = cv2.imread(f'{self.name}')
        return read

    def view(self):
        read = self.read()
        cv2.imshow("Image", read)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def view_child(self, image):
        viewImage(image, 'image')

class RectangledImage(Image):
    def __init__(self, name):
        super().__init__(name)

    def add_rectangle(self, left_top_x, left_top_y, right_bottom_x, right_bottom_y, frame_thickness=5):
        read = self.read()
        read = cv2.rectangle(read, (left_top_x, left_top_y), (right_bottom_x, right_bottom_y), (0, 255, 255),
                             frame_thickness)
        return read


class ScaleImage(Image):
    def __init__(self, name):
        super().__init__(name)

    def scale_img(self, scale_percent):
        # scale by width/length
        read = cv2.imread(f'{self.name}')
        width = int(read.shape[1] * scale_percent / 100)
        height = int(read.shape[0] * scale_percent / 100)
        dim = (width, height)
        resized_img = cv2.resize(read, dim, interpolation=cv2.INTER_AREA)
        return resized_img


class CropImage(Image):
    def __init__(self, name):
        super().__init__(name)

    def crop_img(self, y_start, y_end, x_start, x_end):
        read = self.read()
        cropped_img = read[y_start:y_end, x_start:x_end]
        return cropped_img


class GrayImage(Image):
    def __init__(self, name):
        super().__init__(name)

    def gray_img(self):
        read = self.read()
        gray_image = cv2.cvtColor(read, cv2.COLOR_BGR2GRAY)
        return gray_image


class BlurredImage(RectangledImage):
    def __init__(self, name):
        super().__init__(name)

    # Gaussian Blur
    # def add_blur(self, left_top_x, left_top_y, right_bottom_x, right_bottom_y, blur_x, blur_y, read):
    #     blur_area = read[left_top_y:right_bottom_y, left_top_x:right_bottom_x]
    #     blur_image = read.copy()
    #     if int(blur_x) % 2 == 0:
    #         blur_x += 1
    #     if int(blur_y) % 2 == 0:
    #         blur_y += 1
    #     blur_area = cv2.GaussianBlur(blur_area, (int(blur_x), int(blur_y)), 0)
    #     blur_image[left_top_y:left_top_y + blur_area.shape[0], left_top_x:left_top_x + blur_area.shape[1]] = blur_area
    #     return blur_image

    # Average
    def add_blur(self, left_top_x, left_top_y, right_bottom_x, right_bottom_y,blur_1,blur_2, read):
        blur_area = read[left_top_y:right_bottom_y, left_top_x:right_bottom_x]
        blur_image = read.copy()
        blur_area = cv2.blur(blur_area, (blur_1, blur_2))
        blur_image[left_top_y:left_top_y + blur_area.shape[0], left_top_x:left_top_x + blur_area.shape[1]] = blur_area
        return blur_image



# test_img = Image('assignment1.png')
# test_img.read()
# test_img.view()
#
# test_rect_img = RectangledImage('assignment1.png')
# img = test_rect_img.add_rectangle(480, 17, 920, 720, 5)
# test_rect_img.view_child(img)
#
# test_blured_img = BlurredImage('assignment1.png')
# img = test_blured_img.add_blur(480, 17, 920, 720,44, 7, img)
# test_blured_img.view_child(img)
#
# test_scale_img = ScaleImage('assignment1.png')
# img = test_scale_img.scale_img(13)
# test_scale_img.view_child(img)
#
# cropped_img = CropImage('assignment1.png')
# img = cropped_img.crop_img(200,400,360, 520)
# cropped_img.view_child(img)
#
# gray_img = GrayImage('assignment1.png')
# img = gray_img.gray_img()
# gray_img.view_child(img)
#


def task():
    Shrek = BlurredImage('assignment1.png')
    img = Shrek.read()
    Shrek.view_child(img)
    frame = [480, 17, 920, 720]
    img_rect = Shrek.add_rectangle(frame[0], frame[1], frame[2], frame[3], 5)
    Shrek.view_child(img_rect)
    img_blur = Shrek.add_blur(frame[0], frame[1], frame[2], frame[3], 33, 33, img_rect)
    Shrek.view_child(img_blur)
    save = str(input('Do you want to save final image?: '))
    if save in ['', 'yes', 'Yes', 'YES']:
        cv2.imwrite('assignment_final.png', img_blur)
    else:
        sys.exit('Ok, good bye, dear friend :)!')


task()


def kernel_discussion():
    # Average
    image = cv2.imread('assignment1.png')
    aver_blur_3 = cv2.blur(image, (2, 2))
    viewImage(aver_blur_3, '3x3')
    aver_blur_6 = cv2.blur(image, (6, 6))
    viewImage(aver_blur_6, '6x6')
    aver_blur_9 = cv2.blur(image, (9, 9))
    viewImage(aver_blur_9, '9x9')
    time.sleep(2)

    # Gaussian  blur values must be odd,  0 is standard deviation, computer will calculate it automatically
    gauss_blur_3 = cv2.GaussianBlur(image, (3, 3), 0)
    viewImage(gauss_blur_3, '3x3')
    gauss_blur_7 = cv2.GaussianBlur(image, (7, 7), 0)
    viewImage(gauss_blur_7, '7x7')
    gauss_blur_9 = cv2.GaussianBlur(image, (11, 11), 0)
    viewImage(gauss_blur_9, '11x11')
    time.sleep(2)

    # Median blur values must be odd
    med_blur_3 = cv2.medianBlur(image, 3)
    viewImage(med_blur_3, '3x3')
    med_blur_7 = cv2.medianBlur(image, 7)
    viewImage(med_blur_7, '3x3')
    med_blur_11 = cv2.medianBlur(image, 11)
    viewImage(med_blur_11, '3x3')

kernel_discussion()