import os
import requests
from bs4 import BeautifulSoup

# Create directory for plugin descriptions
os.makedirs('hop_plugins', exist_ok=True)

# Fetch main transforms page
base_plugins_url = "https://hop.apache.org/manual/latest/pipeline/transforms/"
transforms_url = "https://hop.apache.org/manual/latest/pipeline/transforms.html"

response = requests.get(transforms_url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find all plugin links (they're in <li> tags within the main <div>)
all_links = []
main_div = soup.find('div', {'class': 'body'})
if main_div:
    for li in main_div.find_all('li'):
        link = li.find('a')
        if link and link.get('href'):
            all_links.append(link['href'])

plugin_links = filter(lambda i : i.startswith('transforms/'), all_links)
plugin_links = set(plugin_links)
plugin_links = list(plugin_links)
plugin_links.sort()

plugin_names = [p.split("/")[1].split(".")[0] for p in plugin_links]

plugin_names = ["metastructure"]# plugin_names[0:2]

# for l in plugin_names:
#     print(l)
# print(len(plugin_names))

for plugin_name in plugin_names:
    plugin_url = base_plugins_url + plugin_name + '.html'
    
    try:
        # Fetch plugin page
        plugin_response = requests.get(plugin_url)
        plugin_soup = BeautifulSoup(plugin_response.text, 'html5lib')
        
        # Find plugin name
        plugin_name_in_doc = plugin_soup.find('h1')
        plugin_name_in_doc = plugin_name_in_doc.get_text(strip=True) if plugin_name_in_doc else "UnknownPlugin"

        description_section = plugin_soup.find('h2', id='_description').parent
        paragraphs = description_section.select('.sectionbody .paragraph')
        description = "\n".join(p.get_text(strip=True) for p in paragraphs)
        
        # Save to file
        with open(f'c:/Users/mohammad/Desktop/hop/hop_plugins/{plugin_name}.txt', 'w', encoding='utf-8') as f:
            f.write(f"Plugin: {plugin_name_in_doc}\n\nDescription:\n{description}")
            
        print(f"Saved {plugin_name}")
        
    except Exception as e:
        print(f"Error processing {plugin_name}: {str(e)}")

print("Crawling completed!")