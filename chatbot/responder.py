import json
import re
import urllib.error
import urllib.request

from django.conf import settings

from .search import SearchResult, search_knowledge

MAX_SNIPPET_CHARS = 700


def _split_sentences(text: str) -> list[str]:
    parts = re.split(r'(?<=[.!?؟\n])\s+', text.strip())
    return [part.strip() for part in parts if part.strip()]


def _pick_relevant_sentences(content: str, query: str, *, max_sentences: int = 4) -> str:
    sentences = _split_sentences(content)
    if not sentences:
        return content[:MAX_SNIPPET_CHARS]

    query_tokens = set(re.findall(r'[\w\u0600-\u06FF]{2,}', query.lower()))
    ranked = []
    for sentence in sentences:
        sentence_lower = sentence.lower()
        hits = sum(1 for token in query_tokens if token in sentence_lower)
        ranked.append((hits, sentence))

    ranked.sort(key=lambda item: item[0], reverse=True)
    selected = [sentence for hits, sentence in ranked if hits > 0][:max_sentences]
    if not selected:
        selected = sentences[:max_sentences]

    snippet = ' '.join(selected)
    if len(snippet) > MAX_SNIPPET_CHARS:
        snippet = snippet[:MAX_SNIPPET_CHARS].rstrip() + '…'
    return snippet


def _confidence(score: float) -> str:
    if score >= 8:
        return 'high'
    if score >= 4:
        return 'medium'
    return 'low'


def _fallback_answer(locale: str) -> str:
    if locale == 'en':
        return (
            'I could not find enough information about this on the official university website. '
            'Please contact the university directly for more details.'
        )
    return (
        'لم أجد معلومات كافية عن هذا السؤال في محتوى موقع الجامعة الرسمي. '
        'يمكنك التواصل مع الجامعة مباشرة للحصول على تفاصيل أدق.'
    )


def _format_sources(results: list[SearchResult]) -> list[dict]:
    seen = set()
    sources = []
    for result in results:
        chunk = result.chunk
        key = (chunk.path, chunk.title)
        if key in seen:
            continue
        seen.add(key)
        sources.append(
            {
                'title': chunk.title,
                'url': chunk.path,
                'category': chunk.category,
            }
        )
    return sources


def _build_context(results: list[SearchResult]) -> str:
    blocks = []
    for index, result in enumerate(results, start=1):
        chunk = result.chunk
        blocks.append(
            f'[{index}] {chunk.title}\n'
            f'الفئة: {chunk.category}\n'
            f'الرابط: {chunk.path}\n'
            f'المحتوى:\n{chunk.content[:1800]}'
        )
    return '\n\n'.join(blocks)


def _call_gemini(query: str, context: str, locale: str) -> str | None:
    api_key = getattr(settings, 'GEMINI_API_KEY', '') or ''
    if not api_key:
        return None

    if locale == 'en':
        system = (
            'You are the official assistant for Al Jazeera Private University (JPU) website. '
            'Answer ONLY using the provided website context. '
            'If the context does not contain the answer, clearly say the information is not available on the website. '
            'Do not invent facts, dates, fees, or contacts. '
            'Keep the answer concise, helpful, and mention relevant page links from the context.'
        )
    else:
        system = (
            'أنت المساعد الرسمي لموقع جامعة الجزيرة الخاصة. '
            'أجب فقط اعتماداً على محتوى الموقع المرفق. '
            'إذا لم تجد الإجابة في السياق، قل بوضوح أن المعلومة غير متوفرة على الموقع. '
            'لا تخترع حقائق أو أرقاماً أو رسوماً أو تواريخ. '
            'اجعل الإجابة مختصرة ومفيدة واذكر روابط الصفحات المناسبة من السياق.'
        )

    payload = {
        'system_instruction': {'parts': [{'text': system}]},
        'contents': [
            {
                'role': 'user',
                'parts': [
                    {
                        'text': (
                            f'سياق الموقع:\n{context}\n\n'
                            f'سؤال المستخدم ({locale}):\n{query}'
                        ),
                    }
                ],
            }
        ],
        'generationConfig': {
            'temperature': 0.2,
            'maxOutputTokens': 700,
        },
    }

    model = getattr(settings, 'GEMINI_MODEL', 'gemini-2.0-flash')
    url = f'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}'
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST',
    )

    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            data = json.loads(response.read().decode('utf-8'))
        candidates = data.get('candidates') or []
        if not candidates:
            return None
        parts = candidates[0].get('content', {}).get('parts') or []
        text = ''.join(part.get('text', '') for part in parts).strip()
        return text or None
    except (urllib.error.URLError, TimeoutError, KeyError, json.JSONDecodeError, ValueError):
        return None


def _local_answer(query: str, results: list[SearchResult], locale: str) -> str:
    top = results[0]
    snippet = _pick_relevant_sentences(top.chunk.content, query)
    sources = _format_sources(results[:3])

    if locale == 'en':
        intro = f'Based on the official website ({top.chunk.title}):'
        links = '\n'.join(f'- {source["title"]}: {source["url"]}' for source in sources)
        return f'{intro}\n\n{snippet}\n\nRelated pages:\n{links}'

    intro = f'حسب المعلومات المنشورة على موقع الجامعة ({top.chunk.title}):'
    links = '\n'.join(f'- {source["title"]}: {source["url"]}' for source in sources)
    return f'{intro}\n\n{snippet}\n\nصفحات ذات صلة:\n{links}'


def answer_query(query: str, *, locale: str = 'ar') -> dict:
    cleaned = (query or '').strip()
    locale = 'en' if locale == 'en' else 'ar'

    if not cleaned:
        message = 'اكتب سؤالك من فضلك.' if locale == 'ar' else 'Please type your question.'
        return {
            'answer': message,
            'sources': [],
            'confidence': 'low',
            'grounded': True,
        }

    results = search_knowledge(cleaned, limit=5)
    if not results:
        return {
            'answer': _fallback_answer(locale),
            'sources': [],
            'confidence': 'low',
            'grounded': True,
        }

    context = _build_context(results)
    llm_answer = _call_gemini(cleaned, context, locale)
    answer = llm_answer or _local_answer(cleaned, results, locale)
    sources = _format_sources(results[:3])

    return {
        'answer': answer,
        'sources': sources,
        'confidence': _confidence(results[0].score),
        'grounded': True,
    }
