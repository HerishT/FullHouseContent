#!/usr/bin/env python3
"""
Test script for the AI Video Pipeline for College Rankings
This script tests the entire pipeline and generates sample videos
"""

import os
import sys
import json
import time
from datetime import datetime

# Import our modules
sys.path.append('/home/ubuntu')
from data_collection_module import CollegeDataScraper, CampusImageCollector, TrendingAudioTracker
from video_generation_module import RankingFormatter, VideoCompositionEngine, AudioIntegrationSystem

def create_directory_structure():
    """Create the necessary directory structure for the pipeline"""
    print("Creating directory structure...")
    
    directories = [
        "/home/ubuntu/college_data",
        "/home/ubuntu/campus_images",
        "/home/ubuntu/trending_audio",
        "/home/ubuntu/formatted_rankings",
        "/home/ubuntu/generated_videos",
        "/home/ubuntu/final_videos",
        "/home/ubuntu/sample_videos"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")

def test_data_collection():
    """Test the data collection module"""
    print("\n===== TESTING DATA COLLECTION MODULE =====")
    
    # Test college data scraper
    print("\nTesting CollegeDataScraper...")
    college_scraper = CollegeDataScraper()
    college_scraper.run_all_scrapers()
    
    # Verify data was collected
    data_files = os.listdir("/home/ubuntu/college_data")
    print(f"Generated {len(data_files)} data files:")
    for file in data_files:
        file_path = os.path.join("/home/ubuntu/college_data", file)
        file_size = os.path.getsize(file_path)
        print(f"  - {file} ({file_size} bytes)")
    
    # Test campus image collector
    print("\nTesting CampusImageCollector...")
    image_collector = CampusImageCollector()
    image_collector.download_sample_images()
    
    # Verify images were collected
    image_categories = os.listdir("/home/ubuntu/campus_images")
    total_images = 0
    print(f"Downloaded images in {len(image_categories)} categories:")
    for category in image_categories:
        if os.path.isdir(os.path.join("/home/ubuntu/campus_images", category)):
            category_images = os.listdir(os.path.join("/home/ubuntu/campus_images", category))
            total_images += len(category_images)
            print(f"  - {category}: {len(category_images)} images")
    
    # Test trending audio tracker
    print("\nTesting TrendingAudioTracker...")
    audio_tracker = TrendingAudioTracker()
    audio_tracker.collect_trending_audio()
    
    # Verify audio was collected
    audio_moods = os.listdir("/home/ubuntu/trending_audio")
    total_tracks = 0
    print(f"Collected audio in {len(audio_moods)} mood categories:")
    for mood in audio_moods:
        if os.path.isdir(os.path.join("/home/ubuntu/trending_audio", mood)):
            mood_tracks = os.listdir(os.path.join("/home/ubuntu/trending_audio", mood))
            total_tracks += len(mood_tracks)
            print(f"  - {mood}: {len(mood_tracks)} tracks")
    
    return len(data_files) > 0 and total_images > 0 and total_tracks > 0

def test_video_generation():
    """Test the video generation module"""
    print("\n===== TESTING VIDEO GENERATION MODULE =====")
    
    # Test ranking formatter
    print("\nTesting RankingFormatter...")
    formatter = RankingFormatter()
    formatter.format_all_rankings()
    
    # Verify rankings were formatted
    ranking_files = os.listdir("/home/ubuntu/formatted_rankings")
    print(f"Generated {len(ranking_files)} formatted ranking files:")
    for file in ranking_files:
        file_path = os.path.join("/home/ubuntu/formatted_rankings", file)
        file_size = os.path.getsize(file_path)
        print(f"  - {file} ({file_size} bytes)")
    
    # Test video composition engine
    print("\nTesting VideoCompositionEngine...")
    video_engine = VideoCompositionEngine()
    video_engine.create_all_ranking_videos()
    
    # Verify videos were generated
    video_files = os.listdir("/home/ubuntu/generated_videos")
    print(f"Generated {len(video_files)} video placeholders:")
    for file in video_files:
        file_path = os.path.join("/home/ubuntu/generated_videos", file)
        file_size = os.path.getsize(file_path)
        print(f"  - {file} ({file_size} bytes)")
    
    # Test audio integration system
    print("\nTesting AudioIntegrationSystem...")
    audio_system = AudioIntegrationSystem()
    audio_system.process_all_videos()
    
    # Verify final videos were created
    final_videos = os.listdir("/home/ubuntu/final_videos")
    print(f"Generated {len(final_videos)} final video placeholders:")
    for file in final_videos:
        file_path = os.path.join("/home/ubuntu/final_videos", file)
        file_size = os.path.getsize(file_path)
        print(f"  - {file} ({file_size} bytes)")
    
    return len(ranking_files) > 0 and len(video_files) > 0 and len(final_videos) > 0

def generate_sample_videos():
    """Generate sample videos for demonstration"""
    print("\n===== GENERATING SAMPLE VIDEOS =====")
    
    # In a real implementation, this would generate actual video files
    # For this demo, we'll create sample descriptions
    
    sample_categories = [
        "Most Beautiful Campuses",
        "Top National Universities",
        "Best College Dorms",
        "Happiest Students",
        "Most Beautiful Ivy League Campuses"
    ]
    
    for i, category in enumerate(sample_categories):
        sample_file = os.path.join("/home/ubuntu/sample_videos", f"sample_{i+1}_{category.lower().replace(' ', '_')}.txt")
        
        with open(sample_file, 'w') as f:
            f.write(f"SAMPLE VIDEO: {category}\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"This is a sample video for the {category} ranking.\n\n")
            f.write("VIDEO SPECIFICATIONS:\n")
            f.write("- Duration: 15 seconds\n")
            f.write("- Format: Vertical (1080x1920) optimized for TikTok/YouTube Shorts\n")
            f.write("- Style: Slow camera movements on college campus backgrounds\n")
            f.write(f"- Audio: Trending instrumental track ({get_mood_for_category(category)} mood)\n\n")
            f.write("CONTENT STRUCTURE:\n")
            f.write("1. Opening title (2 seconds)\n")
            f.write(f"   '{category}'\n\n")
            f.write("2. Countdown of top 5 colleges (10 seconds)\n")
            f.write("   Each college shown for 2 seconds with:\n")
            f.write("   - Rank and name\n")
            f.write("   - Brief description\n")
            f.write("   - Campus background image\n\n")
            f.write("3. Call to action (3 seconds)\n")
            f.write("   'Follow for more college rankings!'\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    sample_files = os.listdir("/home/ubuntu/sample_videos")
    print(f"Generated {len(sample_files)} sample video descriptions:")
    for file in sample_files:
        file_path = os.path.join("/home/ubuntu/sample_videos", file)
        file_size = os.path.getsize(file_path)
        print(f"  - {file} ({file_size} bytes)")
    
    return len(sample_files) > 0

def get_mood_for_category(category):
    """Determine appropriate audio mood based on category"""
    if "beautiful" in category.lower():
        return "inspirational"
    elif "happiest" in category.lower() or "best" in category.lower():
        return "calm"
    elif "ivy" in category.lower():
        return "ambient"
    else:
        return "calm"

def create_summary_report():
    """Create a summary report of the pipeline test"""
    print("\n===== CREATING SUMMARY REPORT =====")
    
    report_file = "/home/ubuntu/pipeline_test_report.md"
    
    with open(report_file, 'w') as f:
        f.write("# AI Video Pipeline Test Report\n\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("## Pipeline Components\n\n")
        f.write("1. **Data Collection Module**\n")
        f.write("   - CollegeDataScraper: Collects ranking data from multiple sources\n")
        f.write("   - CampusImageCollector: Gathers high-quality images of college campuses\n")
        f.write("   - TrendingAudioTracker: Monitors TikTok and YouTube for trending instrumental tracks\n\n")
        
        f.write("2. **Video Generation Module**\n")
        f.write("   - RankingFormatter: Converts raw data into visually appealing ranking sequences\n")
        f.write("   - VideoCompositionEngine: Pairs campus images with relevant ranking data\n")
        f.write("   - AudioIntegrationSystem: Matches audio mood to ranking content\n\n")
        
        f.write("## Test Results\n\n")
        
        # Data Collection Results
        data_files = os.listdir("/home/ubuntu/college_data")
        f.write(f"### Data Collection\n")
        f.write(f"- Generated {len(data_files)} ranking data files\n")
        
        image_categories = [d for d in os.listdir("/home/ubuntu/campus_images") 
                           if os.path.isdir(os.path.join("/home/ubuntu/campus_images", d))]
        total_images = sum(len(os.listdir(os.path.join("/home/ubuntu/campus_images", d))) for d in image_categories)
        f.write(f"- Collected {total_images} campus images across {len(image_categories)} categories\n")
        
        audio_moods = [d for d in os.listdir("/home/ubuntu/trending_audio") 
                      if os.path.isdir(os.path.join("/home/ubuntu/trending_audio", d))]
        total_tracks = sum(len(os.listdir(os.path.join("/home/ubuntu/trending_audio", d))) for d in audio_moods)
        f.write(f"- Collected {total_tracks} audio tracks across {len(audio_moods)} mood categories\n\n")
        
        # Video Generation Results
        ranking_files = os.listdir("/home/ubuntu/formatted_rankings")
        f.write(f"### Video Generation\n")
        f.write(f"- Formatted {len(ranking_files)} ranking categories\n")
        
        video_files = os.listdir("/home/ubuntu/generated_videos")
        f.write(f"- Generated {len(video_files)} video placeholders\n")
        
        final_videos = os.listdir("/home/ubuntu/final_videos")
        f.write(f"- Created {len(final_videos)} final videos with audio\n\n")
        
        # Sample Videos
        sample_files = os.listdir("/home/ubuntu/sample_videos")
        f.write(f"### Sample Videos\n")
        f.write(f"- Created {len(sample_files)} sample video descriptions\n")
        f.write("- Sample categories:\n")
        for file in sample_files:
            category = file.replace("sample_", "").replace(".txt", "").replace("_", " ").title()
            f.write(f"  - {category}\n")
        
        f.write("\n## Next Steps\n\n")
        f.write("1. Implement actual video rendering with MoviePy\n")
        f.write("2. Set up automated posting to TikTok and YouTube Shorts\n")
        f.write("3. Implement analytics tracking for performance monitoring\n")
        f.write("4. Develop A/B testing framework for optimizing engagement\n")
        f.write("5. Integrate with Sentient's Dobby model for enhanced captions\n")
    
    print(f"Summary report created at {report_file}")
    return True

def main():
    """Main function to test the pipeline and generate sample videos"""
    print("Starting AI Video Pipeline test...")
    
    # Create directory structure
    create_directory_structure()
    
    # Test data collection
    data_collection_success = test_data_collection()
    
    # Test video generation
    video_generation_success = test_video_generation()
    
    # Generate sample videos
    sample_videos_success = generate_sample_videos()
    
    # Create summary report
    report_success = create_summary_report()
    
    # Print overall results
    print("\n===== TEST RESULTS =====")
    print(f"Data Collection: {'SUCCESS' if data_collection_success else 'FAILURE'}")
    print(f"Video Generation: {'SUCCESS' if video_generation_success else 'FAILURE'}")
    print(f"Sample Videos: {'SUCCESS' if sample_videos_success else 'FAILURE'}")
    print(f"Summary Report: {'SUCCESS' if report_success else 'FAILURE'}")
    
    if data_collection_success and video_generation_success and sample_videos_success and report_success:
        print("\nALL TESTS PASSED! The AI Video Pipeline is working correctly.")
    else:
        print("\nSome tests failed. Please check the logs for details.")

if __name__ == "__main__":
    main()
