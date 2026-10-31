import json
import re

with open('output.txt', 'r', encoding='utf-8') as f:
    text = f.read()

pieces = text.split('')

dictionary = {}

for piece in pieces:
    piece = piece.strip()
    if not piece:
        continue
    
    # Remove newlines within the piece to make matching easier
    piece = piece.replace('\n', ' ')
    piece = re.sub(r'\s+', ' ', piece)

    # Skip headings like A, B, S - Ş, U - Ü
    # Valid terms wouldn't just be uppercase characters of length < 8 lacking definitions
    if len(piece) < 10 and piece.isupper() and not ':' in piece and not '.' in piece:
        continue

    # Try matching "TERM: Definition"
    if ':' in piece:
        parts = piece.split(':', 1)
        term = parts[0].strip()
        defn = parts[1].strip()
        
        # Sometimes there's garbage before the term if it merged. But since we strictly split by bullet,
        # the piece should start with the term.
        # Clean term if it has a letter at the beginning like "F FBK."
        if len(term) < 60:
            dictionary[term] = defn
            continue

    # Try matching "TERM. Definition" where TERM is uppercase (e.g. FBK.)
    if '.' in piece:
        parts = piece.split('.', 1)
        term = parts[0].strip()
        defn = parts[1].strip()
        
        # If term is mostly uppercase
        if term.isupper() and len(term) < 60:
            dictionary[term] = defn
            continue

# Manually cleanup some known artifacts like S - Ş or F
bad_keys = []
for key in dictionary.keys():
    if len(key) <= 2 or re.match(r'^[A-Z]\s*-\s*[A-Z]$', key):
        bad_keys.append(key)

for b in bad_keys:
    del dictionary[b]

with open('dictionary.json', 'w', encoding='utf-8') as f:
    json.dump(dictionary, f, ensure_ascii=False, indent=2)

print(f"Parsed {len(dictionary)} dictionary entries.")
