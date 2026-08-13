"""
debug.py — Debug and test PII detection with full pipeline visualization.
"""

from redactor import create_analyzer, get_recognizer_info, filter_results, dedupe_overlaps

def main():
    """Debug and test the redactor with full pipeline visualization"""
    print("=" * 60)
    print("PII REDACTOR DEBUG - FULL PIPELINE")
    print("=" * 60)
    
    # Create analyzer
    analyzer = create_analyzer()
    
    # Show registered recognizers
    print("\nREGISTERED RECOGNIZERS:")
    for rec_name, entities in get_recognizer_info(analyzer):
        print(f"  - {rec_name} -> {entities}")
    
    # Test text with various PII types
    test_text = """
Mr. Rohan Dey works at Acme Technologies Private Limited in Mumbai.
His email is rohan.dey@gmail.com and phone is +91 9876543210.
He was born on 15 August 1990.
The company was founded on March 15, 2005.
His SSN is 123-45-6789 and credit card is 4111-1111-1111-1111.
His IP is 192.168.1.1.
"""

    print("\n" + "=" * 60)
    print("TEST TEXT:")
    print("=" * 60)
    print(test_text)
    
    # Step 1: Raw detection
    print("\n" + "=" * 60)
    print("STEP 1: RAW RESULTS (before any filtering)")
    print("=" * 60)
    results = analyzer.analyze(text=test_text, language="en")
    
    # Group results by type for better visualization
    raw_by_type = {}
    for r in results:
        entity_text = test_text[r.start:r.end]
        key = r.entity_type
        if key not in raw_by_type:
            raw_by_type[key] = []
        raw_by_type[key].append((r.score, entity_text))
    
    for entity_type, items in sorted(raw_by_type.items()):
        for score, text in items:
            print(f"  {entity_type:<15} {score:.2f} '{text}'")
    
    # Step 2: Filter results
    print("\n" + "=" * 60)
    print("STEP 2: FILTERED RESULTS (after removing non-PII types)")
    print("=" * 60)
    filtered = filter_results(results, test_text)
    
    filtered_by_type = {}
    for r in filtered:
        entity_text = test_text[r.start:r.end]
        key = r.entity_type
        if key not in filtered_by_type:
            filtered_by_type[key] = []
        filtered_by_type[key].append((r.score, entity_text, r.start, r.end))
    
    for entity_type, items in sorted(filtered_by_type.items()):
        for score, text, start, end in items:
            print(f"  {entity_type:<15} {score:.2f} '{text}' [{start}:{end}]")
    
    # Step 3: Deduplicate
    print("\n" + "=" * 60)
    print("STEP 3: DEDUPLICATED RESULTS (after removing overlaps)")
    print("=" * 60)
    deduped = dedupe_overlaps(filtered)
    
    deduped_by_type = {}
    for r in deduped:
        entity_text = test_text[r.start:r.end]
        key = r.entity_type
        if key not in deduped_by_type:
            deduped_by_type[key] = []
        deduped_by_type[key].append((r.score, entity_text, r.start, r.end))
    
    for entity_type, items in sorted(deduped_by_type.items()):
        for score, text, start, end in items:
            print(f"  {entity_type:<15} {score:.2f} '{text}' [{start}:{end}]")
    
    # Step 4: Show what would be redacted
    print("\n" + "=" * 60)
    print("STEP 4: WHAT GETS REDACTED")
    print("=" * 60)
    
    # Show the redacted text
    redacted_text = test_text
    replacements = {}
    for r in deduped:
        fake = "[" + r.entity_type + "_FAKE]"
        replacements[(r.start, r.end)] = fake
    
    # Apply replacements from end to start
    for r in sorted(deduped, key=lambda x: x.start, reverse=True):
        fake = "[" + r.entity_type + "_FAKE]"
        redacted_text = redacted_text[:r.start] + fake + redacted_text[r.end:]
    
    print(redacted_text)
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total raw entities detected: {len(results)}")
    print(f"After filtering: {len(filtered)}")
    print(f"After deduplication: {len(deduped)}")
    
    print("\nEntity types that will be redacted:")
    for entity_type, items in sorted(deduped_by_type.items()):
        print(f"  - {entity_type}: {len(items)} instance(s)")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()