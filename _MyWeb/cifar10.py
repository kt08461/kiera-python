import os
import logging
import numpy as np
from django.shortcuts import render
from django.conf import settings

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def cifar10Main(request):
    if request.method == "POST":
        # ======================================
        # 預測上傳圖片
        # ======================================
        # 圖檔轉Base64
        def imgBase64(img):
            import base64
            from io import BytesIO
        
            img_fp = BytesIO()
            img.save(img_fp, format='png')
            img_b64 = base64.encodebytes(img_fp.getvalue()).decode()
            img_b64 = 'data:image/png;base64,%s' % (str(img_b64))
        
            return img_b64

        # 預測上傳圖片
        import time
        from PIL import Image
        from django.core.files.storage import FileSystemStorage
        
        upload_file = request.FILES['upload_img'] if 'upload_img' in request.FILES else None
        fs = FileSystemStorage()
        nowTime = int(time.time())
        img_ext = upload_file.name.split('.')[-1]
        imgname = f"{nowTime}.{img_ext}"
        imgname = fs.save(imgname, upload_file)
        imgpath = str(settings.MEDIA_ROOT / imgname)
        img = Image.open(imgpath) # 開啟圖片

        # 預測圖檔
        pred_id, pred_np = cifar10_predict(img, imgpath)
        logger.debug(f"pred_id : {pred_id}")
        label_dict = get_labels_dict()

        # 各類預測機率
        # pred_np = np.around(pred_np*100, decimals=2)
        pred_np = pred_np*100
        pred_list = [round(i, 2) for i in pred_np]
        pred_dict = dict(zip(range(pred_np.size), pred_list))

        context = {
            'pred_id' : pred_id,
            'pred_dict' : pred_dict.items(),
            'label_dict' : label_dict.items(),
            'upload_image' : imgBase64(img), # 原圖轉 Base64
        }

        # 刪除png圖檔
        try:
            os.remove(imgpath)
        except OSError as e:
            logger.debug("Error: %s : %s" % (imgpath, e.strerror))

        return render(request, "cifar10_exe.html", context)
    else:
        # ======================================
        # cifar10 主頁顯示
        # ======================================
        return render(request, "cifar10.html")

def cifar10_predict(img, imgpath):
    import cv2
    from . import util_modules as util

    # 讀取預測圖片原始檔
    img = img.resize((32, 32)) # 調整圖片尺寸為 32x32
    img_png_path = imgpath.split('.')[0] + '_' + util.get_random_str() + '.png'
    img.save(img_png_path)

    # 讀取影像並正規化
    test_data = []
    img_cv2 = cv2.imread(img_png_path)
    test_data.append(img_cv2)

    # # 正規化
    test_data = np.array(test_data)/255
    
    # # 預測
    model = cifar10_model() # 模型架構
    model.load_weights(settings.STATIC_ROOT + "/cifar10_weights.h5")
    pred = model.predict(test_data)
    pred_id = np.argmax(pred, axis=1)[0]

    # 刪除png圖檔
    try:
        os.remove(img_png_path)
    except OSError as e:
        logger.debug("Error: %s : %s" % (img_png_path, e.strerror))

    return pred_id, pred[0]

def get_labels_dict():
    # larr = ['airplane','automobile','bird','cat','deer','dog','frog','horse','ship','truck']
    larr = ['飛機','汽車','鳥','貓','鹿','狗','青蛙','馬','船','卡車']
    label_dict = dict(zip(range(10), larr))
    
    return label_dict

def cifar10_model():
    from keras.models import Sequential
    from keras.layers import Dense, Flatten, Dropout
    from keras.layers import Conv2D, MaxPooling2D

    # 宣告這是一個 Sequential 循序性的深度學習模型
    model = Sequential()
    # 加入輸入層和卷積層
    model.add(Conv2D(filters=32, kernel_size=(3,3), input_shape=(32, 32, 3), activation='relu', padding='same'))
    model.add(Conv2D(filters=32, kernel_size=(3,3), activation='relu', padding='same'))
    model.add(MaxPooling2D(pool_size=(2,2))) # 加入池化層
    model.add(Dropout(0.2)) # 加入 Dropput
    
    model.add(Conv2D(filters=64, kernel_size=(3,3), activation='relu', padding='same'))
    model.add(Conv2D(filters=64, kernel_size=(3,3), activation='relu', padding='same'))
    model.add(MaxPooling2D(pool_size=(2,2))) # 加入池化層
    model.add(Dropout(0.2)) # 加入 Dropput
    
    model.add(Conv2D(filters=128, kernel_size=(3,3), activation='relu', padding='same'))
    model.add(Conv2D(filters=128, kernel_size=(3,3), activation='relu', padding='same'))
    model.add(MaxPooling2D(pool_size=(2,2))) # 加入池化層
    model.add(Dropout(0.2)) # 加入 Dropput
    
    # 加入平坦層
    model.add(Flatten())
    model.add(Dense(512, activation='relu')) # 加入全連接層
    model.add(Dropout(0.4)) # 加入 Dropput
    model.add(Dense(512, activation='relu')) # 加入全連接層
    model.add(Dropout(0.4)) # 加入 Dropput
    model.add(Dense(256, activation='relu')) # 加入全連接層
    model.add(Dropout(0.4)) # 加入 Dropput
    # 加入輸出層
    model.add(Dense(10, activation='softmax'))
    
    return model