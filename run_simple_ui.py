#!/usr/bin/env python
"""
Script to run the simplified Gradio UI for the blog generator.
"""
import subprocess
import sys
import os
from pathlib import Path

def main():
    """Run the simplified Gradio UI."""
    # Get the path to the UI file
    current_dir = Path(__file__).parent
    ui_file = current_dir / "src" / "blog_generator" / "simple_ui.py"
    
    if not ui_file.exists():
        print(f"Error: UI file not found at {ui_file}")
        sys.exit(1)
    
    print("🚀 Starting AI Blog Generator UI (Simplified)...")
    print(f"📁 UI file: {ui_file}")
    print("🌐 The UI will open in your default browser at http://localhost:7860")
    print("⏹️  Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        # Run the UI directly with Python
        subprocess.run([
            sys.executable, str(ui_file)
        ])
    except KeyboardInterrupt:
        print("\n👋 UI server stopped by user")
    except Exception as e:
        print(f"❌ Error running UI: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 