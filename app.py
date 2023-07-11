import os
from flask import Flask, request, render_template
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from transformers import pipeline
from dotenv import load_dotenv
from gpt4all import GPT4All

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg']) 

app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']
app.config['UPLOAD_FOLDER'] = 'static/uploads/' 
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('form.html')
    else:
        if 'file' not in request.files:
            flash('No images uploaded')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No images uploaded')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # process images
            captioner = pipeline("image-to-text",model="nlpconnect/vit-gpt2-image-captioning")
            description = captioner(filepath)[0]['generated_text']
            model = GPT4All('orca-mini-3b.ggmlv3.q4_0.bin')
            prompt = 'Write a story about ' + description + ':'
            result = model.generate(prompt, max_tokens=5000,temp=0.7, top_k=40, top_p=0.1, repeat_penalty=1.18, repeat_last_n=64, n_batch=8, n_predict=None, streaming=False)
            return render_template('results.html', filename=filename, result=result)
        else:
            flash('Allowed extensions: png, jpg, jpeg')
            return redirect(request.url)

@app.route('/display/<filename>')
def display_image(filename):
	return redirect(url_for('static', filename='uploads/' + filename), code=301)

@app.route('/dashboard')
def dashboard():
    return render_template('index.html')

if __name__ == '__main__':
    load_dotenv()
    app.run()