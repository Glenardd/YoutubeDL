from flask import Flask, render_template, request, url_for, redirect
from  pytube import YouTube
import urllib.parse
import os

app = Flask(__name__)
app.secret_key = '272727'
# Routes are here
@app.route("/", methods=['GET','POST'])
def index():

    if request.method == "POST":
        url_one = request.form['video-url']
        
        encoded_url = urllib.parse.quote(url_one, safe='')

        print('------------------')
        print('-------encoded--------')
        print(encoded_url)
        print('------------------')
        print('------------------')

        return redirect(url_for('response', url=encoded_url))

        # yt = YouTube(str(url_one))
        # thumbnail_link = yt.thumbnail_url
        # title = yt.title

    else:
        return render_template('index.html')

@app.route('/response/<url>', methods=['GET'])
def response(url):
    encode_url = urllib.parse.unquote(url)
    url_str = str(encode_url)

    print('------------------')
    print('-------unquoted---------')
    print(url_str)
    print('------------------')
    print('------------------')

    
    yt = YouTube(url_str)
    thumbnail = yt.thumbnail_url
    title = yt.title

    return render_template('response.html', thumbnail=thumbnail, title=title)

        
@app.route('/download' ,methods=['POST', 'GET'])
def download():
        if request.method == "POST":
            if 'link_yt' in session:
                link_url = session['link_yt']

                yt = YouTube(str(link_url))
                thumbnail = yt.thumbnail_url
                title = yt.title

                download_dir = f"{os.getenv('USERPROFILE')}\\Downloads"

                yt.streams.filter(progressive=True).get_by_resolution('720p').download(download_dir)

                return render_template('response.html', thumbnail=thumbnail, title=title)
            else:
                return redirect(url_for('index'))
            
@app.route('/return', methods=['POST', 'GET'])
def Return():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")