import scrapetube
import re

# entities recognition
def get_names(title):
    # split title by '|'
    title = title.split('|')[0]
    # remove numbers
    title = re.sub(r'\d+', '', title)
    # remove parenthesis 
    title = re.sub(r'\(.*?\)', '', title)
    names = None
    if '-' in title:
        names = title.split('-')
    if 'vs' in title:
        names = title.split('vs')
    if names:
        names = sorted(names)
    return names


def main(category_name):
    videosInfo = []
    urls = [
        'https://www.youtube.com.ar/tycsports/videos',
        'https://www.youtube.com.ar/user/espndeportes/videos'
    ]
    for url in urls:
        videos = scrapetube.get_channel(channel_url=url, limit=50)
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
            
            negatives = ['dijo', 'dijeron', 'entrevista', 'conferencia', 'habla', 'hablan', 'habló', 'hablaron', 'hablando', 'hablaba']
            if any(negative in title.lower() for negative in negatives):
                continue
            
            # using SpaCy to get the names of the players or teams
            names = get_names(title)
            
            if names and video_category == category_name:
                videosInfo.append({
                    'video_id': video_id,
                    'title': title,
                    'date': date,
                    'category': video_category,
                    'names': names
                })



if __name__ == '__main__':
    main('futbol')
