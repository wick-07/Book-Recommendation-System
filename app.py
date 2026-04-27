import streamlit as st
import pickle
import numpy as np 
import pandas as pd

st.markdown("""
<style>
.book-card {
    background-color: #ffffff;
    padding: 10px;
    border-radius: 12px;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
    text-align: center;
    margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)

# st.header("The Book Recommender System")
st.markdown("<h1 style='text-align:center; color:#4A90E2;'>📚 Book Recommender System</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Discover your next favorite book!</p>", unsafe_allow_html=True)

popular=pickle.load(open('popular.pkl','rb'))
pt=pickle.load(open('pt.pkl','rb'))
books=pickle.load(open('books.pkl','rb'))
similarity_scores=pickle.load(open('similarity_scores.pkl','rb'))

st.sidebar.title("Top 50 Books")

if st.sidebar.button("SHOW"):
    cols_per_row=5
    num_rows=10
    for rows in range(num_rows):
        cols=st.columns(cols_per_row)
        for col in range(cols_per_row):
            books_idx=rows*cols_per_row+col
            if books_idx<len(popular):
                with cols[col]:
                     # st.image(popular.iloc[books_idx]['Image-URL-M'])
                     # st.text(popular.iloc[books_idx]["Book-Title"])
                     # st.text(popular.iloc[books_idx]["Book-Author"])
                     
                     st.markdown("<div class='book-card'>", unsafe_allow_html=True)
                     st.image(popular.iloc[books_idx]['Image-URL-M'])
                     st.markdown(f"""
                     <b style='font-size:16px;'>{popular.iloc[books_idx]["Book-Title"]}</b><br>
                     <span style='color:gray; font-size:14px;'>Author: {popular.iloc[books_idx]["Book-Author"]}</span>
                     """, unsafe_allow_html=True)
                     st.markdown("</div>", unsafe_allow_html=True)

def recommend(book_name):
    index=np.where(pt.index==book_name)[0][0]
    similar_items=sorted(list(enumerate(similarity_scores[index])),key=lambda x:x[1],reverse=True)[1:6]
    data=[]
    for i in similar_items:
        items=[]
        temp_df=books[books['Book-Title']==pt.index[i[0]]]
        items.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        items.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        items.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        data.append(items)
    return data           

book_list=pt.index.values
st.sidebar.title("Similar Books Suggestions")
selected_book=st.sidebar.selectbox("Select a book from the dropdown",book_list)

if st.sidebar.button("Recommend Me"):
    book_recommend=recommend(selected_book)
    cols=st.columns(5)
    for col_idx in range(5):
        with cols[col_idx]:
            if col_idx < len(book_recommend):
                st.image(book_recommend[col_idx][2])
                # st.text(book_recommend[col_idx][0])
                # st.text(book_recommend[col_idx][1])
                st.markdown(f"""
                <b style='font-size:16px;'>{book_recommend[col_idx][0]}</b><br>
                <span style='color:gray; font-size:14px;'>Author: {book_recommend[col_idx][1]}</span>
                """, unsafe_allow_html=True)

                
    