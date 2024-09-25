import pandas as pd
import re
from fuzzywuzzy import fuzz

def clean_text(text):
    text = text.lower()
    text = re.sub(r"[.,'\/\\\[\]`]", '', text)
    text = re.sub(r"\b(ltd|co|corporation|inc|corp|llc|ltd\.|co\.|corp\.|inc\.)\b", '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def clean_dataframe(df):
    return df.apply(lambda col: col.apply(lambda x: clean_text(str(x)) if isinstance(x, str) else x))

path = r"C:\users\andrei\desktop\veridion\r\date\facebook_dataset.csv"
dateFacebook = pd.read_csv(path, sep=',', on_bad_lines='skip', low_memory=False)
dateFacebook = clean_dataframe(dateFacebook)
dateFacebook.rename(columns={'domain': 'fb_domain', 'address': 'fb_address', 
                              'city': 'fb_city', 'name': 'fb_name', 
                              'country_name': 'fb_nume_tara'}, inplace=True)

path = r"C:\users\andrei\desktop\veridion\r\date\google_dataset.csv"
dateGoogle = pd.read_csv(path, sep=',', on_bad_lines='skip', low_memory=False)
dateGoogle = clean_dataframe(dateGoogle)
dateGoogle.rename(columns={'domain': 'go_domain', 'address': 'go_address', 
                           'city': 'go_city', 'name': 'go_name', 
                           'country_name': 'go_nume_tara'}, inplace=True)

path = r"C:\users\andrei\desktop\veridion\r\date\website_dataset.csv"
dateWeb = pd.read_csv(path, sep='\t', on_bad_lines='skip', low_memory=False)
dateWeb = clean_dataframe(dateWeb)
dateWeb.rename(columns={'root_domain': 'w_domain', 'legal_name': 'w_name', 
                           'city': 'w_city', 'name': 'w_name', 
                           'main_country': 'w_website'}, inplace=True)

# def count_similarities(df1, df2, col1, col2, threshold=80):
#     def check_similarity(name):
#         for _, row in df2.iterrows():
#             score = fuzz.token_set_ratio(name, row[col2])
#             if score >= threshold:
#                 return True
#         return False

#     count = df1[col1].apply(check_similarity).sum()
#     return count
    
# dateFacebook_sample = dateFacebook.sample(n=1000)
# dateGoogle_sample = dateGoogle.sample(n=1000)
# dateWeb_sample = dateWeb.sample(n=1000)

# similar_fb_go = count_similarities(dateFacebook_sample, dateGoogle_sample, 'fb_name', 'go_name')
# similar_fb_w = count_similarities(dateFacebook_sample, dateWeb_sample, 'fb_name', 'w_name')
# similar_go_w = count_similarities(dateGoogle_sample, dateWeb_sample, 'go_name', 'w_name')

# percent_fb_go = (similar_fb_go / len(dateFacebook_sample)) * 100
# percent_fb_w = (similar_fb_w / len(dateFacebook_sample)) * 100
# percent_go_w = (similar_go_w / len(dateGoogle_sample)) * 100

# print(f"numarul de inregistrari similare intre facebook si google: {similar_fb_go} ({percent_fb_go:.2f}%)")
# print(f"numarul de inregistrari similare intre facebook si website: {similar_fb_w} ({percent_fb_w:.2f}%)")
# print(f"numarul de inregistrari similare intre google si website: {similar_go_w} ({percent_go_w:.2f}%)")

def count_similarities_three(df1, df2, df3, col1, col2, col3, threshold=80):
    def check_similarity_three(name):
        for _, row2 in df2.iterrows():
            score2 = fuzz.token_set_ratio(name, row2[col2])
            if score2 >= threshold:
                for _, row3 in df3.iterrows():
                    score3 = fuzz.token_set_ratio(name, row3[col3])
                    if score3 >= threshold:
                        return True
        return False

    count = df1[col1].apply(check_similarity_three).sum()
    return count

dateFacebook_sample = dateFacebook.sample(n=1000)
dateGoogle_sample = dateGoogle.sample(n=1000)
dateWeb_sample = dateWeb.sample(n=1000)

percent_fb_go = (similar_fb_go / len(dateFacebook_sample)) * 100
percent_fb_w = (similar_fb_w / len(dateFacebook_sample)) * 100
percent_go_w = (similar_go_w / len(dateGoogle_sample)) * 100

similar_fb_go_w = count_similarities_three(dateFacebook_sample, dateGoogle_sample, dateWeb_sample, 'fb_name', 'go_name', 'w_name')
percent_fb_go_w = (similar_fb_go_w / len(dateFacebook_sample)) * 100

print(f"numarul de inregistrari similare intre facebook, google si website: {similar_fb_go_w} ({percent_fb_go_w:.2f}%)")
