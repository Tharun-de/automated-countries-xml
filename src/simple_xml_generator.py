"""
Simple XML Generator for Countries

Purpose: Generate XML files from REST Countries API data
Learning: Demonstrates API-to-XML conversion without hardcoding

This script shows:
1. How to fetch data from REST Countries API
2. How to convert JSON to XML structure
3. How to generate your target XML format
4. Basic error handling and logging
"""

import requests
import xml.etree.ElementTree as ET
from xml.dom import minidom
from typing import Dict, List, Any, Optional
from datetime import datetime
import json

class CountryXMLGenerator:
    """
    Generates XML for countries using REST Countries API
    
    This class demonstrates:
    - API integration
    - Data transformation (JSON to XML)
    - XML generation with proper formatting
    - Error handling
    """
    
    def __init__(self):
        self.api_base = "https://restcountries.com/v3.1"
        self.session = requests.Session()
        self.session.timeout = 10
        
    def fetch_country_data(self, country_names: List[str]) -> List[Dict[str, Any]]:
        """
        Fetch data for specific countries from the API
        
        Args:
            country_names: List of country names to fetch
            
        Returns:
            List of country data dictionaries
        """
        countries_data = []
        
        for country_name in country_names:
            try:
                print(f"🔍 Fetching data for: {country_name}")
                url = f"{self.api_base}/name/{country_name}"
                response = self.session.get(url)
                response.raise_for_status()
                
                data = response.json()
                if data and len(data) > 0:
                    countries_data.append(data[0])  # Take first result
                    print(f"✅ Successfully fetched: {country_name}")
                else:
                    print(f"⚠️  No data found for: {country_name}")
                    
            except requests.exceptions.RequestException as e:
                print(f"❌ Error fetching {country_name}: {e}")
                continue
                
        return countries_data
    
    def extract_xml_data(self, country_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract relevant data for XML generation from API response
        
        Args:
            country_data: Raw country data from API
            
        Returns:
            Dictionary with data formatted for XML
        """
        name_data = country_data.get("name", {})
        currencies = country_data.get("currencies", {})
        
        # Extract native name
        native_names = name_data.get("nativeName", {})
        local_name = ""
        
        if "hin" in native_names:  # Hindi for India
            local_name = native_names["hin"].get("official", "")
        elif "jpn" in native_names:  # Japanese for Japan
            local_name = native_names["jpn"].get("official", "")
        elif native_names:  # First available native name for others
            first_lang = list(native_names.keys())[0]
            local_name = native_names[first_lang].get("official", "")
        
        # Extract currency info (take first currency if multiple)
        currency_info = {
            "code": "",
            "name": "",
            "symbol": ""
        }
        
        if currencies:
            currency_code = list(currencies.keys())[0]
            currency_data = currencies[currency_code]
            currency_info = {
                "code": currency_code,
                "name": currency_data.get("name", ""),
                "symbol": currency_data.get("symbol", "")
            }
        
        return {
            "code": country_data.get("cca2", ""),
            "original_name": name_data.get("official", ""),
            "common_name": name_data.get("common", ""),
            "local_name": local_name,
            "currency": currency_info
        }
    
    def create_xml_element(self, parent: ET.Element, tag: str, text: str = "") -> ET.Element:
        """
        Create XML element with text content
        
        Args:
            parent: Parent XML element
            tag: Tag name for the element
            text: Text content for the element
            
        Returns:
            Created XML element
        """
        element = ET.SubElement(parent, tag)
        if text:
            element.text = str(text)
        return element
    
    def generate_xml(self, countries_data: List[Dict[str, Any]], output_file: str = "output/countries.xml"):
        """
        Generate XML file from countries data
        
        Args:
            countries_data: List of country data from API
            output_file: Path to output XML file
        """
        print(f"📝 Generating XML with {len(countries_data)} countries...")
        
        # Create root element (no wrapper for your exact format)
        root = ET.Element("root")  # Temporary root, we'll remove it later
        
        # Process each country
        for country_data in countries_data:
            xml_data = self.extract_xml_data(country_data)
            
            # Create Countries element for each country
            country_elem = ET.SubElement(root, "Countries")
            
            # Add country details
            self.create_xml_element(country_elem, "Code", xml_data["code"])
            self.create_xml_element(country_elem, "OriginalName", xml_data["original_name"])
            self.create_xml_element(country_elem, "CommonName", xml_data["common_name"])
            self.create_xml_element(country_elem, "LocalName", xml_data["local_name"])
            
            # Add currency details
            currency_elem = ET.SubElement(country_elem, "OfficialCurrency")
            currency_data = xml_data["currency"]
            self.create_xml_element(currency_elem, "Code", currency_data["code"])
            self.create_xml_element(currency_elem, "Name", currency_data["name"])
            self.create_xml_element(currency_elem, "Symbol", currency_data["symbol"])
        
        # Convert to string and format nicely
        xml_str = ET.tostring(root, encoding='unicode')
        
        # Remove the temporary root wrapper to match your exact format
        xml_str = xml_str.replace('<root>', '').replace('</root>', '')
        
        # Add XML declaration
        final_xml = '<?xml version="1.0" encoding="UTF-8"?>\n' + xml_str
        
        # Pretty format using minidom
        try:
            # Parse the XML string (need to wrap it for minidom)
            wrapped_xml = f'<root>{xml_str}</root>'
            dom = minidom.parseString(wrapped_xml)
            
            # Get pretty printed version and remove wrapper
            pretty_xml = dom.documentElement.innerHTML
            final_xml = '<?xml version="1.0" encoding="UTF-8"?>\n' + pretty_xml
            
        except Exception as e:
            print(f"⚠️  Formatting warning: {e}")
            # Fallback to basic formatting
            pass
        
        # Ensure output directory exists
        import os
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # Write to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(final_xml)
        
        print(f"✅ XML generated successfully: {output_file}")
        return output_file
    
    def generate_countries_xml(self, country_names: List[str], output_file: str = "output/countries.xml"):
        """
        Main method to generate XML from country names
        
        Args:
            country_names: List of country names to include
            output_file: Path to output XML file
        """
        print("🚀 Starting Countries XML Generation")
        print(f"📋 Countries to fetch: {', '.join(country_names)}")
        
        # Fetch data from API
        countries_data = self.fetch_country_data(country_names)
        
        if not countries_data:
            print("❌ No country data fetched. Cannot generate XML.")
            return None
        
        # Generate XML
        return self.generate_xml(countries_data, output_file)

def main():
    """Main function to demonstrate XML generation"""
    print("🌍 Countries XML Generator - Demo")
    print("=" * 50)
    
    # Create generator instance
    generator = CountryXMLGenerator()
    
    # Test with India and Japan (your example countries)
    test_countries = ["india", "japan"]
    
    # Generate XML
    output_file = generator.generate_countries_xml(test_countries)
    
    if output_file:
        print(f"\n🎉 Success! Check your generated XML file: {output_file}")
        
        # Show a preview of the generated XML
        try:
            with open(output_file, 'r', encoding='utf-8') as f:
                content = f.read()
                print("\n📄 Generated XML Preview:")
                print("-" * 30)
                print(content[:1000] + "..." if len(content) > 1000 else content)
        except Exception as e:
            print(f"⚠️  Could not preview file: {e}")
    
    print("\n🔄 Next Steps:")
    print("1. Check the generated XML file")
    print("2. Compare with your target format")
    print("3. Test with more countries")
    print("4. Set up GitHub Actions automation")

if __name__ == "__main__":
    main() 