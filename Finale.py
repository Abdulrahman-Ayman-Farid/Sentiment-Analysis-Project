import pandas as pd
import torch
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification

# Load the trained model
model_path = (r'path/to/module')  # Update with the path to the trained model 'config file'
model = DistilBertForSequenceClassification.from_pretrained(model_path)
tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')

# Read the feedback data from Excel
excel_file = r"path/to/Feedbacks/excel_Sheet"  # Update with the path to your Excel file
feedback_df = pd.read_excel(excel_file)

# Tokenize the feedback text
tokenized_feedbacks = feedback_df['Feedback'].apply(lambda x: tokenizer.encode(x, max_length=128, truncation=True, padding='max_length'))
X = torch.tensor(tokenized_feedbacks.tolist())

# Perform inference
with torch.no_grad():
    outputs = model(X)
    predicted_labels = torch.argmax(outputs.logits, dim=1)

# Convert numerical labels to human-readable terms
sentiment_labels = {0: "negative", 1: "positive", 2: "neutral"}  # Update if needed
predicted_sentiments = [sentiment_labels[label.item()] for label in predicted_labels]

# Add predicted sentiments to the DataFrame
feedback_df['Predicted Sentiment'] = predicted_sentiments

# Save the DataFrame with predicted sentiments to a new Excel file
output_excel_file = r'path/to/output/excel_Sheet'  # Update with the desired output path
feedback_df.to_excel(output_excel_file, index=False)
