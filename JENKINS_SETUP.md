# Jenkins CI/CD Setup Guide - Local Practice

## Overview

This guide explains how to set up Jenkins locally to practice the CI/CD pipeline defined in `Jenkinsfile`.

**Key Concepts You'll Learn:**
- Jenkins pipeline structure and stages
- Automated test execution
- Test result reporting
- Build artifact management
- CI/CD best practices

## Prerequisites

- Jenkins 2.387+ (LTS version recommended)
- Python 3.9+
- Git
- 2GB RAM minimum for Jenkins
- Port 8080 available (or configure different port)

## Installation Options

### Option 1: Docker (Recommended for Quick Setup)

**Advantages:** Isolated environment, easy cleanup, reproducible setup

```bash
# Pull Jenkins Docker image
docker pull jenkins/jenkins:lts

# Run Jenkins container
docker run -d -p 8080:8080 -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  --name jenkins \
  jenkins/jenkins:lts

# Access Jenkins at http://localhost:8080
# Get initial password:
docker logs jenkins | grep "Initial Admin password"
```

### Option 2: Direct Installation (macOS/Linux)

```bash
# Homebrew (macOS)
brew install jenkins-lts
brew services start jenkins-lts

# Ubuntu/Debian
wget -q -O - https://pkg.jenkins.io/debian-stable/jenkins.io.key | sudo apt-key add -
sudo sh -c 'echo deb https://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list'
sudo apt-get update
sudo apt-get install jenkins
sudo systemctl start jenkins
```

### Option 3: Windows Installation

1. Download Jenkins installer from https://www.jenkins.io/download/
2. Run installer (.msi file)
3. Follow installation wizard
4. Jenkins will start automatically at http://localhost:8080

## Initial Jenkins Configuration

### Step 1: Access Jenkins UI
```
Open browser: http://localhost:8080
```

### Step 2: Unlock Jenkins
```
1. Get initial admin password from logs (Docker) or terminal
2. Paste password in Jenkins UI
3. Click "Continue"
```

### Step 3: Install Suggested Plugins
```
1. Click "Install suggested plugins"
2. Wait for installation to complete
3. Create first admin user
```

### Step 4: Install Required Plugins
```
Jenkins Dashboard → Manage Jenkins → Manage Plugins

Search and install:
✓ Pipeline
✓ Git
✓ GitHub
✓ GitHub API
✓ JUnit Plugin
✓ Cobertura Plugin
✓ HTML Publisher Plugin
✓ AnsiColor
```

## Creating a Pipeline Job

### Step 1: Create New Job
```
1. Click "New Item" on Jenkins dashboard
2. Enter job name: "automotive-testing"
3. Select "Pipeline"
4. Click "OK"
```

### Step 2: Configure Pipeline Source
```
In Job Configuration:

Pipeline section:
├─ Definition: Pipeline script from SCM
├─ SCM: Git
├─ Repository URL: https://github.com/Ron-Mat/test.git
├─ Branch: */main
└─ Script Path: Jenkinsfile
```

### Step 3: Configure Build Triggers
```
Build Triggers:
✓ GitHub hook trigger for GITScm polling
✓ Poll SCM (H H * * * - daily check)
✓ Build periodically (H 2 * * * - nightly at 2 AM)
```

### Step 4: Save Configuration
```
Click "Save" button
```

## Running Pipeline

### Manual Trigger
```
1. Click "Build Now" button
2. Monitor build progress in "Build History"
3. Click build number to view console output
```

### Automated Trigger (GitHub Webhook)
```
1. Go to GitHub repository settings
2. Webhooks → Add webhook
3. Payload URL: http://your-jenkins:8080/github-webhook/
4. Events: Push events
5. Click "Add webhook"
6. Push code to trigger pipeline
```

## Monitoring Pipeline Execution

### Build Console Output
```
Jenkins Dashboard → automotive-testing → #[build number]
Click "Console Output" to see full pipeline execution log
```

### Test Results
```
Pipeline execution → Test Result page shows:
- Total tests
- Passed/Failed counts
- Failure details
- Test execution time
```

### Jenkins Graphical Test Trend

Jenkins creates a built-in graph from JUnit XML results when the pipeline calls `junit(...)`.

To view it:

```
1. Run the job at least 2-3 times so Jenkins has history.
2. Open the job page, for example local-automotive-testing.
3. Look for Test Result Trend on the project page.
4. Open a build and click Test Result for package/class/test breakdown.
5. Compare builds to see whether failures, skipped tests, and duration are improving or getting worse.
```

This project publishes three JUnit result files:

```
test-results/junit.xml                  # SWE4 unit tests
test-results/integration-junit.xml      # SWE5 integration tests
test-results/qualification-junit.xml    # SWE6 qualification tests
```

The `scripts/generate_ci_reports.py` script also creates:

```
test-results/test-metrics.csv
```

Use this CSV for optional custom graph practice with Jenkins plugins such as Plot Plugin or dashboard/reporting plugins. The built-in Jenkins graph does not need this CSV; it uses JUnit XML directly.

### Coverage Report
```
Pipeline execution → Coverage Report tab shows:
- Code coverage percentage
- Coverage by file
- Uncovered lines
```

## Troubleshooting

### Issue: "Python: command not found"
```
Solution:
1. Configure Jenkins to use correct Python path
2. Jenkins → Manage Jenkins → Configure System
3. Global properties → Environment variables
4. Add: PYTHON_HOME=/path/to/python
```

### Issue: "Git: command not found"
```
Solution:
1. Install Git on Jenkins system
2. Or configure Jenkins Git plugin path:
   Jenkins → Manage Jenkins → Configure System
   Git installations → Add Git
```

### Issue: Pipeline fails on dependencies
```
Solution:
1. Check virtual environment activation in Jenkinsfile
2. Ensure pip packages install correctly
3. Review console output for specific errors
```

### Issue: Test results not published
```
Solution:
1. Verify test results directory path in Jenkinsfile
2. Check JUnit XML format is correct
3. Ensure junit() step includes correct file paths
```

## Best Practices for Local Testing

### Before Every Commit
```bash
# 1. Run tests locally
bash run_tests.sh  # macOS/Linux
run_tests.bat      # Windows

# 2. Check coverage
coverage report

# 3. Verify all tests pass
# 4. Then commit and push
```

### After Pushing to GitHub
```
1. Watch GitHub Actions pipeline in Actions tab
2. Monitor Jenkins builds if webhook configured
3. Review test results
4. Check coverage reports
5. Verify deployment artifacts
```

## Advanced Configuration

### Parallel Test Execution
```groovy
// In Jenkinsfile, modify Unit Tests stage:
parallel(
    'Engine Tests': {
        // Run TestVehicleEngineControl
    },
    'Speed Tests': {
        // Run TestVehicleSpeedControl
    },
    'Diagnostics Tests': {
        // Run TestVehicleDiagnostics
    }
)
```

### Email Notifications
```
Jenkins → Manage Jenkins → Configure System
Email Notification section:
- SMTP Server: [your email provider]
- Default user e-mail suffix: @example.com

Pipeline → Post-build Actions
- Add: Email Notification
- Recipients: your@email.com
```

### Slack Integration
```
1. Install Slack Plugin
2. Configure Slack credentials
3. In Jenkinsfile, add:
   post {
       always {
           slackSend(color: 'good', message: 'Test Results: ${BUILD_URL}')
       }
   }
```

## Maintenance Tasks

### Regular Updates
```
Jenkins Dashboard → Manage Jenkins → Manage Plugins
Check for plugin updates monthly
Keep Jenkins LTS version current
```

### Log Rotation
```
Job Configuration → Log Rotation:
- Days to keep builds: 30
- Max # of builds: 100
```

### Backup Jenkins Configuration
```bash
# Backup Jenkins home directory
docker cp jenkins:/var/jenkins_home ./jenkins_backup

# Or direct backup if installed locally
cp -r ~/.jenkins ./jenkins_backup
```

## Comparison: Jenkins vs GitHub Actions

| Feature | Jenkins | GitHub Actions |
|---------|---------|-----------------|
| Setup | Self-hosted, more config | Built-in, minimal setup |
| Control | Full control | Less customization |
| Hosting | Your infrastructure | GitHub cloud |
| Cost | Free (infrastructure cost) | Free (generous limits) |
| Learning Curve | Steeper | Easier |
| For Practice | Good for real scenarios | Good for quick setup |

**For this practice project:**
- **Start with:** GitHub Actions (easier to setup)
- **Learn:** Both to understand CI/CD concepts
- **Career:** Jenkins more common in enterprises

## Next Steps

1. **Week 1:** Get Jenkins running, create pipeline job
2. **Week 2:** Run manual builds, monitor test results
3. **Week 3:** Setup GitHub webhook for automation
4. **Week 4:** Add email/Slack notifications
5. **Week 5+:** Experiment with advanced configurations

## Resources

- [Jenkins Documentation](https://www.jenkins.io/doc/)
- [Jenkins Pipeline Examples](https://www.jenkins.io/doc/pipeline/tour/overview/)
- [Jenkinsfile Reference](https://www.jenkins.io/doc/book/pipeline/syntax/)
- [Job DSL Plugin](https://wiki.jenkins.io/display/JENKINS/Job+DSL+Plugin) (Advanced)

## Quick Reference

```bash
# Docker quick commands
docker start jenkins          # Start container
docker stop jenkins           # Stop container
docker logs jenkins           # View logs
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword

# Jenkins CLI (if configured)
jenkins-cli -s http://localhost:8080 build automotive-testing
```

## Support

For questions:
1. Check Jenkins logs for errors
2. Review Jenkinsfile comments for explanation
3. Refer to Jenkins documentation
4. Check GitHub Actions equivalent if stuck

---

**Last Updated:** April 2026
**Difficulty:** Intermediate
**Time to Setup:** 30-60 minutes
