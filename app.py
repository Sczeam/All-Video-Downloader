import os
from flask import Flask, render_template, request, send_file
import subprocess

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

    # Use yt-dlp to fetch video title
    cmd_title = f'yt-dlp --get-title --no-warnings {url}'
    result = subprocess.run(cmd_title, capture_output=True, text=True, shell=True)
    video_title = result.stdout.strip()

    # Get the absolute path of the "downloads" folder on the server
    downloads_folder = os.path.abspath('downloads')

    # Construct the full file path on the server
    file_path = os.path.join(downloads_folder, f'{video_title}.{extension}')

    # Construct the command to download the video
    cmd = f'yt-dlp {format_option} --output "{file_path}" {url}'
    subprocess.run(cmd, shell=True)

    # Check if the file exists on the server
    if os.path.exists(file_path):
        # Send the file to the client for download
        return send_file(file_path, as_attachment=True)

    # If the file doesn't exist, you can handle the error here, e.g., show an error page.
    return "File not found.", 404

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
