##This is the Google Review collector, to collector review from: https://play.google.com/store/apps/details?id=fi.thl.koronahaavi&hl=fi
##First import needed packages
import json
import pandas as pd
from tqdm import tqdm
import seaborn as sns
import matplotlib.pyplot as plt
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalFormatter

from google_play_scraper import Sort, reviews, app
sns.set(style='whitegrid', palette='muted', font_scale=1.2)
#choose the app name, you can change to other app or apps if you want
app_packages = [
  'fi.thl.koronahaavi'] #https://play.google.com/store/apps/details?id=gov.michigan.MiCovidExposurew.
#wechat: com.tencent.mm
#fr.gouv.android.stopcovid
#com.eg.android.AlipayGphone
#fi.thl.koronahaavi

def format_title(title):
  sep_index = title.find(':') if title.find(':') != -1 else title.find('-')
  if sep_index != -1:
    title = title[:sep_index]
  return title[:10]

fig, axs = plt.subplots(2, len(app_infos) // 2, figsize=(14, 5))

for i, ax in enumerate(axs.flat):
  ai = app_infos[i]
  img = plt.imread(ai['icon'])
  ax.imshow(img)
  ax.set_title(format_title(ai['title']))
  ax.axis('off')
##scrpa app review
app_reviews = []

for ap in tqdm(app_packages):
  for score in list(range(1, 6)):
    for sort_order in [Sort.MOST_RELEVANT, Sort.NEWEST, Sort.RATING]:
      rvs, _ = reviews(
        ap,
        lang='fi', #change here for Finnish Language
        country='fi', #change here for country in Finland
        sort=sort_order,
        #count= 200000 if score == 3 else 100000,
        filter_score_with=score
      )
      for r in rvs:
        r['sortOrder'] = 'most_relevant' if sort_order == Sort.MOST_RELEVANT else 'newest'
        r['appId'] = ap
      app_reviews.extend(rvs)

"""Note that we're adding the app id and sort order to each review. Here's an example for one:"""

#print_json(app_reviews[0])

"""`repliedAt` and `replyContent` contain the developer response to the review. Of course, they can be missing.

How many app reviews did we get?
"""

#print(len(app_reviews), type(app_reviews))

"""Let's save the reviews to a CSV file:"""
print(type(app_reviews))

app_reviews_df = pd.DataFrame(app_reviews)

print(len(app_reviews_df))

app_reviews_df_text = app_reviews_df["content"].tolist()

app_reviews_df_text = list(dict.fromkeys(app_reviews_df_text))

print(len(app_reviews_df_text))
app_text_df = pd.DataFrame(app_reviews_df_text)

app_text_df.to_csv('reviews.txt', index=None, header=False, encoding='utf-8')

