"""Build Postman folder 9 with POST/PATCH/DELETE for every dashboard resource + Chatbot."""
import json
from pathlib import Path

BEARER = {
    "type": "bearer",
    "bearer": [{"key": "token", "value": "{{access_token}}", "type": "string"}],
}


def crud_triplet(section: str, name: str, base_path: str, post_body: str, patch_body: str, post_extra=None):
    list_url = f"{{{{base_url}}}}/api/v1/dashboard/{base_path}/"
    detail_url = f"{{{{base_url}}}}/api/v1/dashboard/{base_path}/{{{{sample_id}}}}/"

    return [
        {
            "name": f"{section} — {name} — POST (إضافة)",
            "request": {
                "method": "POST",
                "auth": BEARER,
                "header": [{"key": "Content-Type", "value": "application/json"}],
                "body": {"mode": "raw", "raw": post_body},
                "url": list_url,
                "description": post_extra or "إنشاء سجل جديد.",
            },
            "response": [],
        },
        {
            "name": f"{section} — {name} — PATCH (تعديل)",
            "request": {
                "method": "PATCH",
                "auth": BEARER,
                "header": [{"key": "Content-Type", "value": "application/json"}],
                "body": {"mode": "raw", "raw": patch_body},
                "url": detail_url,
                "description": "تعديل جزئي عبر ID.",
            },
            "response": [],
        },
        {
            "name": f"{section} — {name} — DELETE (حذف)",
            "request": {
                "method": "DELETE",
                "auth": BEARER,
                "url": detail_url,
                "description": "حذف عبر ID.",
            },
            "response": [],
        },
    ]


def main():
    path = Path(__file__).resolve().parent / "JDU_Backend_API.postman_collection.json"
    data = json.loads(path.read_text(encoding="utf-8"))

    subs = []

    # =========================
    # 9.1 Core
    # =========================
    subs.append({
        "name": "9.1 Core — CRUD",
        "description": "Core dashboard endpoints",
        "item": []
        + crud_triplet("Core", "universities", "core/universities",
            '{\n  "name_ar": "جامعة",\n  "name_en": "University"\n}',
            '{\n  "name_ar": "تعديل"\n}'
        )
        + crud_triplet("Core", "branches", "core/branches",
            '{\n  "university": 1,\n  "name": "فرع"\n}',
            '{\n  "name": "فرع محدث"\n}'
        )
    })

    # =========================
    # 9.2 Academics
    # =========================
    subs.append({
        "name": "9.2 Academics — CRUD",
        "description": "Academics dashboard",
        "item": []
        + crud_triplet("Academics", "colleges", "academics/colleges",
            '{\n  "university": 1,\n  "name_ar": "كلية"\n}',
            '{\n  "name_ar": "تعديل"\n}'
        )
        + crud_triplet("Academics", "programs", "academics/programs",
            '{\n  "department": 1,\n  "name_ar": "برنامج"\n}',
            '{\n  "name_ar": "تعديل"\n}'
        )
    })

    # =========================
    # 9.3 News
    # =========================
    subs.append({
        "name": "9.3 News — CRUD",
        "description": "News dashboard",
        "item": [
            {
                "name": "News — articles — POST (multipart)",
                "request": {
                    "method": "POST",
                    "auth": BEARER,
                    "body": {
                        "mode": "formdata",
                        "formdata": [
                            {"key": "title_ar", "value": "خبر", "type": "text"},
                            {"key": "content", "value": "نص", "type": "text"},
                            {"key": "image", "type": "file", "src": []},
                        ],
                    },
                    "url": "{{base_url}}/api/v1/dashboard/news/articles/",
                },
                "response": [],
            },
            {
                "name": "News — articles — PATCH",
                "request": {
                    "method": "PATCH",
                    "auth": BEARER,
                    "header": [{"key": "Content-Type", "value": "application/json"}],
                    "body": {"mode": "raw", "raw": '{\n  "title_ar": "تعديل"\n}'},
                    "url": "{{base_url}}/api/v1/dashboard/news/articles/{{sample_id}}/",
                },
                "response": [],
            },
            {
                "name": "News — articles — DELETE",
                "request": {
                    "method": "DELETE",
                    "auth": BEARER,
                    "url": "{{base_url}}/api/v1/dashboard/news/articles/{{sample_id}}/",
                },
                "response": [],
            },
        ],
    })

    # =========================
    # 9.4 Careers
    # =========================
    subs.append({
        "name": "9.4 Careers — CRUD",
        "description": "Careers dashboard",
        "item": []
        + crud_triplet("Careers", "postings", "careers/postings",
            '{\n  "title": "وظيفة"\n}',
            '{\n  "title": "تعديل"\n}'
        )
    })

    # =========================
    # 9.5 Admissions
    # =========================
    subs.append({
        "name": "9.5 Admissions — CRUD",
        "description": "Admissions dashboard",
        "item": []
        + crud_triplet("Admissions", "students", "admissions/students",
            '{\n  "full_name": "طالب"\n}',
            '{\n  "status": "inactive"\n}'
        )
    })

    # =========================
    # 9.6 Services
    # =========================
    subs.append({
        "name": "9.6 Services — CRUD",
        "description": "Services dashboard",
        "item": []
        + crud_triplet("Services", "list", "services/list",
            '{\n  "name_ar": "خدمة"\n}',
            '{\n  "name_ar": "تعديل"\n}'
        )
    })

    # =========================
    # 🤖 9.7 Chatbot (NO AUTH)
    # =========================
    chatbot_section = {
        "name": "9.7 Chatbot — AI Assistant",
        "description": "/chatbot_ask/ — لا يحتاج JWT (AllowAny)",
        "item": [
            {
                "name": "Chatbot — سؤال عربي",
                "request": {
                    "method": "POST",
                    "header": [{"key": "Content-Type", "value": "application/json"}],
                    "body": {
                        "mode": "raw",
                        "raw": (
                            "{\n"
                            '  "message": "ما هي شروط القبول؟",\n'
                            '  "locale": "ar"\n'
                            "}"
                        ),
                    },
                    "url": "{{base_url}}/chatbot_ask/",
                },
                "response": [],
            },
            {
                "name": "Chatbot — سؤال إنجليزي",
                "request": {
                    "method": "POST",
                    "header": [{"key": "Content-Type", "value": "application/json"}],
                    "body": {
                        "mode": "raw",
                        "raw": (
                            "{\n"
                            '  "message": "What are the admission requirements?",\n'
                            '  "locale": "en"\n'
                            "}"
                        ),
                    },
                    "url": "{{base_url}}/chatbot_ask/",
                },
                "response": [],
            },
            {
                "name": "Chatbot — Response Example",
                "request": {
                    "method": "GET",
                    "url": "{{base_url}}/chatbot_ask/",
                    "description": (
                        "Response:\n\n"
                        "{\n"
                        '  "answer": "...",\n'
                        '  "sources": [...],\n'
                        '  "confidence": "high"\n'
                        "}\n"
                    ),
                },
                "response": [],
            },
        ],
    }

    # =========================
    # FINAL FOLDER 9
    # =========================
    folder_9 = {
        "name": "9 — Dashboard CRUD كامل + Chatbot",
        "description": "CRUD كامل لكل الداشبورد + Chatbot AI",
        "item": subs + [chatbot_section],
    }

    items = data["item"]

    idx = next(
        (i for i, x in enumerate(items)
         if isinstance(x, dict) and str(x.get("name", "")).startswith("9 —")),
        None,
    )

    if idx is not None:
        items[idx] = folder_9
    else:
        items.append(folder_9)

    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print("OK — folder 9 updated with Chatbot")


if __name__ == "__main__":
    main()