"""
REST Countries API Test Script

Purpose: Test API connectivity and explore the data structure
Learning: Understand what data we get from the API before converting to XML

Run this script to see:
1. How to make API calls
2. What data structure we get back
3. How to filter specific countries
4. Error handling for API calls
"""

import requests
import json
from typing import Dict, List, Any
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax

# Initialize rich console for pretty printing
console = Console()

# API endpoints we'll use
API_BASE = "https://restcountries.com/v3.1"
ALL_COUNTRIES_URL = f"{API_BASE}/all"
FILTERED_URL = f"{API_BASE}/all?fields=name,cca2,currencies,capital,region"

def test_api_connection():
    """Test basic API connectivity"""
    console.print(Panel("🌐 Testing API Connection", style="bold green"))
    
    try:
        response = requests.get(f"{API_BASE}/name/india", timeout=10)
        response.raise_for_status()
        console.print("✅ API is accessible")
        return True
    except requests.exceptions.RequestException as e:
        console.print(f"❌ API connection failed: {e}", style="bold red")
        return False

def fetch_single_country(country_name: str) -> Dict[str, Any]:
    """
    Fetch data for a single country to examine the structure
    
    Args:
        country_name: Name of the country to fetch
    
    Returns:
        Dictionary containing country data
    """
    url = f"{API_BASE}/name/{country_name}"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data and len(data) > 0:
            return data[0]  # API returns a list, take first result
        else:
            return {}
            
    except requests.exceptions.RequestException as e:
        console.print(f"❌ Error fetching {country_name}: {e}", style="bold red")
        return {}

def display_country_structure(country_data: Dict[str, Any]):
    """Display the structure of country data we receive from API"""
    console.print(Panel("📊 Sample Country Data Structure", style="bold blue"))
    
    # Show relevant fields for our XML generation
    relevant_fields = {
        "name": country_data.get("name", {}),
        "cca2": country_data.get("cca2", ""),
        "currencies": country_data.get("currencies", {}),
        "capital": country_data.get("capital", []),
        "region": country_data.get("region", "")
    }
    
    # Pretty print JSON
    json_str = json.dumps(relevant_fields, indent=2, ensure_ascii=False)
    syntax = Syntax(json_str, "json", theme="monokai", line_numbers=True)
    console.print(syntax)

def extract_xml_relevant_data(country_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract only the data we need for XML generation
    This shows the mapping from API response to our XML structure
    """
    name_data = country_data.get("name", {})
    currencies = country_data.get("currencies", {})
    
    # Extract native name (we'll use Hindi for India, first available for others)
    native_names = name_data.get("nativeName", {})
    local_name = ""
    
    if "hin" in native_names:  # Hindi for India
        local_name = native_names["hin"].get("official", "")
    elif native_names:  # First available native name for other countries
        first_lang = list(native_names.keys())[0]
        local_name = native_names[first_lang].get("official", "")
    
    # Extract currency info (take first currency if multiple)
    currency_info = {}
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

def test_multiple_countries():
    """Test with multiple countries to see data variations"""
    test_countries = ["india", "japan", "united states", "germany"]
    
    console.print(Panel("🌍 Testing Multiple Countries", style="bold cyan"))
    
    for country in test_countries:
        console.print(f"\n🔍 Fetching data for: {country.title()}")
        
        country_data = fetch_single_country(country)
        if country_data:
            xml_data = extract_xml_relevant_data(country_data)
            
            # Show what we'd put in XML
            console.print(f"XML Data: {json.dumps(xml_data, indent=2, ensure_ascii=False)}")
        else:
            console.print(f"❌ No data found for {country}")

def main():
    """Main test function"""
    console.print(Panel("🚀 REST Countries API Test", style="bold magenta"))
    
    # Test 1: Basic connectivity
    if not test_api_connection():
        return
    
    # Test 2: Single country detailed view
    console.print("\n" + "="*50)
    india_data = fetch_single_country("india")
    if india_data:
        display_country_structure(india_data)
        
        # Show XML mapping
        console.print(Panel("🎯 Data for XML Generation", style="bold yellow"))
        xml_data = extract_xml_relevant_data(india_data)
        console.print(json.dumps(xml_data, indent=2, ensure_ascii=False))
    
    # Test 3: Multiple countries
    console.print("\n" + "="*50)
    test_multiple_countries()
    
    # Test 4: Show API rate limits and best practices
    console.print(Panel("💡 API Best Practices", style="bold green"))
    console.print("✅ Use timeouts for requests")
    console.print("✅ Handle errors gracefully")
    console.print("✅ Cache responses when possible")
    console.print("✅ Respect rate limits")
    console.print("✅ Filter fields to reduce response size")

if __name__ == "__main__":
    main() 