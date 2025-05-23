# 🌍 Countries XML Auto-Generator

**A Proof of Concept for Automated XML Generation from REST APIs**

## 📋 Project Overview

This project demonstrates how to automatically generate XML documents from live API data, specifically creating country and currency XML files that stay up-to-date without manual intervention.

## 🎯 Learning Objectives

- **API Integration**: Fetching data from REST Countries API
- **XML Schema Design**: Creating modular, reusable XSD schemas
- **Data Processing**: Converting JSON to structured XML
- **Automation**: Using GitHub Actions for scheduled updates
- **Documentation**: Creating comprehensive technical documentation

## 🏗️ Architecture

```
REST Countries API → Python Scripts → XML Generation → GitHub Actions → Auto-Updates
```

## 📁 Project Structure

```
CountryXML-AutoGenerator/
├── docs/                    # Documentation and learning materials
├── schemas/                 # XML Schema definitions (XSD)
├── src/                     # Python source code
├── examples/                # Sample data and test files
├── output/                  # Generated XML files
├── .github/workflows/       # GitHub Actions automation
└── tests/                   # Unit tests and validation
```

## 🚀 Quick Start

1. **Clone the repository**
2. **Install dependencies**: `pip install -r requirements.txt`
3. **Run manual test**: `python src/manual_test.py`
4. **Generate XML**: `python src/xml_generator.py`

## 🌐 API Used

**REST Countries API**: `https://restcountries.com/`
- Free, no API key required
- Comprehensive country data
- Real-time updates

## 📚 Documentation

- [Architecture Guide](docs/ARCHITECTURE.md)
- [API Integration](docs/API_INTEGRATION.md)
- [XML Schema Design](docs/XML_GENERATION.md)
- [GitHub Actions Setup](docs/GITHUB_ACTIONS.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)

## 🔄 Automation

The system automatically updates XML files daily using GitHub Actions when country data changes.

## 🧪 Testing

```bash
# Run all tests
python -m pytest tests/

# Test API connection
python examples/test_api.py

# Validate XML output
python examples/validate_xml.py
```

## 📊 Sample Output

The system generates XML files like:

```xml
<Countries>
    <Code>IN</Code>
    <OriginalName>Republic of India</OriginalName>
    <CommonName>India</CommonName>
    <LocalName>भारत गणराज्य</LocalName>
    <OfficialCurrency>
      <Code>INR</Code>
      <Name>Indian Rupee</Name>
      <Symbol>₹</Symbol>
    </OfficialCurrency>
</Countries>
```
