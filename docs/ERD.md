# JDU Backend — ERD (Entity Relationship Diagram)

قاعدة البيانات: **PostgreSQL** (Neon / Railway)  
المشروع: Django REST API — جامعة الجزيرة الخاصة

---

## ملفات ERD

| الملف | الاستخدام |
|-------|-----------|
| [`jdu_backend.dbml`](./jdu_backend.dbml) | استيراد في [dbdiagram.io](https://dbdiagram.io/d) أو [dbdocs.io](https://dbdocs.io) |
| هذا الملف | مخطط Mermaid + شرح العلاقات |

---

## مخطط العلاقات (Mermaid)

```mermaid
erDiagram
    auth_user ||..o{ dashboard : "JWT is_staff"

    core_university ||--o{ core_socialmedia : has
    core_university ||--o{ core_branch : has
    core_university ||--o{ academics_college : has
    core_university ||--o{ news_news : publishes
    core_university ||--o{ news_event : hosts
    core_university ||--o{ news_announcement : posts
    core_university ||--o{ careers_jobposting : offers
    core_university ||--o{ services_library : has

    academics_college ||--o{ academics_department : contains
    academics_department ||--o{ academics_program : offers
    academics_department ||--o{ academics_academicstaff : employs
    academics_academicstaff ||--o{ academics_research : publishes

    academics_program ||--|| admissions_admission : "1:1 info"
    academics_program ||--o{ admissions_application : receives

    admissions_student ||--o{ admissions_application : submits

    careers_jobposting ||--o{ careers_jobapplication : receives

    core_university {
        int id PK
        string name_ar
        string name_en
        string location
        string email
        string phone
        image logo
    }

    core_language {
        int id PK
        string code UK
        string label
    }

    core_socialmedia {
        int id PK
        int university_id FK
        string platform
        string url
    }

    core_branch {
        int id PK
        int university_id FK
        string name
        text address
        decimal latitude
        decimal longitude
    }

    core_page {
        int id PK
        string slug UK
        string title_ar
        string title_en
        text content_ar
        text content_en
        string page_type
    }

    core_contactmessage {
        int id PK
        string sender_name
        string sender_email
        string subject
        text message
        datetime sent_at
        string status
    }

    academics_college {
        int id PK
        int university_id FK
        string name_ar
        string name_en
        text description
    }

    academics_department {
        int id PK
        int college_id FK
        string name_ar
        string name_en
    }

    academics_program {
        int id PK
        int department_id FK
        string name_ar
        string name_en
        string level
        file study_plan
    }

    academics_academicstaff {
        int id PK
        int department_id FK
        string full_name
        string title
        text bio
        string email
        string staff_type
        image photo
    }

    academics_research {
        int id PK
        int staff_id FK
        string title
        text abstract
        date published_date
        string url
    }

    news_news {
        int id PK
        int university_id FK
        string title_ar
        string title_en
        text content
        date publish_date
        image image
    }

    news_event {
        int id PK
        int university_id FK
        string title_ar
        string title_en
        datetime event_date
        string location
        text description
        image image
    }

    news_announcement {
        int id PK
        int university_id FK
        string title
        text body
        date date
    }

    careers_jobposting {
        int id PK
        int university_id FK
        string title
        string job_type
        text description
        text requirements
        date deadline
        string status
    }

    careers_jobapplication {
        int id PK
        int job_id FK
        string applicant_name
        string applicant_email
        file cv
        date apply_date
        string status
    }

    admissions_student {
        int id PK
        string full_name
        string email UK
        string national_id UK
        string status
    }

    admissions_admission {
        int id PK
        int program_id FK_UK
        text requirements
        text procedure
        decimal tuition_fee
        text academic_calendar
    }

    admissions_application {
        int id PK
        int student_id FK
        int program_id FK
        date apply_date
        string status
        file form_file
    }

    services_service {
        int id PK
        string name_ar
        string name_en
        string service_type
        string url
        text description
    }

    services_library {
        int id PK
        int university_id FK
        string name
        string location
        string access_url
    }
```

---

## هيكل التطبيقات (21 جدول + auth)

```
core/
├── University          ← الجامعة (مركز العلاقات)
├── Language            ← لغات الموقع (مستقل)
├── SocialMedia         → University
├── Branch              → University
├── Page                ← صفحات ثابتة (about, vision, ...)
└── ContactMessage      ← رسائل الزوار (مستقل)

academics/
├── College             → University
├── Department          → College
├── Program             → Department
├── AcademicStaff       → Department
└── Research            → AcademicStaff

news/
├── News                → University
├── Event               → University
└── Announcement        → University

careers/
├── JobPosting          → University
└── JobApplication      → JobPosting

admissions/
├── Student             ← (مستقل)
├── Admission           → Program (OneToOne)
└── Application         → Student + Program

services/
├── Service             ← (مستقل)
└── Library             → University
```

---

## العلاقات الرئيسية

| من | إلى | نوع | on_delete |
|----|-----|-----|-----------|
| SocialMedia, Branch, College, News, Event, Announcement, JobPosting, Library | University | N:1 | CASCADE |
| Department | College | N:1 | CASCADE |
| Program, AcademicStaff | Department | N:1 | CASCADE |
| Research | AcademicStaff | N:1 | CASCADE |
| Admission | Program | 1:1 | CASCADE |
| Application | Student, Program | N:1 | CASCADE |
| JobApplication | JobPosting | N:1 | CASCADE |

---

## جداول بدون FK (مستقلة)

- `core_language` — قائمة اللغات
- `core_page` — محتوى الصفحات (slug فريد)
- `core_contactmessage` — رسائل «اتصل بنا»
- `services_service` — خدمات (بوابة، Moodle، مكتبة)
- `admissions_student` — يُنشأ تلقائياً عند POST طلب قبول عام
- `auth_user` — مستخدمو Django (JWT + Dashboard)

---

## كيف تعرض المخطط

1. **dbdiagram.io:** افتح [dbdiagram.io/d](https://dbdiagram.io/d) → Import → الصق محتوى `jdu_backend.dbml`
2. **VS Code / Cursor:** ثبّت إضافة Mermaid وافتح هذا الملف
3. **GitHub:** Mermaid يُعرض تلقائياً في README

---

## أوامر Django مفيدة

```bash
# رسم ERD تلقائي (يتطلب graphviz + pydot)
python manage.py graph_models -a -g -o docs/jdu_models.dot
dot -Tpng docs/jdu_models.dot -o docs/jdu_models.png

# قائمة الجداول
python manage.py inspectdb
```
