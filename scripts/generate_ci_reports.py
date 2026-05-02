"""Generate Jenkins-friendly static HTML reports from JUnit XML.

pytest-html reports are useful locally, but Jenkins artifact viewing can block
the JavaScript used to render their dynamic tables. These static reports use
only plain HTML and CSS, so they remain readable from archived artifacts.
"""

from __future__ import annotations

import argparse
import html
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
from xml.etree import ElementTree


@dataclass
class TestCase:
    classname: str
    name: str
    duration: float
    status: str
    message: str


@dataclass
class SuiteReport:
    title: str
    level: str
    xml_file: str
    html_file: str
    tests: int
    passed: int
    failures: int
    errors: int
    skipped: int
    duration: float
    cases: list[TestCase]


SUITES = [
    {
        "title": "SWE4 Unit Test Summary",
        "level": "SWE4",
        "xml": "junit.xml",
        "html": "unit-summary.html",
        "purpose": "Component-level verification for VehicleController behavior.",
    },
    {
        "title": "SWE5 Integration Test Summary",
        "level": "SWE5",
        "xml": "integration-junit.xml",
        "html": "integration-summary.html",
        "purpose": "Interface verification between VehicleController and TransmissionController.",
    },
    {
        "title": "SWE6 Qualification Test Summary",
        "level": "SWE6",
        "xml": "qualification-junit.xml",
        "html": "qualification-summary.html",
        "purpose": "End-to-end acceptance checks for software readiness and timing.",
    },
]


def parse_junit(xml_path: Path, suite: dict[str, str]) -> SuiteReport:
    if not xml_path.exists():
        return SuiteReport(
            title=suite["title"],
            level=suite["level"],
            xml_file=suite["xml"],
            html_file=suite["html"],
            tests=0,
            passed=0,
            failures=0,
            errors=0,
            skipped=0,
            duration=0.0,
            cases=[],
        )

    root = ElementTree.parse(xml_path).getroot()
    suites = root.findall("testsuite") if root.tag == "testsuites" else [root]
    cases: list[TestCase] = []
    total_duration = 0.0
    failures = 0
    errors = 0
    skipped = 0

    for test_suite in suites:
        total_duration += float(test_suite.attrib.get("time", "0") or 0)
        for case in test_suite.findall("testcase"):
            status = "PASSED"
            message = ""
            failure = case.find("failure")
            error = case.find("error")
            skip = case.find("skipped")
            if failure is not None:
                status = "FAILED"
                failures += 1
                message = failure.attrib.get("message", "") or failure.text or ""
            elif error is not None:
                status = "ERROR"
                errors += 1
                message = error.attrib.get("message", "") or error.text or ""
            elif skip is not None:
                status = "SKIPPED"
                skipped += 1
                message = skip.attrib.get("message", "") or skip.text or ""

            cases.append(
                TestCase(
                    classname=case.attrib.get("classname", ""),
                    name=case.attrib.get("name", ""),
                    duration=float(case.attrib.get("time", "0") or 0),
                    status=status,
                    message=message.strip(),
                )
            )

    tests = len(cases)
    return SuiteReport(
        title=suite["title"],
        level=suite["level"],
        xml_file=suite["xml"],
        html_file=suite["html"],
        tests=tests,
        passed=tests - failures - errors - skipped,
        failures=failures,
        errors=errors,
        skipped=skipped,
        duration=total_duration,
        cases=cases,
    )


def css() -> str:
    return """
body { font-family: Arial, sans-serif; margin: 2rem; color: #17212b; line-height: 1.45; }
h1 { margin-bottom: 0.2rem; }
.meta { color: #5f6b7a; margin-bottom: 1.5rem; }
.cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 0.75rem; margin: 1rem 0 1.5rem; }
.card { border: 1px solid #d8dee6; border-radius: 6px; padding: 0.8rem; background: #f8fafc; }
.num { font-size: 1.5rem; font-weight: 700; }
.label { color: #5f6b7a; font-size: 0.85rem; }
table { border-collapse: collapse; width: 100%; margin-top: 1rem; }
th, td { border: 1px solid #d8dee6; padding: 0.55rem; text-align: left; vertical-align: top; }
th { background: #eef2f7; }
.PASSED { color: #0f7b32; font-weight: 700; }
.FAILED, .ERROR { color: #b42318; font-weight: 700; }
.SKIPPED { color: #8a5a00; font-weight: 700; }
a { color: #1455d9; }
"""


def status_badge(report: SuiteReport) -> str:
    return "PASSED" if report.failures == 0 and report.errors == 0 else "FAILED"


def suite_html(report: SuiteReport, project: str, build: str, purpose: str) -> str:
    rows = []
    for case in report.cases:
        rows.append(
            "<tr>"
            f"<td class='{case.status}'>{html.escape(case.status)}</td>"
            f"<td>{html.escape(case.classname)}</td>"
            f"<td>{html.escape(case.name)}</td>"
            f"<td>{case.duration:.3f}s</td>"
            f"<td>{html.escape(case.message)}</td>"
            "</tr>"
        )
    if not rows:
        rows.append("<tr><td colspan='5'>No test cases found. Check the JUnit XML artifact.</td></tr>")

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{html.escape(report.title)}</title>
  <style>{css()}</style>
</head>
<body>
  <h1>{html.escape(report.title)}</h1>
  <div class="meta">Project: {html.escape(project)} | Build: {html.escape(build)} | Status: {status_badge(report)}</div>
  <p>{html.escape(purpose)}</p>
  <div class="cards">
    <div class="card"><div class="num">{report.tests}</div><div class="label">Total tests</div></div>
    <div class="card"><div class="num">{report.passed}</div><div class="label">Passed</div></div>
    <div class="card"><div class="num">{report.failures}</div><div class="label">Failed</div></div>
    <div class="card"><div class="num">{report.errors}</div><div class="label">Errors</div></div>
    <div class="card"><div class="num">{report.skipped}</div><div class="label">Skipped</div></div>
    <div class="card"><div class="num">{report.duration:.3f}s</div><div class="label">Duration</div></div>
  </div>
  <table>
    <thead>
      <tr><th>Result</th><th>Class</th><th>Test</th><th>Duration</th><th>Message</th></tr>
    </thead>
    <tbody>
      {''.join(rows)}
    </tbody>
  </table>
  <p><a href="{html.escape(report.xml_file)}">Raw JUnit XML</a> | <a href="report-index.html">Report index</a></p>
</body>
</html>
"""


def index_html(reports: Iterable[SuiteReport], project: str, build: str) -> str:
    rows = []
    for report in reports:
        rows.append(
            "<tr>"
            f"<td>{html.escape(report.level)}</td>"
            f"<td><a href='{html.escape(report.html_file)}'>{html.escape(report.title)}</a></td>"
            f"<td class='{status_badge(report)}'>{status_badge(report)}</td>"
            f"<td>{report.tests}</td>"
            f"<td>{report.passed}</td>"
            f"<td>{report.failures}</td>"
            f"<td>{report.errors}</td>"
            f"<td>{report.duration:.3f}s</td>"
            "</tr>"
        )

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{html.escape(project)} Build {html.escape(build)} Reports</title>
  <style>{css()}</style>
</head>
<body>
  <h1>{html.escape(project)} CI Test Reports</h1>
  <div class="meta">Build: {html.escape(build)}</div>
  <table>
    <thead>
      <tr><th>Level</th><th>Report</th><th>Status</th><th>Total</th><th>Passed</th><th>Failed</th><th>Errors</th><th>Duration</th></tr>
    </thead>
    <tbody>{''.join(rows)}</tbody>
  </table>
  <h2>Additional Artifacts</h2>
  <ul>
    <li><a href="coverage/index.html">Coverage HTML Report</a></li>
    <li><a href="unit-test-report.html">pytest-html Unit Report</a></li>
    <li><a href="integration-test-report.html">pytest-html Integration Report</a></li>
    <li><a href="qualification-test-report.html">pytest-html Qualification Report</a></li>
  </ul>
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-dir", default="test-results")
    parser.add_argument("--project", default="automotive-software-testing")
    parser.add_argument("--build", default="local")
    args = parser.parse_args()

    results_dir = Path(args.results_dir)
    results_dir.mkdir(parents=True, exist_ok=True)

    reports: list[SuiteReport] = []
    for suite in SUITES:
        report = parse_junit(results_dir / suite["xml"], suite)
        reports.append(report)
        (results_dir / suite["html"]).write_text(
            suite_html(report, args.project, args.build, suite["purpose"]),
            encoding="utf-8",
        )

    (results_dir / "report-index.html").write_text(
        index_html(reports, args.project, args.build),
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
