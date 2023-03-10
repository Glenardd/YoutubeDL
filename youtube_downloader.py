from flask import Flask, render_template, request, url_for, redirect, send_file, session
from  pytube import YouTube
from io import BytesIO

app = Flask(__name__)

app.secret_key = 'mysecret'

# Routes are here
@app.route("/", methods=['GET','POST'])
def index():

    if request.method == "POST":
        session['url'] = request.form['video-url']

        return redirect(url_for('response'))

    else:
        return render_template('index.html')

@app.route('/response', methods=["POST", "GET"])
def response():
    
    url = session.get('url')
    str_url = str(url)

    yt = YouTube(str_url)
    thumbnail = yt.thumbnail_url    
    title = yt.title

    stream = yt.streams.filter(progressive=True, mime_type='video/mp4')

    if request.method == "GET":
        return render_template('response.html', thumbnail_=thumbnail, title_=title,stream=stream)
    else:
        return redirect(url_for('download'))

@app.route('/download', methods=['POST'])
def download():

    buffer = BytesIO()

    url_ = session['url']
    select = request.form['resolution']
    str_url = str(url_)

    yt = YouTube(str_url)

    # video = yt.streams.filter(progressive=True, mime_type='video/mp4').get_lowest_resolution().stream_to_buffer(buffer)

    yt.streams.filter(progressive=True, mime_type='video/mp4').get_by_itag(select).stream_to_buffer(buffer)

    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name=f"{yt.title}.mp4" ,mimetype='video/mp4') 
   

@app.route('/return', methods=['POST'])
def Return():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)