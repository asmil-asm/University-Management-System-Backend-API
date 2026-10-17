import re
from dataclasses import dataclass

from .knowledge import KnowledgeChunk, build_knowledge_base

ARABIC_STOP_WORDS = {
    'في', 'من', 'على', 'إلى', 'الى', 'عن', 'هل', 'ما', 'ماذا', 'كيف', 'أين', 'اين',
    'هذا', 'هذه', 'ذلك', 'التي', 'الذي', 'هي', 'هو', 'ان', 'أن', 'او', 'أو', 'مع',
    'كل', 'بعض', 'عند', 'لدى', 'لي', 'ليش', 'شو', 'شنو', 'بدي', 'بدك', 'عم', 'عندي',
    'the', 'a', 'an', 'is', 'are', 'was', 'were', 'what', 'how', 'where', 'when', 'who',
    'and', 'or', 'for', 'to', 'of', 'in', 'on', 'at', 'by', 'with', 'about',
}

QUERY_SYNONYMS = {
    'رسوم': ['رسوم', 'أقساط', 'اقساط', 'تكلفة', 'تكلفه', 'fees', 'tuition', 'cost', 'price'],
    'قبول': ['قبول', 'تسجيل', 'انضمام', 'admission', 'admissions', 'enroll', 'registration'],
    'كلية': ['كلية', 'كليات', 'college', 'colleges', 'faculty', 'faculties'],
    'برنامج': ['برنامج', 'برامج', 'تخصص', 'program', 'programs', 'major'],
    'خبر': ['خبر', 'أخبار', 'اخبار', 'news', 'article', 'articles'],
    'فعالية': ['فعالية', 'فعاليات', 'event', 'events', 'activity'],
    'وظيفة': ['وظيفة', 'وظائف', 'توظيف', 'job', 'jobs', 'career', 'careers'],
    'تواصل': ['تواصل', 'اتصال', 'هاتف', 'رقم', 'بريد', 'ايميل', 'contact', 'phone', 'email'],
    'موقع': ['موقع', 'عنوان', 'مكان', 'location', 'address', 'where'],
    'مكتبة': ['مكتبة', 'library', 'libraries'],
    'خدمة': ['خدمة', 'خدمات', 'بوابة', 'portal', 'service', 'services', 'lms'],
}


@dataclass(frozen=True)
class SearchResult:
    chunk: KnowledgeChunk
    score: float


def _normalize(text: str) -> str:
    text = (text or '').lower()
    text = text.replace('أ', 'ا').replace('إ', 'ا').replace('آ', 'ا').replace('ى', 'ي').replace('ة', 'ه')
    text = re.sub(r'[^\w\s\u0600-\u06FF]', ' ', text)
    return re.sub(r'\s+', ' ', text).strip()


def tokenize(text: str) -> list[str]:
    return [token for token in _normalize(text).split() if len(token) >= 2 and token not in ARABIC_STOP_WORDS]


def _expand_tokens(tokens: list[str]) -> set[str]:
    expanded = set(tokens)
    for token in tokens:
        for synonyms in QUERY_SYNONYMS.values():
            normalized_group = {_normalize(word) for word in synonyms}
            if token in normalized_group:
                expanded.update(normalized_group)
    return expanded


def _score_chunk(chunk: KnowledgeChunk, query_tokens: set[str]) -> float:
    if not query_tokens:
        return 0.0

    title_tokens = set(tokenize(chunk.title))
    content_tokens = set(tokenize(chunk.content))
    haystack = f'{chunk.title} {chunk.content}'
    normalized_haystack = _normalize(haystack)

    title_hits = len(query_tokens & title_tokens)
    content_hits = len(query_tokens & content_tokens)
    phrase_bonus = 0.0

    joined_query = ' '.join(sorted(query_tokens))
    if len(joined_query) >= 4 and joined_query in normalized_haystack:
        phrase_bonus = 3.0

    category_boost = {
        'university': 0.5,
        'page': 0.4,
        'admission': 0.4,
        'college': 0.3,
        'career': 0.3,
        'news': 0.2,
    }.get(chunk.category, 0.0)

    return (title_hits * 4.0) + (content_hits * 1.5) + phrase_bonus + category_boost


def search_knowledge(query: str, *, limit: int = 5) -> list[SearchResult]:
    query_tokens = _expand_tokens(tokenize(query))
    if not query_tokens:
        return []

    scored: list[SearchResult] = []
    for chunk in build_knowledge_base():
        score = _score_chunk(chunk, query_tokens)
        if score > 0:
            scored.append(SearchResult(chunk=chunk, score=score))

    scored.sort(key=lambda item: item.score, reverse=True)
    return scored[:limit]
