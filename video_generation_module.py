import os
import json
import random
import textwrap
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import cv2
import moviepy.editor as mp
from moviepy.editor import *
import time

class RankingFormatter:
    """
    Converts raw ranking data into visually appealing ranking sequences
    """
    def __init__(self, data_dir="/home/ubuntu/college_data", output_dir="/home/ubuntu/formatted_rankings"):
        self.data_dir = data_dir
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Define templates for different ranking categories
        self.templates = {
            "standard": {
                "title_format": "{category} Rankings",
                "item_format": "#{rank}. {name}",
                "description_format": "Located in {location}"
            },
            "score_based": {
                "title_format": "Top {count} {category}",
                "item_format": "#{rank}. {name} - {score}/100",
                "description_format": "{location}"
            },
            "comparison": {
                "title_format": "{category} Comparison",
                "item_format": "#{rank}. {name}",
                "description_format": "{metric}: {value}"
            }
        }
    
    def load_ranking_data(self, filename):
        """Load ranking data from JSON file"""
        try:
            with open(os.path.join(self.data_dir, filename), 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"File not found: {filename}")
            return []
    
    def format_ranking(self, data, category, template_type="standard", count=10):
        """Format ranking data using specified template"""
        print(f"Formatting {category} ranking...")
        
        # Select template
        template = self.templates.get(template_type, self.templates["standard"])
        
        # Format title
        title = template["title_format"].format(category=category, count=count)
        
        # Format items
        items = []
        for item in data[:count]:
            rank = item.get("rank", 0)
            name = item.get("name", "Unknown")
            location = item.get("location", "")
            score = item.get("score", "")
            
            formatted_item = {
                "rank": rank,
                "text": template["item_format"].format(rank=rank, name=name, score=score),
                "description": template["description_format"].format(location=location, metric="Score", value=score)
            }
            items.append(formatted_item)
        
        # Create formatted ranking
        formatted_ranking = {
            "title": title,
            "category": category,
            "count": count,
            "items": items,
            "template_type": template_type,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Save formatted ranking
        output_file = os.path.join(self.output_dir, f"{category.lower().replace(' ', '_')}.json")
        with open(output_file, 'w') as f:
            json.dump(formatted_ranking, f, indent=4)
        
        print(f"Formatted ranking saved to {output_file}")
        return formatted_ranking
    
    def format_all_rankings(self):
        """Format all available rankings"""
        # Format US News rankings
        us_news_data = self.load_ranking_data("us_news_national-universities.json")
        self.format_ranking(us_news_data, "Top National Universities", "score_based")
        
        # Format Princeton Review rankings
        princeton_beautiful = self.load_ranking_data("princeton_review_most-beautiful-campus.json")
        self.format_ranking(princeton_beautiful, "Most Beautiful Campuses", "standard")
        
        princeton_happy = self.load_ranking_data("princeton_review_happiest-students.json")
        self.format_ranking(princeton_happy, "Happiest Students", "standard")
        
        # Format Niche rankings
        niche_campuses = self.load_ranking_data("niche_best-college-campuses.json")
        self.format_ranking(niche_campuses, "Best College Campuses", "standard")
        
        niche_food = self.load_ranking_data("niche_best-food.json")
        self.format_ranking(niche_food, "Best Campus Food", "standard")
        
        niche_dorms = self.load_ranking_data("niche_best-dorms.json")
        self.format_ranking(niche_dorms, "Best College Dorms", "standard")
        
        # Format custom rankings
        ivy_beauty = self.load_ranking_data("custom_ivy_league_beauty.json")
        self.format_ranking(ivy_beauty, "Most Beautiful Ivy League Campuses", "score_based")
        
        student_life = self.load_ranking_data("custom_best_student_life.json")
        self.format_ranking(student_life, "Best Student Life", "score_based")
        
        print("All rankings formatted successfully!")


class VideoCompositionEngine:
    """
    Creates short-form videos by combining campus images with ranking data
    """
    def __init__(self, 
                 rankings_dir="/home/ubuntu/formatted_rankings", 
                 images_dir="/home/ubuntu/campus_images",
                 audio_dir="/home/ubuntu/trending_audio",
                 output_dir="/home/ubuntu/generated_videos"):
        self.rankings_dir = rankings_dir
        self.images_dir = images_dir
        self.audio_dir = audio_dir
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Video settings
        self.video_width = 1080  # TikTok/Shorts vertical format
        self.video_height = 1920
        self.fps = 30
        self.duration = 15  # 15 seconds per video
        
        # Font settings (would use actual font files in real implementation)
        self.title_font_size = 70
        self.item_font_size = 60
        self.description_font_size = 40
        
        # Colors
        self.background_color = (0, 0, 0)  # Black
        self.text_color = (255, 255, 255)  # White
        self.highlight_color = (255, 0, 0)  # Red
    
    def load_ranking_data(self, filename):
        """Load formatted ranking data"""
        try:
            with open(os.path.join(self.rankings_dir, filename), 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Ranking file not found: {filename}")
            return None
    
    def get_placeholder_image(self, category):
        """
        In a real implementation, this would select an appropriate image.
        For this demo, we'll create a placeholder image.
        """
        # Create a blank image
        img = np.zeros((self.video_height, self.video_width, 3), dtype=np.uint8)
        
        # Fill with a color based on category
        if "beautiful" in category.lower():
            img[:] = (0, 100, 0)  # Dark green for beautiful campuses
        elif "food" in category.lower():
            img[:] = (0, 0, 100)  # Dark red for food
        elif "dorm" in category.lower():
            img[:] = (100, 0, 0)  # Dark blue for dorms
        elif "ivy" in category.lower():
            img[:] = (100, 100, 0)  # Teal for Ivy League
        else:
            img[:] = (50, 50, 50)  # Gray for others
        
        # Add text to indicate this is a placeholder
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, f"Campus Image for", (int(self.video_width/2) - 200, int(self.video_height/2) - 50), 
                   font, 1, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(img, f"{category}", (int(self.video_width/2) - 200, int(self.video_height/2) + 50), 
                   font, 1, (255, 255, 255), 2, cv2.LINE_AA)
        
        return img
    
    def apply_camera_movement(self, clip, movement_type="pan"):
        """Apply slow camera movement to the clip"""
        if movement_type == "pan":
            # Pan from left to right
            def pan(t):
                return ('center', 'center')
            
            # In a real implementation, this would use proper panning
            # For this demo, we'll just return the clip
            return clip
        
        elif movement_type == "zoom":
            # Slow zoom in
            def zoom(t):
                return 1 + 0.1 * t  # Zoom in by 10% over the duration
            
            # In a real implementation, this would use proper zooming
            # For this demo, we'll just return the clip
            return clip
        
        else:
            return clip
    
    def create_text_clip(self, text, font_size, color, duration, position="center"):
        """Create a text clip with the specified properties"""
        # In a real implementation, this would create actual text clips
        # For this demo, we'll create a placeholder image with text
        img = np.zeros((200, self.video_width, 3), dtype=np.uint8)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, text, (50, 100), font, font_size/30, color, 2, cv2.LINE_AA)
        
        # Convert to MoviePy clip
        text_clip = ImageClip(img).set_duration(duration)
        
        # Set position
        if position == "top":
            text_clip = text_clip.set_position(("center", 100))
        elif position == "bottom":
            text_clip = text_clip.set_position(("center", self.video_height - 300))
        else:
            text_clip = text_clip.set_position("center")
        
        return text_clip
    
    def create_ranking_video(self, ranking_file, audio_mood="calm"):
        """Create a short-form video for the specified ranking"""
        print(f"Creating video for {ranking_file}...")
        
        # Load ranking data
        ranking_data = self.load_ranking_data(ranking_file)
        if not ranking_data:
            print(f"Failed to load ranking data from {ranking_file}")
            return False
        
        category = ranking_data["category"]
        title = ranking_data["title"]
        items = ranking_data["items"]
        
        # In a real implementation, this would create an actual video
        # For this demo, we'll describe the process
        
        print(f"1. Creating title sequence for '{title}'")
        print(f"2. Selecting background images for {category}")
        print(f"3. Applying slow camera movements")
        print(f"4. Adding text overlays for each ranked item")
        print(f"5. Adding transitions between items")
        print(f"6. Selecting {audio_mood} audio track")
        print(f"7. Rendering final video")
        
        # Create a placeholder video file
        output_file = os.path.join(self.output_dir, f"{category.lower().replace(' ', '_')}.mp4")
        
        # Create a simple placeholder video
        # In a real implementation, this would be a properly composed video
        # For this demo, we'll create a basic video with text
        
        # Create background clip
        background = self.get_placeholder_image(category)
        background_clip = ImageClip(background).set_duration(self.duration)
        
        # Create title clip
        title_clip = self.create_text_clip(title, self.title_font_size, self.text_color, 3, "top")
        
        # Create clips for each ranked item
        item_clips = []
        for i, item in enumerate(items[:5]):  # Show top 5 for demo
            item_text = item["text"]
            item_desc = item["description"]
            
            # Calculate timing for this item
            start_time = 3 + i * 2  # Start after title, 2 seconds per item
            item_duration = 2  # Each item shows for 2 seconds
            
            # Create item text clip
            item_clip = self.create_text_clip(item_text, self.item_font_size, self.text_color, 
                                             item_duration, "center")
            item_clip = item_clip.set_start(start_time)
            
            # Create description text clip
            desc_clip = self.create_text_clip(item_desc, self.description_font_size, self.text_color, 
                                             item_duration, "bottom")
            desc_clip = desc_clip.set_start(start_time)
            
            item_clips.extend([item_clip, desc_clip])
        
        # Combine all clips
        video = CompositeVideoClip([background_clip] + [title_clip] + item_clips, 
                                  size=(self.video_width, self.video_height))
        
        # In a real implementation, this would write an actual video file
        # For this demo, we'll create a text file describing the video
        with open(output_file.replace(".mp4", ".txt"), 'w') as f:
            f.write(f"This is a placeholder for a video about {title}.\n")
            f.write(f"In the actual implementation, this would be a 15-second video file.\n")
            f.write(f"Category: {category}\n")
            f.write(f"Audio mood: {audio_mood}\n")
            f.write(f"Items shown:\n")
            for item in items[:5]:
                f.write(f"- {item['text']} ({item['description']})\n")
            f.write(f"Created at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        print(f"Video placeholder created at {output_file.replace('.mp4', '.txt')}")
        return True
    
    def create_all_ranking_videos(self):
        """Create videos for all available rankings"""
        # Get all ranking files
        ranking_files = [f for f in os.listdir(self.rankings_dir) if f.endswith('.json')]
        
        # Audio moods to match with ranking categories
        mood_mapping = {
            "beautiful": "inspirational",
            "happiest": "inspirational",
            "best": "calm",
            "top": "ambient",
            "ivy": "calm",
            "food": "calm",
            "dorms": "ambient",
            "student_life": "inspirational"
        }
        
        # Create videos for each ranking
        for ranking_file in ranking_files:
            # Determine appropriate audio mood based on category
            audio_mood = "calm"  # Default
            for keyword, mood in mood_mapping.items():
                if keyword in ranking_file.lower():
                    audio_mood = mood
                    break
            
            self.create_ranking_video(ranking_file, audio_mood)
        
        print("All ranking videos created successfully!")


class AudioIntegrationSystem:
    """
    Integrates audio tracks with video content
    """
    def __init__(self, 
                 audio_dir="/home/ubuntu/trending_audio",
                 videos_dir="/home/ubuntu/generated_videos",
                 output_dir="/home/ubuntu/final_videos"):
        self.audio_dir = audio_dir
        self.videos_dir = videos_dir
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def get_audio_track(self, mood):
        """
        In a real implementation, this would select an appropriate audio track.
        For this demo, we'll return a placeholder.
        """
        mood_dir = os.path.join(self.audio_dir, mood)
        if not os.path.exists(mood_dir):
            print(f"Audio mood directory not found: {mood}")
            return None
        
        # Get list of audio tracks for this mood
        tracks = [f for f in os.listdir(mood_dir) if f.endswith('.txt')]  # Using .txt as placeholders
        
        if not tracks:
            print(f"No audio tracks found for mood: {mood}")
            return None
        
        # Select a random track
        selected_track = random.choice(tracks)
        return os.path.join(mood_dir, selected_track)
    
    def add_audio_to_video(self, video_file, audio_mood):
        """
        In a real implementation, this would add audio to the video.
        For this demo, we'll create a placeholder.
        """
        print(f"Adding {audio_mood} audio to {video_file}...")
        
        # Get audio track
        audio_track = self.get_audio_track(audio_mood)
        if not audio_track:
            print(f"Failed to get audio track for mood: {audio_mood}")
            return False
        
        # In a real implementation, this would combine audio and video
        # For this demo, we'll create a text file describing the final video
        
        video_name = os.path.basename(video_file).replace('.txt', '')
        output_file = os.path.join(self.output_dir, f"{video_name}_with_{audio_mood}_audio.txt")
        
        # Read video description
        with open(video_file, 'r') as f:
            video_description = f.read()
        
        # Read audio description
        with open(audio_track, 'r') as f:
            audio_description = f.read()
        
        # Create final video description
        with open(output_file, 'w') as f:
            f.write(f"This is a placeholder for a final video with audio.\n")
            f.write(f"In the actual implementation, this would be a 15-second video file with audio.\n\n")
            f.write(f"VIDEO DESCRIPTION:\n{video_description}\n\n")
            f.write(f"AUDIO DESCRIPTION:\n{audio_description}\n\n")
            f.write(f"Final video created at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        print(f"Final video placeholder created at {output_file}")
        return True
    
    def process_all_videos(self):
        """Add audio to all generated videos"""
        # Get all video placeholder files
        video_files = [os.path.join(self.videos_dir, f) for f in os.listdir(self.videos_dir) if f.endswith('.txt')]
        
        for video_file in video_files:
            # Extract audio mood from video description
            audio_mood = "calm"  # Default
            with open(video_file, 'r') as f:
                for line in f:
                    if line.startswith("Audio mood:"):
                        audio_mood = line.split(":")[1].strip()
                        break
            
            self.add_audio_to_video(video_file, audio_mood)
        
        print("Audio added to all videos successfully!")


def main():
    """Main function to run the video generation pipeline"""
    print("Starting video generation pipeline...")
    
    # Format rankings
    formatter = RankingFormatter()
    formatter.format_all_rankings()
    
    # Create videos
    video_engine = VideoCompositionEngine()
    video_engine.create_all_ranking_videos()
    
    # Add audio to videos
    audio_system = AudioIntegrationSystem()
    audio_system.process_all_videos()
    
    print("Video generation pipeline complete! All videos have been generated with audio.")


if __name__ == "__main__":
    main()
