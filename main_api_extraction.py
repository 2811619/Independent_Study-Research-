from sec_api import QueryApi
import csv
import pandas as pd
import ast
import requests
from bs4 import BeautifulSoup
def query_api():
    queryApi = QueryApi(api_key="1cfa66868c4848442291415ad9c4eadfe10220f89e396eb128c67d369cc700a5")

    # return 10 most recently filed filings by Tesla
    base_query = {
    "query": { "query_string": {
    "query": "PLACEHOLDER"
    } },
    "from": "0",
    "size": "50",
    "sort": [{ "filedAt": { "order": "desc" } }]
    }

    field_names = ["id", "accessionNo", "companyName", "companyNameLong", "ticker", 
               "cik", "filedAt", "items", "formType", "periodOfReport", 
               "linkToHtml", "linkToFilingDetails", "linkToTxt", "description", 
               "documentFormatFiles", "dataFiles", "seriesAndClassesContractsInformation",  
               "linkToXbrl", "entities"]

    with open('filings1.csv', 'a', encoding='UTF8') as f:
        writer = csv.DictWriter(f, fieldnames=field_names)
        writer.writeheader()
        for year in range(2023, 2010, -1):
            print("starting {year}".format(year=year))
            for month in range(1, 13, 1):
                universe_query = \
                "formType:\"SD\" AND " + \
                "filedAt:[{year}-{month:02d}-01 TO {year}-{month:02d}-31]" \
                .format(year=year, month=month)

                base_query["query"]["query_string"]["query"] = universe_query;

                for from_batch in range(0, 1100, 50):
                    base_query["from"] = from_batch;

                    response = queryApi.get_filings(base_query)

                    filings = response['filings']

                    # every item in field_names represents a filing parameter
                    # and the column name in the CSV file
            
                    writer.writerows(filings)

def make_dataframe():
    data = pd.read_csv(r"/Users/mohamedgani/Downloads/CIS_698_main/CIS_698_ex_url_extracting/filings1.csv")
    for index, value in data['documentFormatFiles'].iteritems():
        # convert the string to a list of dictionaries
        value_list = ast.literal_eval(value)
        # access the documentUrl of the first dictionary in the list
        for i in range (len(value_list)):
            document_url = value_list[i]['documentUrl']
            with open("ex_filing_url.txt", "a") as file:
                file.write(document_url+"\n")

def cleaning_url():
    filename = 'ex_filing_url.txt'

    # Open the file and read its contents into a list
    with open(filename) as f:
        filenames = f.read().splitlines()

    # Remove the file extensions
    for i in range(len(filenames)):
        filenames[i] = filenames[i].replace('.txt', '').replace('.jpg', '')

    # Write the updated filenames back to the file
    with open('filtering_ex_url.txt', 'w') as f:
        f.write('\n'.join(filenames))

def filtering_ex_url():
    with open('filtering_ex_url.txt', 'r') as f:
        filenames = f.read().splitlines()

    htm_filenames = [f for f in filenames if f.endswith('.htm')]

    with open('htm_filenames.txt', 'w') as f:
        for filename in htm_filenames:
            f.write(filename + '\n')

def htm_ex_url():
    with open("htm_filenames.txt", "r") as file:
        for line in file:
            if "ex" in line:
                with open('final_htm_filenames.txt', 'a') as f:
                    f.write(line)
                    
def write_ex_csv():
    field_names = ["id", "b title", "corresponding p text"]
    with open('output_final.csv', mode='a', newline='') as file:
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
                    writer.writerow([count, headers[i], contents[i]])

if __name__ == "__main__":
    query_api()
    make_dataframe()
    cleaning_url()
    filtering_ex_url()
    htm_ex_url()
    write_ex_csv()
