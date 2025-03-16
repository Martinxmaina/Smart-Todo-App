from flask import Flask, request, render_template, redirect, url_for, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from typing import Optional
from datetime import datetime
import os

from models import Base, Task
from ai_service import AIService

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todos.db")
engine = create_engine(DATABASE_URL)

# Create session factory
Session = scoped_session(sessionmaker(bind=engine))

# Create tables
Base.metadata.create_all(engine)

# Flask app setup
app = Flask(__name__)
app.secret_key = "your-secret-key-here"  # Add this line for flash messages

# Routes
@app.route("/", methods=["GET"])
def home():
    db = Session()
    try:
        tasks = db.query(Task).all()
        return render_template("index.html", tasks=tasks)
    finally:
        db.close()

@app.route("/tasks", methods=["POST"])
def create_task():
    db = Session()
    try:
        title = request.form["title"]
        description = request.form.get("description")
        due_date = request.form.get("due_date")

        # Parse due date if provided in the form
        parsed_due_date = None
        if due_date:
            try:
                parsed_due_date = datetime.strptime(due_date, "%Y-%m-%d")
            except ValueError:
                pass
        
        # If no date was provided in the form, try to extract it from the description
        if not parsed_due_date and description:
            extracted_date = AIService.extract_date_from_text(description)
            if extracted_date:
                parsed_due_date = extracted_date
                flash(f"Due date automatically set to {parsed_due_date.strftime('%Y-%m-%d')} based on your description!", "info")

        # Use AI to analyze task
        analysis = AIService.analyze_task(title, description, parsed_due_date)

        # Create new task
        new_task = Task(
            title=title,
            description=description,
            due_date=parsed_due_date,
            priority=analysis["priority"],
            ai_notes=analysis["ai_notes"]
        )

        db.add(new_task)
        db.commit()
        flash("Task added successfully!", "success")
        return redirect(url_for("home"))
    finally:
        db.close()

# Similarly, add flash messages to the create_task_from_text function
@app.route("/tasks/text", methods=["POST"])
def create_task_from_text():
    db = Session()
    try:
        text_message = request.form.get("text_message")
        if not text_message:
            return redirect(url_for("home"))
            
        # Parse the text message using AI
        parsed_data = AIService.parse_text_message(text_message)
        
        # Parse due date if provided
        parsed_due_date = parsed_data.get("due_date")
        
        # Use AI to analyze task
        analysis = AIService.analyze_task(
            parsed_data.get("title"), 
            parsed_data.get("description"), 
            parsed_due_date
        )
        
        # Create new task
        new_task = Task(
            title=parsed_data.get("title"),
            description=parsed_data.get("description"),
            due_date=parsed_due_date,
            priority=parsed_data.get("priority") or analysis["priority"],
            ai_notes=analysis["ai_notes"]
        )

        db.add(new_task)
        db.commit()
        flash("Task added successfully!", "success")  # Add this line
        return redirect(url_for("home"))
    finally:
        db.close()

@app.route("/tasks/<int:task_id>/complete", methods=["POST"])
def complete_task(task_id):
    db = Session()
    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            return "Task not found", 404

        task.completed = not task.completed
        db.commit()
        return redirect(url_for("home"))
    finally:
        db.close()

@app.route("/tasks/<int:task_id>/delete", methods=["POST"])
def delete_task(task_id):
    db = Session()
    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            return "Task not found", 404

        db.delete(task)
        db.commit()
        return redirect(url_for("home"))
    finally:
        db.close()

# API endpoints for potential integration
@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    db = Session()
    try:
        tasks = db.query(Task).all()
        return [{"id": task.id, 
                "title": task.title,
                "description": task.description,
                "due_date": task.due_date,
                "completed": task.completed,
                "priority": task.priority,
                "ai_notes": task.ai_notes} for task in tasks]
    finally:
        db.close()

if __name__ == "__main__":
    app.run(debug=True)