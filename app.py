import os
from flask import Flask, request, render_template
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from transformers import pipeline
from dotenv import load_dotenv
import urllib.request
from gpt4all import GPT4All
import time

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg']) 

app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']
app.config['UPLOAD_FOLDER'] = 'static/uploads/' 
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate(filepath, filename):
    # process image
    captioner = pipeline('image-to-text',model='nlpconnect/vit-gpt2-image-captioning')
    description = captioner(filepath)[0]['generated_text']
    # generate story
    model = GPT4All('orca-mini-3b.ggmlv3.q4_0.bin')
    prompt = 'Write a story about ' + description[:-1] + ':'
    result = model.generate(prompt, max_tokens=1000,temp=0.7, top_k=40, top_p=0.1, repeat_penalty=1.18, repeat_last_n=64, n_batch=8, n_predict=None, streaming=False)
    return render_template('results.html', filename=filename, result=result)

filename = 'cat.jpg'
filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

@app.route('/app', methods=['GET', 'POST'])
def form():
    if request.method == 'GET':
        # filename using current time
        global filename
        global filepath
        filename = time.strftime('%Y%m%d-%H%M%S')
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        urllib.request.urlretrieve('https://picsum.photos/600/400', filepath)
        return render_template('form.html', imgpath=filepath)
    else:
        if 'file' not in request.files:
            return generate(filepath, filename)
        
        file = request.files['file']
        if file.filename == '':
            return generate(filepath, filename)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            return generate(filepath, filename)
        else:
            flash('Allowed extensions: png, jpg, jpeg')
            return redirect(request.url)

@app.route('/display/<filename>')
def display_image(filename):
	return redirect(url_for('static', filename='uploads/' + filename), code=301)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    load_dotenv()
    app.run()