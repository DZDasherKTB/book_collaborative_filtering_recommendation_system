from flask import Flask, render_template, request
import pickle
import numpy as np
import pandas as pd
import random

popular_df = pickle.load(open('./popular.pkl','rb'))
recommend_df = pickle.load(open('./recommendation_dataframe.pkl','rb'))

def recommend_book(book_name):
    matches = recommend_df[recommend_df['Book_Name'] == book_name]
    if matches.empty:
        return []  # gracefully handle unknown books
    
    similar_items = matches['sorted_scores'].values[0]
    selected_items = random.sample(similar_items, min(8, len(similar_items)))

    recommendations = []
    for i in selected_items:
        book = recommend_df.iloc[i[0]]
        recommendations.append({
            'name': book['Book_Name'],
            'author': book['Book-Author'],
            'publisher': book['Publisher'],
            'year': book['Year-Of-Publication'],
            'image': book['Image-URL-L'],
        })
    return recommendations


app = Flask(__name__)

@app.route('/')
def index():
  return render_template(
    'index.html',
    book_name=list(popular_df['Book-Title'].values),
    author=list(popular_df['Book-Author'].values),
    publisher=list(popular_df['Publisher'].values),
    rating=list(popular_df['avg_ratings'].round(2).values),  # ✅ rounded to .2f
    votes=list(popular_df['num_ratings'].values),
    year=list(popular_df['Year-Of-Publication'].values),
    image=list(popular_df['Image-URL-L'].values)
)

@app.route('/recommend', methods=['GET', 'POST'])
def recommend():
    book_names = list(recommend_df['Book_Name'].unique())

    if request.method == 'POST':
        book_name = request.form.get('book_name')
        recommendations = recommend_book(book_name)
        return render_template(
            'recommend.html',
            book_names=book_names,
            recommendations=recommendations,
            input_name=book_name
        )

    return render_template(
        'recommend.html',
        book_names=book_names,
        recommendations=[],
        input_name=None
    )
if __name__ == '__main__':
  app.run()