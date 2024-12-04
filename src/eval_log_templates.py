import nltk
from nltk.translate.bleu_score import sentence_bleu
from rouge import Rouge
from nltk.metrics import edit_distance

# Sample sentences
ground_truth = "The cat sat on the mat."
processed = "The cat is sitting on the mat."

# Ensure that NLTK and other required libraries are installed
nltk.download('punkt')

# 1. Edit Distance
def calculate_edit_distance(ref, hyp):
    distance = edit_distance(ref, hyp)
    print(f"Edit Distance: {distance}")

# 2. ROUGE-L Score
def calculate_rouge_l(ref, hyp):
    rouge = Rouge()
    scores = rouge.get_scores(hyp, ref, avg=True)
    print(f"ROUGE-L Score: {scores['rouge-l']}")

# Calculating metrics for the given sentences
calculate_edit_distance(ground_truth, processed)
calculate_rouge_l(ground_truth, processed)
