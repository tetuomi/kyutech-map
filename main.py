from flask import Flask, redirect, request, render_template, url_for, flash, session
from PIL import Image
from werkzeug import secure_filename
import os, io
import base64


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join("file://", os.getcwd(), 'uploads')
app.secret_key = 'ahiahi'


def pla_num(number):
    if number == 0:
        return '銅像'
    elif number == 33:
        return '図書館'
    elif number == 55:
        return '食堂'

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
                image = Image.open(img)
                buf = io.BytesIO()
                image.save(buf, 'png')
                qr_b64str = base64.b64encode(buf.getvalue()).decode("utf-8")
                qr_b64data = "data:image/png;base64,{}".format(qr_b64str)

                number = 55

                return render_template('predict.html', img=qr_b64data, number=number, place=pla_num(number))

    else:
        return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host='0.0.0.0')


