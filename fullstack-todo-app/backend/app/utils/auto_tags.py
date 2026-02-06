"""Auto-tag generation from todo title and description keywords."""

STOP_WORDS = frozenset({
    "a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "is", "it", "this", "that", "are", "was",
    "be", "have", "has", "had", "do", "does", "did", "will", "would",
    "could", "should", "may", "might", "can", "shall", "not", "no", "so",
    "if", "then", "than", "too", "very", "just", "about", "up", "out",
    "all", "also", "as", "into", "some", "my", "your", "our", "their",
    "its", "been", "being", "get", "got", "make", "need", "want", "know",
    "take", "come", "going", "thing", "things", "like", "more", "only",
    "over", "such", "after", "before", "between", "each", "every", "own",
    "same", "other", "which", "when", "where", "what", "who", "how",
    "new", "now", "way", "still", "use", "here", "there",
})

CATEGORY_KEYWORDS: dict[str, set[str]] = {
    "work": {
        "meeting", "project", "deadline", "client", "presentation",
        "report", "office", "team", "manager", "colleague", "email",
        "review", "sprint", "standup", "stakeholder", "deliverable",
        "proposal", "contract", "invoice", "milestone",
    },
    "personal": {
        "family", "friend", "birthday", "gift", "hobby", "vacation",
        "travel", "home", "house", "apartment", "pet", "dog", "cat",
        "party", "wedding", "anniversary", "dinner", "lunch",
    },
    "finance": {
        "budget", "payment", "invoice", "tax", "salary", "expense",
        "invest", "investment", "bank", "loan", "mortgage", "insurance",
        "bill", "receipt", "savings", "financial", "accounting", "refund",
    },
    "health": {
        "doctor", "appointment", "exercise", "gym", "workout", "run",
        "yoga", "meditation", "diet", "nutrition", "medicine",
        "prescription", "hospital", "dentist", "therapy", "mental",
        "sleep", "wellness", "checkup", "vitamin",
    },
    "learning": {
        "study", "course", "book", "read", "reading", "learn", "training",
        "tutorial", "lecture", "exam", "test", "homework", "assignment",
        "research", "certificate", "class", "workshop", "seminar",
        "practice", "skill",
    },
    "tech": {
        "code", "coding", "programming", "deploy", "deployment", "server",
        "database", "api", "bug", "fix", "debug", "update", "upgrade",
        "install", "configure", "setup", "backup", "security", "test",
        "testing", "release", "feature", "software", "app", "website",
    },
    "urgent": {
        "urgent", "asap", "immediately", "critical", "emergency",
        "important", "priority", "rush", "hurry", "overdue",
    },
    "shopping": {
        "buy", "purchase", "order", "shop", "shopping", "grocery",
        "groceries", "store", "amazon", "delivery",
    },
    "errands": {
        "pickup", "dropoff", "return", "mail", "post", "laundry",
        "clean", "cleaning", "repair", "maintenance", "renew",
    },
}


def extract_tags(title: str, description: str | None = None) -> list[str]:
    """
    Extract tags from todo title and description using keyword matching.

    Args:
        title: The todo title.
        description: Optional todo description.

    Returns:
        List of up to 5 auto-generated tags.
    """
    text = title.lower()
    if description:
        text += " " + description.lower()

    # Tokenize: split on non-alphanumeric characters
    words = set()
    for word in text.split():
        cleaned = "".join(c for c in word if c.isalnum())
        if cleaned and cleaned not in STOP_WORDS:
            words.add(cleaned)

    # Match against category keyword maps
    matched_categories: list[str] = []
    for category, keywords in CATEGORY_KEYWORDS.items():
        if words & keywords:
            matched_categories.append(category)

    # Extract significant standalone words (4+ chars, not in stop words)
    significant_words = sorted(
        [w for w in words if len(w) >= 4 and w not in STOP_WORDS],
    )

    # Build tag list: categories first, then significant words
    tags: list[str] = list(matched_categories)
    for word in significant_words:
        if word not in tags and not any(word in kw for kw in matched_categories):
            tags.append(word)
        if len(tags) >= 5:
            break

    return tags[:5]
