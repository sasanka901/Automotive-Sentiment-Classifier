# 🚗 Automotive Sentiment Classifier

An end-to-end machine learning application that classifies user reviews for automotive services as either **Positive** or **Negative**. 

Live Demo: [Test the Trained Model Here](https://automotive-sentiment-classifier-1va.vercel.app/)

---

## 📊 Dataset

This model is trained using the highly popular **Yelp Open Dataset**, which contains over one million user reviews. Since the original dataset covers a broad range of businesses, the data was filtered to strictly isolate reviews belonging to the **Automotive** and **Service Stations** categories.

* **Dataset Source:** [Yelp Open Dataset](https://business.yelp.com/data/resources/open-dataset/)

### Label Engineering & Dataset Balance
The original Yelp dataset rates reviews on a scale from 1 to 5. To frame this as a binary sentiment classification problem, the ratings were mapped as follows:
* **Negative Reviews:** Ratings of `1` and `2`
* **Positive Reviews:** Ratings of `4` and `5`
* **Removed:** Neutral reviews rated `3` were discarded to prevent ambiguity and improve dataset quality.

The finalized dataset consists of **229,961 reviews**, with a balanced distribution of **60% positive** and **40% negative** reviews.

---

## 🧼 Data Preprocessing

To clean the raw text and ensure the model focuses only on meaningful language patterns, the following preprocessing pipeline was applied:

1. **Null Value Removal:** Eliminated empty or missing reviews.
2. **URL & Link Removal:** Stripped out website links and web addresses.
3. **Punctuation & Special Character Removal:** Cleared text of non-alphanumeric noise.
4. **Number Stripping:** Removed all numerical values to prevent specific data points (like mileages, dates, years, and prices) from skewing the model.
5. **Custom Stopword Filtering:** Standard stopwords were removed, with a critical exception: **negation and contraction words were preserved** because they heavily influence sentiment.
   
   * *Preserved Negations:* `{'not', 'no', 'never', 'neither', 'nor', 'but', 'cannot', 'barely', 'hardly', 'scarcely', 'without', 'against'}`
   * *Preserved Contraction Remnants:* `{'don', 't', 'doesn', 'didn', 'wasn', 'weren', 'haven', 'hasn', 'hadn', 'won', 'wouldn', 'shann', 'shouldn', 'can', 'couldn', 'isn', 'aren', 'ain'}`

---

## ⚙️ Feature Engineering

To transform the cleaned text into a format suitable for machine learning, we utilized Scikit-Learn's `TfidfVectorizer` with the following configuration:
* **`ngram_range=(1,2)`:** Extracted both unigrams (single words) and bigrams (two-word phrases). This ensures that paired words like *"not good"* or *"never again"* maintain their unique contextual meanings rather than being evaluated in isolation.
* **`max_features=3000`:** Limited the feature matrix to the top 3,000 most frequent terms to optimize training speed and prevent overfitting.

---

## 🤖 Model Training & Evaluation

This project utilizes the **Naive Bayes** classifier for text classification. Naive Bayes is a supervised learning algorithm based on **Bayes' Theorem** of probability. It is exceptionally well-suited for text classification and sentiment analysis because it is computationally efficient, highly scalable, and performs remarkably well on high-dimensional text data.

The trained model achieved an overall accuracy of **94% (0.94)**.

### Classification Report
<img width="484" height="168" alt="Screenshot 2026-06-10 000029" src="https://github.com/user-attachments/assets/de1c6317-5af4-4742-9be3-b5ca8a5fec56" />
