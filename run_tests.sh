#!/bin/bash
# Quick Start Script for Running Tests Locally
#
# This script demonstrates how to run the test suite and CI/CD checks
# locally before pushing to GitHub
#
# Usage: bash run_tests.sh

echo "=========================================="
echo "  Automotive Software Testing - Local Run"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python installation
echo -e "${BLUE}[1/6] Checking Python installation...${NC}"
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9+"
    exit 1
fi
python3 --version
echo -e "${GREEN}✓ Python installation verified${NC}"
echo ""

# Create virtual environment
echo -e "${BLUE}[2/6] Setting up virtual environment...${NC}"
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${GREEN}✓ Virtual environment already exists${NC}"
fi
echo ""

# Activate virtual environment
echo -e "${BLUE}[3/6] Activating virtual environment...${NC}"
source venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"
echo ""

# Install dependencies
echo -e "${BLUE}[4/6] Installing dependencies...${NC}"
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt > /dev/null 2>&1
echo -e "${GREEN}✓ Dependencies installed${NC}"
echo ""

# Run unit tests
echo -e "${BLUE}[5/6] Running unit tests...${NC}"
echo "========== UNIT TESTS =========="
python3 test_helloworld.py

TEST_EXIT_CODE=$?
echo ""

# Generate coverage report
echo -e "${BLUE}[6/6] Generating coverage report...${NC}"
coverage run --source=. -m pytest test_helloworld.py 2>/dev/null || true
coverage report
coverage html -d coverage_report 2>/dev/null || true
echo -e "${GREEN}✓ Coverage report: coverage_report/index.html${NC}"
echo ""

# Summary
echo "=========================================="
echo -e "${YELLOW}  Test Results Summary${NC}"
echo "=========================================="
if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✓ All tests PASSED!${NC}"
    echo ""
    echo "Next steps:"
    echo "  1. Review coverage report: open coverage_report/index.html"
    echo "  2. Check test results above"
    echo "  3. Push changes to GitHub to run CI/CD pipeline"
    echo ""
    echo "To view coverage in browser:"
    echo "  - macOS/Linux: open coverage_report/index.html"
    echo "  - Windows: start coverage_report/index.html"
else
    echo -e "${YELLOW}⚠ Some tests failed - see details above${NC}"
fi
echo ""
echo "For more information, see README.md"
