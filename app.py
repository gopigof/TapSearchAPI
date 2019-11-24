from flask import Flask, render_template, request, send_from_directory
from PyPDF2 import PdfFileReader
from IndexClass import TapSearchAPI
from timeit import default_timer
import os
import glob

UPLOAD_FOLDER = 'files'
ALLOWED_EXT = {'pdf': 'pdf', 'img': ['png', 'jpeg', 'jpg']}
FILE_NAMES = []

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
api_object = TapSearchAPI()


@app.route('/', methods=['GET'])
def base():
    return render_template('base.html')


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/indexing_done', methods=['GET', 'POST'])
def indexing_done():
    if request.method == 'POST':
        text = request.form['text']
        api_object.index(text)
        return render_template('indexing_done.html')


@app.route('/viewindex', methods=['GET', 'POST'])
def viewindex():
    return render_template('viewindex.html', result=api_object.InvertedIndex)


@app.route('/search')
def search():
    return render_template('search.html')


@app.route('/searchresult', methods=['POST', 'GET'])
def searchresult():
    if request.method == 'POST':
        initial_time = default_timer()
        keyword = request.form['keyword']
        result = [(k, v, k.split()[0]) for k,v in api_object.search(keyword)]
        print(f'Time elapsed for Search {keyword}: {default_timer() - initial_time}')
        return render_template('searchresult.html', result={'key':keyword, 'res':result})


@app.route('/clear')
def clear():
    api_object.clear()
    files = glob.glob(os.path.join(os.getcwd(), 'files', '*'))
    for f in files:
        os.remove(f)
    print(glob.glob(os.getcwd()+app.config['UPLOAD_FOLDER']))
    return render_template('clear.html')


@app.route('/upload')
def upload():
    return render_template('upload.html')


@app.route('/upload_process', methods=['GET', 'POST'])
def upload_process():
    if request.method == 'POST':
        file = request.files.getlist('file')
        print(file)
        for f in file:
            if f.filename[-3:] == 'pdf':
                if f.filename in FILE_NAMES:
                    f.filename = f.filename+api_object.char_generate()
                FILE_NAMES.append(f.filename)
                f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
                pdf_object = PdfFileReader(f)
                text = ''
                for i in range(pdf_object.getNumPages()):
                    text += pdf_object.getPage(i).extractText()
                api_object.index(text, name=f.filename)
                print(api_object.InvertedIndex)

            elif f.filename[-3] in ALLOWED_EXT['img']:
                if f.filename in FILE_NAMES:
                    f.filename = f.filename + api_object.char_generate()
                FILE_NAMES.append(f.filename)
                f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
                api_object.image(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))

            else:
                print(f'Error {f} is not a pdf. Please enter a PDF')
        return render_template('indexing_done.html')


@app.route('/files/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], as_attachment=True, filename=filename)


if __name__ == '__main__':
    app.run(debug=True)
