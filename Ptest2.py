import os
import cv2
import math
from flask import Flask, request, render_template
from flask_dropzone import Dropzone


pathh = "D:/PythonCH/Flask-test/upload/"

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config.update(
    UPLOADED_PATH=os.path.join(basedir, 'upload'),
    # Flask-Dropzone config:
    DROPZONE_ALLOWED_FILE_TYPE='image',
    DROPZONE_MAX_FILE_SIZE=3,
    DROPZONE_MAX_FILES=30,
)
dropzone = Dropzone(app)


@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        for f in request.files.getlist('file'):
            atpath = pathh+f.filename
            btpath = f.filename
            if not os.path.isfile(atpath):
                ctpath = os.path.splitext(btpath)[0]
                f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))
            elif os.path.isfile(atpath):
                for count in range(1, 201):
                    ctpath = os.path.splitext(btpath)[0] + "_%d" % count
                    dtpath = pathh + ctpath + os.path.splitext(btpath)[-1]
                    etpath = ctpath + os.path.splitext(btpath)[-1]
                    if os.path.isfile(dtpath):
                        continue
                    else:
                        f.save(os.path.join(app.config['UPLOADED_PATH'], dtpath))
                        f.filename = etpath
                        break
#無法使重複檔案建立新名稱
        folder_path = "D:/PythonCH/Flask-test/upload/cut/" + ctpath + "/"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        img = cv2.imread("D:/PythonCH/Flask-test/upload/%s" % f.filename)
        w = 256
        h = 256
        sp = img.shape
        sz1 = sp[0]  # height(rows) of image
        sz2 = sp[1]  # width(columns) of image
        num_x = math.ceil(sz2 / w)
        num_y = math.ceil(sz1 / h)

        # 裁切區域的 x 與 y 座標（左上角）
        for count_y in range(num_y):
            for count_x in range(num_x):
                x = count_x * 256
                y = count_y * 256
                # 裁切圖片
                if (count_x + 1) * 256 > sz2:
                    crop_img = img[y:y + h, x:sz2]

                elif (count_y + 1) * 256 > sz1:
                    crop_img = img[y:sz1, x:x + w]

                elif (count_x + 1) * 256 > sz2 and (count_y + 1) * 256 > sz2:
                    crop_img = img[y:sz1, x:sz2]

                else:
                    crop_img = img[y:y + h, x:x + w]

                number = count_y * num_y + count_x + 1
                cv2.imwrite(folder_path + '%d_' % number + '%s' % f.filename, crop_img)

    return render_template('Ptest2.html')


@app.route('/SegNet', methods=['POST'])
def segnet():
    if request.method=='POST':
        os.system("python test4.py")
        return render_template('test3.html')


@app.route('/ResNet', methods=['POST'])
def resnet():
    if request.method=='POST':
        return render_template('test3.html')


@app.route('/VGG', methods=['POST'])
def vgg():
    if request.method=='POST':
        return render_template('test3.html')



if __name__ == '__main__':
    app.run(debug=True)
