from flask import Flask, request, render_template, url_for
from PIL import Image
import os, io
import base64


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join("file://", os.getcwd(), 'uploads')

def pla_num(number):
    if number == 0:
        return '銅像'
    elif number == 33:
        return '図書館'
    elif number == 55:
        return '食堂'

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        return redirect(url_for('predict'))
    else:
        return render_template('index.html')


@app.route('/predict', methods=['GET','POST'])
def predict():
    img = request.files["file"]
    image = Image.open(img)
    buf = io.BytesIO()
    image.save(buf, 'png')
    qr_b64str = base64.b64encode(buf.getvalue()).decode("utf-8")
    qr_b64data = "data:image/png;base64,{}".format(qr_b64str)

    number = 55

    return render_template('predict.html', img=qr_b64data, number=number, place=pla_num(number))


if __name__ == "__main__":
    app.run(port=8000, debug=True)


