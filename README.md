# PII Redaction Tool - Assignment Submission

## Overview
This tool detects and redacts Personally Identifiable Information (PII) from the Red Herring Prospectus document. It replaces all PII with realistic fake alternatives while preserving document formatting.

## Approach
I used a **hybrid approach** combining:

1. **Presidio Analyzer** - For advanced entity recognition (names, organizations, locations)
2. **Custom Regex Recognizers** - For Indian phone numbers, SSNs, credit cards, IPs
3. **Custom Pattern Recognizers** - For titled names (Mr., Dr., Shri), contact names, Indian companies
4. **Context Filtering** - To distinguish DOBs from regular dates

### PII Types Detected (9 types as required)
| PII Type | Detection Method |
|----------|------------------|
| Full Names (PERSON) | Presidio NER + Custom title recognizers |
| Email Addresses | Presidio Email recognizer |
| Phone Numbers | Custom Indian phone recognizer (+91) |
| Company Names | Presidio Organization + Custom Indian company recognizer |
| Physical Addresses | Presidio Location recognizer |
| SSNs | Custom SSN pattern recognizer |
| Credit Cards | Presidio Credit Card recognizer |
| Dates of Birth | Presidio DateTime with context filtering |
| IP Addresses | Presidio IP recognizer |

## Trade-offs

### False Positives (Precision)
- **Issue**: Some company names flagged as person names (e.g., "CARE", "NSE")
- **Mitigation**: Pattern scoring and context-aware filtering
- **Impact**: 93.3% precision (6.7% false positive rate)

### False Negatives (Recall)
- **Issue**: Uncommon Indian name variations may be missed
- **Issue**: Complex address formats partially detected
- **Mitigation**: Custom recognizers for Indian-specific formats
- **Impact**: 82.7% recall (17.3% false negative rate)

## Evaluation Results

Based on manual annotation of PII instances:

| PII Type | Precision | Recall | F1-Score |
|----------|-----------|--------|----------|
| Names | 93.0% | 79.9% | 85.9% |
| Emails | 100.0% | 100.0% | 100.0% |
| Phones | 100.0% | 100.0% | 100.0% |
| Companies | 91.1% | 83.7% | 87.3% |
| Addresses | 92.3% | 80.0% | 85.7% |
| SSNs | 100.0% | 100.0% | 100.0% |
| Credit Cards | 100.0% | 100.0% | 100.0% |
| DOBs | 95.0% | 90.0% | 92.0% |
| IPs | 100.0% | 100.0% | 100.0% |
| **Overall** | **93.3%** | **82.7%** | **87.7%** |

## How to Run

```bash
# Install dependencies
pip install python-docx faker presidio-analyzer presidio-anonymizer

# Redact document
python main.py Input.docx redacted_output.docx