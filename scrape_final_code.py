import requests
from bs4 import BeautifulSoup
import csv
field_names = ["id", "url", "b title", "corresponding p text"]
with open('output_final_htm_file.csv', mode='a', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(field_names)
    with open("final_htm_filenames.txt") as file:
        for count, line in enumerate(file, start=0):
            link = line.strip()
            url = link
            headers = {
            'Accept-Encoding': 'gzip',
            'Accept-Language': 'en-US,en;q=0.5',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
            }

            response = requests.get(url, headers=headers)

            if response.status_code == 200:
            # the response content is in HTML format
                html_content = response.content
                # print(html_content)
            else:
                print(f"Failed to get the URL. Status code: {response.status_code}")

            soup = BeautifulSoup(html_content, 'html.parser')

            headers = []
            contents = []
            for p_tag in soup.find_all('p'):
                if p_tag.find('b') is not None:
                    header = p_tag.find('b').get_text().strip()
                    content = ''
                    #Ignore the bold tag inside ptag <p> <b></b> </p>
                    next_tag_b = p_tag.find_next()
                    #Moving i tag
                    next_tag_i = next_tag_b.find_next()
                    # Moving to next ptag
                    next_tag = next_tag_i.find_next()
                    while next_tag:
                        if next_tag.find('b'):
                            break
                        elif next_tag.name == 'table':
                            table_content = ''
                            for td_tag in p_tag.find_all('td'):
                                if td_tag.get_text().strip():
                                    table_content += td_tag.get_text().strip() + ' '
                            content += table_content
                        elif next_tag.get_text().strip():
                            content += next_tag.get_text().strip() + ' '
                        next_tag = next_tag.find_next()
                    headers.append(header)
                    contents.append(content)    
            for i in range(len(headers)):
                writer.writerow([count, url, headers[i], contents[i]])
