from flask import Flask, render_template
import scrapetube
import re

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# entities recognition
def get_names(title):
    # split title by '|'
    title = title.split('|')[0]
    # remove numbers
    title = re.sub(r'\d+', '', title)
    # remove parenthesis 
    title = re.sub(r'\(.*?\)', '', title)
    names = title.split('-')
    names = sorted(names)
    return names

@app.route('/category/<category_name>')
def category(category_name):
    videos = scrapetube.get_channel(channel_url='https://www.youtube.com.ar/tycsports/videos', limit=50)

    videosInfo = []

    for video in videos:
        video_id = video['videoId']
        title = video['title']['runs'][0]['text']
        date = video['publishedTimeText']['simpleText']
        video_category = None
        redex = re.search(r'\d+(\s*\(.*?\))?\s*-\s*(\(.*?\)\s*)?\d+', title)
        if 'wimbledon' in title:
            video_category = 'wimbledon'
        elif 'liga' in title.lower() or redex:
            video_category = 'futbol'
        elif 'nba' in title.lower():
            video_category = 'nba'
        
        # using SpaCy to get the names of the players or teams
        names = get_names(title)
        
        if video_category == category_name:
            videosInfo.append({
                'video_id': video_id,
                'title': title,
                'date': date,
                'category': video_category,
                'names': names
            })

    return render_template('category.html', videos=videosInfo, category=category_name)

if __name__ == '__main__':
    app.run(debug=True)
