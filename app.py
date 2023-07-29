import os
from flask import Flask, render_template, request, send_file
import yt_dlp
import subprocess
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    download_format = request.form['format']

    if download_format == 'mp4':
        format_option = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
        extension = 'mp4'
    else:
        format_option = 'bestaudio/best'
        extension = 'mp3'
    
    # Use yt-dlp to fetch video title
    cmd_title = f'yt-dlp --get-title --no-warnings {url}'
    result = subprocess.run(cmd_title, capture_output=True, text=True, shell=True)
    video_title = result.stdout.strip()

    # Truncate video title if it exceeds the maximum filename length (e.g., 255 characters for FAT32)
    max_filename_length = 255
    if len(video_title) > max_filename_length:
        video_title = video_title[:max_filename_length]

    # Download video using yt-dlp
    ydl_opts = {
        'format': format_option,
         'playlist_items': '1',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        video_bytes = BytesIO(ydl.download([url]))

    # Send the file to the client for download
    return send_file(video_bytes, as_attachment=True, attachment_filename=f'{video_title}.{extension}')

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
