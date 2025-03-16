import os
from datetime import datetime
from typing import Optional, Dict, Any
from dotenv import load_dotenv
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
import re
from datetime import datetime, timedelta

load_dotenv()
mistral_api_key = os.getenv("MISTRAL_API_KEY")
if not mistral_api_key:
    raise ValueError("MISTRAL_API_KEY environment variable is not set")
client = MistralClient(api_key=mistral_api_key)

class AIService:
    @staticmethod
    def convert_markdown_to_plain_text(text: str) -> str:
        """Convert markdown formatting to plain text."""
        # Remove bold/italic formatting
        text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)  # Remove **bold**
        text = re.sub(r'\*(.*?)\*', r'\1', text)      # Remove *italic*
        text = re.sub(r'__(.*?)__', r'\1', text)      # Remove __bold__
        text = re.sub(r'_(.*?)_', r'\1', text)        # Remove _italic_
        
        # Remove markdown headers
        text = re.sub(r'^#{1,6}\s+(.*?)$', r'\1', text, flags=re.MULTILINE)
        
        # Remove bullet points
        text = re.sub(r'^\s*[\*\-\+]\s+(.*?)$', r'\1', text, flags=re.MULTILINE)
        
        # Remove numbered lists
        text = re.sub(r'^\s*\d+\.\s+(.*?)$', r'\1', text, flags=re.MULTILINE)
        
        # Remove code blocks and inline code
        text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
        text = re.sub(r'`(.*?)`', r'\1', text)
        
        return text

    @staticmethod
    def analyze_task(title: str, description: Optional[str], due_date: Optional[datetime]) -> Dict[str, Any]:
        prompt = f"Analyze this task and provide a brief, fun response:\nTitle: {title}\n"
        if description:
            prompt += f"Description: {description}\n"
        if due_date:
            prompt += f"Due Date: {due_date.strftime('%Y-%m-%d')}\n"
        
        prompt += "\nProvide a short, engaging analysis with:\n"
        prompt += "\n1. A brief, fun comment about the task\n"
        prompt += "\n2. One quick tip\n"
        prompt += "\nFormat your response like this example:\n"
        prompt += "\nComment: Looks like someone's feeling inspired!\n\n"
        prompt += "\nTip: Grab a canvas and let your imagination run wild!\n"
        prompt += "\nKeep it concise and add a touch of humor!\n"
        prompt += "\nIMPORTANT: Format your response as plain text. Do not use markdown formatting like bold, italic, or bullet points.\n"
        prompt += "\nDo NOT include any priority level in your response text as this is handled separately.\n"

        try:
            messages = [
                ChatMessage(role="system", content="You are a friendly and witty task assistant. Keep responses short, fun, and actionable. Use plain text only, no markdown formatting. Format your response with 'Comment:' and 'Tip:' on separate lines with spacing between them."),
                ChatMessage(role="user", content=prompt)
            ]
            response = client.chat(model="mistral-large-latest", messages=messages)

            analysis = response.choices[0].message.content
            
            # Convert any remaining markdown to plain text
            analysis = AIService.convert_markdown_to_plain_text(analysis)
            
            # Determine priority from task content
            priority = 1
            if title:
                title_lower = title.lower()
                if any(word in title_lower for word in ["urgent", "asap", "important", "high priority"]):
                    priority = 3
                elif any(word in title_lower for word in ["medium", "moderate"]):
                    priority = 2
            
            if description:
                desc_lower = description.lower()
                if any(word in desc_lower for word in ["urgent", "asap", "important", "high priority"]):
                    priority = 3
                elif any(word in desc_lower for word in ["medium", "moderate"]):
                    priority = 2

            return {
                "priority": priority,
                "ai_notes": analysis
            }
        except Exception as e:
            print(f"Error calling Mistral AI API: {e}")
            return {
                "priority": priority,
                "ai_notes": "Comment: Oops! My circuits are a bit fuzzy right now.\n\nTip: Let's keep it simple!"
            }

    @staticmethod
    def parse_text_message(text: str) -> Dict[str, Any]:
        try:
            # Extract date from text
            extracted_date = AIService.extract_date_from_text(text)
            
            prompt = f"Parse this task and extract key info with a fun twist:\n{text}\n\n"
            prompt += "Extract:\n"
            prompt += "1. Task title\n"
            prompt += "2. Priority level\n"
            prompt += "3. A short, witty comment\n"
            prompt += "\nIMPORTANT: Format your response as plain text. Do not use markdown formatting like bold, italic, or bullet points."
            
            messages = [
                ChatMessage(role="system", content="You are a friendly task parser that keeps things fun and simple. Use plain text only, no markdown formatting."),
                ChatMessage(role="user", content=prompt)
            ]
            response = client.chat(model="mistral-large-largest", messages=messages)

            # Process the response and extract information
            analysis = response.choices[0].message.content
            
            # Convert any remaining markdown to plain text
            analysis = AIService.convert_markdown_to_plain_text(analysis)
            
            # Simple priority detection
            priority = 1
            if any(word in text.lower() for word in ["urgent", "asap", "important", "high priority"]):
                priority = 3
            elif any(word in text.lower() for word in ["medium", "moderate"]):
                priority = 2
            
            return {
                "title": text.split("\n")[0],  # Use first line as title
                "description": analysis,
                "priority": priority,
                "due_date": extracted_date
            }
        except Exception as e:
            print(f"Error parsing text message: {e}")
            return {
                "title": text,
                "description": "Let's keep it simple and get it done!",
                "priority": 1,
                "due_date": None
            }
    
    @staticmethod
    def extract_date_from_text(text: str) -> Optional[datetime]:
        """Extract date from natural language text."""
        if not text:
            return None
            
        text = text.lower()
        today = datetime.now()
        
        # Check for "today"
        if "today" in text:
            return today
            
        # Check for "tomorrow"
        if "tomorrow" in text:
            return today + timedelta(days=1)
            
        # Check for "next week"
        if "next week" in text:
            return today + timedelta(days=7)
            
        # Check for days of the week
        days = {
            "monday": 0, "tuesday": 1, "wednesday": 2, 
            "thursday": 3, "friday": 4, "saturday": 5, "sunday": 6
        }
        
        for day, day_num in days.items():
            # Check for "this [day]"
            this_day_pattern = f"this {day}"
            if this_day_pattern in text:
                days_ahead = (day_num - today.weekday()) % 7
                if days_ahead == 0:  # Today is the day mentioned
                    days_ahead = 7
                return today + timedelta(days=days_ahead)
                
            # Check for "next [day]"
            next_day_pattern = f"next {day}"
            if next_day_pattern in text:
                days_ahead = (day_num - today.weekday()) % 7
                if days_ahead == 0:  # Today is the day mentioned
                    days_ahead = 7
                return today + timedelta(days=days_ahead + 7)
                
            # Check for just the day name
            if f" {day}" in f" {text} ":
                days_ahead = (day_num - today.weekday()) % 7
                if days_ahead == 0:  # Today is the day mentioned
                    days_ahead = 7
                return today + timedelta(days=days_ahead)
                
        # Try to use AI to extract date
        try:
            prompt = f"Extract only the due date from this text in YYYY-MM-DD format. If no specific date is mentioned, respond with 'None':\n\n{text}"
            
            messages = [
                ChatMessage(role="system", content="You are a helpful assistant that extracts dates from text."),
                ChatMessage(role="user", content=prompt)
            ]
            response = client.chat(model="mistral-tiny", messages=messages)
            
            date_text = response.choices[0].message.content.strip()
            
            # Try to parse the date
            if date_text and date_text.lower() != "none":
                # Look for YYYY-MM-DD pattern
                date_match = re.search(r'\d{4}-\d{2}-\d{2}', date_text)
                if date_match:
                    return datetime.strptime(date_match.group(), "%Y-%m-%d")
            
            return None
        except Exception as e:
            print(f"Error extracting date with AI: {e}")
            return None