DATASET HANDOFF

Project: Explainable Phishing Email Detection
Using Large Language Models

LABELS
0 = Legitimate
1 = Phishing

FILES
train.csv: Model training
validation.csv: Model development
test.csv: Final evaluation

MODEL INPUT
Use email_text for both TF-IDF and LLM experiments.
Use label as the classification target.

Do NOT use source, original_row, fingerprint,
or label as model input features.

EVIDENCE VALIDATION
Use the same email_text that was supplied to the LLM.
Retain original fields for audit purposes.

DATASET SOURCES
Phishing: Nazario_5
Legitimate: Enron, Ling, SpamAssassin

KNOWN LIMITATIONS
Source and label are perfectly confounded.
Standardizing input does not eliminate source bias.
The near-duplicate grouping used an approximate
TF-IDF nearest-neighbor approach.
Labels have not been exhaustively verified.
Results must be interpreted within these limits.

SPLITTING
V2 group-based split; random_state=42.
Do not combine and randomly resplit these files.
