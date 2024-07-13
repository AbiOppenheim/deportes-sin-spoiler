from flask import Flask, render_template
from supabase import create_client
import os

app = Flask(__name__)

# Initialize Supabase client
supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")

supabase = create_client(supabase_url, supabase_key)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/category/<category>')
def category(category):
    response = supabase.table("deportes_sin_spoiler_videos").select("*").eq("category", category).execute()
    videos = response.data
    return render_template('category.html', videos=videos, category=category)

if __name__ == '__main__':
    app.run(debug=True)