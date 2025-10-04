# Movie API

Simple Django API for getting movie data from OMDB.

## How to run

1. Install Python packages:
   ```bash
   pip install -r backend/requirements.txt
   ```

2. Go to backend folder:
   ```bash
   cd backend
   ```

3. Start the server:
   ```bash
   python manage.py runserver
   ```

4. Open http://127.0.0.1:8000/ in your browser

## What it does

- Get movie details by title
- Get TV episode info  
- Find top movies by genre

## API Examples

- Movie: `/api/movie/?title=The Matrix`
- Episode: `/api/episode/?series_title=Breaking Bad&season=1&episode_number=1`
- Genre: `/api/movies/genre/?genre=Action`