from flask import Flask, render_template, request, url_for, redirect, send_file
from  pytube import YouTube
import os
import urllib.parse
from io import BytesIO

app = Flask(__name__)

# Routes are here
@app.route("/", methods=['GET','POST'])
def index():

    if request.method == "POST":
        url_ = urllib.parse.quote(request.form['video-url'], safe='')

        return redirect(url_for('response', url=url_))

    else:
        return render_template('index.html')

@app.route('/response/<string:url>', methods=["POST", "GET"])
def response(url):
        
    encoded_url = urllib.parse.unquote(url)
    str_url = str(encoded_url)

    yt = YouTube(str_url)
    thumbnail = yt.thumbnail_url    
    title = yt.title

    if request.method == "GET":
        return render_template('response.html', thumbnail_=thumbnail, title_=title, url=str(encoded_url))
    else:
        return redirect(url_for('download'))

@app.route('/download', methods=['POST'])
def download():

    buffer = BytesIO()

    url_ = request.form['video-url']
    str_url = str(url_)

    yt = YouTube(str_url)
    
    if os.name == 'nt':
        download_dir = f"{os.getenv('USERPROFILE')}//Downloads"

    video = yt.streams.filter(progressive=True).get_by_resolution('720p')

    video.stream_to_buffer(buffer)
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name=f"{yt.title}.mp4" ,mimetype='video/mp4') 
   

@app.route('/return', methods=['POST'])
def Return():
    return redirect(url_for('index'))
    
if __name__ == '__main__':
    app.run(debug=True)