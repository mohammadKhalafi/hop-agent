import os
import requests
from bs4 import BeautifulSoup

def get_list_content(soup, seperator_str):
    lists = []
    for ul in soup.find_all('ul'):
        lists.extend([li.get_text(strip=True) for li in ul.find_all('li')])

    return seperator_str.join(lists)
    

def get_cell_content(cell):
    paragraphs = [div.get_text(strip=True) for div in cell.find_all('div', class_='paragraph')]
    lists_cotent = get_list_content(cell, ', ')
    paragraphs.append(lists_cotent)
    cell_content = " ".join(paragraphs)
    if cell_content != "" : return cell_content
    return cell.get_text(strip=True)


def extract_section(section, name):
    all_elements = section.find_all(['div','table', 'code'])
    all_elements = list(all_elements)
    soup_content = [name + '\n']

    iterated_elements = []
    for element in all_elements:
        if any(iterated_element in element.parents for iterated_element in iterated_elements):
            continue
        if element.name == "div":
            classes = element.get("class", [])
            if 'sect2' in classes:
                iterated_elements.append(element)
                sect2_title = element.find(['h2', 'h3'])
                sect2_name = sect2_title.get_text(strip=True) if sect2_title else "Unnamed Subsection"
                soup_content.extend(extract_section(element, '\n' + name + ' -> ' + sect2_name))
            elif 'paragraph' in classes:
                iterated_elements.append(element)
                p = element.find('p')
                p_text = p.get_text(strip=True)
                soup_content.append(p_text)
            elif 'ulist' in classes:
                iterated_elements.append(element)
                list_content = get_list_content(element, '\n')
                soup_content.append(list_content)

        elif element.name == "table":
            iterated_elements.append(element)
            table = element
            rows = []
            for row in table.find_all('tr'):
                cells = [cell for cell in row.find_all(['th', 'td'])]
                cell_texts = []
                for cell in cells:
                    cell_texts.append(get_cell_content(cell))
                rows.append(" | ".join(cell_texts))
            soup_content.extend(rows)
    
        elif element.name == "code":
            iterated_elements.append(element)
            code_content = element.get_text(strip=True)
            code_content+='\n'
            soup_content.append(code_content)


    return soup_content


def extract_sections(soup):
    sect1_contents = []
    for sect1 in soup.find_all('div', class_='sect1'):
        sect1_title = sect1.find(['h2', 'h3'])
        if sect1_title:
            sect1_name = sect1_title.get_text(strip=True)
        else:
            sect1_name = "Unknown Section"

        if sect1_name == "Supported Engines": continue

        sectionbody = sect1.find('div', class_='sectionbody')
        if not sectionbody:
            continue  # Skip if no section body
        
        extracteds = extract_section(sectionbody, sect1_name)
        extracteds_str = '\n'.join(extracteds)
        sect1_contents.append(extracteds_str)
    
    return '\n\n\n'.join(sect1_contents)
            
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

# plugin_names = ["kafkaconsumer"]# plugin_names[0:2] "metastructure", "monetdbbulkloader", 
# plugin_names = plugin_names[0:10]


for plugin_name in plugin_names:
    plugin_url = base_plugins_url + plugin_name + '.html'
    
    try:
        # Fetch plugin page
        plugin_response = requests.get(plugin_url)
        plugin_soup = BeautifulSoup(plugin_response.text, 'html5lib')
        
        # Find plugin name
        plugin_name_in_doc = plugin_soup.find('h1')
        plugin_name_in_doc = plugin_name_in_doc.get_text(strip=True) if plugin_name_in_doc else "UnknownPlugin"

        data = extract_sections(plugin_soup)

        # Save to file
        with open(f'c:/Users/mohammad/Desktop/hop/hop_plugins/{plugin_name}.txt', 'w', encoding='utf-8') as f:
            f.write(f"Plugin: {plugin_name_in_doc}\n\n{data}")
            
        print(f"Saved {plugin_name}")
        
    except Exception as e:
        print(f"Error processing {plugin_name}: {str(e)}")

print("Crawling completed!")