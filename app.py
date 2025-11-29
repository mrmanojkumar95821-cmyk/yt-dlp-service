from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'status': 'running',
        'message': 'yt-dlp API service',
        'endpoints': {
            '/download': 'Get video URL - ?url=YOUTUBE_URL&quality=1080'
        }
    })

@app.route('/download', methods=['GET'])
def download():
    video_url = request.args.get('url')
    quality = request.args.get('quality', '1080')

    if not video_url:
        return jsonify({'error': 'Missing url parameter'}), 400

    try:
        # ✅ import yt_dlp inside function (faster startup)
        import yt_dlp

        ydl_opts = {
            'format': 'best[ext=mp4]/best',
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)

            if 'formats' in info:
                formats = info['formats']
                video_formats = [
                    f for f in formats if f.get('vcodec') != 'none' and f.get('ext') == 'mp4'
                ]
                video_formats.sort(key=lambda x: x.get('height', 0), reverse=True)

                if video_formats:
                    best_format = video_formats[0]
                    return jsonify({
                        'success': True,
                        'url': best_format['url'],
                        'video_id': info.get('id'),
                        'title': info.get('title'),
                        'duration': info.get('duration'),
                        'quality': best_format.get('height'),
                        'format': best_format.get('format_note')
                    })

            if 'url' in info:
                return jsonify({
                    'success': True,
                    'url': info['url'],
                    'video_id': info.get('id'),
                    'title': info.get('title'),
                    'duration': info.get('duration')
                })

            return jsonify({'error': 'No suitable format found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    # ✅ Render dynamically assigns PORT
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
