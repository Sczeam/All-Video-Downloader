import os
import shutil
import yt_dlp
from flask import Flask, render_template, request, send_file, make_response, jsonify
from yt_dlp.utils import DownloadError

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    format_choice = request.form['format']

    # Validate the user input and handle errors here if necessary

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
            # 'ext': 'mp3',  # Explicitly specify the extension for MP3 downloads
        }
    else:
        ydl_opts = {
            "quiet": True,
            'format': 'bestvideo+bestaudio/best',
            "merge_output_format": "mp4",
            # 'writethumbnail':True,
            'outtmpl': os.path.join(temp_dir, 'video.%(ext)s'),
            'progress_hooks': [],
            'playlist_items': '1',
        }

    
    current_directory = os.getcwd()  # Get the current working directory
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except DownloadError as e:
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
    response.set_cookie('downloadCompleted', 'true')

    return response
def mark_download_completed(response):
    response.headers['Content-Disposition'] = 'attachment; filename=' + filename
    # Set the downloadCompleted flag to true (using a hidden input field)
    response.set_cookie('downloadCompleted', 'true')
    return response

@app.route('/check_download_completion')
def check_download_completion():
    # Check if the downloadCompleted cookie is set to true
    download_completed = request.cookies.get('downloadCompleted', False)
    return jsonify(download_completed)

@app.route('/termandcondition')
def termandcondition():
    return render_template('termandcondition.html')

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

if __name__ == '__main__':
    app.run(debug=True)
