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
    if 'link' in session:
        link = session['link']
        link_= str(link)

        yt = YouTube(link_)
        thumbnail = yt.thumbnail_url
        title = yt.title

        return render_template('response.html', thumbnail=thumbnail, title=title, link=link)
    return redirect(url_for('index'))
    
        
@app.route('/download')
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
            
@app.route('/return')
def Return():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    # app.run(debug=True)
    