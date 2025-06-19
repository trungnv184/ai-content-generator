from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
import os
from datetime import datetime

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

            # Add frontmatter to the content
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            frontmatter = f"""---
title: "{topic} - Technical Deep Dive"
author: "AI Blog Writer"
date: "{timestamp}"
tags: ["{topic}", "technology", "tutorial"]
categories: ["Technical"]
status: "published"
featured: false
---

"""
            # Combine frontmatter with content
            full_content = frontmatter + content

            # Save the blog post
            filepath = self.save_blog_post(full_content, topic)

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
