import scrapetube
import re
from supabase import create_client
import os
import datetime
from datetime import datetime, timedelta

# Supabase setup
supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")

supabase = create_client(supabase_url, supabase_key)

# Authenticate (if using authentication)

# data = supabase.auth.sign_in_with_oauth({
#   "provider": 'github'
# })


def get_names(title, channel):
    if channel == 'tycsports':
        title = title.split('|')[0]  # split title by '|'
        pattern = r"(.+)\s+\d+\s*(?:\(\d+\))*\s*-\s*(?:\(\d+\))*\s*\d+\s+(.+)"
        match = re.match(pattern, title.strip())
        if match:
            name1 = match.group(1)
            name2 = match.group(2)
            name1 = re.sub(r'(?<!Sub-)\b\d+\b|\(\d+\)', '', name1).strip()
            name2 = re.sub(r'(?<!Sub-)\b\d+\b|\(\d+\)', '', name2).strip()
            return name1, name2
        else:
            return None
    elif channel == 'espndeportes':
        title = title.split('|')[0]  # split title by '|'
        nameAndSurname = r'([A-Z][a-z]+ [A-Z][a-z]+)'
        pattern = rf'{nameAndSurname}.*{nameAndSurname}'
        match = re.search(pattern, title)

        if match:
            name1 = match.group(1)
            name2 = match.group(2)
            return name1, name2
        else:
            return None
    return None

def update_database():
    videosInfo = []
    channels = [ 'tycsports', 'espndeportes', 'ESPNFans']
    for channel in channels:
        videos = scrapetube.get_channel(channel_url=f'https://www.youtube.com.ar/{channel}/videos', limit=200)
        for video in videos:
            video_id = video['videoId']
            title = video['title']['runs'][0]['text']
            publishedTimeText = video['publishedTimeText']['simpleText']
            

            video_category = getCategory(title)

            negatives = ['dijo', 'dijeron', 'entrevista', 'conferencia', 'habla', 'hablan', 'habló', 'hablaron', 'hablando', 'hablaba', '"']
            if any(negative in title.lower() for negative in negatives) or (video_category is None):
                continue

            names = get_names(title, channel)
            if names is None:
                continue

            presentation = ' vs '.join(names) if names else title
            
            video_info = {
                "id": 1,
                'video_id': video_id,
                'title': title,
                'publishedTimeText': publishedTimeText,
                'category': video_category,
                'presentation': presentation,
                'channel' : channel,
                'created_at': datetime.now().strftime("%Y-%m-%d")
            }
            videosInfo.append(video_info)

    # Remove all rows with 'created_at' exceeding 1 week (that column has type 'date')
    keepLastWeekVideos()

    # get all id's
    IDs = supabase.table("deportes_sin_spoiler_videos").select("id").execute().data
    IDs = [video['id'] for video in IDs]
    max_id = 0 if not IDs else max(IDs)
    for video in videosInfo:
        video['id'] = max_id + 1
        max_id += 1

    for video in videosInfo:

        response = supabase.table("deportes_sin_spoiler_videos").select("*").eq("video_id", f"{video['video_id']}").execute()

        if not response.data:
            response = (
                supabase.table("deportes_sin_spoiler_videos")
                .insert(video)
                .execute()
            )


def keepLastWeekVideos():
    oneWeekAgo = datetime.now() - timedelta(days=7)
    oneWeekAgo = oneWeekAgo.strftime("%Y-%m-%d")
    response = supabase.table("deportes_sin_spoiler_videos").delete().lte("created_at", oneWeekAgo).execute()
    for video in response.data:
        response = supabase.table("deportes_sin_spoiler_videos").delete().eq("id", video['id']).execute()


def getCategory(title):
    video_category = None
    redex = re.search(r'\d+(\s*\(.*?\))?\s*-\s*(\(.*?\)\s*)?\d+', title)
    if 'wimbledon' in title.lower():
        video_category = 'Wimbledon'
    elif 'liga' in title.lower() or redex:
        video_category = 'Fútbol'
    elif 'nba' in title.lower():
        video_category = 'NBA'
    return video_category


if __name__ == "__main__":
    update_database()
