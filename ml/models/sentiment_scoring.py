# ==============================================================================
# Customer Support Operations Intelligence Platform - Sentiment Scoring Model
# ==============================================================================

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report

def train_sentiment_model(df):
    """
    Trains a text classifier to predict sentiment label and score from ticket text.
    """
    print("\n--- Training Sentiment Scoring Model ---")
    
    X = df["ticket_text"]
    y = df["ground_truth_sentiment"]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    sentiment_pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(max_features=2500, stop_words='english')),
        ('clf', LogisticRegression(max_iter=1000, multi_class='multinomial', C=1.0))
    ])
    
    # Train
    sentiment_pipeline.fit(X_train, y_train)
    y_pred = sentiment_pipeline.predict(X_test)
    
    sentiment_metrics = classification_report(y_test, y_pred, output_dict=True)
    print("Sentiment Prediction Test Accuracy:", round(sentiment_metrics["accuracy"], 4))
    
    # Predict all rows to generate predictions schema records
    pred_labels = sentiment_pipeline.predict(X)
    pred_probs = sentiment_pipeline.predict_proba(X)
    
    # Get index of classes to calculate score
    # classes_ list order usually: ['Negative', 'Neutral', 'Positive']
    classes = list(sentiment_pipeline.classes_)
    neg_idx = classes.index("Negative")
    pos_idx = classes.index("Positive")
    
    # Sentiment score = P(Positive) - P(Negative), maps cleanly to [-1.0, 1.0]
    sentiment_scores = pred_probs[:, pos_idx] - pred_probs[:, neg_idx]
    
    results = pd.DataFrame({
        "ticket_id": df["ticket_id"],
        "sentiment_label": pred_labels,
        "sentiment_score": np.round(sentiment_scores, 4)
    })
    
    return results, sentiment_metrics
