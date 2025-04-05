import os
import json
import sys
import time
import random
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_from_directory, abort
import logging
from logging.handlers import RotatingFileHandler

# Add parent directory to path to import our modules
sys.path.append('/home/ubuntu')
try:
    from data_collection_module import CollegeDataScraper, CampusImageCollector, TrendingAudioTracker
    from video_generation_module import RankingFormatter, VideoCompositionEngine, AudioIntegrationSystem
except ImportError as e:
    print(f"Error importing modules: {e}")

# Configure logging
log_dir = '/home/ubuntu/web_interface/logs'
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'app.log')

logger = logging.getLogger('college_video_app')
logger.setLevel(logging.INFO)
handler = RotatingFileHandler(log_file, maxBytes=10485760, backupCount=5)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Create Flask app
app = Flask(__name__)

# Create necessary directories
os.makedirs('/home/ubuntu/web_interface/static/videos', exist_ok=True)
os.makedirs('/home/ubuntu/web_interface/static/images', exist_ok=True)
os.makedirs('/home/ubuntu/web_interface/static/data', exist_ok=True)

# Global variables to store pipeline state
pipeline_status = {
    "data_collection": "not_started",
    "video_generation": "not_started",
    "last_run": None,
    "videos_generated": []
}

# Default audio moods in case file loading fails
DEFAULT_AUDIO_MOODS = {
    "Sad": ["Weightless - Marconi Union", "Sad Piano Melody", "Melancholy Strings"],
    "Calm": ["Gentle Waves", "Soft Piano", "Morning Coffee"],
    "Ambient": ["Space Ambient", "Forest Sounds", "Night Atmosphere"],
    "Inspirational": ["Rising Hope", "Epic Journey", "New Beginnings"]
}

# Load ranking categories
def load_ranking_categories():
    try:
        with open('/home/ubuntu/college_ranking_categories.md', 'r') as f:
            content = f.read()
            
        categories = []
        current_section = None
        
        for line in content.split('\n'):
            if line.startswith('## '):
                current_section = line[3:].strip()
            elif line.startswith('- **') and '**' in line:
                category = line.split('**')[1].strip()
                if current_section and category:
                    categories.append({
                        "name": category,
                        "section": current_section
                    })
        
        # If no categories were found, provide some defaults
        if not categories:
            categories = [
                {"name": "Most Beautiful Campuses", "section": "Campus Features"},
                {"name": "Top National Universities", "section": "Academic Rankings"},
                {"name": "Best College Dorms", "section": "Student Life"},
                {"name": "Happiest Students", "section": "Student Life"},
                {"name": "Best Campus Food", "section": "Student Life"},
                {"name": "Most Beautiful Ivy League Campuses", "section": "Elite Schools"},
                {"name": "Best Student Life", "section": "Student Life"}
            ]
        
        return categories
    except Exception as e:
        logger.error(f"Error loading ranking categories: {e}")
        # Return default categories if file loading fails
        return [
            {"name": "Most Beautiful Campuses", "section": "Campus Features"},
            {"name": "Top National Universities", "section": "Academic Rankings"},
            {"name": "Best College Dorms", "section": "Student Life"},
            {"name": "Happiest Students", "section": "Student Life"},
            {"name": "Best Campus Food", "section": "Student Life"},
            {"name": "Most Beautiful Ivy League Campuses", "section": "Elite Schools"},
            {"name": "Best Student Life", "section": "Student Life"}
        ]

# Load audio tracks
def load_audio_tracks():
    try:
        with open('/home/ubuntu/trending_audio_tracks.md', 'r') as f:
            content = f.read()
            
        tracks = []
        current_section = None
        
        for line in content.split('\n'):
            if line.startswith('## '):
                current_section = line[3:].strip()
            elif line.startswith('- **') and '**' in line:
                track = line.split('**')[1].strip()
                if current_section and track:
                    tracks.append({
                        "name": track,
                        "mood": current_section
                    })
        
        # If no tracks were found, use defaults
        if not tracks:
            for mood, mood_tracks in DEFAULT_AUDIO_MOODS.items():
                for track in mood_tracks:
                    tracks.append({"name": track, "mood": mood})
        
        return tracks
    except Exception as e:
        logger.error(f"Error loading audio tracks: {e}")
        # Return default tracks if file loading fails
        default_tracks = []
        for mood, mood_tracks in DEFAULT_AUDIO_MOODS.items():
            for track in mood_tracks:
                default_tracks.append({"name": track, "mood": mood})
        return default_tracks

# Run the actual pipeline
def run_actual_pipeline(selected_categories, selected_audio_mood):
    try:
        logger.info(f"Starting pipeline with categories: {selected_categories}, audio mood: {selected_audio_mood}")
        
        # Create output directories if they don't exist
        os.makedirs('/home/ubuntu/college_data', exist_ok=True)
        os.makedirs('/home/ubuntu/campus_images', exist_ok=True)
        os.makedirs('/home/ubuntu/trending_audio', exist_ok=True)
        os.makedirs('/home/ubuntu/formatted_rankings', exist_ok=True)
        os.makedirs('/home/ubuntu/generated_videos', exist_ok=True)
        os.makedirs('/home/ubuntu/final_videos', exist_ok=True)
        
        # Run data collection
        logger.info("Starting data collection")
        college_scraper = CollegeDataScraper()
        college_scraper.run_all_scrapers()
        
        image_collector = CampusImageCollector()
        image_collector.download_sample_images()
        
        audio_tracker = TrendingAudioTracker()
        audio_tracker.collect_trending_audio()
        logger.info("Data collection completed")
        
        # Format rankings
        logger.info("Starting ranking formatting")
        formatter = RankingFormatter()
        formatter.format_all_rankings()
        logger.info("Ranking formatting completed")
        
        # Generate videos for selected categories only
        logger.info("Starting video generation")
        video_engine = VideoCompositionEngine()
        
        # Get all available ranking files
        ranking_files = [f for f in os.listdir('/home/ubuntu/formatted_rankings') if f.endswith('.json')]
        
        # Filter to only include selected categories
        selected_ranking_files = []
        for ranking_file in ranking_files:
            # Extract category name from filename
            category_name = ranking_file.replace('.json', '').replace('_', ' ').title()
            
            # Check if this category was selected
            for selected_category in selected_categories:
                if selected_category.lower() in category_name.lower():
                    selected_ranking_files.append(ranking_file)
                    break
        
        # Generate videos for selected categories
        for ranking_file in selected_ranking_files:
            video_engine.create_ranking_video(ranking_file, selected_audio_mood)
        
        logger.info("Video generation completed")
        
        # Add audio to videos
        logger.info("Starting audio integration")
        audio_system = AudioIntegrationSystem()
        audio_system.process_all_videos()
        logger.info("Audio integration completed")
        
        # Get list of generated videos
        generated_videos = []
        video_files = [f for f in os.listdir('/home/ubuntu/final_videos') if f.endswith('.txt')]
        
        for video_file in video_files:
            # Extract category from filename
            category = video_file.replace('_with_', ' ').replace('_audio.txt', '').replace('_', ' ').title()
            
            # Create video info
            video_id = f"video_{int(time.time())}_{category.lower().replace(' ', '_')}"
            video_info = {
                "id": video_id,
                "category": category,
                "audio_mood": selected_audio_mood,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "url": f"/static/videos/{video_id}.txt"
            }
            
            # Copy the video file to the web static directory
            with open(os.path.join('/home/ubuntu/final_videos', video_file), 'r') as src_file:
                content = src_file.read()
                
                with open(f"/home/ubuntu/web_interface/static/videos/{video_id}.txt", 'w') as dest_file:
                    dest_file.write(content)
            
            generated_videos.append(video_info)
        
        logger.info(f"Pipeline completed successfully, generated {len(generated_videos)} videos")
        return generated_videos
    
    except Exception as e:
        logger.error(f"Error running pipeline: {e}")
        return []

@app.route('/')
def index():
    try:
        categories = load_ranking_categories()
        audio_tracks = load_audio_tracks()
        
        # Group categories by section
        grouped_categories = {}
        for category in categories:
            section = category["section"]
            if section not in grouped_categories:
                grouped_categories[section] = []
            grouped_categories[section].append(category["name"])
        
        # Group audio tracks by mood
        grouped_tracks = {}
        for track in audio_tracks:
            mood = track["mood"]
            if mood not in grouped_tracks:
                grouped_tracks[mood] = []
            grouped_tracks[mood].append(track["name"])
        
        # If no audio tracks were found, use defaults
        if not grouped_tracks:
            grouped_tracks = DEFAULT_AUDIO_MOODS
        
        logger.info(f"Loaded {len(grouped_categories)} category sections and {len(grouped_tracks)} audio moods")
        
        return render_template('index.html', 
                              categories=grouped_categories,
                              audio_tracks=grouped_tracks,
                              pipeline_status=pipeline_status)
    except Exception as e:
        logger.error(f"Error rendering index page: {e}")
        return "An error occurred while loading the page. Please check the logs for details.", 500

@app.route('/api/status')
def get_status():
    try:
        return jsonify(pipeline_status)
    except Exception as e:
        logger.error(f"Error getting status: {e}")
        return jsonify({"error": "An error occurred while getting status"}), 500

@app.route('/api/run_pipeline', methods=['POST'])
def run_pipeline():
    try:
        data = request.json
        selected_categories = data.get('categories', [])
        selected_audio_mood = data.get('audio_mood', 'calm')
        
        if not selected_categories:
            return jsonify({"error": "No categories selected"}), 400
        
        # Update status
        pipeline_status["data_collection"] = "in_progress"
        pipeline_status["video_generation"] = "not_started"
        pipeline_status["last_run"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pipeline_status["videos_generated"] = []
        
        logger.info(f"Starting pipeline with categories: {selected_categories}, audio mood: {selected_audio_mood}")
        
        # Run the actual pipeline
        generated_videos = run_actual_pipeline(selected_categories, selected_audio_mood)
        
        # Update status
        pipeline_status["data_collection"] = "completed"
        pipeline_status["video_generation"] = "completed"
        pipeline_status["videos_generated"] = generated_videos
        
        return jsonify({
            "status": "success",
            "message": f"Generated {len(generated_videos)} videos",
            "videos": generated_videos
        })
    except Exception as e:
        logger.error(f"Error running pipeline: {e}")
        
        # Update status to failed
        pipeline_status["data_collection"] = "failed"
        pipeline_status["video_generation"] = "failed"
        
        return jsonify({"error": f"An error occurred while running the pipeline: {str(e)}"}), 500

@app.route('/api/videos')
def get_videos():
    try:
        return jsonify({
            "videos": pipeline_status["videos_generated"]
        })
    except Exception as e:
        logger.error(f"Error getting videos: {e}")
        return jsonify({"error": "An error occurred while getting videos"}), 500

@app.route('/static/videos/<path:filename>')
def serve_video(filename):
    try:
        return send_from_directory('/home/ubuntu/web_interface/static/videos', filename)
    except Exception as e:
        logger.error(f"Error serving video file {filename}: {e}")
        abort(404)

@app.route('/static/css/<path:filename>')
def serve_css(filename):
    try:
        return send_from_directory('/home/ubuntu/web_interface/static/css', filename)
    except Exception as e:
        logger.error(f"Error serving CSS file {filename}: {e}")
        abort(404)

@app.route('/static/js/<path:filename>')
def serve_js(filename):
    try:
        return send_from_directory('/home/ubuntu/web_interface/static/js', filename)
    except Exception as e:
        logger.error(f"Error serving JS file {filename}: {e}")
        abort(404)

@app.route('/static/images/<path:filename>')
def serve_image(filename):
    try:
        return send_from_directory('/home/ubuntu/web_interface/static/images', filename)
    except Exception as e:
        logger.error(f"Error serving image file {filename}: {e}")
        abort(404)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    # Create a placeholder campus image if it doesn't exist
    placeholder_dir = '/home/ubuntu/web_interface/static/images'
    placeholder_file = os.path.join(placeholder_dir, 'campus-placeholder.jpg')
    
    if not os.path.exists(placeholder_file):
        try:
            import numpy as np
            import cv2
            
            # Create a simple gradient image as a placeholder
            img = np.zeros((400, 800, 3), dtype=np.uint8)
            for i in range(400):
                for j in range(800):
                    img[i, j] = [i % 256, (i + j) % 256, j % 256]
            
            cv2.imwrite(placeholder_file, img)
            logger.info(f"Created placeholder image at {placeholder_file}")
        except Exception as e:
            logger.error(f"Error creating placeholder image: {e}")
    
    # Create error templates if they don't exist
    templates_dir = '/home/ubuntu/web_interface/templates'
    
    if not os.path.exists(os.path.join(templates_dir, '404.html')):
        with open(os.path.join(templates_dir, '404.html'), 'w') as f:
            f.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>404 - Page Not Found</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
    <div class="container py-5">
        <div class="row justify-content-center">
            <div class="col-md-8 text-center">
              
(Content truncated due to size limit. Use line ranges to read in chunks)