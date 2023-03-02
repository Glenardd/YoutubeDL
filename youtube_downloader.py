from flask import Flask, render_template, request, url_for, redirect, session
from  pytube import YouTube
import os

app = Flask(__name__)
app.secret_key = '272727'

# Routes are here
@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        url = request.form['video-url']
        session['link'] = url
        session['link_yt'] = url

        return redirect(url_for('response'))
    else:
        return render_template('index.html')

@app.route('/response')
def response():
    try:
        if 'link' in session:
            link = session['link']
            link_= str(link)

            yt = YouTube(link_)
            thumbnail = yt.thumbnail_url
            title = yt.title

            return render_template('response.html', thumbnail=thumbnail, title=title, link=link)
        else:
            return redirect(url_for('index'))
    except:
        return redirect(url_for('index'))
    
        
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
    app.run(debug=False, host="0.0.0.0")