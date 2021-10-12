# import the necessary packages
from mrcnn.config import Config
from mrcnn import model as modellib
import numpy as np
import cv2


def remove_transparan(inputan_gambar,gambar_transparan,lokasi):
    class myMaskRCNNConfig(Config):
        # give the configuration a recognizable name
        NAME = "MaskRCNN_inference"
        
        # set the number of GPUs to use along with the number of images
        # per GPU
        GPU_COUNT = 1
        IMAGES_PER_GPU = 1
        
        # number of classes (we would normally add +1 for the background
        # but the background class is *already* included in the class
        # names)
        NUM_CLASSES = 1+80

    config = myMaskRCNNConfig()
    model = modellib.MaskRCNN(mode='inference', config=config, model_dir='./')
    model.load_weights('D:/semester 4/Ai/Tubes/mask_rcnn_coco.h5',by_name=True)
    CLASS_NAMES = ['BG', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush']

    image = cv2.imread(inputan_gambar)
    
    # Inisialisasi Dimensi
    height_image,width_image = image.shape[0], image.shape[1]

    # Deteksi gambar berdasarkan model
    results = model.detect([image], verbose=0)
    # Ambil dari indeks pertama
    r = results[0]
    # masks, class_ids, score, rois
    mask,classes = r['masks'],r['class_ids']
    mask = mask.astype(np.uint8)
    # Inisialisasi Dimensi
    height_mask,width_mask = mask.shape[0], mask.shape[1]
    classes = classes.astype(np.uint8)

    # Ambil indeks pertama dari classes
    jumlah_classes = classes.shape[0]

    # Matrix 0 Supaya menampung hasil masking, dan tetap sesuai
    hasil = np.zeros((height_mask,width_mask))
    for i in range(jumlah_classes):
        hasil += mask[:,:,i]
    hasil = (hasil > 0)*1

    hasil_remove_transparan = image.copy()
    background_transparan = cv2.imread(gambar_transparan)
    masking_remove = hasil
    lokasi = lokasi
    # Inisialisasi Dimensi
    height_transparan , widht_transparan = masking_remove.shape[:2]
    # Resize bg ditambah 500 
    background_transparan = cv2.resize(background_transparan,(height_transparan+500, widht_transparan+500))
    # Crop Tinggi dan Lebarnya dan warna
    background_transparan = background_transparan[:height_transparan, :widht_transparan, :] 
    # Menyatukan background dengan hasil gambar masking, convert
    background_transparan *= (1-masking_remove).astype(np.uint8)[..., None]
    hasil_remove_transparan *= masking_remove.astype(np.uint8)[..., None]
    hasil_remove_transparan += background_transparan
    filename = cv2.imwrite(lokasi, hasil_remove_transparan)                #save hasil 
    return filename