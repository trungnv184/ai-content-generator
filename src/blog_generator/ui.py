import gradio as gr
import sys
import warnings
import traceback
from datetime import datetime
import markdown
import os
from pathlib import Path
import threading
import time

# Add the src directory to the path so we can import our modules
sys.path.append(str(Path(__file__).parent))

from blog_generator.crew import BlogGenerator

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

class BlogGeneratorUI:
    def __init__(self):
        self.generator = None
        self.crew = None
        self.generation_status = "idle"
        self.current_result = None
        self.error_message = None
    
    def initialize_agents(self):
        """Initialize the blog generator and crew."""
        try:
            if self.generator is None:
                self.generator = BlogGenerator()
            if self.crew is None:
                self.crew = self.generator.crew()
            return True
        except Exception as e:
            self.error_message = f"Error initializing agents: {str(e)}"
            return False
    
    def generate_blog_post(self, topic, show_diagrams, save_to_file, progress=gr.Progress()):
        """Generate a blog post using the AI agents."""
        if not topic.strip():
            return "❌ Please enter a topic to generate a blog post.", "", "idle"
        
        try:
            self.generation_status = "generating"
            self.error_message = None
            
            # Initialize agents
            progress(0.1, desc="🤖 Initializing AI agents...")
            if not self.initialize_agents():
                return f"❌ {self.error_message}", "", "error"
            
            # Create crew
            progress(0.2, desc="🔄 Creating crew...")
            if self.crew is None:
                self.crew = self.generator.crew()
            
            # Generate blog post
            progress(0.3, desc="⚡ Generating blog post...")
            inputs = {'topic': topic.strip()}
            
            # Update progress during generation
            def update_progress():
                for i in range(4, 10):
                    time.sleep(2)  # Simulate work
                    progress(i/10, desc=f"🔄 AI agents working... ({i*10}%)")
            
            # Start progress thread
            progress_thread = threading.Thread(target=update_progress)
            progress_thread.start()
            
            # Generate the blog post
            result = self.crew.kickoff(inputs=inputs)
            
            # Wait for progress thread to finish
            progress_thread.join()
            
            progress(1.0, desc="✅ Blog post generated successfully!")
            
            # Store the result
            self.current_result = result
            self.generation_status = "completed"
            
            # Format the result for display
            formatted_result = self.format_blog_post(result, topic.strip(), show_diagrams)
            
            return "✅ Blog post generated successfully!", formatted_result, "completed"
            
        except Exception as e:
            self.generation_status = "error"
            self.error_message = str(e)
            error_msg = f"❌ Error occurred during generation: {str(e)}"
            return error_msg, "", "error"
    
    def format_blog_post(self, content, topic, show_diagrams):
        """Format the blog post with proper styling and diagrams."""
        try:
            # Add frontmatter
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            frontmatter = f"""---
title: "{topic}"
author: "AI Blog Generator"
date: "{timestamp}"
---

"""
            
            # Format the content
            formatted_content = f"""{frontmatter}
# {topic}

{content}

---

*Generated on {timestamp} using AI Blog Generator*
"""
            
            return formatted_content
            
        except Exception as e:
            return f"Error formatting content: {str(e)}\n\nOriginal content:\n{content}"
    
    def download_markdown(self, content):
        """Create a downloadable markdown file."""
        if not content:
            return None
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"blog_post_{timestamp}.md"
        
        return (filename, content)
    
    def download_html(self, content):
        """Create a downloadable HTML file."""
        if not content:
            return None
        
        try:
            # Convert markdown to HTML
            html_content = markdown.markdown(content, extensions=['fenced_code', 'tables', 'codehilite'])
            
            # Create full HTML document
            full_html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Generated Blog Post</title>
    <meta charset="utf-8">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
            color: #333;
        }}
        h1, h2, h3, h4, h5, h6 {{
            color: #2c3e50;
            margin-top: 2rem;
            margin-bottom: 1rem;
        }}
        code {{
            background-color: #f8f9fa;
            padding: 2px 4px;
            border-radius: 3px;
            font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
        }}
        pre {{
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            border-left: 4px solid #667eea;
        }}
        pre code {{
            background-color: transparent;
            padding: 0;
        }}
        blockquote {{
            border-left: 4px solid #667eea;
            margin: 0;
            padding-left: 1rem;
            color: #666;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 1rem 0;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }}
        th {{
            background-color: #f8f9fa;
        }}
        .header {{
            text-align: center;
            margin-bottom: 2rem;
            padding-bottom: 1rem;
            border-bottom: 2px solid #667eea;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>AI Generated Blog Post</h1>
        <p>Generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
    </div>
    {html_content}
</body>
</html>
"""
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"blog_post_{timestamp}.html"
            
            return (filename, full_html)
            
        except Exception as e:
            return None

def create_ui():
    """Create the Gradio interface."""
    ui = BlogGeneratorUI()
    
    # Custom CSS for better styling
    custom_css = """
    .gradio-container {
        max-width: 1200px !important;
    }
    .main-header {
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
        font-size: 1.1rem;
    }
    """
    
    with gr.Blocks(css=custom_css, title="AI Blog Generator") as demo:
        # Header
        gr.HTML("""
        <div class="main-header">✍️ AI Blog Generator</div>
        <div class="sub-header">Generate comprehensive technical blog posts using AI agents</div>
        """)
        
        with gr.Row():
            with gr.Column(scale=1):
                # Input section
                gr.Markdown("### 📝 Blog Topic")
                topic_input = gr.Textbox(
                    label="Enter your blog topic",
                    placeholder="Example: Top 10 questions will ask for Engineering Manager position and provide best answers",
                    lines=4,
                    max_lines=6
                )
                
                with gr.Row():
                    show_diagrams = gr.Checkbox(
                        label="Generate Technical Diagrams",
                        value=True,
                        info="Include system architecture and workflow diagrams"
                    )
                    save_to_file = gr.Checkbox(
                        label="Save to File",
                        value=True,
                        info="Save the generated blog post as a markdown file"
                    )
                
                generate_btn = gr.Button(
                    "🎯 Generate Blog Post",
                    variant="primary",
                    size="lg"
                )
                
                # Status output
                status_output = gr.Textbox(
                    label="Status",
                    interactive=False,
                    value="⏳ Ready to generate blog post"
                )
                
                # About section
                gr.Markdown("""
                ### ℹ️ About
                This AI blog generator uses multiple specialized agents:
                
                - **Researcher** 🔍: Gathers comprehensive information
                - **Technical Writer** ✍️: Creates well-structured content
                - **Technical Reviewer** 🔍: Ensures quality and accuracy
                - **Technical Publisher** 📝: Formats and publishes the final post
                
                The process typically takes 2-5 minutes depending on the topic complexity.
                """)
            
            with gr.Column(scale=2):
                # Output section
                gr.Markdown("### 📄 Generated Blog Post")
                
                # Tabs for different views
                with gr.Tabs():
                    with gr.TabItem("📖 Formatted View"):
                        formatted_output = gr.Markdown(
                            label="Blog Post Preview",
                            value="*Blog post will appear here after generation*"
                        )
                    
                    with gr.TabItem("📝 Raw Markdown"):
                        raw_output = gr.Code(
                            label="Raw Markdown",
                            language="markdown",
                            value="*Raw markdown will appear here after generation*"
                        )
                    
                    with gr.TabItem("💾 Download"):
                        gr.Markdown("### Download Options")
                        
                        download_md_btn = gr.DownloadButton(
                            label="📥 Download as Markdown",
                            variant="secondary"
                        )
                        
                        download_html_btn = gr.DownloadButton(
                            label="🌐 Download as HTML",
                            variant="secondary"
                        )
        
        # Footer
        gr.HTML(f"""
        <div style='text-align: center; color: #666; padding: 2rem; border-top: 1px solid #eee; margin-top: 2rem;'>
            <p>Built with ❤️ using CrewAI and Gradio</p>
            <p>Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        </div>
        """)
        
        # Event handlers
        def on_generate(topic, show_diagrams, save_to_file, progress=gr.Progress()):
            status, content, generation_status = ui.generate_blog_post(topic, show_diagrams, save_to_file, progress)
            
            # Update outputs based on generation status
            if generation_status == "completed":
                # Update formatted view
                formatted_content = ui.format_blog_post(content, topic, show_diagrams)
                
                # Update raw markdown
                raw_content = content
                
                # Update download buttons
                md_file = ui.download_markdown(formatted_content)
                html_file = ui.download_html(formatted_content)
                
                return status, formatted_content, raw_content, md_file, html_file
            else:
                return status, "*Generation failed*", "*Generation failed*", None, None
        
        # Connect the generate button
        generate_btn.click(
            fn=on_generate,
            inputs=[topic_input, show_diagrams, save_to_file],
            outputs=[status_output, formatted_output, raw_output, download_md_btn, download_html_btn]
        )
        
        # Auto-update download buttons when content changes
        def update_downloads(content):
            if content and content != "*Generation failed*":
                md_file = ui.download_markdown(content)
                html_file = ui.download_html(content)
                return md_file, html_file
            return None, None
        
        formatted_output.change(
            fn=update_downloads,
            inputs=[formatted_output],
            outputs=[download_md_btn, download_html_btn]
        )
    
    return demo

def main():
    """Main function to launch the Gradio interface."""
    demo = create_ui()
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True,
        quiet=False
    )

if __name__ == "__main__":
    main() 