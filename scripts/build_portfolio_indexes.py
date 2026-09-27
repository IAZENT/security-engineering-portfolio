#!/usr/bin/env python3
"""Generate public portfolio indexes from the published report catalog."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "content" / "portfolio.json"
DOCS = ROOT / "docs"
REPORTS_DIR = DOCS / "pentesting" / "reports"
START = "<!-- GENERATED_REPORTS_START -->"
END = "<!-- GENERATED_REPORTS_END -->"
NAV_START = "  # GENERATED_PORTFOLIO_NAV_START"
NAV_END = "  # GENERATED_PORTFOLIO_NAV_END"


def published_reports(data):
    return sorted(
        [item for item in data.get("reports", []) if item.get("status") == "published"],
        key=lambda item: item.get("date", ""),
        reverse=True,
    )


def report_item(item, report_prefix="", pdf_prefix=None):
    tags = " · ".join(item.get("tags", []))
    pdf_prefix = report_prefix if pdf_prefix is None else pdf_prefix
    pdf = f"[PDF]({pdf_prefix}{item['pdf']})"
    return f"- **{item['title']}** ({item['date']}) - {item['summary']}  \n  {tags} · [Read report]({report_prefix}{item['slug']}.md) · {pdf}"


def report_section_item(item, report_prefix="", pdf_prefix=None):
    tags = " · ".join(item.get("tags", []))
    pdf_prefix = report_prefix if pdf_prefix is None else pdf_prefix
    return "\n".join(
        [
            f"### {item['title']}",
            "",
            f"**Published:** {item['date']}  ",
            f"{item['summary']}  ",
            f"{tags} · [Read report]({report_prefix}{item['slug']}.md) · [PDF]({pdf_prefix}{item['pdf']})",
            "",
        ]
    )


def generated_home_block(reports):
    if not reports:
        return "## Published work\n\nNo published reports yet."

    latest = reports[0]
    tags = "".join(f"<span>{tag}</span>" for tag in latest.get("tags", []))
    latest_block = f"""## Latest published report

<div class=\"featured-work\" markdown>

<div class=\"featured-work__copy\" markdown>

<p class=\"portfolio-kicker\">{latest['title'].upper()} · {latest['date']}</p>

### {latest['title']}

{latest['summary']}

<div class=\"work-tags\" markdown>{tags}</div>

[Read the walkthrough/report](pentesting/reports/{latest['slug']}.md){{ .md-button .md-button--primary }}
[Download PDF](pentesting/reports/{latest['pdf']}){{ .md-button }}

</div>

<div class=\"featured-work__visual\" markdown>

![DVWA web application security lab](assets/portfolio-cover.png)

</div>

</div>

## Top published reports

{chr(10).join(report_item(item, 'pentesting/reports/') for item in reports[:3])}
"""
    return latest_block.strip()


def replace_generated_home(block):
    path = DOCS / "index.md"
    text = path.read_text()
    before, marker, rest = text.partition(START)
    if not marker:
        raise SystemExit("Homepage is missing GENERATED_REPORTS_START marker")
    _, end_marker, after = rest.partition(END)
    if not end_marker:
        raise SystemExit("Homepage is missing GENERATED_REPORTS_END marker")
    path.write_text(f"{before}{START}\n\n{block}\n\n{END}{after}")


def replace_generated_nav(reports):
    path = ROOT / "mkdocs.yml"
    text = path.read_text()
    before, marker, rest = text.partition(NAV_START)
    if not marker:
        raise SystemExit("mkdocs.yml is missing GENERATED_PORTFOLIO_NAV_START marker")
    _, end_marker, after = rest.partition(NAV_END)
    if not end_marker:
        raise SystemExit("mkdocs.yml is missing GENERATED_PORTFOLIO_NAV_END marker")
    lines = [
        NAV_START,
        "  - Penetration Testing:",
        "      - Published Reports: pentesting/index.md",
    ]
    lines += [
        f"      - {item['title']}: pentesting/reports/{item['slug']}.md"
        for item in reports
    ]
    lines += [NAV_END]
    path.write_text(f"{before}{chr(10).join(lines)}{after}")


def write_section(path, title, intro, items, report_prefix="../"):
    lines = [f"# {title}", "", intro, ""]
    if items:
        lines += ["## Published work", ""]
        lines += [report_section_item(item, report_prefix) for item in items]
        lines += ["Content is listed newest first. Each published item has an explicit scope and a matching public deliverable."]
    else:
        lines += ["## No published work yet", "", "This section is ready for its first publication. New entries will appear here automatically when they are added to the portfolio catalog and pass the publication checks."]
    path.write_text("\n".join(lines) + "\n")


def main():
    data = json.loads(CATALOG.read_text())
    reports = published_reports(data)
    replace_generated_home(generated_home_block(reports))
    replace_generated_nav(reports)
    write_section(
        DOCS / "pentesting" / "index.md",
        "Penetration Testing",
        "Published penetration-test walkthroughs and reports from authorized lab environments.",
        [item for item in reports if "pentesting" in item.get("channels", [])],
        report_prefix="reports/",
    )
    write_section(
        REPORTS_DIR / "index.md",
        "Published Penetration-Test Reports",
        "Practical reports with a clear scope, evidence, impact, remediation, and retest criteria.",
        reports,
        report_prefix="",
    )
    write_section(
        DOCS / "walkthroughs" / "index.md",
        "Practical Walkthroughs",
        "Standalone practical walkthroughs from setup and testing through interpretation and cleanup. Penetration-test reports remain in the Penetration Testing section.",
        [item for item in reports if "walkthroughs" in item.get("channels", [])],
        report_prefix="../pentesting/reports/",
    )
    write_section(
        DOCS / "research" / "index.md",
        "Security Research",
        "Technical research that separates verified facts, interpretation, sources, and open questions.",
        [],
    )
    write_section(
        DOCS / "projects" / "index.md",
        "Security Engineering Projects",
        "Security tooling, home labs, automation, and secure infrastructure work.",
        [],
    )


if __name__ == "__main__":
    main()
