# ==============================================================================
# Customer Support Operations Intelligence Platform - Escalation Risk Model
# ==============================================================================

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, roc_auc_score

def train_escalation_risk_model(df):
    """
    Trains a model to predict the probability of ticket escalation.
    """
    print("\n--- Training Escalation Risk Model ---")
    
    # Feature columns
    categorical_features = [
        "ground_truth_category",
        "customer_segment",
        "ground_truth_priority",
        "channel_name",
        "agent_seniority_level",
        "agent_team"
    ]
    numeric_features = ["creation_hour"]
    
    # Target
    y = df["is_escalated"].astype(int)
    X = df[categorical_features + numeric_features]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Transformer for categorical variables
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ],
        remainder='passthrough'
    )
    
    escalation_pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('clf', RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42))
    ])
    
    # Train
    escalation_pipeline.fit(X_train, y_train)
    y_pred = escalation_pipeline.predict(X_test)
    y_prob = escalation_pipeline.predict_proba(X_test)[:, 1]
    
    escalation_metrics = classification_report(y_test, y_pred, output_dict=True)
    auc_score = roc_auc_score(y_test, y_prob)
    escalation_metrics["roc_auc"] = auc_score
    print("Escalation Prediction Test Accuracy:", round(escalation_metrics["accuracy"], 4))
    print("Escalation Prediction ROC-AUC Score:", round(auc_score, 4))
    
    # Predict all rows to generate predictions schema records
    all_probs = escalation_pipeline.predict_proba(X)[:, 1]
    
    results = pd.DataFrame({
        "ticket_id": df["ticket_id"],
        "escalation_probability": np.round(all_probs, 4)
    })
    
    return results, escalation_metrics
