import subprocess
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    download_format = request.form['format']

    if download_format == 'mp4':
        format_option = '--format bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
        extension = 'mp4'
    else:
        format_option = '--format bestaudio/best'
        extension = 'mp3'

    cmd = f'yt-dlp {format_option} --output "downloads/%(title)s.{extension}" {url}'
    subprocess.run(cmd, shell=True)

    return redirect(url_for('index'))

# Route for Terms and Conditions page
@app.route('/termandcondition')
def terms_and_conditions():
    return render_template('termandcondition.html')

# Route for About Us page
@app.route('/aboutus')
def about_us():
    return render_template('aboutus.html')

if __name__ == '__main__':
    app.run(debug=True)
