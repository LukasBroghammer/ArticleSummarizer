import tkinter as tk
from tkinter import ttk
from newspaper import Article
from textblob import TextBlob
from langdetect import detect
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize  
from googletrans import Translator
import nltk
from ttkthemes import ThemedStyle

# Download necessary NLTK resources
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

# Global variables for detected language and article
detected_language = ''
article = None


def translate_text(text, target_language='en'):
    translator = Translator()

    try:
        translation = translator.translate(text, dest=target_language)
        return translation.text
    except Exception as e:
        print(f"Translation error: {e}")
    
    

def change_language(*args):
    selected_language.set(language_var.get())
    

def summarize():


    global detected_language, article

    url = utext.get('1.0', 'end').strip()

    # Load the article, analyze it
    article = Article(url)
    article.download()
    article.parse()
    article.nlp()

    # Get the detected language
    detected_language = detect(article.text)

    # Set default language to detected language
    selected_language.set(detected_language)
    language_var.set(detected_language)
    
   
    def remove_stop_words(sentence, language='english'):
        language = language.lower()

        # Mapping for different languages
        language_mapping = {
            'de': 'german',
            'fr': 'french',
            # Add more language mappings as needed
        }

       
        mapped_language = language_mapping.get(language, 'english')
        stop_words_set = set(stopwords.words(mapped_language))

        words = word_tokenize(sentence)

        # Filter out stop words
        filtered_words = [word for word in words if word.lower() not in stop_words_set and any(c.isalpha() for c in word)]

        return ' '.join(filter(None, filtered_words))

    # Process and filter the keywords based on the detected language
    filtered_keywords = [remove_stop_words(keyword, language=detected_language) for keyword in article.keywords]

    # Remove empty strings from the list of keywords
    filtered_keywords = list(filter(None, filtered_keywords))

    # Perform sentiment analysis
    analysis = TextBlob(article.text)

    # Output article information
    title_var.set(article.title)
    author_var.set(article.authors)
    publish_date_var.set(str(article.publish_date))
    keywords_var.set("\n".join(filtered_keywords))
    summary_var.set(article.summary)
    sentiment_var.set(f'Polarity: {analysis.sentiment.polarity}, Sentiment: {"positive" if analysis.sentiment.polarity > 0 else "negative" if analysis.sentiment.polarity < 0 else "neutral"}')

    # Update Text widgets with new values
    title_text.config(state='normal')
    title_text.delete('1.0', tk.END)
    title_text.insert(tk.END, title_var.get())

    author_text.config(state='normal')
    author_text.delete('1.0', tk.END)
    author_text.insert(tk.END, author_var.get())

    publish_date_text.config(state='normal')
    publish_date_text.delete('1.0', tk.END)
    publish_date_text.insert(tk.END, publish_date_var.get())

    keywords_text.config(state='normal')
    keywords_text.delete('1.0', tk.END)
    keywords_text.insert(tk.END, keywords_var.get())
    
    summary_text.config(state='normal')
    summary_text.delete('1.0', tk.END)
    summary_text.insert(tk.END, summary_var.get())

    sentiment_text.config(state='normal')
    sentiment_text.delete('1.0', tk.END)
    sentiment_text.insert(tk.END, sentiment_var.get())

    
    translate_btn['state'] = 'normal'


def translate():

    global detected_language, article

    target_language = selected_language.get()
    
    if target_language != detected_language:
        article.title = translate_text(article.title, target_language)
        article.summary = translate_text(article.summary, target_language)
        article.keywords = [translate_text(keyword, target_language) for keyword in article.keywords]

        # Update Text widgets with translated values
        title_text.config(state='normal')
        title_text.delete('1.0', tk.END)
        title_text.insert(tk.END, article.title)
        title_text.config(state='disabled')

        keywords_text.config(state='normal')
        keywords_text.delete('1.0', tk.END)
        keywords_text.insert(tk.END, "\n".join(article.keywords))
        keywords_text.config(state='disabled')

        summary_text.config(state='normal')
        summary_text.delete('1.0', tk.END)
        summary_text.insert(tk.END, article.summary)
        summary_text.config(state='disabled')

   

# GUI
root = tk.Tk()
root.title('Summarizer')

style = ThemedStyle(root)
style.set_theme('radiance')  

url_label = ttk.Label(root, text='URL:')
url_label.grid(row=0, column=0, padx=10, pady=10, sticky='e')

utext = tk.Text(root, height=1, width=60)
utext.grid(row=0, column=1, padx=10, pady=10, sticky='w')

language_options = ['en', 'de', 'fr']  
selected_language = tk.StringVar()
language_var = tk.StringVar()
language_dropdown = tk.OptionMenu(root, language_var, *language_options, command=change_language)
language_dropdown.grid(row=0, column=2, padx=10, pady=10, sticky='w')

# Labels for various information
labels = ['Title:', 'Author:', 'Publication Date:', 'Keywords:', 'Summary:', 'Sentiment Analysis:']
for i, label_text in enumerate(labels):
    label = ttk.Label(root, text=label_text)
    label.grid(row=i+1, column=0, padx=10, pady=5, sticky='e')

# Variables to store information
title_var = tk.StringVar()
author_var = tk.StringVar()
publish_date_var = tk.StringVar()
summary_var = tk.StringVar()
sentiment_var = tk.StringVar()
keywords_var = tk.StringVar()  # Add a variable for keywords

# Text Widget for Title
title_text = tk.Text(root, height=1, width=60, state='disabled')  # Set height and width as needed
title_text.grid(row=1, column=1, padx=10, pady=5, sticky='w')

# Text Widget for Author
author_text = tk.Text(root, height=1, width=60, state='disabled')  # Set height and width as needed
author_text.grid(row=2, column=1, padx=10, pady=5, sticky='w')

# Text Widget for Publication Date
publish_date_text = tk.Text(root, height=1, width=60, state='disabled')  # Set height and width as needed
publish_date_text.grid(row=3, column=1, padx=10, pady=5, sticky='w')

# Text Widget for Keywords
keywords_text = tk.Text(root, height=1, width=60, state='disabled')  # Set height and width as needed
keywords_text.grid(row=4, column=1, padx=10, pady=5, sticky='w')

# Text Widget for Summary
summary_text = tk.Text(root, height=5, width=60, state='disabled')  # Set height and width as needed
summary_text.grid(row=5, column=1, padx=10, pady=5, sticky='w')

# Text Widget for Sentiment Analysis
sentiment_text = tk.Text(root, height=1, width=60, state='disabled')  # Set height and width as needed
sentiment_text.grid(row=6, column=1, padx=10, pady=5, sticky='w')

# Button to trigger summarization
btn = ttk.Button(root, text='Summarize', command=summarize)
btn.grid(row=7, column=1, columnspan=1, pady=5, padx=5)

# Translate button
translate_btn = ttk.Button(root, text='Translate', command=translate, state='disabled')
translate_btn.grid(row=8, column=1, columnspan=1, pady=5, padx=5)

root.mainloop()
