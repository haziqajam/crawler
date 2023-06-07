import argparse
import requests
from bs4 import BeautifulSoup
import json

def crawler(url, depth):
    if depth < 0:
        return []

    result = []
    visited_urls = set()
    visited_urls.add(url)

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract images
        images = soup.find_all('img')
        for image in images:
            image_url = image['src']
            image_data = {
                'imageUrl': image_url,
                'sourceUrl': url,
                'depth': depth
            }
            result.append(image_data)
            print(len(result))

        if depth > 0:
            # Find links
            links = soup.find_all('a')
            for link in links:
                if 'href' in link.attrs:
                    href = link['href']
                    if href.startswith('http') and href not in visited_urls:
                        visited_urls.add(href)
                        subresult = crawler(href, depth - 1)

                        result.extend(subresult)
                    print(len(result))
            

    except Exception as e:
        print(e)
        
    return result

# Argument parsing
parser = argparse.ArgumentParser()
parser.add_argument('starturl', type=str, )
parser.add_argument('depth', type=int)
args = parser.parse_args()

url = args.starturl
depth = args.depth

results = {'results': crawler(url, depth)}

# Save results to JSON file
with open('results.json', 'w') as file:
    json.dump(results, file)
