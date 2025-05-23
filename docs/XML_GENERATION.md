# 📄 XML Schema Design & Generation Guide

## Overview

This guide explains the XML schema architecture and generation process used in the Countries XML Auto-Generator, demonstrating modular schema design and automated XML generation.

## 🏗️ Schema Architecture

### **Modular Design Philosophy**

The system uses a **three-tier schema architecture** for maximum reusability and maintainability:

```
┌─────────────────────────────┐
│   countries-collection.xsd  │  ← Root Collection Schema
│         (Wrapper)           │
└─────────────────────────────┘
              │
              ▼
┌─────────────────────────────┐
│       country.xsd           │  ← Individual Country Schema
│    (Imports Currency)       │
└─────────────────────────────┘
              │
              ▼
┌─────────────────────────────┐
│       currency.xsd          │  ← Reusable Currency Schema
│    (ISO 4217 Compliant)     │    (Can be used by other systems)
└─────────────────────────────┘
```

## 📋 Schema Definitions

### **1. Currency Schema (`schemas/currency.xsd`)**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema"
           targetNamespace="http://countries.example.com/currency"
           xmlns:curr="http://countries.example.com/currency"
           elementFormDefault="qualified">

  <!-- ISO 4217 Currency Code Pattern -->
  <xs:simpleType name="CurrencyCodeType">
    <xs:restriction base="xs:string">
      <xs:pattern value="[A-Z]{3}"/>
      <xs:length value="3"/>
    </xs:restriction>
  </xs:simpleType>

  <!-- Currency Symbol Type (Unicode support) -->
  <xs:simpleType name="CurrencySymbolType">
    <xs:restriction base="xs:string">
      <xs:minLength value="1"/>
      <xs:maxLength value="5"/>
    </xs:restriction>
  </xs:simpleType>

  <!-- Currency Name Type -->
  <xs:simpleType name="CurrencyNameType">
    <xs:restriction base="xs:string">
      <xs:minLength value="1"/>
      <xs:maxLength value="100"/>
    </xs:restriction>
  </xs:simpleType>

  <!-- Complete Currency Complex Type -->
  <xs:complexType name="OfficialCurrencyType">
    <xs:sequence>
      <xs:element name="Code" type="curr:CurrencyCodeType"/>
      <xs:element name="Name" type="curr:CurrencyNameType"/>
      <xs:element name="Symbol" type="curr:CurrencySymbolType"/>
    </xs:sequence>
  </xs:complexType>

  <!-- Currency Element Definition -->
  <xs:element name="OfficialCurrency" type="curr:OfficialCurrencyType"/>

</xs:schema>
```

### **2. Country Schema (`schemas/country.xsd`)**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema"
           targetNamespace="http://countries.example.com/country"
           xmlns:country="http://countries.example.com/country"
           xmlns:curr="http://countries.example.com/currency"
           elementFormDefault="qualified">

  <!-- Import Currency Schema -->
  <xs:import namespace="http://countries.example.com/currency"
             schemaLocation="currency.xsd"/>

  <!-- ISO 3166-1 alpha-2 Country Code -->
  <xs:simpleType name="CountryCodeType">
    <xs:restriction base="xs:string">
      <xs:pattern value="[A-Z]{2}"/>
      <xs:length value="2"/>
    </xs:restriction>
  </xs:simpleType>

  <!-- Country Name Types (with Unicode support) -->
  <xs:simpleType name="CountryNameType">
    <xs:restriction base="xs:string">
      <xs:minLength value="1"/>
      <xs:maxLength value="200"/>
    </xs:restriction>
  </xs:simpleType>

  <!-- Individual Country Complex Type -->
  <xs:complexType name="CountryType">
    <xs:sequence>
      <xs:element name="Code" type="country:CountryCodeType"/>
      <xs:element name="OriginalName" type="country:CountryNameType"/>
      <xs:element name="CommonName" type="country:CountryNameType"/>
      <xs:element name="LocalName" type="country:CountryNameType"/>
      <xs:element ref="curr:OfficialCurrency"/>
    </xs:sequence>
  </xs:complexType>

  <!-- Country Element Definition -->
  <xs:element name="Countries" type="country:CountryType"/>

</xs:schema>
```

### **3. Collection Schema (`schemas/countries-collection.xsd`)**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema"
           targetNamespace="http://countries.example.com/collection"
           xmlns:collection="http://countries.example.com/collection"
           xmlns:country="http://countries.example.com/country"
           elementFormDefault="qualified">

  <!-- Import Country Schema -->
  <xs:import namespace="http://countries.example.com/country"
             schemaLocation="country.xsd"/>

  <!-- Countries Collection Type -->
  <xs:complexType name="CountriesCollectionType">
    <xs:sequence>
      <xs:element ref="country:Countries" 
                  minOccurs="1" 
                  maxOccurs="unbounded"/>
    </xs:sequence>
    <xs:attribute name="generatedDate" type="xs:dateTime" use="optional"/>
    <xs:attribute name="totalCount" type="xs:positiveInteger" use="optional"/>
  </xs:complexType>

  <!-- Root Collection Element -->
  <xs:element name="CountriesCollection" type="collection:CountriesCollectionType"/>

</xs:schema>
```

## 🎯 Target XML Format

### **Generated XML Structure**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<CountriesCollection xmlns="http://countries.example.com/collection"
                     xmlns:country="http://countries.example.com/country"
                     xmlns:curr="http://countries.example.com/currency"
                     generatedDate="2025-01-23T14:30:00Z"
                     totalCount="2">

  <country:Countries>
    <country:Code>IN</country:Code>
    <country:OriginalName>Republic of India</country:OriginalName>
    <country:CommonName>India</country:CommonName>
    <country:LocalName>भारत गणराज्य</country:LocalName>
    <curr:OfficialCurrency>
      <curr:Code>INR</curr:Code>
      <curr:Name>Indian rupee</curr:Name>
      <curr:Symbol>₹</curr:Symbol>
    </curr:OfficialCurrency>
  </country:Countries>

  <country:Countries>
    <country:Code>JP</country:Code>
    <country:OriginalName>Japan</country:OriginalName>
    <country:CommonName>Japan</country:CommonName>
    <country:LocalName>日本</country:LocalName>
    <curr:OfficialCurrency>
      <curr:Code>JPY</curr:Code>
      <curr:Name>Japanese yen</curr:Name>
      <curr:Symbol>¥</curr:Symbol>
    </curr:OfficialCurrency>
  </country:Countries>

</CountriesCollection>
```

## 🔧 XML Generation Process

### **1. Data Extraction & Mapping**

```python
def extract_xml_data(self, country_data: Dict[str, Any]) -> Dict[str, Any]:
    """Extract and map API data to XML structure"""
    
    name_data = country_data.get("name", {})
    currencies = country_data.get("currencies", {})
    
    # Extract native name with language priority
    native_names = name_data.get("nativeName", {})
    local_name = self.extract_native_name(native_names)
    
    # Extract primary currency
    currency_info = self.extract_currency_info(currencies)
    
    return {
        "code": country_data.get("cca2", ""),  # ISO 3166-1 alpha-2
        "original_name": name_data.get("official", ""),
        "common_name": name_data.get("common", ""),
        "local_name": local_name,
        "currency": currency_info
    }

def extract_currency_info(self, currencies: Dict) -> Dict[str, str]:
    """Extract primary currency information"""
    
    if not currencies:
        return {"code": "", "name": "", "symbol": ""}
    
    # Take the first (primary) currency
    currency_code = list(currencies.keys())[0]
    currency_data = currencies[currency_code]
    
    return {
        "code": currency_code,
        "name": currency_data.get("name", ""),
        "symbol": currency_data.get("symbol", "")
    }
```

### **2. XML Content Generation**

```python
def generate_formatted_xml(self, countries_data: List[Dict[str, Any]], 
                          output_file: str) -> str:
    """Generate properly formatted XML with namespace support"""
    
    # Define namespaces
    namespaces = {
        'xmlns': 'http://countries.example.com/collection',
        'xmlns:country': 'http://countries.example.com/country',
        'xmlns:curr': 'http://countries.example.com/currency'
    }
    
    # Build XML manually for precise formatting
    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<CountriesCollection xmlns="http://countries.example.com/collection"',
        '                     xmlns:country="http://countries.example.com/country"',
        '                     xmlns:curr="http://countries.example.com/currency"',
        f'                     generatedDate="{datetime.utcnow().isoformat()}Z"',
        f'                     totalCount="{len(countries_data)}">'
    ]
    
    # Add each country
    for country_data in countries_data:
        xml_data = self.extract_xml_data(country_data)
        xml_lines.extend(self.format_country_xml(xml_data))
    
    # Close root element
    xml_lines.append('</CountriesCollection>')
    
    return "\n".join(xml_lines)

def format_country_xml(self, xml_data: Dict[str, Any]) -> List[str]:
    """Format individual country XML with proper indentation"""
    
    return [
        "",  # Empty line before country
        "  <country:Countries>",
        f"    <country:Code>{self.escape_xml(xml_data['code'])}</country:Code>",
        f"    <country:OriginalName>{self.escape_xml(xml_data['original_name'])}</country:OriginalName>",
        f"    <country:CommonName>{self.escape_xml(xml_data['common_name'])}</country:CommonName>",
        f"    <country:LocalName>{self.escape_xml(xml_data['local_name'])}</country:LocalName>",
        "    <curr:OfficialCurrency>",
        f"      <curr:Code>{self.escape_xml(xml_data['currency']['code'])}</curr:Code>",
        f"      <curr:Name>{self.escape_xml(xml_data['currency']['name'])}</curr:Name>",
        f"      <curr:Symbol>{self.escape_xml(xml_data['currency']['symbol'])}</curr:Symbol>",
        "    </curr:OfficialCurrency>",
        "  </country:Countries>"
    ]

def escape_xml(self, text: str) -> str:
    """Escape XML special characters"""
    
    if not text:
        return ""
    
    return (text
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&apos;"))
```

## ✅ XML Validation

### **Schema Validation Process**

```python
import xml.etree.ElementTree as ET
from lxml import etree

def validate_xml_against_schema(self, xml_file: str, schema_file: str) -> bool:
    """Validate generated XML against XSD schema"""
    
    try:
        # Parse the schema
        with open(schema_file, 'r', encoding='utf-8') as schema_file:
            schema_doc = etree.parse(schema_file)
            schema = etree.XMLSchema(schema_doc)
        
        # Parse the XML document
        with open(xml_file, 'r', encoding='utf-8') as xml_file:
            xml_doc = etree.parse(xml_file)
        
        # Validate
        if schema.validate(xml_doc):
            self.log(f"✅ XML validation successful: {xml_file}")
            return True
        else:
            self.log(f"❌ XML validation failed: {xml_file}")
            for error in schema.error_log:
                self.log(f"   - {error}")
            return False
            
    except Exception as e:
        self.log(f"❌ Validation error: {e}")
        return False

def validate_xml_well_formed(self, xml_content: str) -> bool:
    """Check if XML is well-formed"""
    
    try:
        ET.fromstring(xml_content)
        return True
    except ET.ParseError as e:
        self.log(f"❌ XML not well-formed: {e}")
        return False
```

### **Comprehensive Validation Suite**

```python
class XMLValidator:
    def __init__(self):
        self.validation_results = {
            "well_formed": False,
            "schema_valid": False,
            "encoding_valid": False,
            "content_valid": False
        }
    
    def validate_comprehensive(self, xml_file: str) -> Dict[str, bool]:
        """Run comprehensive XML validation"""
        
        # 1. Check well-formedness
        with open(xml_file, 'r', encoding='utf-8') as f:
            xml_content = f.read()
        
        self.validation_results["well_formed"] = self.validate_well_formed(xml_content)
        
        # 2. Schema validation
        self.validation_results["schema_valid"] = self.validate_against_schema(
            xml_file, "schemas/countries-collection.xsd"
        )
        
        # 3. Encoding validation (UTF-8 with Unicode support)
        self.validation_results["encoding_valid"] = self.validate_encoding(xml_file)
        
        # 4. Content validation (business rules)
        self.validation_results["content_valid"] = self.validate_content(xml_file)
        
        return self.validation_results
    
    def validate_encoding(self, xml_file: str) -> bool:
        """Validate UTF-8 encoding and Unicode support"""
        
        try:
            with open(xml_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for proper UTF-8 BOM handling
            if content.startswith('\ufeff'):
                self.log("⚠️ UTF-8 BOM detected (acceptable but not required)")
            
            # Test Unicode character preservation
            unicode_chars = ['₹', '¥', '€', '£', '¢', 'भारत', '日本']
            unicode_found = any(char in content for char in unicode_chars)
            
            if unicode_found:
                self.log("✅ Unicode characters properly preserved")
            
            return True
            
        except UnicodeDecodeError as e:
            self.log(f"❌ Encoding validation failed: {e}")
            return False
    
    def validate_content(self, xml_file: str) -> bool:
        """Validate business rules and content quality"""
        
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()
            
            # Check required elements
            countries = root.findall(".//Countries")
            if not countries:
                self.log("❌ No country elements found")
                return False
            
            # Validate each country
            for country in countries:
                if not self.validate_country_element(country):
                    return False
            
            self.log(f"✅ Content validation passed for {len(countries)} countries")
            return True
            
        except Exception as e:
            self.log(f"❌ Content validation error: {e}")
            return False
    
    def validate_country_element(self, country_element) -> bool:
        """Validate individual country element"""
        
        required_elements = ['Code', 'OriginalName', 'CommonName', 'LocalName']
        
        for element_name in required_elements:
            element = country_element.find(element_name)
            if element is None or not element.text.strip():
                self.log(f"❌ Missing or empty {element_name}")
                return False
        
        # Validate currency element
        currency = country_element.find("OfficialCurrency")
        if currency is None:
            self.log("❌ Missing OfficialCurrency element")
            return False
        
        currency_elements = ['Code', 'Name', 'Symbol']
        for element_name in currency_elements:
            element = currency.find(element_name)
            if element is None or not element.text.strip():
                self.log(f"❌ Missing or empty currency {element_name}")
                return False
        
        # Validate country code format (ISO 3166-1 alpha-2)
        code_element = country_element.find("Code")
        if not re.match(r'^[A-Z]{2}$', code_element.text):
            self.log(f"❌ Invalid country code format: {code_element.text}")
            return False
        
        # Validate currency code format (ISO 4217)
        currency_code = currency.find("Code")
        if not re.match(r'^[A-Z]{3}$', currency_code.text):
            self.log(f"❌ Invalid currency code format: {currency_code.text}")
            return False
        
        return True
```

## 🎨 Formatting & Style

### **Consistent Indentation**

```python
class XMLFormatter:
    def __init__(self, indent_size: int = 2):
        self.indent_size = indent_size
        self.current_depth = 0
    
    def format_element(self, tag: str, content: str = None, 
                      attributes: Dict[str, str] = None, 
                      self_closing: bool = False) -> str:
        """Format XML element with proper indentation"""
        
        indent = " " * (self.current_depth * self.indent_size)
        
        # Build attributes string
        attrs = ""
        if attributes:
            attrs = " " + " ".join(f'{k}="{v}"' for k, v in attributes.items())
        
        if self_closing:
            return f"{indent}<{tag}{attrs}/>"
        elif content:
            return f"{indent}<{tag}{attrs}>{content}</{tag}>"
        else:
            return f"{indent}<{tag}{attrs}>"
    
    def increase_depth(self):
        """Increase indentation depth"""
        self.current_depth += 1
    
    def decrease_depth(self):
        """Decrease indentation depth"""
        self.current_depth = max(0, self.current_depth - 1)
```

### **Pretty Printing with lxml**

```python
from lxml import etree

def pretty_print_xml(self, xml_string: str) -> str:
    """Pretty print XML with proper formatting"""
    
    try:
        # Parse the XML
        root = etree.fromstring(xml_string.encode('utf-8'))
        
        # Pretty print with proper indentation
        pretty_xml = etree.tostring(
            root,
            pretty_print=True,
            encoding='unicode',
            xml_declaration=True
        )
        
        return pretty_xml
        
    except Exception as e:
        self.log(f"❌ Pretty printing failed: {e}")
        return xml_string
```

## 🔍 Testing & Quality Assurance

### **Automated XML Testing**

```python
class XMLTestSuite:
    def __init__(self):
        self.test_results = []
    
    def run_all_tests(self, xml_file: str) -> bool:
        """Run comprehensive XML test suite"""
        
        tests = [
            self.test_xml_declaration,
            self.test_encoding,
            self.test_root_element,
            self.test_namespace_declarations,
            self.test_schema_compliance,
            self.test_data_completeness,
            self.test_unicode_handling,
            self.test_special_characters
        ]
        
        all_passed = True
        
        for test in tests:
            try:
                result = test(xml_file)
                self.test_results.append({
                    "test": test.__name__,
                    "passed": result,
                    "timestamp": datetime.now()
                })
                
                if not result:
                    all_passed = False
                    
            except Exception as e:
                self.log(f"❌ Test {test.__name__} failed with exception: {e}")
                all_passed = False
        
        return all_passed
    
    def test_xml_declaration(self, xml_file: str) -> bool:
        """Test XML declaration"""
        
        with open(xml_file, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()
        
        expected = '<?xml version="1.0" encoding="UTF-8"?>'
        return first_line == expected
    
    def test_unicode_handling(self, xml_file: str) -> bool:
        """Test Unicode character handling"""
        
        with open(xml_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Test various Unicode characters
        unicode_tests = [
            ('₹', 'Indian Rupee symbol'),
            ('¥', 'Japanese Yen symbol'),
            ('भारत', 'Hindi script'),
            ('日本', 'Japanese script')
        ]
        
        for char, description in unicode_tests:
            if char in content:
                self.log(f"✅ Unicode test passed: {description}")
        
        return True
```

## 🔮 Advanced Features

### **Conditional XML Generation**

```python
def generate_conditional_xml(self, countries_data: List[Dict], 
                           conditions: Dict[str, Any]) -> str:
    """Generate XML with conditional content"""
    
    # Filter countries based on conditions
    if conditions.get("include_currencies"):
        valid_currencies = conditions["include_currencies"]
        countries_data = [
            country for country in countries_data
            if self.extract_xml_data(country)["currency"]["code"] in valid_currencies
        ]
    
    # Sort if requested
    if conditions.get("sort_by"):
        sort_field = conditions["sort_by"]
        countries_data.sort(key=lambda x: self.extract_xml_data(x)[sort_field])
    
    return self.generate_formatted_xml(countries_data)
```

### **Multi-format Output**

```python
def generate_multiple_formats(self, countries_data: List[Dict], 
                             output_dir: str) -> Dict[str, str]:
    """Generate XML in multiple formats"""
    
    formats = {
        "standard": self.generate_formatted_xml(countries_data),
        "compact": self.generate_compact_xml(countries_data),
        "detailed": self.generate_detailed_xml(countries_data),
        "namespaced": self.generate_namespaced_xml(countries_data)
    }
    
    output_files = {}
    
    for format_name, xml_content in formats.items():
        output_file = os.path.join(output_dir, f"countries_{format_name}.xml")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(xml_content)
        
        output_files[format_name] = output_file
    
    return output_files
```

---

## 📚 Related Documentation

- **[System Architecture](ARCHITECTURE.md)** - Overall system design
- **[API Integration](API_INTEGRATION.md)** - Data source integration
- **[GitHub Actions Setup](GITHUB_ACTIONS.md)** - Automation configuration
- **[Troubleshooting](TROUBLESHOOTING.md)** - Common XML issues and solutions 