# AI-Powered Todo List Application

A modern, retro-themed todo list application with AI capabilities powered by Mistral AI. This application helps you manage tasks with intelligent insights, natural language processing, and automatic date detection.

## Features

- **Task Management**: Create, complete, and delete tasks
- **AI-Powered Insights**: Get personalized comments and tips for each task
- **Natural Language Processing**: Add tasks using natural language
- **Automatic Date Detection**: The app automatically detects dates from your descriptions
- **Priority Management**: Tasks are automatically assigned priority levels
- **Beautiful UI**: Enjoy a nostalgic UI

<img width="1266" alt="Screenshot 2025-03-15 at 01 28 36" src="https://github.com/user-attachments/assets/a4e7428a-7ccf-4af1-a8b9-1a3baab155e0" />
<img width="1280" alt="Screenshot 2025-03-15 at 01 29 10" src="https://github.com/user-attachments/assets/0104017d-c2a0-4d84-87f8-a76d5412a0e3" />

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables in `.env`:
   ```
   MISTRAL_API_KEY=your_api_key
   DATABASE_URL=sqlite:///./todos.db
   ```

3. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

## API Endpoints

- `POST /tasks`: Create a new task
- `GET /tasks`: List all tasks
- `PUT /tasks/{task_id}`: Update a task
- `DELETE /tasks/{task_id}`: Delete a task
- `POST /webhook`: n8n webhook endpoint

## AI Integration

The application uses Mistralai API to analyze task descriptions and calendar events to intelligently assign and prioritize tasks.
