# 🎣 Phishing Website Detector

A machine learning mini-project that predicts whether a website is **phishing** or **legitimate**, based on 15 key URL and website characteristics — built with scikit-learn and deployed as an interactive web app using Streamlit.

🔗 **Live App:** [https://phishing-website-detectorx.streamlit.app/]

---

## 📌 Objective

This project was built as a supervised machine learning mini-project, following a structured workflow: dataset selection, exploratory data analysis, preprocessing, model training, evaluation, and deployment. The goal is to classify a website as legitimate or phishing using pre-extracted URL and page-behavior features, and to make that model usable through a simple interactive interface.

---

## 🗂️ Dataset

- **Type:** Supervised, binary classification
- **Source:** UCI-style Phishing Websites dataset (feature-engineered, not raw URLs)
- **Rows:** ~11,000+ website samples
- **Target column:** `class` → `1` = Legitimate, `-1` = Phishing
- **Features:** 30 pre-engineered indicators describing URL structure, domain trust signals, and page behavior (e.g. `UsingIP`, `LongURL`, `HTTPS`, `SubDomains`, `AnchorURL`), each encoded as:
  - `1` → safe/legitimate signal
  - `0` → suspicious/ambiguous signal
  - `-1` → phishing-style signal

---

## 🔍 Exploratory Data Analysis

- Checked dataset shape, data types, null values, and duplicates
- Verified class balance using a count plot
- Visualized feature distributions with histograms
- Explored feature relationships with a correlation heatmap and bar plots
- Noted that scatter plots add little value here since all features are categorical rather than continuous

---

## ⚙️ Preprocessing

- No encoding was required — the dataset was already numerically pre-encoded
- Feature scaling was tested (helped resolve a Logistic Regression convergence warning) but is not required for the final Random Forest model, since tree-based models don't rely on feature scale
- Removed the `Index` column after discovering it was leaking information (it isn't a real website characteristic and shouldn't influence predictions)

---

## 🤖 Models Trained & Compared

| Model | Accuracy | Notes |
|---|---|---|
| Logistic Regression | ~93% | Required feature scaling to converge reliably |
| Decision Tree | ~96% | Prone to overfitting compared to the ensemble version |
| **Random Forest (all 30 features)** | ~97% | Best overall performance |
| **Random Forest (top 15 features)** | ~94% | Final model — smaller accuracy trade-off for a much simpler, more usable input form |

**Final model:** Random Forest Classifier, trained on the **top 15 most important features**, selected using Random Forest's built-in feature importance ranking.

### Selected Features
`UsingIP`, `LongURL`, `ShortURL`, `Symbol@`, `Redirecting//`, `PrefixSuffix-`, `SubDomains`, `HTTPS`, `DomainRegLen`, `Favicon`, `NonStdPort`, `HTTPSDomainURL`, `RequestURL`, `AnchorURL`, `LinksInScriptTags`

---

## 📊 Evaluation

Evaluated using Accuracy, Precision, Recall, F1-Score, and a Confusion Matrix — with particular attention to **recall on the phishing class**, since failing to catch an actual phishing site is a more costly error than a false alarm on a legitimate one.

_(Fill in your final numbers here once confirmed on the corrected 15-feature model:)_
- Accuracy: `94%`
- Precision: `95%`
- Recall: `92%`
- F1-Score: `94%`

---

## 🖥️ App Features

- Simple, guided input form — 15 plain-language questions instead of raw numeric codes
- Instant prediction with a confidence score
- **"What We Found In Your Answers"** section — explains *why* the model reached its conclusion by listing which specific answers looked suspicious or phishing-like
- Sidebar with project background, tech stack, and model performance
- Clear academic-use disclaimer

---

## 🛠️ Tech Stack

- **Python**
- **pandas / NumPy** — data handling
- **scikit-learn** — model training (Logistic Regression, Decision Tree, Random Forest)
- **Matplotlib / Seaborn** — EDA visualizations
- **Streamlit** — interactive web app / deployment

---

## 🚀 Running Locally

```bash
git clone https://github.com/Kaiser1210supreme/phishing-website-detector.git
cd phishing-website-detector
pip install -r requirements.txt
streamlit run app.py
```

---

## 📁 Project Structure

```
phishing-website-detector/
├── app.py               # Streamlit app
├── phishing_model.pkl   # Trained Random Forest model
├── requirements.txt     # Python dependencies
└── README.md
```

---

## ⚠️ Disclaimer

This project was built for **academic and learning purposes** as part of a supervised machine learning mini-project. It is **not** a production-grade security tool and should not be solely relied upon to determine whether a real website is safe. Always use official browser security warnings, antivirus tools, or verified sources for actual phishing detection.

---

## 👤 Author

Rishabh Yadav
