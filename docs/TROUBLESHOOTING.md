# 🔧 Troubleshooting Guide

## Overview

This guide provides solutions to common issues encountered while using the Countries XML Auto-Generator, covering API problems, XML generation issues, GitHub Actions failures, and system configuration problems.

## 🚨 Common Issues & Solutions

### **1. API Connection Issues**

#### **❌ Problem: API Connectivity Failed**
```
❌ API connectivity test failed: HTTPSConnectionPool(host='restcountries.com', port=443)
```

**🔍 Diagnosis:**
- Network connectivity issues
- Firewall blocking outbound connections
- DNS resolution problems
- API service downtime

**✅ Solutions:**

1. **Test Basic Connectivity:**
```bash
# Test DNS resolution
nslookup restcountries.com

# Test basic HTTP connection
curl -I "https://restcountries.com/v3.1/name/india"

# Test with Python requests
python -c "import requests; print(requests.get('https://restcountries.com/v3.1/name/india').status_code)"
```

2. **Configure Proxy (if behind corporate firewall):**
```python
import os
import requests

# Set proxy environment variables
os.environ['HTTP_PROXY'] = 'http://proxy.company.com:8080'
os.environ['HTTPS_PROXY'] = 'https://proxy.company.com:8080'

# Or configure in session
session = requests.Session()
session.proxies = {
    'http': 'http://proxy.company.com:8080',
    'https': 'https://proxy.company.com:8080'
}
```

3. **Check API Status:**
- Visit https://restcountries.com/ to verify service status
- Check for maintenance announcements
- Try alternative endpoints

---

#### **❌ Problem: Country Not Found (404)**
```
⚠️ Country not found: xyz-country
```

**🔍 Diagnosis:**
- Typo in country name
- Country name not recognized by API
- Using incorrect language/format

**✅ Solutions:**

1. **Use Correct Country Names:**
```python
# ✅ Correct formats
valid_names = [
    "india",           # English common name
    "united states",   # Full name with spaces
    "uk",             # Common abbreviation
    "south korea"     # Full descriptive name
]

# ❌ Incorrect formats
invalid_names = [
    "hindustan",      # Historical/alternative name
    "america",        # Ambiguous
    "england",        # Part of UK, not a country
    "south-korea"     # Hyphenated format not supported
]
```

2. **Check Available Country Names:**
```bash
# Get all countries to see available names
curl "https://restcountries.com/v3.1/all?fields=name"
```

3. **Use Alternative Name Formats:**
```python
def try_multiple_names(country_input):
    """Try different name variations"""
    
    variations = [
        country_input.lower(),
        country_input.lower().replace("-", " "),
        country_input.lower().replace("_", " "),
        country_input.title()
    ]
    
    for variation in variations:
        try:
            response = requests.get(f"https://restcountries.com/v3.1/name/{variation}")
            if response.status_code == 200:
                return response.json()
        except:
            continue
    
    return None
```

---

### **2. XML Generation Issues**

#### **❌ Problem: Path Handling Error**
```
❌ Error during XML generation: [WinError 3] The system cannot find the path specified: ''
```

**🔍 Diagnosis:**
- Empty output directory path
- Missing directory creation
- Invalid file path characters

**✅ Solutions:**

1. **Fixed Path Handling Code:**
```python
def safe_file_creation(output_file: str):
    """Safely create file with directory handling"""
    
    # Handle relative vs absolute paths
    if not os.path.isabs(output_file):
        output_file = os.path.abspath(output_file)
    
    # Create directory if it doesn't exist
    output_dir = os.path.dirname(output_file)
    if output_dir:  # Only create if directory path exists
        os.makedirs(output_dir, exist_ok=True)
    
    return output_file
```

2. **Test File Creation:**
```bash
# Test with simple filename
python src/automated_generator.py --countries "india" --output "test.xml"

# Test with full path
python src/automated_generator.py --countries "india" --output "output/test.xml"
```

---

#### **❌ Problem: Unicode Characters Not Displaying**
```
<?xml version="1.0" encoding="UTF-8"?>
<LocalName>???????</LocalName>
```

**🔍 Diagnosis:**
- Incorrect encoding settings
- Terminal/console encoding issues
- Font rendering problems

**✅ Solutions:**

1. **Verify UTF-8 Encoding:**
```python
def write_xml_with_utf8(content: str, output_file: str):
    """Write XML with proper UTF-8 encoding"""
    
    with open(output_file, 'w', encoding='utf-8', newline='\n') as f:
        f.write(content)
    
    # Verify encoding
    with open(output_file, 'r', encoding='utf-8') as f:
        read_content = f.read()
        print(f"Unicode test: {'✅' if 'भारत' in read_content else '❌'}")
```

2. **Set Console Encoding (Windows):**
```cmd
# Set UTF-8 code page
chcp 65001

# Or use PowerShell
[Console]::OutputEncoding = [Text.UTF8Encoding]::UTF8
```

3. **Test Unicode Support:**
```python
def test_unicode_support():
    """Test Unicode character handling"""
    
    test_chars = {
        'hindi': 'भारत गणराज्य',
        'japanese': '日本',
        'currency_symbols': '₹¥€£'
    }
    
    for name, chars in test_chars.items():
        try:
            encoded = chars.encode('utf-8')
            decoded = encoded.decode('utf-8')
            print(f"✅ {name}: {chars} (OK)")
        except Exception as e:
            print(f"❌ {name}: Error - {e}")
```

---

### **3. GitHub Actions Issues**

#### **❌ Problem: Workflow Not Triggering**
```
No workflow runs found
```

**🔍 Diagnosis:**
- Workflow file syntax errors
- Incorrect file location
- GitHub Actions not enabled

**✅ Solutions:**

1. **Verify Workflow File Location:**
```
# Correct location
.github/workflows/update-countries.yml

# ❌ Common mistakes
.github/workflow/update-countries.yml    # Missing 's'
github/workflows/update-countries.yml    # Missing '.'
.github/workflows/update-countries.yaml  # Wrong extension
```

2. **Validate YAML Syntax:**
```bash
# Install YAML validator
pip install pyyaml

# Validate syntax
python -c "import yaml; yaml.safe_load(open('.github/workflows/update-countries.yml'))"
```

3. **Enable GitHub Actions:**
- Go to repository **Settings** → **Actions** → **General**
- Set **Actions permissions** to "Allow all actions and reusable workflows"
- Save settings

---

#### **❌ Problem: Permission Denied in GitHub Actions**
```
error: failed to push some refs to 'https://github.com/user/repo.git'
fatal: Authentication failed
```

**🔍 Diagnosis:**
- GITHUB_TOKEN permissions insufficient
- Repository settings blocking Actions

**✅ Solutions:**

1. **Update Workflow Permissions:**
```yaml
name: Update Countries XML

on:
  schedule:
    - cron: '0 6 * * *'
  workflow_dispatch:

permissions:
  contents: write    # Allow pushing commits
  actions: read      # Allow reading workflow info

jobs:
  update-xml:
    runs-on: ubuntu-latest
    steps:
      # ... rest of workflow
```

2. **Check Repository Settings:**
- Go to **Settings** → **Actions** → **General**
- Under **Workflow permissions**:
  - Select "Read and write permissions"
  - Check "Allow GitHub Actions to create and approve pull requests"

---

#### **❌ Problem: Python Dependencies Not Installing**
```
ERROR: Could not find a version that satisfies the requirement requests
```

**🔍 Diagnosis:**
- Missing requirements.txt
- Incorrect Python version
- Package name typos

**✅ Solutions:**

1. **Verify requirements.txt:**
```txt
requests>=2.25.0
lxml>=4.6.0
```

2. **Update Workflow Python Setup:**
```yaml
- name: Set up Python
  uses: actions/setup-python@v4
  with:
    python-version: '3.9'

- name: Install dependencies
  run: |
    python -m pip install --upgrade pip
    pip install -r requirements.txt
```

---

### **4. Configuration Issues**

#### **❌ Problem: Config File Not Found**
```
Error loading config file: [Errno 2] No such file or directory: 'config/countries.json'
```

**🔍 Diagnosis:**
- File path incorrect
- File not committed to repository
- Working directory issues

**✅ Solutions:**

1. **Verify File Existence:**
```bash
# Check if file exists
ls -la config/countries.json

# Check current working directory
pwd

# List all files in config directory
ls -la config/
```

2. **Create Default Config:**
```python
def create_default_config(config_path: str):
    """Create default configuration file"""
    
    default_config = {
        "countries": [
            "india",
            "japan",
            "germany",
            "france",
            "brazil"
        ],
        "output": {
            "directory": "output",
            "filename": "countries.xml"
        },
        "api": {
            "timeout": 10,
            "max_retries": 3
        }
    }
    
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(default_config, f, indent=2)
    
    print(f"✅ Created default config: {config_path}")
```

---

### **5. Performance Issues**

#### **❌ Problem: Slow API Responses**
```
⏰ Timeout for: some-country
🔌 Connection error for: another-country
```

**🔍 Diagnosis:**
- Network latency
- API rate limiting
- Large country lists

**✅ Solutions:**

1. **Implement Retry Logic:**
```python
import time
from functools import wraps

def retry_on_failure(max_retries=3, delay=1):
    """Decorator for retrying failed API calls"""
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise e
                    
                    wait_time = delay * (2 ** attempt)  # Exponential backoff
                    print(f"⏳ Retry {attempt + 1}/{max_retries} in {wait_time}s...")
                    time.sleep(wait_time)
            
        return wrapper
    return decorator

@retry_on_failure(max_retries=3, delay=2)
def fetch_country_data(country_name: str):
    # Your API call here
    pass
```

2. **Implement Caching:**
```python
import pickle
from datetime import datetime, timedelta

class APICache:
    def __init__(self, cache_duration_hours=24):
        self.cache_file = "cache/api_cache.pkl"
        self.cache_duration = timedelta(hours=cache_duration_hours)
        self.cache = self.load_cache()
    
    def get(self, key: str):
        """Get cached data if still valid"""
        
        if key in self.cache:
            item = self.cache[key]
            if datetime.now() - item['timestamp'] < self.cache_duration:
                return item['data']
        
        return None
    
    def set(self, key: str, data):
        """Cache data with timestamp"""
        
        self.cache[key] = {
            'data': data,
            'timestamp': datetime.now()
        }
        self.save_cache()
```

---

### **6. Development Environment Issues**

#### **❌ Problem: Import Errors**
```
ModuleNotFoundError: No module named 'requests'
```

**✅ Solutions:**

1. **Set Up Virtual Environment:**
```bash
# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (Mac/Linux)
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

2. **Verify Python Path:**
```python
import sys
print("Python executable:", sys.executable)
print("Python path:", sys.path)
```

---

#### **❌ Problem: Git Issues**
```
fatal: not a git repository
```

**✅ Solutions:**

1. **Initialize Git Repository:**
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/username/repo.git
git push -u origin main
```

2. **Fix Remote URL:**
```bash
# Check current remote
git remote -v

# Update remote URL
git remote set-url origin https://github.com/username/repo.git
```

---

## 🔍 Debugging Tools

### **1. API Testing Script**
```python
def debug_api_connection():
    """Comprehensive API debugging"""
    
    print("🔍 API Debug Information")
    print("=" * 50)
    
    # Test basic connectivity
    try:
        response = requests.get("https://restcountries.com/v3.1/name/india", timeout=10)
        print(f"✅ API Status: {response.status_code}")
        print(f"✅ Response Time: {response.elapsed.total_seconds():.2f}s")
        
        data = response.json()
        print(f"✅ Data Received: {len(data)} items")
        
    except Exception as e:
        print(f"❌ API Error: {e}")
    
    # Test DNS resolution
    try:
        import socket
        ip = socket.gethostbyname("restcountries.com")
        print(f"✅ DNS Resolution: {ip}")
    except Exception as e:
        print(f"❌ DNS Error: {e}")
    
    # Test SSL/TLS
    try:
        import ssl
        context = ssl.create_default_context()
        with socket.create_connection(("restcountries.com", 443), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname="restcountries.com") as ssock:
                print(f"✅ SSL/TLS: {ssock.version()}")
    except Exception as e:
        print(f"❌ SSL Error: {e}")

if __name__ == "__main__":
    debug_api_connection()
```

### **2. XML Validation Script**
```python
def debug_xml_generation(xml_file: str):
    """Debug XML generation issues"""
    
    print(f"🔍 XML Debug: {xml_file}")
    print("=" * 50)
    
    # Check file existence
    if not os.path.exists(xml_file):
        print(f"❌ File not found: {xml_file}")
        return
    
    # Check file size
    file_size = os.path.getsize(xml_file)
    print(f"📄 File Size: {file_size} bytes")
    
    # Check encoding
    try:
        with open(xml_file, 'r', encoding='utf-8') as f:
            content = f.read()
        print("✅ UTF-8 Encoding: OK")
    except UnicodeDecodeError as e:
        print(f"❌ Encoding Error: {e}")
        return
    
    # Check XML well-formedness
    try:
        import xml.etree.ElementTree as ET
        tree = ET.parse(xml_file)
        print("✅ Well-formed XML: OK")
        
        root = tree.getroot()
        countries = root.findall(".//Countries")
        print(f"📊 Countries Found: {len(countries)}")
        
    except ET.ParseError as e:
        print(f"❌ XML Parse Error: {e}")
    
    # Check Unicode characters
    unicode_chars = ['₹', '¥', 'भारत', '日本']
    found_unicode = [char for char in unicode_chars if char in content]
    
    if found_unicode:
        print(f"✅ Unicode Characters: {', '.join(found_unicode)}")
    else:
        print("⚠️ No Unicode characters found")

if __name__ == "__main__":
    debug_xml_generation("output/countries.xml")
```

### **3. System Information Script**
```python
def system_debug_info():
    """Collect system debug information"""
    
    import platform
    import sys
    
    print("🖥️ System Information")
    print("=" * 50)
    print(f"Platform: {platform.platform()}")
    print(f"Python Version: {sys.version}")
    print(f"Python Executable: {sys.executable}")
    print(f"Working Directory: {os.getcwd()}")
    
    # Check installed packages
    try:
        import pkg_resources
        installed_packages = [d for d in pkg_resources.working_set]
        print(f"Installed Packages: {len(installed_packages)}")
        
        # Check specific packages
        required_packages = ['requests', 'lxml']
        for package in required_packages:
            try:
                version = pkg_resources.get_distribution(package).version
                print(f"✅ {package}: {version}")
            except pkg_resources.DistributionNotFound:
                print(f"❌ {package}: Not installed")
                
    except ImportError:
        print("⚠️ pkg_resources not available")
    
    # Check network connectivity
    try:
        import urllib.request
        urllib.request.urlopen('https://google.com', timeout=5)
        print("✅ Internet Connection: OK")
    except:
        print("❌ Internet Connection: Failed")

if __name__ == "__main__":
    system_debug_info()
```

---

## 📞 Getting Help

### **GitHub Issues**
If you encounter issues not covered in this guide:

1. **Search existing issues**: Check if someone else has reported the same problem
2. **Create detailed bug report**: Include error messages, system info, and steps to reproduce
3. **Provide context**: Mention your operating system, Python version, and configuration

### **Self-Help Checklist**
Before seeking help, try these steps:

- [ ] Check API connectivity with `curl` or browser
- [ ] Verify all files are in correct locations  
- [ ] Validate JSON configuration files
- [ ] Test with minimal country list (e.g., just "india")
- [ ] Check Python virtual environment activation
- [ ] Verify GitHub Actions permissions
- [ ] Review workflow logs for specific error messages

### **Useful Commands for Debugging**
```bash
# Test API manually
curl "https://restcountries.com/v3.1/name/india"

# Validate JSON config
python -m json.tool config/countries.json

# Test XML generation
python src/automated_generator.py --countries "india" --output "debug.xml"

# Check Python installation
python --version
pip list

# Validate YAML workflow
python -c "import yaml; yaml.safe_load(open('.github/workflows/update-countries.yml'))"
```

---

## 📚 Related Documentation

- **[System Architecture](ARCHITECTURE.md)** - Understanding the system design
- **[API Integration](API_INTEGRATION.md)** - API-specific troubleshooting
- **[XML Schema Design](XML_GENERATION.md)** - XML validation and formatting
- **[GitHub Actions Setup](GITHUB_ACTIONS.md)** - Automation configuration and debugging 