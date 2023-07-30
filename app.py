import os
import shutil
import yt_dlp
from flask import Flask, render_template, request, send_file, make_response

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    format_choice = request.form['format']

    # Download the video/audio using yt-dlp
    temp_dir = 'temp_downloads'  # Create a temporary directory to store the downloaded file
    os.makedirs(temp_dir, exist_ok=True)

    if format_choice == 'mp3':
        ydl_opts = {
            "quiet": True,
            'format': 'bestaudio[ext=m4a]/best',
            'outtmpl': os.path.join(temp_dir, 'audio.mp3'),
            'progress_hooks': [],
            'playlist_items': '1',
        }
    else:
        ydl_opts = {
            "quiet": True,
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best',
            "merge_output_format": "mp4",
            'outtmpl': os.path.join(temp_dir, 'video.%(ext)s'),
            'progress_hooks': [],
            'playlist_items': '1',
        }

    current_directory = os.getcwd()  # Get the current working directory
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except yt_dlp.utils.DownloadError as e:
        # Handle the error gracefully
        error_message = "The video cannot be downloaded from Instagram currently. Please try again later or download from another URL."
        return render_template('error.html', error_message=error_message)

    # Change the working directory back to the original directory
    os.chdir(current_directory)

    # Move the downloaded file to the client's downloads folder
    downloads_folder = os.path.expanduser('~')  # Get the absolute path to the Downloads folder
    if format_choice == 'mp3':
        filename = 'audio.mp3'
    else:
        filename = 'video.mp4'
    shutil.move(os.path.join(temp_dir, filename), os.path.join(downloads_folder, filename))

    # Clean up temporary files
    # shutil.rmtree(temp_dir)

    # Return the file for download to the client
    response = make_response(send_file(
        os.path.join(downloads_folder, filename),
        as_attachment=True,
        download_name=filename,
    ))
    response.set_cookie('downloadCompleted', 'true')  # Set the downloadCompleted cookie

    return response

@app.route('/termandcondition')
def termandcondition():
    return render_template('termandcondition.html')

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

if __name__ == '__main__':
    app.run(debug=True)
