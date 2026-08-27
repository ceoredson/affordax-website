from datetime import date
from pathlib import Path
from urllib.parse import urlparse
from uuid import uuid4

from django.conf import settings
from django.core.files.images import ImageFile
from django.core.management.base import BaseCommand
from wagtail.images import get_image_model
from wagtail.models import Page, Site

from pages.models import (
    AudiencePage,
    HomePage,
    HomeProofPoint,
    InsightIndexPage,
    InsightPage,
    StandardPage,
)


def cta(heading, text, label, url):
    return ("call_to_action", {"eyebrow": "Start deliberately", "heading": heading, "text": text, "primary": {"label": label, "url": url}})


def features(heading, items, eyebrow="Designed around the work"):
    return ("feature_grid", {"eyebrow": eyebrow, "heading": heading, "intro": "", "features": [{"number": f"0{i}", "title": title, "text": text} for i, (title, text) in enumerate(items, 1)]})


def process(heading, items):
    return ("process", {"eyebrow": "One accountable thread", "heading": heading, "steps": [{"title": title, "text": text} for title, text in items]})


HOME_BODY = [
    features("Less chasing. More certainty at every hand-off.", [
        ("A decision with context", "An authorised enquiry produces an allocation for the requesting provider without turning a salary record into an open file."),
        ("A hold that means one thing", "Temporary reservations protect an agreed monthly amount while an application moves through approval."),
        ("An outcome you can trace", "Payroll expectations, collections and exceptions remain connected instead of scattering across email and spreadsheets."),
    ]),
    process("From employee request to reconciled result", [
        ("Authorise the enquiry", "The institution records why the employee requested the check and where the underlying evidence can be retrieved."),
        ("Allocate and reserve", "The configured policy calculates a privacy-safe amount and places a time-limited hold."),
        ("Review independently", "A separate authorised person approves or rejects the proposed deduction instruction."),
        ("Collect and reconcile", "The employer processes payroll; providers and finance teams follow every full, partial or exceptional result."),
    ]),
    ("metric_band", {"metrics": [
        {"value": "01", "label": "shared workflow instead of bilateral spreadsheets"},
        {"value": "48h", "label": "normal reservation window before fresh review"},
        {"value": "2-person", "label": "maker-checker decisions on financial actions"},
        {"value": "MWK", "label": "a platform designed around the local payroll context"},
    ]}),
    ("editorial", {"eyebrow": "Privacy is a product decision", "heading": "Useful to a lender without opening an employee's payslip.", "body": "<p>The requesting institution needs a clear allocation and the state of its own obligations. It does not need another holder's identity, another lender's amount, or a breakdown of salary components.</p><p>That boundary is carried through enquiry, reservation, collection reporting and provider-to-provider settlement.</p>", "image_side": "right"}),
    ("quote", {"quote": "The strongest financial workflow is the one people can explain, operate and reconcile without private knowledge or heroic memory.", "attribution": "Platform principle", "role": "Accountability by design"}),
    ("faq", {"eyebrow": "Before the first conversation", "heading": "Questions, answered plainly", "items": [
        {"question": "Does the platform lend money?", "answer": "<p>No. Participating financial institutions originate their own products. The platform coordinates authorised affordability, deduction and reconciliation workflows.</p>"},
        {"question": "Can a provider see an employee's full salary?", "answer": "<p>The intended provider response is an allocated amount and its own records—not salary components or another holder's commitments.</p>"},
        {"question": "What does an employer change?", "answer": "<p>The employer maintains workforce and payroll facts, reviews validated deduction instructions and runs a controlled monthly payroll process.</p>"},
        {"question": "Is a reservation already a deduction?", "answer": "<p>No. It is a temporary hold. A deduction becomes active only after the required instruction and approval workflow.</p>"},
    ]}),
    cta("Bring the real workflow to the table.", "We will discuss your current process, failure points, responsibilities and evidence—not run a generic sales presentation.", "Book a conversation", "/enquire/demo/"),
]


EMPLOYER_BODY = [
    features("Payroll control without another month-end maze", [
        ("One workforce record", "Maintain employment and payroll facts once, with role-based access for HR, payroll and finance."),
        ("Maker-checker payroll", "Separate upload from confirmation so validation results receive independent review."),
        ("Visible exceptions", "See partial, suspended and disputed outcomes instead of discovering them through reconciliation calls."),
    ]),
    process("A measured employer onboarding", [("Understand the payroll", "Map columns, timing, roles and current deduction relationships."), ("Prove with synthetic data", "Run the workflow without exposing employee information."), ("Pilot deliberately", "Start with trained users, named support owners and daily reconciliation."), ("Expand from evidence", "Broaden only after complete payroll cycles reconcile cleanly.")]),
    cta("Make payroll administration easier to account for.", "Tell us about your workforce and current deduction process. Do not send employee data through this form.", "Employer enquiry", "/enquire/employer/"),
]


PROVIDER_BODY = [
    features("Origination connected to the collection reality", [
        ("Authorised enquiry", "Record the application purpose and evidence reference before checking the employee."),
        ("Private allocation", "Work with the monthly amount available to your institution, not a competitor's portfolio."),
        ("Governed consolidation", "Request a payoff quote, record settlement evidence and wait for receipt confirmation before replacement."),
        ("Collection outcomes", "Follow full, partial, zero and reversed outcomes through one portfolio view."),
        ("Balance discipline", "Termed obligations reduce through append-only movements and complete at zero."),
        ("Integration paths", "Use controlled files and signed webhooks without sharing a human administrator account."),
    ], eyebrow="For licensed providers"),
    process("A safer provider-to-provider replacement", [("Request", "Name the existing provider and employee-authorised loan reference."), ("Quote", "The existing provider verifies its own record and issues a payoff amount."), ("Fund", "The replacement provider submits an exact payment reference."), ("Confirm", "The existing provider confirms receipt before its payroll instruction closes.")]),
    cta("Discuss the operating model behind your products.", "Bring your approval, settlement, balance and reconciliation questions.", "Provider enquiry", "/enquire/provider/"),
]


SEO_BY_SLUG = {
    "home": (
        "Payroll Affordability & Deductions in Malawi",
        "Affordax connects Malawi employers and financial providers through controlled affordability checks, payroll deductions, collection outcomes and reconciliation.",
    ),
    "employers": (
        "Payroll Deduction Management for Malawi Employers",
        "Give payroll teams a controlled workflow for employee records, deduction instructions, monthly processing, exceptions and reconciliation in Malawi.",
    ),
    "providers": (
        "Salary-Backed Lending Infrastructure in Malawi",
        "Connect affordability checks, governed deduction approvals, payroll collection outcomes and reconciliation for licensed financial providers in Malawi.",
    ),
    "how-it-works": (
        "How Affordax Payroll Deductions Work",
        "See how Affordax connects employee-authorised affordability enquiries, reservations, independent approvals, payroll outcomes and reconciliation.",
    ),
    "trust": (
        "Security, Privacy and Payroll Controls",
        "Understand the access controls, independent approvals, privacy boundaries, audit evidence and operational safeguards designed into Affordax.",
    ),
    "about": (
        "About Affordax Malawi",
        "Affordax is building accountable affordability, payroll deduction and reconciliation infrastructure for Malawi's private-sector employers and providers.",
    ),
    "privacy": (
        "Privacy Notice",
        "Read how the Affordax public website handles enquiry details, security metadata and requests concerning personal information.",
    ),
    "terms": (
        "Website Terms",
        "Read the terms that apply when using the Affordax public website and its employer, provider, demonstration and contact enquiry channels.",
    ),
    "insights": (
        "Payroll Affordability Insights for Malawi",
        "Practical articles about salary affordability, payroll deductions, responsible lending, privacy and reconciliation in Malawi's private sector.",
    ),
    "reservation-is-not-a-deduction": (
        "Why an Affordability Reservation Is Not a Deduction",
        "Learn why temporarily reserving affordability and activating a payroll deduction are separate decisions with different controls and evidence.",
    ),
    "payroll-affordability-malawi": (
        "What Is Payroll Affordability in Malawi?",
        "A practical explanation of payroll affordability, protected take-home pay and responsible salary-backed commitments for Malawi employees and lenders.",
    ),
    "payroll-deduction-management": (
        "How Payroll Deduction Management Protects Employees",
        "See how controlled instructions, validation, priority rules, exception handling and reconciliation improve payroll deductions for every participant.",
    ),
    "salary-backed-lending-malawi": (
        "Salary-Backed Lending in Malawi's Private Sector",
        "Explore how verified employment, affordability controls, governed payroll deductions and reconciliation can support responsible lending in Malawi.",
    ),
}


INSIGHT_ARTICLES = [
    {
        "title": "Why a reservation is not a deduction",
        "slug": "reservation-is-not-a-deduction",
        "summary": "Temporary capacity and an approved payroll obligation solve different problems. Treating them as one creates confusion and risk.",
        "body": "<h2>Two different decisions</h2><p>A reservation temporarily protects allocated monthly capacity while an application is completed. It expires or is consumed. It is not yet an instruction to payroll.</p><h2>The approval seam</h2><p>An obligation becomes eligible for collection only after the required product, terms, evidence and independent approval are recorded.</p>",
    },
    {
        "title": "What is payroll affordability in Malawi?",
        "slug": "payroll-affordability-malawi",
        "summary": "Payroll affordability asks what an employee can responsibly commit each month while preserving statutory deductions and protected take-home pay.",
        "body": "<h2>Affordability is a monthly capacity, not a salary disclosure</h2><p>A useful affordability decision answers a narrow question: what monthly amount can this employee allocate without crossing the applicable protected take-home boundary? A financial provider needs that decision and the state of its own commitments. It does not need an unrestricted view of the employee's payslip or another provider's portfolio.</p><h2>The calculation must begin with reliable payroll facts</h2><p>Gross pay alone is not enough. A controlled process starts with current employer-supplied payroll information, accounts for statutory deductions and applies the configured protection policy before considering existing authorised commitments. Because salaries and employment status can change, the result is point-in-time evidence rather than a permanent promise.</p><h2>Reservations prevent the same capacity being promised twice</h2><p>When an employee continues an application, a short-lived reservation can hold the allocated amount while approval is completed. The hold must expire if the application does not progress. Only an independently approved obligation should become eligible for payroll collection.</p><h2>Payroll remains the collection reality</h2><p>An earlier affordability result cannot guarantee that every future payroll period will collect in full. Leave, salary changes, termination and higher-priority deductions can affect the outcome. That is why each period needs a clear requested amount, collected amount and exception reason.</p><h2>A responsible process stays explainable</h2><p>Employees, employers and providers should be able to understand why a decision was made, who approved it and what happened in payroll. The specific legal, employment and product rules always depend on the applicable agreements and Malawi requirements; technology should make those rules visible and consistently operated.</p>",
    },
    {
        "title": "How payroll deduction management protects employees and employers",
        "slug": "payroll-deduction-management",
        "summary": "A controlled deduction workflow replaces scattered instructions with validation, independent approval, visible exceptions and reconciled outcomes.",
        "body": "<h2>The risk begins before payroll is run</h2><p>When deduction instructions arrive through unrelated emails, spreadsheets and bilateral processes, payroll teams spend valuable time deciding which record is current. Employees face the risk of duplicated, obsolete or unaffordable deductions, while providers struggle to explain missing collections.</p><h2>One instruction needs one accountable lifecycle</h2><p>A sound process records the employee, provider, amount, start conditions and supporting authority. Material changes should follow a maker-checker process rather than silently editing the active instruction. Cancellation, correction and reversal need preserved evidence so the history remains understandable.</p><h2>Validation should happen before confirmation</h2><p>Payroll files should be checked for the correct employer, period, employee identifiers, duplicate rows and usable salary values. Separating upload from confirmation gives another authorised person the opportunity to review errors before financial processing begins.</p><h2>Exceptions are outcomes, not missing data</h2><p>Every due obligation should receive a period outcome, including when nothing was collected. Full, partial, zero, suspended and reversed results allow each participant to distinguish an affordability protection from a processing failure.</p><h2>Reconciliation closes the operational loop</h2><p>After payroll, expected and observed amounts should be compared by employer and provider. Differences need a named owner, supporting evidence and a dispute path. This turns month-end from a search across inboxes into a process that can be reviewed and improved.</p>",
    },
    {
        "title": "Salary-backed lending in Malawi's private sector",
        "slug": "salary-backed-lending-malawi",
        "summary": "Responsible salary-backed lending depends on verified employment, privacy-conscious affordability, governed deductions and transparent collection outcomes.",
        "body": "<h2>Employment can support access without becoming unrestricted access</h2><p>Formal employment gives a lender useful evidence about regular income, but it should not open an employee's full payroll record to every provider. A neutral affordability layer can return an allocation for the requesting institution while keeping salary components and competing obligations private.</p><h2>Origination and collection are connected but distinct</h2><p>The provider still owns product design, credit assessment and the lending relationship. Payroll deduction management does not issue the loan. It coordinates the authorised monthly obligation and reports what happened when the employer processed payroll.</p><h2>Independent approval protects the instruction</h2><p>A reservation should not automatically become a deduction. Product terms, authority evidence and the proposed monthly amount need review by an appropriately authorised person. Increases and replacements should receive fresh affordability evidence.</p><h2>Collection outcomes improve portfolio decisions</h2><p>Providers need more than a total remittance. They need stable outcomes for each expected collection: requested, collected, partial, suspended, reversed or completed. That history supports customer service, portfolio monitoring and reconciliation without exposing another provider's data.</p><h2>Trust comes from operating discipline</h2><p>Employers need predictable files and fewer bilateral exceptions. Employees need protected take-home pay and understandable commitments. Providers need reliable evidence and timely results. A shared, auditable workflow can align those needs while leaving each institution responsible for its legal and contractual duties.</p>",
    },
]


class Command(BaseCommand):
    help = "Create a carefully designed initial public website without overwriting editorial work."

    def handle(self, *args, **options):
        root = Page.get_first_root_node()
        home = HomePage.objects.first()
        if home is None:
            root.get_children().filter(content_type__model="page").delete()
            home = HomePage(title="Home", slug="home", show_in_menus=False, eyebrow="Affordability and payroll, connected", hero_title="Financial workflows should not depend on guesswork.", hero_text="One accountable network for employers and financial providers—from an employee-authorised enquiry to a reconciled payroll result.", search_description="A connected affordability, deduction and payroll workflow for employers and financial providers.", body=HOME_BODY)
            root.add_child(instance=home)
            for value, label in [("Private", "provider views designed around allocated affordability"), ("Governed", "financial actions with accountable approvals"), ("Traceable", "outcomes connected through reconciliation")]:
                HomeProofPoint.objects.create(page=home, value=value, label=label)
            home.save_revision().publish()
        public_url = urlparse(settings.PUBLIC_SITE_URL)
        Site.objects.update_or_create(
            is_default_site=True,
            defaults={
                "hostname": public_url.hostname or "localhost",
                "port": public_url.port or (443 if public_url.scheme == "https" else 8000),
                "site_name": "Public website",
                "root_page": home,
            },
        )
        self._audience(home, "Employers", "employers", "For employers", "Give payroll teams one accountable deduction workflow.", "Move from scattered instructions to controlled employee records, independent payroll approval and visible collection outcomes.", "Start an employer conversation", "/enquire/employer/", EMPLOYER_BODY)
        self._audience(home, "Financial providers", "providers", "For financial providers", "Know what can be allocated. Follow what was collected.", "Originate salary-backed products through an authorised, privacy-conscious workflow connected to payroll and reconciliation.", "Start a provider conversation", "/enquire/provider/", PROVIDER_BODY)
        self._standard(home, "How it works", "how-it-works", "The operating model", "Four linked decisions—not one black-box score.", [process("The complete path", [("Employee request", "The provider records purpose and authority evidence."), ("Affordability", "Configured policy returns a privacy-safe allocation."), ("Reservation and approval", "A temporary hold supports an independently reviewed instruction."), ("Payroll and reconciliation", "Every due obligation receives a result and every variance can be investigated.")]), cta("See it against your own process.", "A useful demonstration starts with the questions your teams already argue about.", "Book a conversation", "/enquire/demo/")])
        self._standard(home, "Trust centre", "trust", "Trust is operational", "Controls matter only when people can see who acts, what changes and how recovery works.", [features("A visible control model", [("Scoped access", "Institution and role determine what a user may see and do."), ("Independent decisions", "Sensitive financial actions use distinct proposal and approval responsibilities."), ("Preserved evidence", "Important financial history is corrected through new evidence, not silent rewriting."), ("Incident discipline", "Incorrect allocation, privacy exposure or unexplained variance should stop intake and preserve records.")]), cta("Bring your security questions.", "Ask about data handling, integration, access and operational recovery before discussing rollout.", "Contact the team", "/enquire/contact/")])
        about = self._standard(home, "About", "about", "Why this work exists", "Private-sector payroll should make responsible financial access easier—not make employees, employers and providers carry more administrative uncertainty.", [("editorial", {"eyebrow": "A neutral operating layer", "heading": "Built between institutions, accountable to the people in the records.", "body": "<p>The platform does not issue loans or replace an employer's lawful payroll authority. It coordinates how authorised affordability, obligations, payroll outcomes and disputes move between organisations.</p><p>Our measure of progress is not the number of screens. It is whether each participant can understand its responsibility and reconcile the result.</p>", "image_side": "left"}), cta("Help shape the operating standard.", "We are speaking with employers, providers and specialists who know where existing processes break.", "Talk with us", "/enquire/contact/")])
        self._ensure_founder_profile(about)
        self._standard(home, "Privacy", "privacy", "Privacy notice", "A plain-language overview of information handled by the public website. Product-platform privacy notices are provided separately to participating institutions.", [features("Public website information", [("What we collect", "Contact and organisation details you choose to submit, plus limited security metadata."), ("Why", "To respond, assess onboarding interest, handle complaints and protect forms from abuse."), ("What not to send", "Do not submit passwords, one-time codes, full identity numbers, payroll files or salary details."), ("Your request", "Contact the team to ask about access, correction or deletion where applicable.")])])
        self._standard(home, "Terms", "terms", "Website terms", "This website provides information and enquiry channels. It does not grant portal access, approve a loan or authorise a payroll deduction.", [features("Using this website", [("Accurate enquiries", "Submit information you are authorised to provide."), ("No sensitive uploads", "Public forms are not a channel for employee or payroll files."), ("No financial decision", "Illustrations and explanations are not credit approval or legal advice."), ("Separate agreements", "Live institutional use requires signed terms, onboarding and approved operating controls.")])])
        insights = InsightIndexPage.objects.child_of(home).filter(slug="insights").first()
        if insights is None:
            insights = InsightIndexPage(title="Insights", slug="insights", introduction="Short, practical notes on affordability, payroll operations, privacy and reconciliation.", show_in_menus=True)
            home.add_child(instance=insights)
            insights.save_revision().publish()
        for article_data in INSIGHT_ARTICLES:
            if not InsightPage.objects.child_of(insights).filter(slug=article_data["slug"]).exists():
                article = InsightPage(
                    title=article_data["title"],
                    slug=article_data["slug"],
                    publication_date=date(2026, 8, 27),
                    summary=article_data["summary"],
                    body=article_data["body"],
                )
                insights.add_child(instance=article)
                article.save_revision().publish()
        self._apply_seo(home)
        self.stdout.write(self.style.SUCCESS("Initial public website content is ready."))

    def _audience(self, parent, title, slug, label, hero, text, action, url, body):
        if not AudiencePage.objects.child_of(parent).filter(slug=slug).exists():
            page = AudiencePage(title=title, slug=slug, show_in_menus=True, audience_label=label, hero_title=hero, hero_text=text, action_label=action, action_url=url, body=body)
            parent.add_child(instance=page)
            page.save_revision().publish()

    def _standard(self, parent, title, slug, eyebrow, intro, body):
        page = StandardPage.objects.child_of(parent).filter(slug=slug).first()
        if page is None:
            page = StandardPage(title=title, slug=slug, show_in_menus=slug in {"how-it-works", "trust", "about"}, eyebrow=eyebrow, introduction=intro, body=body)
            parent.add_child(instance=page)
            page.save_revision().publish()
        return page

    def _apply_seo(self, home):
        pages = [home, *Page.objects.descendant_of(home).specific()]
        for page in pages:
            seo = SEO_BY_SLUG.get(page.slug)
            if seo is None:
                continue
            seo_title, search_description = seo
            if page.seo_title == seo_title and page.search_description == search_description:
                continue
            page.seo_title = seo_title
            page.search_description = search_description
            page.save_revision().publish()

    def _ensure_founder_profile(self, page):
        if any(block.block_type == "founder" for block in page.body):
            return
        image_model = get_image_model()
        image = image_model.objects.filter(title="Precious Ngwira, Chief Executive Officer").first()
        if image is None:
            source = Path(settings.BASE_DIR) / "static/images/precious-ngwira-founder.jpg"
            with source.open("rb") as image_file:
                image = image_model(
                    title="Precious Ngwira, Chief Executive Officer",
                    file=ImageFile(image_file, name="precious-ngwira-founder.jpg"),
                )
                image.save()
        profile = {
            "type": "founder",
            "id": str(uuid4()),
            "value": {
                "image": image.pk,
                "name": "Precious Ngwira",
                "role": "Chief Executive Officer",
                "heading": "Building trust between every participant in the payroll process.",
                "body": "<p>Precious leads the team developing a clearer operating layer for employers and financial providers. The work begins with a practical belief: financial access can grow without making privacy, payroll control or accountability weaker.</p>",
            },
        }
        body = list(page.body.raw_data)
        insert_at = len(body) - 1 if body and body[-1]["type"] == "call_to_action" else len(body)
        body.insert(insert_at, profile)
        page.body = body
        page.save_revision().publish()
