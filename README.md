

---

# 📚✨ Collaborative Book Recommendation System ✨📚

Welcome to the **Collaborative-Based Book Recommendation System**! 🚀
This project recommends books 📖 based on what you like, using **Collaborative Filtering**, **FastAPI** for the backend, and a beautiful **Bootstrap-powered frontend**! 🎨🖥️

---

## 📌 Project Highlights

* 🧠 **Machine Learning**: Collaborative Filtering-based Recommendations
* ⚡ **FastAPI**: Super fast and efficient API backend
* 🎨 **Frontend**: Stunning UI/UX with HTML, CSS (Bootstrap), and smooth gradients
* 📈 **Pickle Files**: Precomputed Pivot Table, Similarity Matrix, and Popular Books
* 🔥 **Docker Ready** (can be containerized easily)
* 🌐 **CORS Enabled**: Supports cross-origin requests
* 🛡️ **Error Handling**: Robust backend with fallbacks and friendly outputs
* 💡 **Different Recommendation Types**: By Book Title, Author Name, or Genre!

---

## 📂 Folder Structure

```bash
├── app.py                 # Main FastAPI app
├── pivot.pkl               # Pickled pivot table for collaborative filtering
├── books.pkl               # Pickled books metadata
├── similar.pkl             # Pickled similarity scores
├── most_rated.pkl          # Pickled dataframe of most popular books
├── templates/              # HTML Frontend (served by FastAPI)
└── README.md               # Project Documentation (you're reading it 😉)
```

---

## 🚀 How To Run the Project

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/book-recommendation-system.git
cd book-recommendation-system
```

### 2. Install the dependencies

```bash
pip install -r requirements.txt
```

*Requirements:*

* fastapi
* uvicorn
* pandas
* numpy
* scikit-learn
* pydantic
* CORS Middleware

### 3. Start the FastAPI server

```bash
uvicorn app:app --reload
```

*It will start running at:*
👉 **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

### 4. Access the Frontend UI

Open your browser and navigate to:
👉 **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

---

## 🔥 API Endpoints

| Method |          Endpoint         |             Description             |
| :----: | :-----------------------: | :---------------------------------: |
|  `GET` |       `/popular_df`       |   Fetch the most popular books 📚   |
| `POST` |  `/recommendations/book`  | Get book recommendations by title ✨ |
| `POST` | `/recommendations/author` |   Get books by similar authors ✍️   |
| `POST` |  `/recommendations/genre` |        Get books by genre 🎭        |
|  `GET` |            `/`            |  Frontend (HTML + Bootstrap UI) 🌟  |

---

## 🧠 Recommendation Logic

* **Collaborative Filtering**: Based on similarity of user ratings.
* **Fallback**: If the queried book/author/genre is not found, random good books are recommended.
* **Popular Books**: Showcase top-rated, most loved books!

---

## 🌟 UI/UX Features

* 🟣 Beautiful **gradient backgrounds** 🎨
* 🟠 **Bootstrap**-styled responsive layouts 📱💻
* 💛 **Hover effects** and **smooth transitions** 🔥
* 💬 **Drop-down selections** for type of recommendation
* 🧩 Cards for displaying book covers, titles, and authors

---

## 📸 Screenshots

|                             Home Page                            |                                Recommendations                               |
| :--------------------------------------------------------------: | :--------------------------------------------------------------------------: |
| ![Home Page](https://via.placeholder.com/400x300?text=Home+Page) | ![Recommendations](https://via.placeholder.com/400x300?text=Recommendations) |

---

## 📢 Future Improvements

* 🧠 Add **Deep Learning**-based recommendation (BERT, Sentence Transformers)
* 📊 Build an **Admin Dashboard** to manage books
* 📱 Create a **Mobile App** version using Flutter
* 📦 Containerize with **Docker** for deployment
* 🌍 Host on **AWS/GCP/Render**

---

## 👤 About Me

I'm passionate about building intelligent, beautiful, and efficient ML/DS/NLP applications! 🚀💻
Explore more of my projects:

* 🔗 [**LinkedIn** (MY profile)](https://www.linkedin.com/in/anurag-raj-770b6524a/)
* 🔗 [**Kaggle** (More ML, DS, and NLP Projects!](https://www.kaggle.com/anuragraj03/code)

---

## 🙌 Let's Connect!

💬 Feel free to [message me on LinkedIn](https://www.linkedin.com/in/anurag-raj-770b6524a/) for collaboration, queries, or just to say hi! 🎉

---


