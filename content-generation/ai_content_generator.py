
# AI Content Generator - Starter Project
# This is a basic implementation of automated blog content generation

import openai
import os
from datetime import datetime
import json

class AIContentGenerator:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if self.api_key:
            openai.api_key = self.api_key
    
    def generate_blog_post(self, topic, target_audience="general", word_count=800):
        """
        Generate a blog post on a given topic
        
        Args:
            topic (str): The main topic for the blog post
            target_audience (str): Target audience (e.g., 'entrepreneurs', 'students')
            word_count (int): Approximate word count for the post
        
        Returns:
            dict: Generated content with title, body, and metadata
        """
        
        prompt = f"""
        Write a comprehensive blog post about '{topic}' for {target_audience}.
        
        Requirements:
        - Approximately {word_count} words
        - Include an engaging title
        - Structure with clear headings and subheadings
        - Include practical tips or actionable advice
        - End with a conclusion that encourages engagement
        - Use a conversational but professional tone
        
        Format the response as:
        TITLE: [Blog post title]
        
        CONTENT:
        [Full blog post content with proper formatting]
        
        TAGS: [5 relevant tags separated by commas]
        """
        
        try:
            # Estimate tokens needed for the blog post
            # Average token length is ~4 characters, or 0.75 words
            # Add a buffer for prompt, formatting, etc.
            estimated_tokens = int(word_count * 1.5)

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert content writer specializing in engaging, SEO-friendly blog posts."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=estimated_tokens,
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            
            # Parse the response
            lines = content.split('\n')
            title = ""
            body = ""
            tags = ""
            current_section = ""
            
            for line in lines:
                if line.startswith("TITLE:"):
                    title = line.replace("TITLE:", "").strip()
                    current_section = "title"
                elif line.startswith("CONTENT:"):
                    current_section = "content"
                elif line.startswith("TAGS:"):
                    tags = line.replace("TAGS:", "").strip()
                    current_section = "tags"
                elif current_section == "content" and line.strip():
                    body += line + "\n"
            
            full_content = title + "\n" + body

            return {
                "title": title,
                "content": body.strip(),
                "tags": [tag.strip() for tag in tags.split(",") if tag.strip()],
                "topic": topic,
                "target_audience": target_audience,
                "word_count": len(full_content.split()),
                "generated_at": datetime.now().isoformat(),
                "status": "success"
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "generated_at": datetime.now().isoformat()
            }
    
    def generate_content_calendar(self, niche, num_posts=30):
        """
        Generate a content calendar with blog post ideas
        
        Args:
            niche (str): The niche or industry focus
            num_posts (int): Number of blog post ideas to generate
        
        Returns:
            list: List of content ideas with titles and descriptions
        """
        
        prompt = f"""
        Create {num_posts} blog post ideas for the {niche} niche.
        
        For each idea, provide:
        1. A compelling title
        2. A brief description (2-3 sentences)
        3. Target audience
        4. Estimated difficulty level (Beginner/Intermediate/Advanced)
        
        Format each idea as:
        IDEA [number]:
        Title: [title]
        Description: [description]
        Audience: [target audience]
        Level: [difficulty level]
        ---
        """
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a content strategist specializing in creating engaging content calendars."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.8
            )
            
            content = response.choices[0].message.content
            ideas = []
            
            # Parse the ideas (simplified parsing)
            sections = content.split('---')
            for section in sections:
                if 'IDEA' in section and 'Title:' in section:
                    lines = section.strip().split('\n')
                    idea = {"generated_at": datetime.now().isoformat()}
                    
                    for line in lines:
                        if line.startswith('Title:'):
                            idea['title'] = line.replace('Title:', '').strip()
                        elif line.startswith('Description:'):
                            idea['description'] = line.replace('Description:', '').strip()
                        elif line.startswith('Audience:'):
                            idea['audience'] = line.replace('Audience:', '').strip()
                        elif line.startswith('Level:'):
                            idea['level'] = line.replace('Level:', '').strip()
                    
                    if 'title' in idea:
                        ideas.append(idea)
            
            return {
                "niche": niche,
                "total_ideas": len(ideas),
                "ideas": ideas,
                "generated_at": datetime.now().isoformat(),
                "status": "success"
            }
            
        except Exception as e:
            return {
                "status": "error", 
                "error": str(e),
                "generated_at": datetime.now().isoformat()
            }

# Example usage and testing
if __name__ == "__main__":
    # Initialize the content generator
    generator = AIContentGenerator()
    
    # Example 1: Generate a single blog post
    print("Generating blog post about 'Passive Income Strategies'...")
    blog_post = generator.generate_blog_post(
        topic="Passive Income Strategies for Beginners",
        target_audience="aspiring entrepreneurs",
        word_count=600
    )
    
    if blog_post["status"] == "success":
        print(f"✅ Generated: {blog_post['title']}")
        print(f"📊 Word count: {blog_post['word_count']}")
        print(f"🏷️ Tags: {', '.join(blog_post['tags'])}")
    else:
        print(f"❌ Error: {blog_post['error']}")
    
    # Example 2: Generate content calendar
    print("\nGenerating content calendar for 'AI and Technology' niche...")
    calendar = generator.generate_content_calendar(
        niche="AI and Technology",
        num_posts=10
    )
    
    if calendar["status"] == "success":
        print(f"✅ Generated {calendar['total_ideas']} content ideas")
        for i, idea in enumerate(calendar['ideas'][:3], 1):
            print(f"  {i}. {idea.get('title', 'No title')}")
    else:
        print(f"❌ Error: {calendar['error']}")
    
    # Save example outputs
    with open('ai_content_examples.json', 'w') as f:
        json.dump({
            "blog_post_example": blog_post,
            "content_calendar_example": calendar
        }, f, indent=2)
    
    print("\n💾 Examples saved to ai_content_examples.json")
