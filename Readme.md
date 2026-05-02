# Automotive CI/CD QA Interview Project

This repository is a hands-on automotive QA project for practicing CI/CD, test automation, and interview answers for SWE4, SWE5, and SWE6 responsibilities.

The project uses a small simulated vehicle control system so you can explain the same ideas that appear in real automotive validation work: unit verification, software integration, qualification testing, HIL readiness, reporting, traceability, and quality gates.

## What This Project Demonstrates

| Area | File or stage | Interview meaning |
| --- | --- | --- |
| Software component under test | `helloworld.py` | A vehicle controller with engine, speed, diagnostics, and fault behavior |
| Supporting subsystem | `subsystem.py` | A transmission controller used for integration scenarios |
| SWE4 style unit tests | `test_helloworld.py` | Verifies component behavior before integration |
| SWE5 style integration tests | `test_integration.py` | Verifies interaction between vehicle and transmission logic |
| SWE6 style qualification tests | `test_qualification.py` | Verifies end-to-end acceptance behavior and timing |
| Test helpers and wrappers | `test_helpers.py` | Reusable setup, assertions, timing, and result analysis |
| Jenkins CI/CD pipeline | `Jenkinsfile` | Automated build, test, coverage, reporting, packaging, and deployment simulation |
| GitHub Actions CI | `.github/workflows/ci.yml` | Cloud CI equivalent for pull requests and pushes |
| Jenkins setup tutorial | `JENKINS_SETUP.md` | Local Jenkins setup and troubleshooting |
| Interview guide | `docs/SWE4_SWE5_SWE6_CICD_INTERVIEW_GUIDE.md` | Tutorial, talking points, and Q&A |

## SWE4, SWE5, SWE6 in This Project

### SWE4: Software Unit Verification

SWE4 focuses on verifying individual software units against expected behavior before they are integrated.

In this project:

- `VehicleController.start_engine()` is tested for success and blocked-start behavior when faults exist.
- `VehicleController.accelerate()` is tested for engine-off behavior and max-speed limits.
- `VehicleController.run_diagnostics()` is tested for readiness, speed validity, and fault count.
- `test_helpers.py` shows reusable wrappers for setup, assertions, timing, and result summaries.

Interview answer:

> In SWE4, I validate software units in isolation. In this project I test the vehicle controller methods directly, including normal, boundary, and fault paths. CI runs those unit tests automatically, publishes JUnit XML and HTML reports, and blocks weak changes early before they reach integration or HIL.

### SWE5: Software Integration and Integration Testing

SWE5 focuses on verifying that multiple software components work together correctly.

In this project:

- `VehicleController` is integrated with `TransmissionController`.
- `test_integration.py` verifies that throttle does not increase speed until the transmission is engaged.
- Integration tests verify interface behavior between components, not only internal function logic.
- Jenkins publishes `integration-junit.xml` and `integration-test-report.html`.

Interview answer:

> In SWE5, I focus on component interaction and interface behavior. In this project, the vehicle controller and transmission controller are tested together. The goal is to catch integration defects such as incorrect state sequencing, wrong assumptions between components, or missing preconditions before the software reaches qualification or HIL benches.

### SWE6: Software Qualification Testing

SWE6 focuses on verifying the integrated software against system or software qualification criteria.

In this project:

- `test_qualification.py` runs an end-to-end driving scenario.
- Qualification checks verify system readiness after start, gear engagement, throttle application, and diagnostics.
- A timing threshold test demonstrates performance acceptance criteria.
- This maps closely to your HIL background, where tests validate real ECU behavior against requirements.

Interview answer:

> My strongest experience is SWE6 and HIL testing. In SWE6, I validate that integrated software meets requirements in realistic scenarios. In this project, the qualification test simulates an end-to-end drive sequence and checks diagnostic readiness and timing. In real HIL, I would extend this by stimulating ECU inputs, measuring CAN/LIN/Ethernet signals, validating DTC behavior, checking power modes, and producing requirement-based pass/fail evidence.

## Pros of CI/CD for SWE4, SWE5, and SWE6

| Level | CI/CD benefit | Why it matters in automotive QA |
| --- | --- | --- |
| SWE4 | Fast feedback on unit defects | Developers find logic errors before code reaches integration |
| SWE4 | Repeatable unit execution | The same unit tests run locally, in pull requests, and in Jenkins |
| SWE4 | Coverage visibility | Teams see which functions and branches still need tests |
| SWE4 | Early quality gates | Bad changes can fail before consuming integration or HIL bench time |
| SWE5 | Automated integration checks | Interface defects are caught as soon as components are combined |
| SWE5 | Stable regression suite | Existing behavior is protected when software components change |
| SWE5 | Better dependency confidence | Teams can see whether component changes broke downstream behavior |
| SWE5 | Faster root cause isolation | Pipeline stages show whether failure is unit, integration, coverage, or reporting related |
| SWE6 | Automated qualification evidence | Reports and artifacts provide objective pass/fail data |
| SWE6 | HIL bench efficiency | CI can pre-screen software using unit/SIL/integration tests before expensive HIL execution |
| SWE6 | Requirement traceability support | Test reports can be linked to requirements, defects, releases, and build numbers |
| SWE6 | Release confidence | Qualification gates help decide whether software is ready for deployment or vehicle-level testing |

## CI/CD Pipeline Flow

The Jenkins pipeline follows this sequence:

1. `Checkout`: pulls the source code.
2. `Setup Environment`: creates a Python virtual environment and installs test tools.
3. `Unit Tests`: runs SWE4-style unit tests and produces JUnit plus HTML reports.
4. `Code Coverage`: measures coverage and creates a coverage HTML report.
5. `Integration Tests (SWE5)`: runs integration checks between vehicle and transmission controllers.
6. `Qualification Tests (SWE6)`: runs end-to-end qualification scenarios and timing checks.
7. `Code Quality Analysis`: runs static checks with flake8.
8. `Test Reporting`: creates a report index linking all reports.
9. `Build Artifact`: creates a deployment placeholder artifact.
10. `Deploy`: packages the artifact and simulates deployment.
11. `Post-build actions`: archives reports and artifacts, then adds quick report links to the Jenkins build description.

Expected Jenkins artifacts include:

- `test-results/report-index.html`
- `test-results/unit-summary.html`
- `test-results/integration-summary.html`
- `test-results/qualification-summary.html`
- `test-results/unit-test-report.html`
- `test-results/integration-test-report.html`
- `test-results/qualification-test-report.html`
- `test-results/coverage/index.html`
- `test-results/test-metrics.csv`
- `test-results/junit.xml`
- `test-results/integration-junit.xml`
- `test-results/qualification-junit.xml`
- `dist/package/artifact.zip`

The `*-summary.html` files are static Jenkins-friendly reports generated from JUnit XML. They are usually better for archived Jenkins viewing than pytest-html because they do not depend on JavaScript.

## Jenkins Graphical Test Views

Jenkins creates its own graphical test trend from the JUnit XML files published by the `junit(...)` steps in the Jenkinsfile.

How to see it:

1. Run the Jenkins job at least two or three times. A trend graph needs build history.
2. Open the Jenkins job page, for example `local-automotive-testing`.
3. Look for `Test Result Trend` on the job page.
4. Open a specific build and select `Test Result`.
5. Jenkins will show total tests, failures, skipped tests, duration, package/class breakdown, and historical trends.

What feeds the Jenkins graph:

- `test-results/junit.xml` for SWE4 unit tests
- `test-results/integration-junit.xml` for SWE5 integration tests
- `test-results/qualification-junit.xml` for SWE6 qualification tests

The project also writes `test-results/test-metrics.csv`, which summarizes total, passed, failed, skipped, duration, and pass-rate data by SWE level. That file is useful for learning how custom charts can be built with optional Jenkins plugins such as Plot, Metrics, or dashboard plugins.

## Run Locally

Windows PowerShell:

```powershell
py -m venv venv
.\venv\Scripts\python.exe -m pip install --upgrade pip
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe -m pytest test_helloworld.py test_integration.py test_qualification.py -v
```

Generate local reports:

```powershell
.\venv\Scripts\python.exe -m pytest test_helloworld.py test_integration.py test_qualification.py `
  --junitxml=test-results/local-junit.xml `
  --html=test-results/local-test-report.html `
  --self-contained-html
```

Coverage:

```powershell
.\venv\Scripts\coverage.exe run --source=. -m pytest test_helloworld.py test_integration.py test_qualification.py
.\venv\Scripts\coverage.exe report
.\venv\Scripts\coverage.exe html -d test-results/coverage
```

## How to Talk About This Project in an Interview

Use this structure:

1. Start with the purpose: "I built a small automotive CI/CD QA project to map unit, integration, and qualification testing into a Jenkins pipeline."
2. Explain SWE4: "Unit tests validate vehicle controller behavior such as engine start, speed limits, diagnostics, and fault handling."
3. Explain SWE5: "Integration tests validate interaction between the vehicle controller and transmission subsystem."
4. Explain SWE6: "Qualification tests simulate end-to-end scenarios and acceptance criteria, similar to HIL-level requirement validation."
5. Explain CI/CD value: "Jenkins runs tests automatically, creates reports, enforces coverage, archives evidence, and packages an artifact."
6. Connect to HIL: "Before using expensive HIL benches, CI can pre-screen builds using unit, SIL, and integration tests. HIL can then focus on ECU I/O, timing, diagnostics, power modes, and real bus behavior."

## HIL Extension Ideas

This project is simulated, but you can explain how you would extend it for real HIL:

- Add CAN signal input/output checks using a Python CAN library or vendor APIs.
- Add diagnostic tests for DTC setting, clearing, aging, and UDS services.
- Add power mode scenarios for sleep, wakeup, ignition on, crank, and shutdown.
- Add calibration/configuration variants.
- Add bench reservation and resource locking in Jenkins.
- Add hardware smoke tests after software package creation.
- Add nightly long-duration regression tests.
- Publish requirement IDs and traceability links in reports.

## Interview Guide

Read the detailed tutorial and question bank here:

- `docs/SWE4_SWE5_SWE6_CICD_INTERVIEW_GUIDE.md`

That guide includes:

- SWE4/SWE5/SWE6 explanations
- CI/CD pros for each level
- HIL interview talking points
- Jenkins questions and answers
- Scenario-based QA questions
- STAR-style answers based on this repository

## Current Project Status

- Unit, integration, and qualification tests are available.
- Jenkins publishes JUnit XML, HTML test reports, coverage reports, and deployment artifacts.
- The project is intentionally small so you can explain every part in an interview.
- The best next improvement is adding requirement IDs to test names and reports for stronger automotive traceability.
