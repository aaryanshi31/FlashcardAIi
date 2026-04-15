import re
from typing import List, Dict


# ── Question templates by difficulty ─────────────────────────────────────────

EASY_TEMPLATES = [
    "What is {phrase}?",
    "Define {phrase}.",
    "What does {phrase} mean?",
    "What is meant by {phrase}?",
]

MEDIUM_TEMPLATES = [
    "Explain the concept of {phrase}.",
    "How does {phrase} work?",
    "Why is {phrase} important?",
    "What is the role of {phrase}?",
    "Describe {phrase} in your own words.",
]

HARD_TEMPLATES = [
    "Analyze the significance of {phrase}.",
    "Compare {phrase} with related concepts.",
    "How would you apply {phrase} in a real-world scenario?",
    "What are the implications of {phrase}?",
    "Evaluate the importance of {phrase}.",
]

TEMPLATE_MAP = {
    "easy": EASY_TEMPLATES,
    "medium": MEDIUM_TEMPLATES,
    "hard": HARD_TEMPLATES,
}


def split_sentences(text: str) -> List[str]:
    """Split text into clean sentences."""
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    # Split on sentence boundaries
    sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z])', text)
    # Filter out very short or empty sentences
    return [s.strip() for s in sentences if len(s.strip()) > 30]


def extract_keyphrases_rake(text: str, max_phrases: int = 30) -> List[str]:
    """
    RAKE (Rapid Automatic Keyword Extraction) — pure Python, no dependencies.
    Extracts multi-word key phrases scored by word co-occurrence.
    """
    # Stopwords list
    stopwords = set("""
    a about above after again against all also am an and any are aren't as at
    be because been before being below between both but by can't cannot could
    couldn't did didn't do does doesn't doing don't down during each few for
    from further get got had hadn't has hasn't have haven't having he he'd he'll
    he's her here here's hers herself him himself his how how's i i'd i'll i'm
    i've if in into is isn't it it's its itself let's me more most mustn't my
    myself no nor not of off on once only or other ought our ours ourselves out
    over own same shan't she she'd she'll she's should shouldn't so some such
    than that that's the their theirs them themselves then there there's these
    they they'd they'll they're they've this those through to too under until up
    very was wasn't we we'd we'll we're we've were weren't what what's when
    when's where where's which while who who's whom why why's will with won't
    would wouldn't you you'd you'll you're you've your yours yourself yourselves
    is are was were be been being have has had having do does did doing will
    would shall should may might must can could ought used need dare
    """.split())

    # Tokenize into words, split on stopwords to get candidate phrases
    words = re.findall(r'\b[a-zA-Z][a-zA-Z\-]*\b', text.lower())

    # Build candidate phrases (consecutive non-stopword sequences)
    candidates = []
    current = []
    for word in words:
        if word not in stopwords and len(word) > 2:
            current.append(word)
        else:
            if current:
                candidates.append(current)
                current = []
    if current:
        candidates.append(current)

    # Score words by degree/frequency ratio
    word_freq = {}
    word_degree = {}
    for phrase in candidates:
        degree = len(phrase) - 1
        for word in phrase:
            word_freq[word] = word_freq.get(word, 0) + 1
            word_degree[word] = word_degree.get(word, 0) + degree

    word_score = {}
    for word in word_freq:
        word_score[word] = (word_degree[word] + word_freq[word]) / word_freq[word]

    # Score each phrase
    phrase_scores = {}
    for phrase in candidates:
        if 1 <= len(phrase) <= 4:  # limit phrase length
            phrase_str = " ".join(phrase)
            score = sum(word_score.get(w, 0) for w in phrase)
            phrase_scores[phrase_str] = score

    # Sort by score, remove duplicates
    sorted_phrases = sorted(phrase_scores.items(), key=lambda x: x[1], reverse=True)
    seen = set()
    unique = []
    for phrase, _ in sorted_phrases:
        if phrase not in seen:
            seen.add(phrase)
            unique.append(phrase)

    return unique[:max_phrases]


def find_answer_sentence(phrase: str, sentences: List[str]) -> str | None:
    """Find the sentence that best contains or explains the phrase."""
    phrase_lower = phrase.lower()
    phrase_words = set(phrase_lower.split())

    best_sentence = None
    best_overlap = 0

    for sentence in sentences:
        sent_lower = sentence.lower()
        sent_words = set(re.findall(r'\b\w+\b', sent_lower))
        overlap = len(phrase_words & sent_words)

        # Prefer sentences that directly contain the phrase
        if phrase_lower in sent_lower:
            overlap += 10

        if overlap > best_overlap:
            best_overlap = overlap
            best_sentence = sentence

    return best_sentence if best_overlap > 0 else None


def generate_flashcards(
    text: str,
    num_cards: int = 8,
    difficulty: str = "medium",
) -> List[Dict[str, str]]:
    """
    Main function: extract keyphrases → match to sentences → build Q&A cards.
    Returns list of {'question': ..., 'answer': ...} dicts.
    """
    sentences = split_sentences(text)
    if not sentences:
        return []

    keyphrases = extract_keyphrases_rake(text, max_phrases=num_cards * 3)
    if not keyphrases:
        return []

    templates = TEMPLATE_MAP.get(difficulty, MEDIUM_TEMPLATES)
    cards = []
    used_sentences = set()

    for i, phrase in enumerate(keyphrases):
        if len(cards) >= num_cards:
            break

        answer_sentence = find_answer_sentence(phrase, sentences)
        if not answer_sentence:
            continue

        # Avoid duplicate answers
        if answer_sentence in used_sentences:
            continue
        used_sentences.add(answer_sentence)

        # Pick a template (cycle through them)
        template = templates[i % len(templates)]
        question = template.format(phrase=phrase.title())

        cards.append({
            "question": question,
            "answer": answer_sentence,
        })

    return cards
