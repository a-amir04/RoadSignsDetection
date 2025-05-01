import os
import time
import shutil
from moviepy.editor import *
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'asf', 'avi', 'gif', 'm4v', 'mkv', 'mov', 'mp4', 'mpeg', 'mpg', 'ts', 'wmv'}

app = Flask(__name__, static_folder='static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # проверим, передается ли в запросе файл
        if 'file' not in request.files:
            # После перенаправления на страницу загрузки
            # покажем сообщение пользователю
            flash('Cannot read the file.')
            return redirect(request.url)
        file = request.files['file']
        # Если файл не выбран, то браузер может
        # отправить пустой файл без имени.
        if file.filename == '':
            flash('File not found.')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect('http://127.0.0.1:5000/video')
        else:
            flash('Format of video is incorrect.')
            return redirect('http://127.0.0.1:5000')
    return render_template('main.html')

@app.route('/video', methods=['GET', 'POST'])
def video():
    if request.method == 'POST':
        os.system('python track.py --yolo_model best.pt --save-vid --save-txt')
        get_files = os.listdir('runs/track')
        clip = VideoFileClip('runs/track/'+get_files[-1]+'/video.mp4')
        clip.write_videofile('static/video.mp4', fps=30)
        shutil.copyfile('runs/track/' + get_files[-1] + '/tracks/video.txt',
                        'static/video.txt')
        return redirect('http://127.0.0.1:5000/result')
    return render_template('video.html')

@app.route('/result', methods=['GET', 'POST'])
def result():
    if request.method == 'POST':
        os.remove('C:/Biometry-master/static/uploads/video.mp4')
        os.remove('C:/Biometry-master/static/video.txt')
        os.remove('C:/Biometry-master/static/video.mp4')
        shutil.rmtree('C:/Biometry-master/runs/track/best_osnet_x0_25')
        return redirect('http://127.0.0.1:5000')
    return render_template('result.html')

if __name__ == '__main__':
    app.secret_key = os.urandom(24)
    app.run()