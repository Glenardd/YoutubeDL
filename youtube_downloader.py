from flask import Flask, render_template, request, url_for, redirect, session
from  pytube import YouTube
from flask_session import Session
import os

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)

# Routes are here
@app.route("/", methods=['GET','POST'])
def index():

    if request.method == "POST":
        session['url_info'] = request.form.get('video-url')
        session['url_download'] = request.form.get('video-url')
        return redirect(url_for('response'))

    else:
        return render_template('index.html')

@app.route('/response', methods=["GET"])
def response():

    download_dir = f"{os.getenv('USERPROFILE')}\\Downloads"
    if 'url_info' in session:
        link = session['url_info']
        
        url_str = str(link)

        yt = YouTube(url_str)
        thumbnail = yt.thumbnail_url    
        title = yt.title

        return render_template('response.html', thumbnail_=thumbnail, title_=title)

    return redirect(url_for('index'))

@app.route('/download')
def download():

    if 'url_download' in session:
        url_link = session['url_download']
        yt = YouTube(url_link)

        download_dir = f"{os.getenv('USERPROFILE')}\\Downloads"

        yt.streams.filter(progressive=True).get_by_resolution('720p').download(download_dir)
    
    return redirect(url_for('response'))

@app.route('/return', methods=['POST'])
def Return():
    session['url_info'] = None
    session['url_download'] = None
    return redirect(url_for('index'))
    
if __name__ == '__main__':
    app.run(debug=True)