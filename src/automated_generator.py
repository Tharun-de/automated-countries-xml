#!/usr/bin/env python3
"""
Automated Countries XML Generator for GitHub Actions

Purpose: Command-line interface for generating countries XML from GitHub Actions
Learning: Shows how to create automation-friendly scripts with CLI arguments

Features:
1. Command-line argument parsing
2. Configurable country lists
3. Error handling for automation
4. Logging and status reporting
5. Integration with GitHub Actions
"""

import argparse
import sys
import os
import json
from typing import List, Dict, Any
from datetime import datetime
import requests

# Import our existing generator
from improved_xml_generator import ImprovedCountryXMLGenerator

class AutomatedCountryGenerator:
    """
    Automation-friendly country XML generator
    
    Designed for use in CI/CD pipelines like GitHub Actions
    """
    
    def __init__(self, verbose: bool = True):
        self.generator = ImprovedCountryXMLGenerator()
        self.verbose = verbose
        
    def log(self, message: str, level: str = "INFO"):
        """Log messages with timestamp"""
        if self.verbose:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{timestamp}] {level}: {message}")
    
    def parse_country_list(self, countries_input: str) -> List[str]:
        """
        Parse comma-separated country list
        
        Args:
            countries_input: Comma-separated string of country names
            
        Returns:
            List of country names
        """
        if not countries_input:
            return []
        
        # Split by comma and clean up
        countries = [country.strip().lower() for country in countries_input.split(',')]
        countries = [country for country in countries if country]  # Remove empty strings
        
        self.log(f"Parsed {len(countries)} countries: {', '.join(countries)}")
        return countries
    
    def test_api_connectivity(self) -> bool:
        """Test if REST Countries API is accessible"""
        try:
            self.log("Testing API connectivity...")
            response = requests.get("https://restcountries.com/v3.1/name/india", timeout=10)
            response.raise_for_status()
            self.log("✅ API is accessible")
            return True
        except Exception as e:
            self.log(f"❌ API connectivity test failed: {e}", "ERROR")
            return False
    
    def generate_xml_with_validation(self, countries: List[str], output_file: str) -> Dict[str, Any]:
        """
        Generate XML with comprehensive validation and error reporting
        
        Args:
            countries: List of country names
            output_file: Output file path
            
        Returns:
            Dictionary with generation results and statistics
        """
        result = {
            "success": False,
            "countries_requested": len(countries),
            "countries_processed": 0,
            "output_file": output_file,
            "errors": [],
            "warnings": []
        }
        
        try:
            # Test API first
            if not self.test_api_connectivity():
                result["errors"].append("API connectivity test failed")
                return result
            
            # Generate XML
            self.log(f"Starting XML generation for {len(countries)} countries...")
            output_path = self.generator.generate_countries_xml(countries, output_file)
            
            if output_path and os.path.exists(output_path):
                # Validate the generated XML
                import xml.etree.ElementTree as ET
                tree = ET.parse(output_path)
                country_elements = tree.findall(".//Countries")
                
                result["success"] = True
                result["countries_processed"] = len(country_elements)
                result["file_size"] = os.path.getsize(output_path)
                
                self.log(f"✅ Successfully generated XML with {len(country_elements)} countries")
                
                # Check for missing countries
                if len(country_elements) < len(countries):
                    missing_count = len(countries) - len(country_elements)
                    result["warnings"].append(f"{missing_count} countries could not be processed")
                
            else:
                result["errors"].append("XML file was not created")
                
        except Exception as e:
            self.log(f"❌ Error during XML generation: {e}", "ERROR")
            result["errors"].append(str(e))
        
        return result
    
    def create_status_report(self, result: Dict[str, Any]) -> str:
        """Create a detailed status report"""
        report_lines = [
            "=" * 50,
            "🌍 COUNTRIES XML GENERATION REPORT",
            "=" * 50,
            f"📅 Timestamp: {datetime.now().isoformat()}",
            f"📊 Countries Requested: {result['countries_requested']}",
            f"📊 Countries Processed: {result['countries_processed']}",
            f"📁 Output File: {result['output_file']}",
            f"✅ Success: {result['success']}"
        ]
        
        if result.get("file_size"):
            report_lines.append(f"📄 File Size: {result['file_size']} bytes")
        
        if result["errors"]:
            report_lines.extend([
                "",
                "❌ ERRORS:",
                *[f"  - {error}" for error in result["errors"]]
            ])
        
        if result["warnings"]:
            report_lines.extend([
                "",
                "⚠️  WARNINGS:",
                *[f"  - {warning}" for warning in result["warnings"]]
            ])
        
        report_lines.append("=" * 50)
        return "\n".join(report_lines)

def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(
        description="Generate Countries XML from REST Countries API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python automated_generator.py --countries "india,japan,germany"
  python automated_generator.py --countries "india,japan" --output "my_countries.xml"
  python automated_generator.py --config config/countries.json
        """
    )
    
    parser.add_argument(
        "--countries",
        type=str,
        help="Comma-separated list of countries to include",
        default="india,japan,germany,france,brazil"
    )
    
    parser.add_argument(
        "--output",
        type=str,
        help="Output XML file path",
        default="output/countries.xml"
    )
    
    parser.add_argument(
        "--config",
        type=str,
        help="JSON config file with countries list (optional)"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging",
        default=True
    )
    
    parser.add_argument(
        "--test-only",
        action="store_true",
        help="Only test API connectivity, don't generate XML"
    )
    
    args = parser.parse_args()
    
    # Create generator
    generator = AutomatedCountryGenerator(verbose=args.verbose)
    
    # Handle test-only mode
    if args.test_only:
        success = generator.test_api_connectivity()
        sys.exit(0 if success else 1)
    
    # Determine countries list
    countries = []
    
    if args.config and os.path.exists(args.config):
        # Load from config file
        try:
            with open(args.config, 'r') as f:
                config = json.load(f)
                countries = config.get("countries", [])
            generator.log(f"Loaded {len(countries)} countries from config file")
        except Exception as e:
            generator.log(f"Error loading config file: {e}", "ERROR")
            sys.exit(1)
    else:
        # Use command line countries
        countries = generator.parse_country_list(args.countries)
    
    if not countries:
        generator.log("No countries specified", "ERROR")
        sys.exit(1)
    
    # Generate XML
    result = generator.generate_xml_with_validation(countries, args.output)
    
    # Print report
    report = generator.create_status_report(result)
    print(report)
    
    # Exit with appropriate code
    sys.exit(0 if result["success"] else 1)

if __name__ == "__main__":
    main() 