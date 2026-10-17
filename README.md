<div align="center">

# 🎓 نظام إدارة الجامعة – الواجهة الخلفية

### University Management System – Backend API

واجهة خلفية (Backend API) متكاملة لنظام إدارة جامعي، مبنية باستخدام **Django** و **Django REST Framework**، وتوفر خدمات RESTful لتشغيل لوحة التحكم والموقع العام.

[![Django](https://img.shields.io/badge/Django-6.0.4-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.17.1-A30000?style=for-the-badge&logo=django&logoColor=white)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](./LICENSE)

[![GitHub stars](https://img.shields.io/github/stars/asmil-asm/university_system_backe-end?style=social)](https://github.com/asmil-asm/university_system_backe-end/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/asmil-asm/university_system_backe-end?style=social)](https://github.com/asmil-asm/university_system_backe-end/network/members)
[![GitHub issues](https://img.shields.io/github/issues/asmil-asm/university_system_backe-end)](https://github.com/asmil-asm/university_system_backe-end/issues)

</div>

---

## 📋 جدول المحتويات

- [نظرة عامة](#-نظرة-عامة)
- [الميزات الرئيسية](#-الميزات-الرئيسية)
- [التقنيات المستخدمة](#-التقنيات-المستخدمة)
- [المتطلبات المسبقة](#-المتطلبات-المسبقة)
- [التثبيت](#-التثبيت)
- [الإعداد](#-الإعداد)
- [التشغيل](#-التشغيل)
- [هيكل المشروع](#-هيكل-المشروع)
- [نقاط النهاية (API)](#-نقاط-النهاية-api)
- [المصادقة والأمان](#-المصادقة-والأمان)
- [نموذج قاعدة البيانات](#-نموذج-قاعدة-البيانات)
- [إدارة الملفات (Media)](#-إدارة-الملفات-media)
- [الاختبار](#-الاختبار)
- [النشر](#-النشر)
- [التكامل مع الواجهة الأمامية](#-التكامل-مع-الواجهة-الأمامية)
- [استكشاف الأخطاء](#-استكشاف-الأخطاء)
- [خارطة الطريق](#-خارطة-الطريق)
- [المساهمة](#-المساهمة)
- [الترخيص](#-الترخيص)
- [التواصل](#-التواصل)

---

## 🎯 نظرة عامة

**الواجهة الخلفية** هي قلب نظام إدارة الجامعة، توفر واجهات RESTful APIs لإدارة:

- المحتوى التعريفي للجامعة (الصفحات، الروابط، الشعار).
- البيانات الأكاديمية (الكليات، الأقسام، البرامج، المقررات).
- نظام القبول والتسجيل.
- الوظائف الشاغرة.
- الأخبار والخدمات.
- رسائل التواصل مع الزوار.
- المستخدمين والصلاحيات.

### الأهداف الرئيسية

- ✅ **RESTful API** معياري ومتوافق مع أفضل الممارسات.
- ✅ **مصادقة JWT** آمنة وحديثة.
- ✅ **دعم كامل للعربية والإنجليزية** في جميع النماذج.
- ✅ **بنية معيارية** (Modular) عبر تطبيقات Django منفصلة.
- ✅ **قابلية التوسع** للتعامل مع بيانات كبيرة.
- ✅ **توثيق تلقائي** لـ API (قيد التطوير).

---

## ✨ الميزات الرئيسية

### 🏛️ إدارة الجامعة
- إدارة معلومات الجامعة (الاسم، الشعار، العنوان، الفروع).
- إدارة روابط التواصل الاجتماعي.
- إدارة اللغات المدعومة (عربي/إنجليزي).

### 📄 إدارة الصفحات
- صفحات ثنائية اللغة (عربي/إنجليزي).
- صفحات ديناميكية قابلة للتعديل (عن الجامعة، الرؤية والرسالة، السياسات...).
- ترجمات منفصلة لكل صفحة.

### 📚 الشؤون الأكاديمية
- إدارة الكليات (Colleges).
- إدارة الأقسام (Departments).
- إدارة البرامج الأكاديمية (Programs).
- إدارة المقررات (Courses).

### 🎓 القبول والتسجيل
- إدارة متطلبات القبول.
- استقبال طلبات التقديم.
- تتبع حالة الطلب (Pending, Accepted, Rejected).
- إدارة مستندات المتقدمين.

### 💼 الوظائف
- نشر الوظائف الشاغرة.
- استقبال طلبات التوظيف.
- تتبع حالة الطلبات.

### 📰 الأخبار
- إنشاء أخبار ثنائية اللغة.
- تصنيف الأخبار.
- إدارة الصور المرفقة.

### 🛠️ الخدمات
- إدارة الخدمات الجامعية.
- تصنيف الخدمات.

### ✉️ رسائل التواصل
- استقبال رسائل من الزوار.
- إدارة الرد على الرسائل.
- تحديد حالة الرسالة (مقروءة/غير مقروءة).

### 🤖 روبوت المحادثة (قيد التطوير)
- تخزين المحادثات.
- إدارة النوايا (Intents).
- معالجة الرسائل آليًا.

### 🔐 الأمان والمصادقة
- مصادقة JWT عبر `djangorestframework-simplejwt`.
- تجديد تلقائي للتوكن.
- إدارة الأدوار والصلاحيات.
- CORS مضبوط للواجهة الأمامية.

### 🌐 التوطين
- دعم كامل للعربية (`ar-sa`) والإنجليزية.
- توقيت `Asia/Damascus`.
- حقول ثنائية اللغة في النماذج.

---

## 🛠️ التقنيات المستخدمة

### Core

| التقنية | الإصدار | الدور |
|---------|---------|-------|
| [Python](https://www.python.org/) | 3.12+ | لغة البرمجة |
| [Django](https://www.djangoproject.com/) | 6.0.4 | إطار العمل |
| [Django REST Framework](https://www.django-rest-framework.org/) | 3.17.1 | بناء API |
| [PostgreSQL](https://www.postgresql.org/) | 15+ | قاعدة البيانات |
| [psycopg2-binary](https://www.psycopg.org/) | - | مشغل PostgreSQL |

### Authentication & Security

| التقنية | الإصدار | الدور |
|---------|---------|-------|
| [djangorestframework-simplejwt](https://django-rest-framework-simplejwt.readthedocs.io/) | 5.5.1 | مصادقة JWT |
| [django-cors-headers](https://github.com/adamchainz/django-cors-headers) | - | إدارة CORS |
| [python-dotenv](https://github.com/theskumar/python-dotenv) | - | متغيرات البيئة |

### Deployment & Static Files

| التقنية | الإصدار | الدور |
|---------|---------|-------|
| [Gunicorn](https://gunicorn.org/) | 23.0.0 | خادم WSGI للإنتاج |
| [WhiteNoise](https://whitenoise.readthedocs.io/) | 6.9.0 | خدمة الملفات الثابتة |

---

## 📦 المتطلبات المسبقة

قبل البدء، تأكد من توفر ما يلي:

| المتطلب | الإصدار الموصى به | التحقق |
|---------|-------------------|--------|
| **Python** | 3.12 أو أحدث | `python --version` |
| **pip** | 23+ | `pip --version` |
| **PostgreSQL** | 15 أو أحدث | `psql --version` |
| **Git** | أي إصدار حديث | `git --version` |

### تثبيت PostgreSQL (إذا لم يكن مثبتًا)

**Ubuntu/Debian:**

```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
