import numpy as np
import cv2

def filter_smoothing(inputan,lokasi):
    img = cv2.imread(inputan) #membaca gambar
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +'./haarcascade_frontalface_default.xml') #load model deteksi wajah haarcasecade
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #ubah gambar ke gray

    #konfigurasi detection wajah
    faces = face_cascade.detectMultiScale(gray,
                                        scaleFactor=1.1, # ukuran gambar diperkecil pada setiap skala gambar
                                        minNeighbors=10, # banyak tetangga yang harus dimiliki setiap persegi panjang kandidat untuk mempertahankannya.
                                        minSize=(80,80) #minimum ukuran
                                    )
    
    #menjalankan algoritma pertama
    try : 
        #looping faces ke dalam variabel                         
        for (x,y,w,h) in faces:
            kebenaran = (x,y,w,h)
        kebenaran = kebenaran in faces  #nilai kebenaran 

    #jika algoritma pertama gagal maka akan limpahkan ke expect
    except : 
        kebenaran = 'False' #nilai kebenaran

    #mencopy gambar ke variabel gaussin
    gaussin = img.copy()
    #jika true akan di gaussin sesuai deteksi
    if str(kebenaran) == 'True' :
        for (x,y,w,h) in faces:
            gaussin[y:y+h,x:x+w] = cv2.GaussianBlur(img[y:y+h,x:x+w] ,(5,5),0)

    #jika tidak akan di gaussin seluruh gambar
    else :
        gaussin = cv2.GaussianBlur(img ,(5,5),0)
    lokasi= lokasi #nama
    filename = cv2.imwrite(lokasi, gaussin) #save hasil
    return filename