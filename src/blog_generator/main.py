#!/usr/bin/env python
import sys
import warnings
import traceback
import argparse
from datetime import datetime

from blog_generator.crew import BlogGenerator

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run_cli(topic=None):
    """
    Run the crew from command line.
    """
    if not topic:
        topic = 'Top 10 questions will ask for Engineering Manager position and provide best answers'
    
    print("Starting blog generation process...")
    inputs = {
        'topic': topic,
    }
    
    try:
        print("Initializing BlogGenerator...")
        generator = BlogGenerator()
        print("Creating crew...")
        crew = generator.crew()
        print("Starting crew execution...")
        result = crew.kickoff(inputs=inputs)
        print(f"Crew execution completed with result: {result}")
        return result
    except Exception as e:
        print("Error occurred during execution:")
        print(traceback.format_exc())
        raise Exception(f"An error occurred while running the crew: {e}")

def run_ui():
    """
    Run the Gradio UI.
    """
    try:
        import subprocess
        import os
        from pathlib import Path
        
        # Get the path to the UI file
        current_dir = Path(__file__).parent
        ui_file = current_dir / "ui.py"
        
        if not ui_file.exists():
            print(f"Error: UI file not found at {ui_file}")
            return
        
        print("🚀 Starting AI Blog Generator UI...")
        print("🌐 The UI will open in your default browser at http://localhost:7860")
        print("⏹️  Press Ctrl+C to stop the server")
        
        # Run gradio
        subprocess.run([
            sys.executable, "-m", "gradio", "run", str(ui_file),
            "--server.port", "7860",
            "--server.address", "0.0.0.0",
            "--quiet"
        ])
    except KeyboardInterrupt:
        print("\n👋 UI server stopped by user")
    except Exception as e:
        print(f"❌ Error running UI: {e}")

def main():
    """
    Main entry point with command line argument parsing.
    """
    parser = argparse.ArgumentParser(description="AI Blog Generator using CrewAI")
    parser.add_argument(
        "--mode", 
        choices=["cli", "ui"], 
        default="cli",
        help="Run mode: cli (command line) or ui (web interface)"
    )
    parser.add_argument(
        "--topic", 
        type=str,
        help="Blog topic (for CLI mode)"
    )
    
    args = parser.parse_args()
    
    if args.mode == "ui":
        run_ui()
    else:
        run_cli(args.topic)

def run():
    """
    Default run function for backward compatibility.
    """
    run_cli()

if __name__ == "__main__":
    main()


