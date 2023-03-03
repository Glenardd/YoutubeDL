from flask import Flask, render_template, request, url_for, redirect, session, send_file
from  pytube import YouTube
from flask_session import Session
import os
import urllib.parse

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"

Session(app)

# Routes are here
@app.route("/", methods=['GET','POST'])
def index():

    if request.method == "POST":
        url_ = urllib.parse.quote(request.form['video-url'], safe='')

        session['url_download'] = request.form.get('video-url')

        return redirect(url_for('response', url=url_))

    else:
        return render_template('index.html')

@app.route('/response/<url>', methods=["GET"])
def response(url):

    download_dir = f"{os.getenv('USERPROFILE')}\\Downloads"
    
    encoded_url = urllib.parse.unquote(url)
    str_url = str(encoded_url)

    yt = YouTube(str_url)
    thumbnail = yt.thumbnail_url    
    title = yt.title

    return render_template('response.html', thumbnail_=thumbnail, title_=title)

@app.route('/download', methods=['GET'])
def download():

    if 'url_download' in session:
        url_link = session['url_download']

        link =urllib.parse.quote(url_link,safe='')

        yt = YouTube(str(url_link))

        download_dir = f"{os.getenv('USERPROFILE')}\\Downloads"

        return send_file(yt.streams.filter(progressive=True).get_by_resolution('720p').download(download_dir), as_attachment=True)

@app.route('/return', methods=['POST'])
def Return():
    session['url_download'] = None
    return redirect(url_for('index'))
    
if __name__ == '__main__':
    app.run(debug=True)