import re
import time
from dataclasses import dataclass
from html import unescape

from django.conf import settings

from academics.models import AcademicStaff, College, Department, Program, Research
from admissions.models import Admission
from careers.models import JobPosting
from core.models import Branch, FormerPresident, Page, SocialMedia, University
from news.models import Announcement, Event, News
from services.models import Library, Service


@dataclass(frozen=True)
class KnowledgeChunk:
    id: str
    category: str
    title: str
    content: str
    path: str


_KNOWLEDGE_CACHE: dict[str, object] = {'chunks': None, 'expires_at': 0.0}
_CACHE_TTL_SECONDS = 120


def _strip_html(text: str) -> str:
    text = unescape(text or '')
    text = re.sub(r'<[^>]+>', ' ', text)
    return re.sub(r'\s+', ' ', text).strip()


def _frontend_path(path: str) -> str:
    base = settings.FRONTEND_URL.rstrip('/')
    return f'{base}{path}'


def _college_slug(name_en: str, name_ar: str) -> str:
    name = (name_en or '').lower()
    ar = name_ar or ''
    if 'pharmacy' in name or 'صيدلة' in ar:
        return 'pharmacy'
    if 'business' in name or 'administration' in name or 'إدارة' in ar or 'اعمال' in ar or 'أعمال' in ar:
        return 'business'
    return 'engineering'


def _chunk(chunk_id: str, category: str, title: str, content: str, path: str) -> KnowledgeChunk:
    return KnowledgeChunk(
        id=chunk_id,
        category=category,
        title=title.strip(),
        content=_strip_html(content),
        path=_frontend_path(path),
    )


def _build_knowledge_chunks() -> list[KnowledgeChunk]:
    chunks: list[KnowledgeChunk] = []

    for uni in University.objects.prefetch_related('social_links', 'branches', 'libraries').all():
        social_lines = '\n'.join(f'{s.platform}: {s.url}' for s in uni.social_links.all())
        branch_lines = '\n'.join(f'{b.name}: {b.address}' for b in uni.branches.all())
        chunks.append(
            _chunk(
                f'university-{uni.id}',
                'university',
                f'{uni.name_ar} / {uni.name_en}',
                (
                    f'الاسم: {uni.name_ar} ({uni.name_en})\n'
                    f'الموقع: {uni.location}\n'
                    f'البريد: {uni.email}\n'
                    f'الهاتف: {uni.phone}\n'
                    f'الفروع:\n{branch_lines}\n'
                    f'وسائل التواصل:\n{social_lines}'
                ),
                '/',
            )
        )

        for branch in uni.branches.all():
            chunks.append(
                _chunk(
                    f'branch-{branch.id}',
                    'branch',
                    branch.name,
                    f'الفرع: {branch.name}\nالعنوان: {branch.address}',
                    '/contact',
                )
            )

        for social in uni.social_links.all():
            chunks.append(
                _chunk(
                    f'social-{social.id}',
                    'social',
                    social.platform,
                    f'{social.platform}: {social.url}',
                    '/',
                )
            )

        for library in uni.libraries.all():
            extra = f'\nرابط الوصول: {library.access_url}' if library.access_url else ''
            chunks.append(
                _chunk(
                    f'library-{library.id}',
                    'library',
                    library.name,
                    f'المكتبة: {library.name}\nالموقع: {library.location}{extra}',
                    '/services',
                )
            )

    for page in Page.objects.all().order_by('slug'):
        chunks.append(
            _chunk(
                f'page-{page.slug}-ar',
                'page',
                page.title_ar,
                f'{page.title_ar}\n{page.content_ar}',
                f'/pages/{page.slug}',
            )
        )
        chunks.append(
            _chunk(
                f'page-{page.slug}-en',
                'page',
                page.title_en,
                f'{page.title_en}\n{page.content_en}',
                f'/pages/{page.slug}',
            )
        )

    for president in FormerPresident.objects.all():
        chunks.append(
            _chunk(
                f'president-{president.id}',
                'president',
                f'{president.name_ar} / {president.name_en}',
                f'رئيس سابق: {president.name_ar} ({president.name_en})\nالفترة: {president.years}',
                '/pages/presidents',
            )
        )

    colleges = College.objects.prefetch_related('departments__programs', 'departments__staff').all()
    for college in colleges:
        dept_lines = []
        program_lines = []
        for dept in college.departments.all():
            dept_lines.append(f'- {dept.name_ar} ({dept.name_en})')
            for program in dept.programs.all():
                program_lines.append(
                    f'- {program.name_ar} ({program.name_en}) — المستوى: {program.get_level_display()}'
                )

        chunks.append(
            _chunk(
                f'college-{college.id}',
                'college',
                f'{college.name_ar} / {college.name_en}',
                (
                    f'الكلية: {college.name_ar} ({college.name_en})\n'
                    f'الوصف: {college.description or ""}\n'
                    f'الأقسام:\n' + '\n'.join(dept_lines) + '\n'
                    f'البرامج:\n' + '\n'.join(program_lines)
                ),
                f'/colleges/{_college_slug(college.name_en, college.name_ar)}',
            )
        )

    for program in Program.objects.select_related('department__college').all():
        college = program.department.college
        chunks.append(
            _chunk(
                f'program-{program.id}',
                'program',
                f'{program.name_ar} / {program.name_en}',
                (
                    f'البرنامج: {program.name_ar} ({program.name_en})\n'
                    f'المستوى: {program.get_level_display()}\n'
                    f'القسم: {program.department.name_ar}\n'
                    f'الكلية: {college.name_ar}'
                ),
                f'/programs/{program.id}',
            )
        )

    for admission in Admission.objects.select_related('program__department__college').all():
        program = admission.program
        chunks.append(
            _chunk(
                f'admission-{admission.id}',
                'admission',
                f'قبول {program.name_ar}',
                (
                    f'برنامج: {program.name_ar} ({program.name_en})\n'
                    f'الكلية: {program.department.college.name_ar}\n'
                    f'المتطلبات: {admission.requirements}\n'
                    f'إجراءات التقديم: {admission.procedure}\n'
                    f'الرسوم: {admission.tuition_fee}\n'
                    f'التقويم الأكاديمي: {admission.academic_calendar}'
                ),
                '/admissions',
            )
        )

    for staff in AcademicStaff.objects.select_related('department__college').all():
        chunks.append(
            _chunk(
                f'staff-{staff.id}',
                'staff',
                staff.full_name,
                (
                    f'الاسم: {staff.full_name}\n'
                    f'الصفة: {staff.title}\n'
                    f'النوع: {staff.staff_type}\n'
                    f'القسم: {staff.department.name_ar}\n'
                    f'الكلية: {staff.department.college.name_ar}\n'
                    f'البريد: {staff.email}\n'
                    f'السيرة: {staff.bio}'
                ),
                f'/colleges/{_college_slug(staff.department.college.name_en, staff.department.college.name_ar)}',
            )
        )

    for research in Research.objects.select_related('staff').all():
        extra = f'\nالرابط: {research.url}' if research.url else ''
        chunks.append(
            _chunk(
                f'research-{research.id}',
                'research',
                research.title,
                (
                    f'البحث: {research.title}\n'
                    f'الباحث: {research.staff.full_name}\n'
                    f'الملخص: {research.abstract}\n'
                    f'تاريخ النشر: {research.published_date}{extra}'
                ),
                f'/colleges/{_college_slug(research.staff.department.college.name_en, research.staff.department.college.name_ar)}',
            )
        )

    for article in News.objects.all().order_by('-publish_date'):
        chunks.append(
            _chunk(
                f'news-{article.id}',
                'news',
                f'{article.title_ar} / {article.title_en}',
                (
                    f'خبر: {article.title_ar} ({article.title_en})\n'
                    f'تاريخ النشر: {article.publish_date}\n'
                    f'{article.content}'
                ),
                f'/news/{article.id}',
            )
        )

    for event in Event.objects.all().order_by('-event_date'):
        chunks.append(
            _chunk(
                f'event-{event.id}',
                'event',
                f'{event.title_ar} / {event.title_en}',
                (
                    f'فعالية: {event.title_ar} ({event.title_en})\n'
                    f'التاريخ: {event.event_date}\n'
                    f'المكان: {event.location}\n'
                    f'{event.description}'
                ),
                f'/events/{event.id}',
            )
        )

    for announcement in Announcement.objects.all().order_by('-date'):
        chunks.append(
            _chunk(
                f'announcement-{announcement.id}',
                'announcement',
                announcement.title,
                f'إعلان: {announcement.title}\nالتاريخ: {announcement.date}\n{announcement.body}',
                f'/announcements/{announcement.id}',
            )
        )

    for job in JobPosting.objects.filter(status='open').order_by('-deadline'):
        chunks.append(
            _chunk(
                f'job-{job.id}',
                'career',
                job.title,
                (
                    f'وظيفة: {job.title}\n'
                    f'النوع: {job.job_type}\n'
                    f'آخر موعد: {job.deadline}\n'
                    f'الوصف: {job.description}\n'
                    f'المتطلبات: {job.requirements}'
                ),
                f'/careers/{job.id}',
            )
        )

    for service in Service.objects.all():
        extra = f'\nالرابط: {service.url}' if service.url else ''
        chunks.append(
            _chunk(
                f'service-{service.id}',
                'service',
                f'{service.name_ar} / {service.name_en}',
                (
                    f'الخدمة: {service.name_ar} ({service.name_en})\n'
                    f'النوع: {service.service_type}\n'
                    f'{service.description}{extra}'
                ),
                '/services',
            )
        )

    static_sections = [
        ('site-home', 'الرئيسية', 'الصفحة الرئيسية لموقع جامعة الجزيرة الخاصة', '/'),
        ('site-colleges', 'الكليات', 'قائمة كليات الجامعة وبرامجها الأكاديمية', '/colleges'),
        ('site-admissions', 'القبول والتسجيل', 'معلومات القبول والتسجيل والرسوم والوثائق المطلوبة', '/admissions'),
        ('site-news', 'الأخبار', 'آخر أخبار الجامعة', '/news'),
        ('site-events', 'الفعاليات', 'فعاليات وأنشطة الجامعة', '/events'),
        ('site-careers', 'التوظيف', 'فرص العمل المتاحة في الجامعة', '/careers'),
        ('site-services', 'الخدمات', 'بوابة الطالب والمكتبة والخدمات الإلكترونية', '/services'),
        ('site-contact', 'اتصل بنا', 'معلومات التواصل مع الجامعة ونموذج المراسلة', '/contact'),
    ]
    for section_id, title, content, path in static_sections:
        chunks.append(_chunk(section_id, 'section', title, content, path))

    return chunks


def build_knowledge_base() -> list[KnowledgeChunk]:
    now = time.time()
    cached = _KNOWLEDGE_CACHE.get('chunks')
    expires_at = _KNOWLEDGE_CACHE.get('expires_at', 0.0)
    if cached is not None and now < float(expires_at):
        return cached  # type: ignore[return-value]

    chunks = _build_knowledge_chunks()
    _KNOWLEDGE_CACHE['chunks'] = chunks
    _KNOWLEDGE_CACHE['expires_at'] = now + _CACHE_TTL_SECONDS
    return chunks
