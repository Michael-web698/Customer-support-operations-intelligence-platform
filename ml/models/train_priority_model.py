# ==============================================================================
# Customer Support Operations Intelligence Platform - Ticket Category & Priority Model
# ==============================================================================

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report

def train_category_and_priority_models(df):
    """
    Trains classification models for ticket auto-classification and priority prediction.
    Returns the category predictions and priority predictions, along with evaluation metrics.
    """
    print("\n--- Training Category Auto-Classification Model ---")
    
    # Preprocessing: target and text
    X = df["ticket_text"]
    y_cat = df["ground_truth_category"]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y_cat, test_size=0.2, random_state=42)
    
    cat_pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(max_features=3000, stop_words='english', ngram_range=(1, 2))),
        ('clf', LogisticRegression(max_iter=1000, C=1.0))
    ])
    
    # Train Category Model
    cat_pipeline.fit(X_train, y_train)
    y_pred = cat_pipeline.predict(X_test)
    
    cat_metrics = classification_report(y_test, y_pred, output_dict=True)
    print("Category Auto-Classification Test Accuracy:", round(cat_metrics["accuracy"], 4))
    
    # Predict all rows to generate scores for predictions schema
    all_pred_categories = cat_pipeline.predict(X)
    
    print("\n--- Training Priority Prediction Model ---")
    y_prio = df["ground_truth_priority"]
    X_train_p, X_test_p, y_train_p, y_test_p = train_test_split(X, y_prio, test_size=0.2, random_state=42)
    
    prio_pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(max_features=3000, stop_words='english', ngram_range=(1, 2))),
        ('clf', LogisticRegression(max_iter=1000, C=1.0))
    ])
    
    # Train Priority Model
    prio_pipeline.fit(X_train_p, y_train_p)
    y_pred_p = prio_pipeline.predict(X_test_p)
    
    prio_metrics = classification_report(y_test_p, y_pred_p, output_dict=True)
    print("Priority Prediction Test Accuracy:", round(prio_metrics["accuracy"], 4))
    
    # Predict all rows
    all_pred_priorities = prio_pipeline.predict(X)
    
    # Return metrics and predictions series
    results = pd.DataFrame({
        "ticket_id": df["ticket_id"],
        "predicted_category": all_pred_categories,
        "predicted_priority": all_pred_priorities
    })
    
    return results, cat_metrics, prio_metrics
