# MoonKnight Backend

A FastAPI backend for the MoonKnight chat application with Supabase integration.

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment setup:**
   ```bash
   cp .env.example .env
   # Edit .env with your Supabase credentials
   ```

3. **Database setup:**
   - Run the SQL schemas in `DataBase/Chat_Database/SupaBase_Scheme.sql`
   - Run the SQL schemas in `DataBase/Usage_Database/SupaBase_Scheme.sql`

4. **Run the server:**
   ```bash
   uvicorn app:app --reload
   ```

## API Endpoints

### Auth
- `POST /auth/signup` - User signup
- `POST /auth/login` - User login
- `POST /auth/refresh` - Refresh tokens

### Chat
- `POST /chat/stream` - Send chat message

### Usage
- `POST /usage/log` - Log usage data
- `GET /usage/{user_id}` - Get user usage data

## Project Structure

```
Backend/
├── app.py                 # Main FastAPI app
├── supabase_client.py     # Supabase client setup
├── Auth/                  # Authentication module
├── Chat_Section/          # Chat functionality
├── Usage/                 # Usage monitoring
├── DataBase/              # Database operations
└── Router/                # API routers
```
