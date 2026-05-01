# Automotive Software Testing - CI/CD Practice Project

> A comprehensive practice project for learning **CI/CD automation, unit testing, and quality engineering** in automotive software development, aligned with professional testing standards (JUnit, Jenkins, GitHub Actions).

## 🎯 Project Overview

This project demonstrates **professional software testing practices** for automotive systems. It serves as a **hands-on learning platform** for:

- ✅ **Unit Testing** - JUnit-style test frameworks (Python unittest)
- ✅ **Helper Functions & Test Wrappers** - Modular test design patterns
- ✅ **CI/CD Pipelines** - Jenkins and GitHub Actions configuration
- ✅ **Test Automation** - Automated test execution and reporting
- ✅ **Quality Metrics** - Code coverage and test analysis
- ✅ **Integration Testing** - Component interaction verification
- ✅ **Diagnostics & Fault Handling** - System health monitoring

## 📋 Project Structure

```
test/
├── helloworld.py              # Main automotive control module
├── test_helloworld.py         # Unit and integration tests (JUnit-style)
├── test_helpers.py            # Test helper functions and wrappers
├── Jenkinsfile                # Jenkins CI/CD pipeline configuration
├── .github/
│   └── workflows/
│       └── ci.yml             # GitHub Actions workflow
└── README.md                  # This file
```

## 📚 Key Responsibilities Covered

This project aligns with professional testing role requirements:

### 1. **Test Script & Helper Function Design**
> "Lead in how test scripts & Helper/Wrappers functions are designed to verify key functional behaviors"

**Implemented in:**
- `test_helloworld.py` - Well-organized test classes with clear responsibilities
- `test_helpers.py` - TestHelper class with setup/teardown, assertions, and result analysis
- Comments explain design decisions for each test method

### 2. **Unit Testing with JUnit Framework**
> "Strong knowledge of Unit test frameworks like JUnit, Unit, etc."

**Implemented in:**
- `test_helloworld.py` - Uses Python's `unittest` framework (JUnit-style)
- Test classes: `TestVehicleEngineControl`, `TestVehicleSpeedControl`, etc.
- Features:
  - setUp/tearDown fixtures (test isolation)
  - Assertion methods (assertEqual, assertTrue, assertFalse, etc.)
  - Clear test naming (test_* convention)
  - Result reporting

### 3. **Test Behavior Efficiency**
> "Establish Key Test Behaviors and drive efficiency in the work product"

**Implemented in:**
- Helper functions reduce code duplication
- Parameterized test scenarios (`setup_automotive_test_scenario`)
- Performance metrics in test execution
- Test result summary and analysis

### 4. **Problem-Solving in Testing Infrastructure**
> "Identify structural challenges with scripts, helpers, benches, etc. and co-develop solutions"

**Demonstrated by:**
- Clear separation of concerns (main code, tests, helpers)
- Extensible test framework for adding new tests
- Reusable helper functions for common operations
- Error handling patterns

### 5. **CI/CD Pipeline Knowledge**
> "Strong knowledge of CICD process pipelines like GitHub Actions and Jenkins"

**Implemented in:**
- `Jenkinsfile` - Full Jenkins pipeline with stages
- `.github/workflows/ci.yml` - GitHub Actions workflow
- Features:
  - Automated testing on every push
  - Test result reporting
  - Code coverage measurement
  - Quality checks
  - Artifact preservation

### 6. **Test Results Analysis & Reporting**
> "Manage department-wide report-outs such as script readiness timing, test execution results"

**Implemented in:**
- `test_helpers.py` - Result tracking and summary generation
- `analyze_test_results()` - Result interpretation
- Jenkins/GitHub Actions - Automated test reporting
- Comments explain metrics collection

### 7. **Automotive Knowledge**
> "Knowledge and familiarity with ... Diagnostics, HWIO, Power Management"

**Simulated in:**
- `VehicleController` - Represents automotive control system
- Methods for diagnostics, fault detection, speed control
- Safety features (fault code checking, speed limits)
- Real-world vehicle testing scenarios

### 8. **Quality Metrics & Continuous Improvement**
> "Define metrics for simulation quality and identify enablers for improved quality"

**Implemented in:**
- Code coverage measurement (80% target)
- Test execution timing
- Pass/fail rate tracking
- Performance benchmarking

## 🚀 Getting Started

### Prerequisites
```bash
python3 --version  # Python 3.9+
pip --version      # pip package manager
```

### Installation

```bash
# Clone the repository
git clone https://github.com/Ron-Mat/test.git
cd test

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install pytest pytest-cov coverage
```

### Running Tests Locally

```bash
# Run all tests with verbose output
python3 test_helloworld.py

# Or use pytest for more detailed reporting
pytest test_helloworld.py -v

# Generate coverage report
coverage run --source=. -m pytest test_helloworld.py
coverage report
coverage html  # Creates HTML report in htmlcov/
```

## 🧪 Test Categories

### Unit Tests
Individual function testing to verify specific behaviors:

```python
# Example: TestVehicleEngineControl
- test_engine_starts_successfully()
- test_engine_cannot_start_with_faults()
- test_fault_code_management()
```

### Integration Tests
Multiple components working together:

```python
# Example: TestIntegrationScenarios
- test_normal_driving_scenario()      # Normal operation
- test_fault_detection_scenario()     # Fault handling
```

### Performance Tests
Verify system meets timing and efficiency requirements:

```python
# Example: TestPerformanceAndMetrics
- test_test_execution_efficiency()
- test_result_analysis()
```

## 🔄 CI/CD Pipeline

### Jenkins Pipeline Stages
1. **Checkout** - Pull latest code
2. **Setup Environment** - Install dependencies
3. **Unit Tests** - Run JUnit tests
4. **Code Coverage** - Measure coverage %
5. **Code Quality** - Style and lint checks
6. **Test Reporting** - Generate reports
7. **Build Artifact** - Prepare for deployment

### GitHub Actions Workflow
1. **Build & Test** - Run all tests
2. **Quality Checks** - Security scanning
3. **Documentation** - Verify docs
4. **Status Check** - Overall workflow status

### Trigger Conditions
- Push to main branch
- Pull requests
- Manual workflow dispatch
- Nightly scheduled runs (2 AM UTC)

## 📊 Code Coverage

View coverage report after running:
```bash
coverage html
open htmlcov/index.html  # macOS
# or
start htmlcov\index.html  # Windows
```

**Target:** 80% code coverage
**Current:** Check with `coverage report`

## 🏗️ Architecture Notes

### VehicleController Class
Represents automotive control system with:
- Engine control (start/stop)
- Speed management (acceleration with limits)
- Diagnostic checking (system health)
- Fault code management (error tracking)

### TestHelper Class
Provides testing utilities:
- Test setup/teardown
- Assertion methods (assertEquals, assertTrue, etc.)
- Result tracking and summary
- Performance measurement

### Test Scenarios
Predefined test cases for:
- **Normal**: Standard operation
- **Fault**: System with active faults
- **Edge Case**: Boundary conditions

## 📖 Comments & Documentation

Each file includes extensive comments explaining:
- What the code does
- Why it's structured this way
- How it relates to job responsibilities
- Best practices being demonstrated

**Key sections marked with:**
```python
# Key Responsibility: "[from job description]"
# Demonstrates: [what this teaches]
```

## ✨ Best Practices Demonstrated

### Code Quality
- Clear variable and function names
- Comprehensive docstrings
- Comments for complex logic
- DRY (Don't Repeat Yourself) principle

### Testing
- Test isolation (setUp/tearDown)
- Single responsibility per test
- Descriptive test names
- Comprehensive assertions

### CI/CD
- Automated testing
- Clear pipeline stages
- Test result reporting
- Artifact preservation

### Documentation
- Inline code comments
- README with examples
- Docstrings in code
- Pipeline documentation

## 🎓 Learning Paths

### Path 1: Unit Testing
1. Study `test_helloworld.py`
2. Add new test methods to `TestVehicleEngineControl`
3. Run locally: `python3 test_helloworld.py`
4. View results

### Path 2: Test Automation
1. Review `test_helpers.py`
2. Create new helper functions
3. Use in new test cases
4. Measure efficiency improvements

### Path 3: CI/CD Integration
1. Review `Jenkinsfile`
2. Review `.github/workflows/ci.yml`
3. Set up Jenkins locally (optional)
4. Push changes and watch pipeline run

### Path 4: Quality Metrics
1. Run coverage: `coverage run ... pytest ...`
2. View report: `coverage html`
3. Identify gaps
4. Write tests to improve coverage

## 🔧 Extending the Project

### Adding New Tests
```python
class TestNewFeature(unittest.TestCase):
    def setUp(self):
        self.vehicle = VehicleController("TEST_NEW")
    
    def test_new_behavior(self):
        # Test implementation
        pass
```

### Adding New Helper Functions
```python
def helper_function_name(param1, param2):
    """Description of what this helper does."""
    # Implementation
    return result
```

### Modifying Pipeline
- **Jenkins**: Edit `Jenkinsfile` stages
- **GitHub Actions**: Edit `.github/workflows/ci.yml` jobs

## 📝 Test Report Example

```
========== RUNNING UNIT TESTS ==========
Tests include:
  ✓ Engine Control Tests
  ✓ Speed Control Tests
  ✓ Diagnostics Tests
  ✓ Integration Scenarios
  ✓ Performance Metrics

Total Tests: 25
Passed: 25
Failed: 0
Pass Rate: 100.00%
Execution Time: 0.152s
```

## 🌐 Resources

### Documentation
- [Python unittest documentation](https://docs.python.org/3/library/unittest.html)
- [Jenkins Pipeline documentation](https://www.jenkins.io/doc/book/pipeline/)
- [GitHub Actions documentation](https://docs.github.com/en/actions)

### Related Technologies
- **Python Testing:** pytest, coverage, unittest
- **Automotive Testing:** HIL (Hardware-in-Loop), SIL (Software-in-Loop)
- **CI/CD Tools:** Jenkins, GitHub Actions, GitLab CI

## 💡 Tips for Practice

1. **Start Simple:** Run tests locally first
2. **Study the Code:** Read comments explaining job responsibilities
3. **Modify Tests:** Add new test cases to explore
4. **Use CI/CD:** Push changes and watch pipeline execute
5. **Review Results:** Check coverage reports and test outputs
6. **Iterate:** Make improvements to testing approach

## 🎯 Professional Alignment

This project teaches skills required for automotive software quality engineering:

| Responsibility | Covered In | Practice Exercise |
|---|---|---|
| Unit test frameworks | test_helloworld.py | Add 5 new test cases |
| Test helpers & wrappers | test_helpers.py | Create custom helper function |
| CI/CD pipelines | Jenkinsfile, ci.yml | Push commit and observe pipeline |
| Test result analysis | test_helpers.py | Modify get_test_summary() |
| Code coverage | .github/workflows/ci.yml | Achieve 85% coverage |
| Integration testing | TestIntegrationScenarios | Add new scenario |
| Fault handling | test_helloworld.py | Add fault tolerance test |
| Performance metrics | TestPerformanceAndMetrics | Create custom metric |

## 📞 Support

For questions or improvements:
1. Review code comments
2. Check docstrings
3. Study example tests
4. Refer to documentation links

## 📄 License

This is a practice/learning project.

---

**Last Updated:** April 2026
**Version:** 1.0
**Status:** Ready for Practice ✅
