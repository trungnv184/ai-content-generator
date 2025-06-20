# AI Blog Generator UI

A modern web interface for the AI Blog Generator built with Gradio and CrewAI.

## Features

- 🎯 **Easy Topic Input**: Simple text area for entering blog topics
- 🚀 **Real-time Generation**: Watch the AI agents work with progress tracking
- 📊 **Progress Tracking**: Visual progress indicators and status updates
- 📖 **Multiple Views**: Formatted preview, raw markdown, and download options
- 💾 **Export Options**: Download as Markdown or HTML files
- 🎨 **Modern UI**: Beautiful, responsive design with custom styling
- 🔄 **Live Updates**: Real-time progress updates during generation

## Quick Start

### Option 1: Using the UI Script

```bash
# Navigate to the project directory
cd apps/crewai-generator/blog_generator

# Run the UI
python run_ui.py
```

### Option 2: Using the Main Script

```bash
# Navigate to the project directory
cd apps/crewai-generator/blog_generator

# Run with UI mode
python -m blog_generator.main --mode ui
```

### Option 3: Direct Gradio Command

```bash
# Navigate to the project directory
cd apps/crewai-generator/blog_generator

# Run gradio directly
gradio run src/blog_generator/ui.py --server.port 7860
```

## How to Use

1. **Enter Your Topic**: In the left panel, enter a detailed description of the blog topic you want to generate
2. **Configure Options**: Choose whether to generate technical diagrams and save to file
3. **Generate**: Click the "Generate Blog Post" button
4. **Wait**: The process takes 2-5 minutes as multiple AI agents work together
5. **View Results**: See the generated content in formatted view, raw markdown, or download it

## UI Components

### Left Panel - Configuration

- **Blog Topic**: Text area for entering your topic
- **Advanced Options**: Toggle for diagrams and file saving
- **Generate Button**: Primary action to start blog generation
- **Status Display**: Real-time status updates
- **About Section**: Information about the AI agents used

### Right Panel - Content Display

- **Tabs Interface**: Three tabs for different content views
  - **Formatted View**: HTML-rendered preview of the blog post
  - **Raw Markdown**: Source markdown code with syntax highlighting
  - **Download**: Export options for Markdown and HTML files

### Progress Tracking

- **Real-time Progress**: Visual progress bar with percentage
- **Status Messages**: Detailed status updates during generation
- **Error Handling**: Clear error messages if something goes wrong

## AI Agents Used

The UI orchestrates four specialized AI agents:

1. **Researcher** 🔍: Gathers comprehensive information about the topic
2. **Technical Writer** ✍️: Creates well-structured, engaging content
3. **Technical Reviewer** 🔍: Ensures quality, accuracy, and completeness
4. **Technical Publisher** 📝: Formats and publishes the final post

## Technical Details

- **Framework**: Gradio for the web interface
- **Backend**: CrewAI for AI agent orchestration
- **Styling**: Custom CSS for modern, responsive design
- **Export**: Markdown and HTML download options
- **Progress**: Real-time status updates and progress indicators
- **Port**: Runs on port 7860 by default

## Troubleshooting

### Common Issues

1. **Port Already in Use**: If port 7860 is busy, you can change it in the launch parameters
2. **Import Errors**: Make sure all dependencies are installed: `uv add gradio markdown`
3. **Slow Generation**: Blog generation typically takes 2-5 minutes depending on topic complexity

### Error Messages

- **"Please enter a topic"**: Make sure you've entered a topic in the input field
- **"Error occurred during generation"**: Check the console for detailed error information
- **"UI file not found"**: Ensure you're running from the correct directory

## Development

To modify the UI:

1. Edit `src/blog_generator/ui.py` for UI changes
2. Edit `src/blog_generator/crew.py` for AI agent changes
3. Edit `config/` files for agent and task configurations

## Browser Compatibility

The UI works best with modern browsers:

- Chrome/Chromium
- Firefox
- Safari
- Edge

## Performance Tips

- Use specific, detailed topics for better results
- The generation process is CPU and memory intensive
- Consider closing other applications during generation for better performance
- The UI provides real-time progress updates so you can monitor the generation process

## Gradio Features Used

- **Blocks Interface**: Modern, flexible layout system
- **Progress Tracking**: Built-in progress indicators
- **Tabbed Interface**: Organized content display
- **Download Buttons**: Easy file export functionality
- **Custom CSS**: Styled interface with gradient headers
- **Real-time Updates**: Live status and progress updates
