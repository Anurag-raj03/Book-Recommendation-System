import pandas as pd
import numpy as np
import pickle
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from pydantic import BaseModel
import uvicorn

# FastAPI Application Setup
app = FastAPI()

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Pickle Files
def load_pickles():
    """Load pickle files for the recommendation system."""
    try:
        with open("pivot.pkl", "rb") as f:
            pt = pickle.load(f)
        with open("books.pkl", "rb") as f:
            books = pickle.load(f)
        with open("similar.pkl", "rb") as f:
            similarity_scores = pickle.load(f)
        with open("most_rated.pkl", "rb") as f:
            popular_df = pickle.load(f)
        return pt, books, similarity_scores, popular_df
    except FileNotFoundError as e:
        print(f"Error loading pickle files: {e}")
        raise

# Load data at startup
pt, books, similarity_scores, popular_df = load_pickles()

def recommend_books(query, recommendation_type='book'):
    """
    Recommend books based on different criteria.
    
    Args:
        query (str): Book title, author, or genre
        recommendation_type (str): Type of recommendation
    
    Returns:
        DataFrame of recommended books
    """
    try:
        # If recommendation type is book
        if recommendation_type == 'book':
            # Try to find similar books
            if query in pt.index:
                index = np.where(pt.index == query)[0][0]
                similar_items = sorted(
                    list(enumerate(similarity_scores[index])), 
                    key=lambda x: x[1], 
                    reverse=True
                )[1:5]  # Top 4 similar books, excluding the first (self)
                
                recommended_books = []
                for i in similar_items:
                    book_details = books[books["Book-Title"] == pt.index[i[0]]]
                    recommended_books.append(book_details.iloc[0])
                
                recommended_df = pd.DataFrame(recommended_books)
                recommended_df.drop_duplicates("Book-Title", inplace=True)
                return recommended_df[["Book-Title", "Book-Author", "Image-URL-M"]]
            else:
                # If book not found, return random recommendations
                return books.sample(n=4)[["Book-Title", "Book-Author", "Image-URL-M"]]
        
        # If recommendation type is author
        elif recommendation_type == 'author':
            # Try to find books by the same author or similar authors
            author_books = books[books["Book-Author"].str.contains(query, case=False, na=False)]
            
            if not author_books.empty:
                # If author found, return 4 unique books
                return author_books.drop_duplicates("Book-Title").sample(n=4)[["Book-Title", "Book-Author", "Image-URL-M"]]
            else:
                # If author not found, return random recommendations
                return books.sample(n=4)[["Book-Title", "Book-Author", "Image-URL-M"]]
        
    except Exception as e:
        print(f"Error in recommendation: {e}")
        return books.sample(n=4)[["Book-Title", "Book-Author", "Image-URL-M"]]

# Pydantic Model for Request
class BookRequest(BaseModel):
    book_name: str

# API Endpoints
@app.get("/popular_df")
async def get_popular_books():
    """Retrieve popular books."""
    return popular_df.to_dict(orient="records")

@app.post("/recommendations/book")
async def get_book_recommendations(book_data: BookRequest):
    """Get book recommendations."""
    recommendations = recommend_books(book_data.book_name, 'book')
    return recommendations.to_dict(orient="records")

@app.post("/recommendations/author")
async def get_author_recommendations(author_data: BookRequest):
    """Get author recommendations."""
    recommendations = recommend_books(author_data.book_name, 'author')
    return recommendations.to_dict(orient="records")

@app.post("/recommendations/genre")
async def get_genre_recommendations(genre_data: BookRequest):
    """Get genre recommendations."""
    # Filter books by genre and return 4 random books
    genre_books = books[books["Book-Title"].str.contains(genre_data.book_name, case=False, na=False)]
    
    if not genre_books.empty:
        return genre_books.sample(n=4)[["Book-Title", "Book-Author", "Image-URL-M"]].to_dict(orient="records")
    else:
        # If no books found for the genre, return random books
        return books.sample(n=4)[["Book-Title", "Book-Author", "Image-URL-M"]].to_dict(orient="records")

@app.get("/", response_class=HTMLResponse)
async def serve_html():
    """Serve the HTML frontend."""
    return HTMLResponse(content='''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>📚 Book Recommendations 📚</title>
    <link href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            background: linear-gradient(to right, #6a11cb 0%, #2575fc 100%);
            font-family: 'Poppins', sans-serif;
            color: white;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 0;
            padding: 20px;
        }
        .container {
            background: rgba(255, 255, 255, 0.2);
            padding: 30px;
            border-radius: 20px;
            backdrop-filter: blur(15px);
            box-shadow: 0 15px 25px rgba(0,0,0,0.1);
            width: 100%;
            max-width: 1400px;
        }
        .recommendation-section {
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 25px;
        }
        .recommendation-section > * {
            flex: 1;
        }
        .btn-custom {
            background: #ffcc00;
            color: black;
            font-weight: bold;
            padding: 10px 20px;
            border-radius: 10px;
            transition: all 0.3s ease;
            font-size: 16px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .btn-custom:hover {
            background: #ffaa00;
            transform: scale(1.05);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        .search-box {
            border: 2px solid #ffcc00;
            border-radius: 10px;
            background: rgba(255,255,255,0.1);
            color: white;
        }
        .search-box::placeholder {
            color: rgba(255,255,255,0.7);
        }
        .card {
            margin-bottom: 25px;
            transition: all 0.3s ease;
            background: rgba(255,255,255,0.1);
            border: none;
            color: white;
        }
        .card:hover {
            transform: scale(1.05);
            box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        }
        .card-img-top {
            height: 350px;
            object-fit: cover;
            border-top-left-radius: 15px;
            border-top-right-radius: 15px;
        }
        .card-body {
            padding: 20px;
        }
        .card-title {
            font-weight: bold;
            font-size: 1.2rem;
            margin-bottom: 10px;
        }
        .card-text {
            font-weight: 300;
            opacity: 0.9;
        }
        .hidden {
            display: none !important;
        }
        #recommendedBooks .col-md-3 {
            display: flex;
        }
        #recommendedBooks .card {
            width: 100%;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="text-center mb-5" style="font-weight: bold; letter-spacing: 2px;">📚 Book Recommendations 📚</h1>
        
        <div class="recommendation-section">
            <select class="form-control search-box" id="recommendationType">
                <option value="">Choose Recommendation Type</option>
                <option value="book">Book</option>
                <option value="author">Author</option>
                <option value="genre">Genre</option>
            </select>
        </div>

        <div id="bookSelection" class="recommendation-section hidden">
            <input type="text" id="bookSearch" class="form-control search-box" placeholder="Search Book Title">
            <select class="form-control search-box" id="bookSelect">
                <option value="">Select a Book</option>
            </select>
            <button class="btn btn-custom" onclick="getRecommendations('book')">Get Recommendations</button>
        </div>

        <div id="authorSelection" class="recommendation-section hidden">
            <input type="text" id="authorSearch" class="form-control search-box" placeholder="Search Author Name">
            <select class="form-control search-box" id="authorSelect">
                <option value="">Select an Author</option>
            </select>
            <button class="btn btn-custom" onclick="getRecommendations('author')">Get Recommendations</button>
        </div>

        <div id="genreSelection" class="recommendation-section hidden">
            <select class="form-control search-box" id="genreSelect">
                <option value="">Select a Genre</option>
            </select>
            <button class="btn btn-custom" onclick="getRecommendations('genre')">Get Recommendations</button>
        </div>

        <div class="row mt-5" id="recommendedBooks"></div>
    </div>

    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
    <script>
        $(document).ready(function () {
            $("#recommendationType").on("change", function () {
                var selectedType = $(this).val();
                $("#bookSelection, #authorSelection, #genreSelection").addClass("hidden");
                $(`#${selectedType}Selection`).removeClass("hidden");
            });

            fetch("/popular_df")
            .then(response => response.json())
            .then(data => {
                data.forEach(book => {
                    $("#bookSelect").append(`<option value="${book['Book-Title']}">${book['Book-Title']}</option>`);
                    $("#authorSelect").append(`<option value="${book['Book-Author']}">${book['Book-Author']}</option>`);
                });

                // Populate genre dropdown
                let genres = ["Fiction", "Mystery", "Fantasy", "Science Fiction", "Romance", "Horror", "Historical"];
                genres.sort(() => Math.random() - 0.5);
                genres.forEach(genre => {
                    $("#genreSelect").append(`<option value="${genre}">${genre}</option>`);
                });
            });

            $("#bookSearch").on("input", function() {
                if ($(this).val()) {
                    $("#bookSelect").val("");
                }
            });
            $("#bookSelect").on("change", function() {
                if ($(this).val()) {
                    $("#bookSearch").val("");
                }
            });

            $("#authorSearch").on("input", function() {
                if ($(this).val()) {
                    $("#authorSelect").val("");
                }
            });
            $("#authorSelect").on("change", function() {
                if ($(this).val()) {
                    $("#authorSearch").val("");
                }
            });
        });

        function getRecommendations(type) {
            let selectedValue, endpoint;
            switch(type) {
                case 'book':
                    selectedValue = $("#bookSelect").val() || $("#bookSearch").val();
                    endpoint = "/recommendations/book";
                    break;
                case 'author':
                    selectedValue = $("#authorSelect").val() || $("#authorSearch").val();
                    endpoint = "/recommendations/author";
                    break;
                case 'genre':
                    selectedValue = $("#genreSelect").val();
                    endpoint = "/recommendations/genre";
                    break;
            }

            fetch(endpoint, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ "book_name": selectedValue })
            })
            .then(response => response.json())
            .then(data => {
                $("#recommendedBooks").empty();
                data.forEach(book => {
                    let openLibraryLink = `https://openlibrary.org/search?q=${encodeURIComponent(book['Book-Title'])}&mode=everything`;
                    $("#recommendedBooks").append(`
                        <div class="col-md-3 mb-4">
                            <div class="card shadow-lg">
                                <img src="${book['Image-URL-M']}" class="card-img-top" alt="Book Image">
                                <div class="card-body">
                                    <h5 class="card-title text-uppercase">${book['Book-Title']}</h5>
                                    <p class="card-text font-weight-light">${book['Book-Author']}</p>
                                    <a href="${openLibraryLink}" class="btn btn-custom btn-block mt-3" target="_blank">Read More</a>
                                </div>
                            </div>
                        </div>
                    `);
                });
            })
            .catch(error => {
                console.error('Error:', error);
                $("#recommendedBooks").html('<div class="col-12 text-center text-white">No recommendations found.</div>');
            });
        }
    </script>
</body>
</html>
    ''')

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)