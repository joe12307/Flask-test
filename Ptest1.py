import os
import cv2
import math
from flask import send_from_directory
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'D:/PY'
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif', 'PNG'])


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('test1.html', template_folder='./')


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        uploaded_files = request.files.getlist("file[]")
        filenames = []
    for file in uploaded_files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],
                                   filename))
            filenames.append(filename)
    img = cv2.imread("D:/PY/%s" % filename)
    w = 128
    h = 128
    sp = img.shape
    sz1 = sp[0]  # height(rows) of image
    sz2 = sp[1]  # width(columns) of image
    num_x = math.ceil(sz2 / w)
    num_y = math.ceil(sz1 / h)

    # 裁切區域的 x 與 y 座標（左上角）
    for count_y in range(num_y):
        for count_x in range(num_x):
            x = count_x * 128
            y = count_y * 128
            # 裁切圖片
            if (count_x + 1) * 128 > sz2:
                crop_img = img[y:y + h, x:sz2]

            elif (count_y + 1) * 128 > sz1:
                crop_img = img[y:sz1, x:x + w]

            elif (count_x + 1) * 128 > sz2 and (count_y + 1) * 128 > sz2:
                crop_img = img[y:sz1, x:sz2]

            else:
                crop_img = img[y:y + h, x:x + w]

            number = count_y * num_y + count_x + 1
            cv2.imwrite('D:/PY/PY_PIC/%d_' % number + '%s' % filename, crop_img)

    return render_template('test1.html', filenames=filenames)


@app.route('/upload/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


if __name__ == '__main__':
    app.run(debug=True)
