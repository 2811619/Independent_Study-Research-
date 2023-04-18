CIS-698 Independent Study Research
Guided by: Moonwon Chung
----------------------------------

Objective:
To build a machine learning based feature extraction algorithm for text mining conflict minerals reports

Tasks to do:
  a. Outline the scope/scale of the project
  b. Data collection from SEC database for conflict mineral reports
  c. Develop training dataset for feature extraction
  d. Develop feature extraction algorithm for reports
  e. Iterate and tune model hyperparameters

Deliverables
  a. Progress report during regular research meetings (2 sessions per week)
  b. Complete a minimum 5-page paper summarizing the applied method and the results of the prediction outcomes of the      machine learning model

Tasks Completed:
  1. Extracted conflict minerals reporting data from the US government website for the past 10 years, on a month-by-month basis, and converting it to a CSV file
  2. Extracted the column containing the URL information for the reporting and saved it as a text file. I noticed that some of the URLs in the extracted column contained unnecessary data such as picture formats (.jpg) and charts. To clean the URL's, I have removed all unnecessary data and kept only those that end with ".htm". The updated URL information has been saved in the same text file.
  3. Written a code to scrape the websites that contain the URLs ending with ".htm". The scraped data includes information from the URL, as well as the text found within the header (<b>) and paragraph (<p>) tags. To store the scraped data, I have created a CSV file that contains the following columns: id, url, b_tag_text, and p_tag_text. The ID column represents a unique identifier for each url.
  4. As part of the conflict minerals reporting data analysis, I have applied the K-Means clustering algorithm to the text found within the header (<b>) tags on the websites we scraped. After applying the clustering algorithm, I filtered the data by group, and have identified a specific group that contains relevant information related to our analysis. Specifically, I have used the cluster group that contains the keyword "results", as this is where we can find information on whether a company has reported using harmful minerals or not. I have dropped any data that does not contain relevant results within this group, and only kept the data that meets this criteria.
  5. After that, I performed text preprocessing on the p_tag by removing unnecessary symbols, stop words, and lemmatizing words.
  6. Then, I applied the SentimentIntensityAnalyzer from the Valder lexicon for preprocessed_p_tag_text to obtain the polarity scores of negative, positive, and neutral sentiments, as well as the overall polarity score and sentiment label (positive, negative, neutral).
