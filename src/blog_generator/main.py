#!/usr/bin/env python
import sys
import warnings
import traceback

from datetime import datetime

from blog_generator.crew import BlogGenerator

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    print("Starting blog generation process...")
    inputs = {
        'topic': 'Tutorial build AI Agent with CrewAI',
    }
    
    try:
        print("Initializing BlogGenerator...")
        generator = BlogGenerator()
        print("Creating crew...")
        crew = generator.crew()
        print("Starting crew execution...")
        result = crew.kickoff(inputs=inputs)
        print(f"Crew execution completed with result: {result}")
    except Exception as e:
        print("Error occurred during execution:")
        print(traceback.format_exc())
        raise Exception(f"An error occurred while running the crew: {e}")

if __name__ == "__main__":
    print("Script started")
    run()
    print("Script completed")


