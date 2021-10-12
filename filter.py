# IMPORT LIBRARY PYTHON UNTUK MENUNJANG FILTER
import cv2
import numpy as np

#filter gray
def filter_gray(inputan_gambar, lokasi):
    image = cv2.imread(inputan_gambar, 0)                   #membaca file dan 0 adalah pengubah gambar jadi gray
    lokasi = lokasi                                         #lokasi
    #lakukan pertama
    try:
        hasil_image = cv2.resize(image, (1920, 1080))       #resize ukuran foto height,widht(1920,1080)
    #jika error ke expect
    except:
        hasil_image = image
    
    filename = cv2.imwrite(lokasi, hasil_image)             #save hasil pixel(nama file,hasil pixel)
    return filename


# filter invert
def filter_invert(inputan_gambar, lokasi):
    input = cv2.imread(inputan_gambar)                      #membaca file
    lokasi = lokasi                                         #lokasi
    #lakukan pertama                                        
    try:
        hasil_image = cv2.resize(input, (1920, 1080))       #resize ukuran foto height,widht(1920,1080)
    except:
        hasil_image = input                                 #resize sama seperti ori

    filename = cv2.bitwise_not(hasil_image)                 #pengubah gambar jadi invert
    filename = cv2.imwrite(lokasi, filename)                #save hasil pixel(nama file,hasil pixel)
    return filename


# filter pixelize
def filter_pixelize(inputan_gambar, lokasi):
    input = cv2.imread(inputan_gambar)                      #membaca file
    lokasi = lokasi                                         #lokasi
    try:
        hasil_image = cv2.resize(input, (1920, 1080))       #resize ukuran foto height,widht(1920,1080)
    except:
        hasil_image = input                                 #resize sama seperti ori

    # ukuran dari image (height,widht)
    height, width = hasil_image.shape[:2]

    # fill ukuran "pixelated" 
    height_pixel, width_pixel = (50, 50)
    
    # Resize fill ukuran "pixelated" ke image dengan ukuran pixelnya
    hasil_image = cv2.resize(hasil_image, (height_pixel, width_pixel), interpolation=cv2.INTER_LINEAR)

    # Resize fill ukuran "pixelated" ke image dengan ukuran image baru
    filename = cv2.resize(hasil_image, (width, height),interpolation=cv2.INTER_NEAREST)
    filename = cv2.imwrite(lokasi, filename)                            #save hasil pixel(nama file,hasil pixel)
    return filename
