from pybooru import Danbooru
import requests
import os

links = []
def download(tag):
  try:
    username = os.getenv('DANBOORU_USER')
    apikey = os.getenv('DANBOORU_KEY')
    client = Danbooru('danbooru', username=username, api_key=apikey)

    print('collecting')
    # Collect links
    while len(links) < 3:  # Checks if the list is full
      posts = client.post_list(tags=tag, page=1, limit=200)
      for post in posts:
        try:
          fileurl = 'http://danbooru.donmai.us' + post['file_url']
        except:
          fileurl = 'http://danbooru.donmai.us' + post['source']
        links.append((post['id'], fileurl))

    print('downloading')
    # Download images
    for id, url in links:
      try:
        res = requests.get(url)
        filename = url.split('/')[-1]
        with open(os.path.join("./tmp/", filename), 'wb') as f:
          f.write(res.content)
      except:
        print('miss')
        continue
  except Exception as e:
    raise e

def main():
  download(tag='rating:s order:rank')

main()
