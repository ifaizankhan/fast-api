import pandas as pd

# Load the dataset
file_path = 'questions_en.xlsx'  # Ensure this is the correct file path
questions_df = pd.read_excel(file_path)

# Parameters for filtering
use = 'Test de positionnement'
subject = 'BDD'

filtered_questions = questions_df
if use:
    filtered_questions = filtered_questions[filtered_questions['use'] == use]
if subject:
    filtered_questions = filtered_questions[filtered_questions['subject'] == subject]

print(f"Filtered Questions Count: {len(filtered_questions)}")
print(filtered_questions)