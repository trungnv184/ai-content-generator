#!/usr/bin/env python
"""
Script to run the Gradio UI for the blog generator.
"""
import subprocess
import sys
import os
from pathlib import Path

def main():
    """Run the Gradio UI."""
    # Get the path to the UI file
    current_dir = Path(__file__).parent
    ui_file = current_dir / "src" / "blog_generator" / "ui.py"
    
    if not ui_file.exists():
        print(f"Error: UI file not found at {ui_file}")
        sys.exit(1)
    
    print("🚀 Starting AI Blog Generator UI...")
    print(f"📁 UI file: {ui_file}")
    print("🌐 The UI will open in your default browser at http://localhost:7860")
    print("⏹️  Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
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
        sys.exit(1)

if __name__ == "__main__":
    main() 