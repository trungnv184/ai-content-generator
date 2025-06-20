from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
import os
from datetime import datetime
from .utils.diagram_generator import DiagramGenerator
from .utils.content_analyzer import ContentAnalyzer

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class BlogGenerator():
    """BlogGenerator crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    def __init__(self):
        super().__init__()
        # Create output directory if it doesn't exist
        self.output_dir = os.path.join(os.getcwd(), "output")
        os.makedirs(self.output_dir, exist_ok=True)

    def save_blog_post(self, content: str, topic: str) -> str:
        """Save the blog post to a markdown file."""
        print("\n=== Starting save_blog_post function ===")
        print(f"Content length: {len(content)} characters")
        print(f"Topic: {topic}")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{topic.replace(' ', '_')}_{timestamp}.md"
        filepath = os.path.join(self.output_dir, filename)
        
        print(f"Output directory: {self.output_dir}")
        print(f"Full filepath: {filepath}")
        
        try:
            with open(filepath, "w") as f:
                f.write(content)
            print(f"Successfully saved blog post to: {filepath}")
            print("=== Completed save_blog_post function ===\n")
            return filepath
        except Exception as e:
            print(f"Error saving blog post: {str(e)}")
            print("=== Failed save_blog_post function ===\n")
            raise

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'], # type: ignore[index]
            verbose=True
        )

    @agent
    def technical_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['technical_writer'], # type: ignore[index]
            verbose=True
        )
    
    @agent
    def technical_reviewer(self) -> Agent:
        return Agent( 
            config= self.agents_config['technical_reviewer'], # type: ignore[index]
            verbose=True
        )

    @agent
    def technical_publisher(self) -> Agent:
        return Agent(
            config= self.agents_config['technical_publisher'], # type: ignore[index]
            verbose=True
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'], # type: ignore[index]
        )
    
    @task
    def technical_writer_task(self) -> Task:    
        return Task(
            config=self.tasks_config['technical_writer_task'], # type: ignore[index]
        )
    
    @task
    def technical_reviewer_task(self) -> Task:
        return Task(
            config=self.tasks_config['technical_reviewer_task'], # type: ignore[index]
        )
    
    def _format_content_sections(self, content: str) -> str:
        """Format content sections for better readability."""
        # Split content into sections
        sections = content.split('\n#')
        formatted_sections = []

        for section in sections:
            if not section.strip():
                continue
            
            # Add back the # if it's not the first section
            if sections.index(section) > 0:
                section = '#' + section
            
            # Clean up the section formatting
            formatted_section = section.strip()
            formatted_sections.append(formatted_section)

        return '\n\n'.join(formatted_sections)

    def _generate_toc(self, content: str) -> str:
        """Generate table of contents from content headings."""
        toc = []
        lines = content.split('\n')
        
        for line in lines:
            if line.startswith('#'):
                # Count the heading level
                level = len(line.split()[0])
                # Get the heading text
                text = ' '.join(line.split()[1:])
                # Create the anchor link
                anchor = text.lower().replace(' ', '-').replace(':', '').replace('(', '').replace(')', '')
                # Add indentation based on heading level
                indent = '  ' * (level - 1)
                toc.append(f"{indent}- [{text}](#{anchor})")

        return '\n'.join(toc)

    @task
    def technical_publisher_task(self) -> Task:
        def save_blog_callback(task_output) -> str:
            print("\n=== Starting save_blog_callback ===")
            # Try to extract the actual content from the TaskOutput object
            if hasattr(task_output, "output"):
                content = task_output.output
            elif isinstance(task_output, str):
                content = task_output
            else:
                print("Unknown task_output type:", type(task_output))
                content = str(task_output)

            print(f"Content length: {len(content)}")
            # Use the topic from the main input or fallback
            topic = self.tasks_config['technical_publisher_task']['description'].split('\n')[0].strip()

            # Add simple frontmatter
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            frontmatter = f"""---
title: "{topic}"
author: "Trung Nguyen"
date: "{timestamp}"
---

"""
            # Analyze content and extract diagram information
            print("Analyzing content for diagram generation...")
            diagrams = ContentAnalyzer.extract_diagram_info(content)
            
            # Generate diagrams based on the analyzed content
            diagram_sections = []
            
            if 'architecture' in diagrams:
                architecture_diagram = DiagramGenerator.generate_diagram('component', diagrams['architecture']['data'])
                diagram_sections.append(f"""
## System Architecture

{architecture_diagram}

""")
            
            if 'workflow' in diagrams:
                workflow_diagram = DiagramGenerator.generate_diagram('flowchart', diagrams['workflow']['data'])
                diagram_sections.append(f"""
## Process Flow

{workflow_diagram}

""")
            
            if 'state_machine' in diagrams:
                state_diagram = DiagramGenerator.generate_diagram('state', diagrams['state_machine']['data'])
                diagram_sections.append(f"""
## State Transitions

{state_diagram}

""")
            
            if 'class' in diagrams:
                class_diagram = DiagramGenerator.generate_diagram('class', diagrams['class']['data'])
                diagram_sections.append(f"""
## Class Structure

{class_diagram}

""")

            # Format the main content with better readability
            formatted_content = self._format_content_sections(content)

            # Combine everything with topic prefix
            content_with_diagrams = f"""{frontmatter}
# {topic}

{formatted_content}

## Technical Diagrams

{''.join(diagram_sections)}

---

*Generated on {timestamp}*
"""

            # Save the blog post
            filepath = self.save_blog_post(content_with_diagrams, topic)

            print("=== Completed save_blog_callback ===\n")
            return filepath

        return Task(
            config=self.tasks_config['technical_publisher_task'], # type: ignore[index]
            context=[
                {
                    "description": "Output directory for the blog post",
                    "expected_output": "Directory path",
                    "output_dir": self.output_dir
                }
            ],
            callback=save_blog_callback,
            dependencies=[self.technical_reviewer_task]  # Add dependency on reviewer task
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents, # type: ignore[index]
            tasks=self.tasks, # type: ignore[index]
            process=Process.sequential,
            verbose=True,
        )
