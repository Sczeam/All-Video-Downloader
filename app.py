import os
import shutil
from flask import Flask, render_template, request, send_file

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    format_choice = request.form['format']

    # Validate the user input and handle errors here if necessary

    # Download the video using yt-dlp
    temp_dir = 'temp_downloads'  # Create a temporary directory to store the downloaded file
    os.makedirs(temp_dir, exist_ok=True)

    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',  # Use the best quality available
        'outtmpl': os.path.join(temp_dir, 'video.mp4'),  # Set the output filename directly
        'progress_hooks': [],  # Avoid printing progress to the console
        'playlist_items': '1',
    }

    import yt_dlp
    current_directory = os.getcwd()  # Get the current working directory
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    # Change the working directory back to the original directory
    os.chdir(current_directory)

    # Move the downloaded file to the client's downloads folder
    downloads_folder = os.path.expanduser('~')  # Get the absolute path to the Downloads folder
    shutil.move(os.path.join(temp_dir, 'video.mp4'), os.path.join(downloads_folder, 'video.mp4'))

    # Clean up temporary files
    os.rmdir(temp_dir)

    # Return the file for download to the client
    return send_file(
        os.path.join(downloads_folder, 'video.mp4'),
        as_attachment=True,
        download_name='video.mp4'
    )

if __name__ == '__main__':
    app.run(debug=True)
