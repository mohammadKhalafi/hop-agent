import os
import requests
from bs4 import BeautifulSoup

def extract3(soup, name):
    all_elements = soup.find_all(['div','table'])
    all_elements = list(all_elements)
    soup_content = [name + '\n']

    iterated_elements = []
    for element in all_elements:
        iterated_elements.append(element)
        if any(iterated_element in element.parents for iterated_element in iterated_elements):
            continue
        if element.name == "div":
            if 'sect2' in element.get("class", []):
                sect2_title = element.find(['h2', 'h3'])
                sect2_name = sect2_title.get_text(strip=True) if sect2_title else "Unnamed Subsection"
                # soup_content.append('\n' + name + ' -> ' + sect2_name)
                soup_content.extend(extract3(element, '\n' + name + ' -> ' + sect2_name))
            elif 'paragraph' in element.get("class", []):
                p = element.find('p')
                p_text = p.get_text(strip=True)
                soup_content.append(p_text)
        elif element.name == "table":
            table = element
            rows = []
            for row in table.find_all('tr'):
                cells = [cell for cell in row.find_all(['th', 'td'])]
                cell_texts = []
                for cell in cells:
                    cell_texts.append(cell.get_text(strip=True))
                rows.append(" | ".join(cells))
            soup_content.extend(rows)
    
    return soup_content



def extract_sections2(soup):
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
        
        extracteds = extract3(sectionbody, sect1_name)
        extracteds_str = '\n'.join(extracteds)
        sect1_contents.append(extracteds_str)
    
    return '\n\n\n'.join(sect1_contents)
            

def extract_sections(soup):
    data = {}

    # Find all sect1 sections
    for sect1 in soup.find_all('div', class_='sect1'):
        sect1_title = sect1.find(['h2', 'h3'])
        if sect1_title:
            sect1_name = sect1_title.get_text(strip=True)
        else:
            sect1_name = "Unknown Section"

        sectionbody = sect1.find('div', class_='sectionbody')
        if not sectionbody:
            continue  # Skip if no section body

        sect1_content = []

        sect2_sections = sectionbody.find_all('div', class_='sect2')

        if sect2_sections:
            # Extract data from each sect2
            for sect2 in sect2_sections:
                sect2_title = sect2.find(['h2', 'h3'])
                sect2_name = sect2_title.get_text(strip=True) if sect2_title else "Unnamed Subsection"
                sect2_content = []

                ts = []
                for table in sect2.find_all('table'):
                    ts.append(table)

                # Extract paragraphs
                for paragraph in sect2.find_all('p'):
                    if not any(table in paragraph.parents for table in ts):  
                        sect2_content.append(paragraph.get_text(strip=True))

                # Extract tables
                for table in ts:
                    rows = []
                    for row in table.find_all('tr'):
                        cells = [cell.get_text(strip=True) for cell in row.find_all(['th', 'td'])]
                        rows.append(" | ".join(cells))
                    sect2_content.extend(rows)

                # Store sect2 data
                data[f"{sect1_name} -> {sect2_name}"] = "\n".join(sect2_content) if sect2_content else "No content found."

        else:
            # No sect2, extract data from sect1 sectionbody
            for table in sectionbody.find_all('table'):
                rows = []
                for row in table.find_all('tr'):
                    cells = [cell.get_text(strip=True) for cell in row.find_all(['th', 'td'])]
                    rows.append(" | ".join(cells))
                sect1_content.extend(rows)

            for paragraph in sectionbody.find_all('p'):
                if paragraph.parent.name != 'td':  
                    sect1_content.append(paragraph.get_text(strip=True))

            # Store sect1 data
            data[sect1_name] = "\n".join(sect1_content) if sect1_content else "No content found."

    return data



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
plugin_names = ["addchecksum"]
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

        # # Find plugin description
        # description_section = plugin_soup.find('h2', id='_description').parent
        # paragraphs = description_section.select('.sectionbody .paragraph')
        # description = "\n".join(p.get_text(strip=True) for p in paragraphs)

        # # Find plugin options
        # options = []
        # options_section = plugin_soup.find('h2', id='_options')
        # table = options_section.find_next('table')
        # for row in table.find('tbody').find_all('tr'):
        #     cells = row.find_all('td')
        #     if len(cells) >= 2:
        #         option_name = cells[0].get_text(strip=True)
        #         option_desc = cells[1].get_text(strip=True)
        #         options.append(f"{option_name}: {option_desc}")
        
        # options = "\n".join(options) 


        # # all data
        # data = {}
        # for section in plugin_soup.find_all(['h2', 'h3']):
            # section_name = section.get_text(strip=True)
            # section_content = []

            # # Find the section body safely
            # section_body = section.find_next_sibling('div', class_='sectionbody')
            # if not section_body:
            #     continue  # Skip if no content found

            # # Extract paragraphs
            # for paragraph in section_body.find_all('p'):
            #     section_content.append(paragraph.get_text(strip=True))

            # # Extract tables
            # table = section_body.find('table')
            # if table:
            #     rows = []
            #     for row in table.find_all('tr'):
            #         cells = [cell.get_text(strip=True) for cell in row.find_all(['th', 'td'])]
            #         rows.append(" | ".join(cells))
            #     section_content.extend(rows)

            # # Extract lists
            # for ul in section_body.find_all('ul'):
            #     for li in ul.find_all('li'):
            #         section_content.append(f"- {li.get_text(strip=True)}")

            # data[section_name] = "\n".join(section_content) if section_content else "No content found."            

        data = extract_sections2(plugin_soup)

        # data_to_write = ""
        # for section, content in data.items():
        #     data_to_write += (f"### {section} ###\n{content}\n\n")

        data_to_write = data

        # Save to file
        with open(f'c:/Users/mohammad/Desktop/hop/hop_plugins/{plugin_name}.txt', 'w', encoding='utf-8') as f:
            # f.write(f"Plugin: {plugin_name_in_doc}\n\nDescription:\n{description}\n\nOptions:\n{options}\n\nAllData:\n{data_to_write}")
            f.write(f"Plugin: {plugin_name_in_doc}\n\n{data_to_write}")
            
        print(f"Saved {plugin_name}")
        
    except Exception as e:
        print(f"Error processing {plugin_name}: {str(e)}")

print("Crawling completed!")