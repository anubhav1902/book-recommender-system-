import streamlit as st
import numpy as np
import pickle

# Load pickled data
popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))

st.title("📚 Book Recommendation System")

# Show top popular books
st.header("🔥 Popular Books")
for i in range(min(5, len(popular_df))):  # Show top 5
    st.image(popular_df['Image-URL-M'].iloc[i], width=120)
    st.markdown(f"**{popular_df['Book-Title'].iloc[i]}**")
    st.write(f"Author: {popular_df['Book-Author'].iloc[i]}")
    st.write(f"Avg Rating: {popular_df['avg_rating'].iloc[i]} ⭐")
    st.write("---")

# Recommend section
st.header("🔍 Recommend Books")
book_name = st.text_input("Enter a Book Name")

if st.button("Recommend"):
    if book_name in pt.index:
        index = np.where(pt.index == book_name)[0][0]
        similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:6]

        st.success("Top 5 Recommended Books:")
        for i in similar_items:
            temp_df = books[books['Book-Title'] == pt.index[i[0]]].drop_duplicates('Book-Title')
            title = temp_df['Book-Title'].values[0]
            author = temp_df['Book-Author'].values[0]
            image = temp_df['Image-URL-M'].values[0]
            st.image(image, width=100)
            st.markdown(f"**{title}**")
            st.write(f"Author: {author}")
            st.write("---")
    else:
        st.error("Book not found in dataset. Try another title.")
