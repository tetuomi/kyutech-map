from flask import Flask, redirect, request, render_template, url_for, flash, session
from keras.backend import tensorflow_backend as backend
from PIL import Image
from werkzeug import secure_filename
import os, io
import base64
from tensorflow.keras.models import model_from_json
import glob
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join("file://", os.getcwd(), 'uploads')
app.secret_key = 'ahiahi'


def pla_num(number):
    if number == 0:
        return '銅像'
    elif number == 3:
        return '教育研究4号棟'
    elif number == 15:
        return '総合研究1号棟'
    elif number == 26:
        return '未来型インタラクティブ教育棟'
    elif number == 33:
        return '図書館'
    elif number == 52:
        return '鳳龍会館'
    elif number == 55:
        return '食堂'
    elif number == 62:
        return 'ものつくり工房'
    elif number == 64:
        return '体育館'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['GET','POST'])
def predict():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(url_for('index'))
        else:
            img = request.files["file"]
            filename = secure_filename(img.filename)
            
            if filename == '':
                flash('ファイルがないお')
                return redirect(url_for('index'))
            else:
                backend.clear_session() # 2回以上連続してpredictするために必要な処理
                # モデルの読み込み
                model = model_from_json(open('and.json', 'r').read())
                
                # 重みの読み込み
                model.load_weights('and_weight.hdf5')
                

                image_size = 60
                
                image = Image.open(img)
                image = image.convert("RGB")
                image = image.resize((image_size, image_size))
                data = np.asarray(image)
                X = np.array(data)
                X = X.astype('float32')
                X = X / 255.0
                X = X[None, ...]
                
                # ぜひともexpected_valueに期待値が0.5未満で0が入るような関数かなんか作って欲しいです。とりあえず今は強制で1入れておきます
                expected_value = 1

                if expected_value == 0:
                    flash('判別不可！もう一回！')
                else:
                    prd = model.predict(X).argmax(axis=1)
                    print(type(prd))
                    ans = [33, 55, 0]
                    number = ans[int(prd)]

                    image = Image.open(img)
                    buf = io.BytesIO()
                    image.save(buf, 'png')
                    qr_b64str = base64.b64encode(buf.getvalue()).decode("utf-8")
                    qr_b64data = "data:image/png;base64,{}".format(qr_b64str)



                    return render_template('predict.html', img=qr_b64data, number=number, place=pla_num(number))

    else:
        return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host='0.0.0.0')


