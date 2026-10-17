"""One-off script to insert quick-guide + chatbot folder into Postman collection. Run: python postman/_update_postman_guide.py"""
import json
from pathlib import Path

path = Path(__file__).resolve().parent / "JDU_Backend_API.postman_collection.json"
data = json.loads(path.read_text(encoding="utf-8"))

bearer = {
    "type": "bearer",
    "bearer": [{"key": "token", "value": "{{access_token}}", "type": "string"}],
}


def req(name, method, url, desc, body=None, headers=None):
    r = {"method": method, "auth": bearer, "url": url, "description": desc}
    if headers:
        r["header"] = headers
    if body:
        r["body"] = body
    return {"name": name, "request": r, "response": []}


# =========================
# 0 — Quick Guide
# =========================
quick_guide = {
    "name": "0 — دليل سريع (بحث · ترقيم · إضافة خبر)",
    "description": (
        "**ابدأ من هنا.** إضافة خبر، الترقيم (pagination)، البحث (search)، والفلترة. "
        "في طلبات **GET** افتح تبويب **Params** لرؤية كل المعاملات.\n\n"
        "**مهم:** نفّذ أولًا مجلد «1 — المصادقة» وانسخ `access` إلى المتغير `access_token`."
    ),
    "item": [
        req(
            "⭐ إضافة خبر — POST (JSON)",
            "POST",
            "{{base_url}}/api/v1/dashboard/news/articles/",
            "إنشاء خبر جديد.",
            headers=[{"key": "Content-Type", "value": "application/json"}],
            body={
                "mode": "raw",
                "raw": (
                    "{\n"
                    '  "university": 1,\n'
                    '  "title_ar": "خبر تجريبي",\n'
                    '  "title_en": "Sample news",\n'
                    '  "content": "نص الخبر الكامل هنا."\n'
                    "}"
                ),
            },
        ),
    ],
}


# =========================
# 1 — Chatbot API
# =========================
chatbot_guide = {
    "name": "1 — Chatbot API (AI Assistant)",
    "description": (
        "**واجهة الشاتبوت الخاصة بالجامعة.**\n"
        "ترسل سؤال ويرجع رد AI + مصادر من قاعدة المعرفة.\n\n"
        "Endpoint: `/chatbot_ask/`"
    ),
    "item": [
        req(
            "💬 إرسال سؤال إلى الشاتبوت",
            "POST",
            "{{base_url}}/chatbot_ask/",
            "إرسال رسالة إلى الذكاء الاصطناعي واستقبال الإجابة.",
            headers=[
                {"key": "Content-Type", "value": "application/json"}
            ],
            body={
                "mode": "raw",
                "raw": (
                    "{\n"
                    '  "message": "ما هي شروط القبول؟",\n'
                    '  "locale": "ar"\n'
                    "}"
                ),
            },
        ),
        req(
            "💬 سؤال باللغة الإنجليزية",
            "POST",
            "{{base_url}}/chatbot_ask/",
            "اختبار الرد باللغة الإنجليزية.",
            headers=[
                {"key": "Content-Type", "value": "application/json"}
            ],
            body={
                "mode": "raw",
                "raw": (
                    "{\n"
                    '  "message": "What are the admission requirements?",\n'
                    '  "locale": "en"\n'
                    "}"
                ),
            },
        ),
        {
            "name": "📖 مثال شكل الرد",
            "request": {
                "method": "GET",
                "header": [],
                "url": "{{base_url}}/chatbot_ask/",
                "description": (
                    "شكل الاستجابة:\n\n"
                    "```json\n"
                    "{\n"
                    '  "answer": "....",\n'
                    '  "sources": [\n'
                    '    {"title": "Page", "url": "https://..."}\n'
                    "  ],\n"
                    '  "confidence": "high",\n'
                    '  "grounded": true\n'
                    "}\n"
                    "```"
                ),
            },
            "response": [],
        },
    ],
}


# =========================
# Insert into collection
# =========================
items = data["item"]

# Replace or insert Quick Guide
idx = next(
    (
        i for i, x in enumerate(items)
        if isinstance(x, dict) and str(x.get("name", "")).startswith("0 —")
    ),
    None,
)

if idx is not None:
    items[idx] = quick_guide
else:
    items.insert(0, quick_guide)

# Insert chatbot guide after quick guide
items.insert(1, chatbot_guide)


# =========================
# Add description note
# =========================
prefix = "**→ للداشبورد:** افتح أولًا «0 — دليل سريع» ثم «1 — Chatbot API».\n\n"
desc = data["info"].get("description", "")
if prefix.strip() not in desc:
    data["info"]["description"] = prefix + desc


# Save file
path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

print("Updated:", path)