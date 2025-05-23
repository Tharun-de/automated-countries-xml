# 🤖 GitHub Actions Automation Guide

## Overview

This document explains how the automated XML generation works using GitHub Actions. The system automatically fetches country data from REST Countries API and updates XML files without manual intervention.

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   GitHub Actions│───▶│   Python Script  │───▶│  Updated Repo   │
│   (Scheduled)   │    │   - Fetch API    │    │   - XML Files   │
│   Daily at 6 AM │    │   - Generate XML │    │   - Auto Commit │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 📅 When It Runs

### Automatic Schedule
- **Daily at 6:00 AM UTC**
- Checks for updated country data
- Only commits changes if data actually changed

### Manual Trigger
- Go to **Actions** tab in GitHub
- Click **"🌍 Auto-Update Countries XML"**
- Click **"Run workflow"**
- Optionally specify countries or force update

## 🔧 Workflow Steps

### 1. **Environment Setup**
```yaml
- Checkout repository
- Set up Python 3.11
- Install dependencies from requirements.txt
```

### 2. **API Testing**
```yaml
- Test REST Countries API connectivity
- Verify API response format
- Continue even if minor issues occur
```

### 3. **XML Generation**
```yaml
- Parse country list (from input or default)
- Fetch latest data from REST Countries API
- Generate formatted XML using our generator
- Validate XML structure and content
```

### 4. **Change Detection**
```yaml
- Compare new XML with existing file
- Count number of countries processed
- Determine if commit is needed
```

### 5. **Commit & Push**
```yaml
- Create detailed commit message with statistics
- Add generated files to git
- Commit with metadata (timestamp, country count, etc.)
- Push changes to repository
```

### 6. **Reporting**
```yaml
- Create workflow summary with results
- Log any errors or warnings
- Provide links to generated files
```

## ⚙️ Configuration

### Default Countries
The workflow uses these countries by default:
- India, Japan, Germany, France, Brazil
- United States, China, Russia, Canada, Australia

### Customization Options

#### 1. **Via Manual Trigger**
```
Countries: "india,japan,france,spain"
Force Update: true/false
```

#### 2. **Via Configuration File**
Edit `config/countries.json`:
```json
{
  "countries": [
    "your",
    "preferred",
    "countries"
  ]
}
```

#### 3. **Via Workflow File**
Edit `.github/workflows/update-countries.yml`:
```yaml
COUNTRIES="${{ github.event.inputs.countries || 'your,default,list' }}"
```

## 📊 Understanding the Output

### Workflow Summary
Each run creates a summary showing:
- ✅/❌ Success status
- 📊 Number of countries processed
- 🔗 Links to generated files
- ⏰ Execution time and details

### Commit Messages
Auto-generated commits include:
```
🌍 Auto-update countries XML data

📅 Updated: 2024-01-15 06:00 UTC
📊 Countries: 10
🤖 Automated via GitHub Actions

Changes:
- Fetched latest data from REST Countries API
- Updated XML with current country and currency information
- Validated XML structure and content
```

## 🚨 Error Handling

### Common Issues & Solutions

#### 1. **API Connectivity Issues**
```
Error: API connectivity test failed
Solution: Usually temporary, will retry next scheduled run
```

#### 2. **Invalid Country Names**
```
Warning: 2 countries could not be processed
Solution: Check country names in configuration
```

#### 3. **XML Generation Errors**
```
Error: XML file was not created
Solution: Check Python dependencies and script errors
```

#### 4. **Permission Issues**
```
Error: Permission denied
Solution: Ensure repository has proper write permissions
```

## 🔍 Monitoring & Debugging

### View Workflow Logs
1. Go to **Actions** tab
2. Click on latest workflow run
3. Expand each step to see detailed logs

### Check Generated Files
1. Look in `output/` directory
2. Verify XML structure and content
3. Check file timestamps

### Monitor API Status
- REST Countries API: https://restcountries.com/
- Check API documentation for any changes

## 🛠️ Customization Examples

### Example 1: European Countries Only
```yaml
# In workflow file
COUNTRIES="germany,france,italy,spain,netherlands,poland"
```

### Example 2: G20 Countries
```json
// In config/countries.json
{
  "countries": [
    "argentina", "australia", "brazil", "canada", "china",
    "france", "germany", "india", "indonesia", "italy",
    "japan", "mexico", "russia", "saudi arabia", "south africa",
    "south korea", "turkey", "united kingdom", "united states"
  ]
}
```

### Example 3: Custom Schedule
```yaml
# Every 12 hours instead of daily
schedule:
  - cron: '0 6,18 * * *'
```

## 📈 Best Practices

### 1. **Repository Maintenance**
- Keep dependencies updated
- Monitor workflow success rate
- Review generated XML periodically

### 2. **Configuration Management**
- Use configuration files for large country lists
- Document any custom changes
- Test configuration changes manually first

### 3. **Error Monitoring**
- Set up email notifications for failures
- Check logs if XML seems outdated
- Verify API status during issues

## 🎯 Advanced Features

### Conditional Updates
The workflow only commits changes when:
- New countries are added/removed from API
- Country names or currencies change
- Manual force update is triggered

### Metadata Tracking
Each commit includes:
- Timestamp of update
- Number of countries processed
- API source information
- Workflow run ID for traceability

### Parallel Processing
Future enhancements could include:
- Batch API requests for better performance
- Parallel XML generation for large country lists
- Caching mechanisms for unchanged data

## 🔗 Related Files

- **Workflow**: `.github/workflows/update-countries.yml`
- **Generator**: `src/automated_generator.py`
- **Config**: `config/countries.json`
- **Output**: `output/countries.xml`
- **Dependencies**: `requirements.txt`

## 💡 Tips for Learning

1. **Start with manual triggers** to understand the process
2. **Check workflow logs** to see each step in detail
3. **Modify country lists** to see how changes are detected
4. **Review commit history** to understand the automation pattern
5. **Experiment with different configurations** safely 