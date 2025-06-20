import gradio as gr
import sys
import warnings
from datetime import datetime
import markdown
from pathlib import Path

# Add the src directory to the path so we can import our modules
sys.path.append(str(Path(__file__).parent))

from blog_generator.crew import BlogGenerator

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def generate_blog_post(topic, progress=gr.Progress()):
    """Generate a blog post using the AI agents."""
    if not topic.strip():
        return "❌ Please enter a topic to generate a blog post.", ""
    
    try:
        progress(0.1, desc="🤖 Initializing AI agents...")
        generator = BlogGenerator()
        
        progress(0.2, desc="🔄 Creating crew...")
        crew = generator.crew()
        
        progress(0.3, desc="⚡ Generating blog post...")
        inputs = {'topic': topic.strip()}
        
        progress(0.5, desc="🔄 AI agents working...")
        result = crew.kickoff(inputs=inputs)
        
        progress(1.0, desc="✅ Blog post generated successfully!")
        
        # Format the result for display
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted_result = f"""---
title: "{topic}"
author: "AI Blog Generator"
date: "{timestamp}"
---

# {topic}

{result}

---

*Generated on {timestamp} using AI Blog Generator*
"""
        
        return "✅ Blog post generated successfully!", formatted_result
        
    except Exception as e:
        error_msg = f"❌ Error occurred during generation: {str(e)}"
        return error_msg, ""

def download_markdown(content):
    """Create a downloadable markdown file."""
    if not content or content == "":
        return None
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"blog_post_{timestamp}.md"
    
    return (filename, content)

def download_html(content):
    """Create a downloadable HTML file."""
    if not content or content == "":
        return None
    
    try:
        # Convert markdown to HTML
        html_content = markdown.markdown(content, extensions=['fenced_code', 'tables'])
        
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

def main():
    """Main function to launch the Gradio interface."""
    
    # Custom CSS
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
        def on_generate(topic, progress=gr.Progress()):
            status, content = generate_blog_post(topic, progress)
            
            if "✅" in status:
                # Update formatted view
                formatted_content = content
                
                # Update raw markdown (remove frontmatter for raw view)
                raw_content = content
                if "---" in content:
                    parts = content.split("---", 2)
                    if len(parts) >= 3:
                        raw_content = parts[2].strip()
                
                # Update download buttons
                md_file = download_markdown(content)
                html_file = download_html(content)
                
                return status, formatted_content, raw_content, md_file, html_file
            else:
                return status, "*Generation failed*", "*Generation failed*", None, None
        
        # Connect the generate button
        generate_btn.click(
            fn=on_generate,
            inputs=[topic_input],
            outputs=[status_output, formatted_output, raw_output, download_md_btn, download_html_btn]
        )
    
    # Launch the interface
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True,
        quiet=False
    )

if __name__ == "__main__":
    main() 