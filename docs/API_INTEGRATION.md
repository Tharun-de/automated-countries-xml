# 🌐 API Integration Guide

## Overview

This guide explains how the Countries XML Auto-Generator integrates with the **REST Countries API** to fetch live country data and convert it to structured XML format.

## 📡 API Information

### **REST Countries API**
- **Base URL**: `https://restcountries.com/v3.1`
- **Type**: Public REST API
- **Authentication**: None required
- **Rate Limits**: Reasonable use policy
- **Documentation**: https://restcountries.com/

### **Why REST Countries API?**
✅ **Free & Open**: No API keys or registration required  
✅ **Comprehensive**: 250+ countries with detailed information  
✅ **Real-time**: Live data updates  
✅ **Reliable**: High uptime and performance  
✅ **Unicode Support**: Native names in original scripts  
✅ **Currency Data**: ISO 4217 compliant currency information  

## 🔌 API Endpoints Used

### **1. Get Country by Name**
```http
GET https://restcountries.com/v3.1/name/{country_name}
```

**Example:**
```bash
curl "https://restcountries.com/v3.1/name/india"
```

**Response Structure:**
```json
[
  {
    "name": {
      "common": "India",
      "official": "Republic of India",
      "nativeName": {
        "hin": {
          "official": "भारत गणराज्य",
          "common": "भारत"
        }
      }
    },
    "cca2": "IN",
    "cca3": "IND",
    "currencies": {
      "INR": {
        "name": "Indian rupee",
        "symbol": "₹"
      }
    }
  }
]
```

### **2. API Connectivity Test**
```http
GET https://restcountries.com/v3.1/name/india
```
Used to verify API availability before processing large country lists.

## 🛠️ Implementation Details

### **HTTP Client Configuration**

```python
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class APIClient:
    def __init__(self):
        self.session = requests.Session()
        self.session.timeout = 10
        
        # Configure retry strategy
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
```

### **Data Fetching Logic**

```python
def fetch_country_data(self, country_names: List[str]) -> List[Dict[str, Any]]:
    """Fetch data for multiple countries with error handling"""
    countries_data = []
    
    for country_name in country_names:
        try:
            url = f"{self.api_base}/name/{country_name}"
            response = self.session.get(url)
            response.raise_for_status()
            
            data = response.json()
            if data and len(data) > 0:
                countries_data.append(data[0])  # Take first match
                self.log(f"✅ Successfully fetched: {country_name}")
            else:
                self.log(f"⚠️ No data found for: {country_name}")
                
        except requests.exceptions.RequestException as e:
            self.log(f"❌ Error fetching {country_name}: {e}")
            continue  # Continue with other countries
            
    return countries_data
```

## 📊 Data Extraction & Mapping

### **Field Mapping Table**

| XML Field | API Path | Example | Notes |
|-----------|----------|---------|-------|
| `<Code>` | `cca2` | "IN" | ISO 3166-1 alpha-2 |
| `<OriginalName>` | `name.official` | "Republic of India" | Official country name |
| `<CommonName>` | `name.common` | "India" | Common country name |
| `<LocalName>` | `name.nativeName.{lang}.official` | "भारत गणराज्य" | Native language name |
| `<Currency><Code>` | `currencies.{code}` | "INR" | ISO 4217 currency code |
| `<Currency><Name>` | `currencies.{code}.name` | "Indian rupee" | Currency full name |
| `<Currency><Symbol>` | `currencies.{code}.symbol` | "₹" | Currency symbol |

### **Native Name Priority Logic**

```python
def extract_native_name(self, native_names: Dict) -> str:
    """Extract native name with language priority"""
    
    # Priority order for language selection
    language_priority = [
        "hin",  # Hindi (India)
        "jpn",  # Japanese (Japan)
        "deu",  # German (Germany)
        "fra",  # French (France)
        "spa",  # Spanish (Spain)
        "ara",  # Arabic (Arab countries)
        "zho"   # Chinese (China)
    ]
    
    # Try priority languages first
    for lang in language_priority:
        if lang in native_names:
            return native_names[lang].get("official", "")
    
    # Fall back to first available language
    if native_names:
        first_lang = list(native_names.keys())[0]
        return native_names[first_lang].get("official", "")
    
    return ""
```

## 🚦 Error Handling

### **API Error Types**

| Error Type | HTTP Code | Handling Strategy |
|------------|-----------|-------------------|
| **Not Found** | 404 | Log warning, continue with other countries |
| **Rate Limited** | 429 | Retry with exponential backoff |
| **Server Error** | 5xx | Retry up to 3 times, then skip |
| **Network Error** | - | Retry with timeout, then skip |
| **Invalid JSON** | 200 | Log error, skip country |

### **Error Handling Implementation**

```python
def safe_api_call(self, country_name: str) -> Optional[Dict]:
    """Make API call with comprehensive error handling"""
    
    try:
        response = self.session.get(
            f"{self.api_base}/name/{country_name}",
            timeout=10
        )
        
        # Handle different response codes
        if response.status_code == 404:
            self.log(f"⚠️ Country not found: {country_name}")
            return None
            
        elif response.status_code == 429:
            self.log(f"⏳ Rate limited, retrying: {country_name}")
            time.sleep(2)  # Wait before retry
            return self.safe_api_call(country_name)
            
        response.raise_for_status()
        
        # Parse JSON response
        data = response.json()
        if not data or len(data) == 0:
            self.log(f"⚠️ Empty response for: {country_name}")
            return None
            
        return data[0]  # Return first match
        
    except requests.exceptions.Timeout:
        self.log(f"⏰ Timeout for: {country_name}")
        return None
        
    except requests.exceptions.ConnectionError:
        self.log(f"🔌 Connection error for: {country_name}")
        return None
        
    except ValueError as e:  # JSON decode error
        self.log(f"📄 Invalid JSON for {country_name}: {e}")
        return None
        
    except Exception as e:
        self.log(f"❌ Unexpected error for {country_name}: {e}")
        return None
```

## 🔍 API Testing & Validation

### **Connectivity Test**

```python
def test_api_connectivity(self) -> bool:
    """Test if REST Countries API is accessible"""
    try:
        response = requests.get(
            "https://restcountries.com/v3.1/name/india",
            timeout=10
        )
        response.raise_for_status()
        
        data = response.json()
        if data and len(data) > 0:
            self.log("✅ API connectivity test passed")
            return True
            
    except Exception as e:
        self.log(f"❌ API connectivity test failed: {e}")
        
    return False
```

### **Data Validation**

```python
def validate_country_data(self, data: Dict) -> bool:
    """Validate country data completeness"""
    
    required_fields = [
        "name",
        "cca2",
        "currencies"
    ]
    
    for field in required_fields:
        if field not in data:
            self.log(f"⚠️ Missing required field: {field}")
            return False
    
    # Validate name structure
    name_data = data.get("name", {})
    if not name_data.get("common") or not name_data.get("official"):
        self.log("⚠️ Incomplete name data")
        return False
    
    # Validate currency structure
    currencies = data.get("currencies", {})
    if not currencies:
        self.log("⚠️ No currency data")
        return False
    
    return True
```

## 📈 Performance Optimization

### **Batch Processing**

```python
async def fetch_countries_async(self, country_names: List[str]) -> List[Dict]:
    """Async batch processing for better performance"""
    
    import asyncio
    import aiohttp
    
    async with aiohttp.ClientSession() as session:
        tasks = [
            self.fetch_single_country(session, country)
            for country in country_names
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter out exceptions and None results
        return [
            result for result in results
            if isinstance(result, dict)
        ]

async def fetch_single_country(self, session, country_name: str) -> Optional[Dict]:
    """Fetch single country data asynchronously"""
    
    try:
        url = f"{self.api_base}/name/{country_name}"
        async with session.get(url, timeout=10) as response:
            if response.status == 200:
                data = await response.json()
                return data[0] if data else None
                
    except Exception as e:
        self.log(f"❌ Async error for {country_name}: {e}")
        
    return None
```

### **Caching Strategy**

```python
import pickle
from datetime import datetime, timedelta

class APICache:
    def __init__(self, cache_duration_hours: int = 24):
        self.cache_file = "cache/api_cache.pkl"
        self.cache_duration = timedelta(hours=cache_duration_hours)
        self.cache = self.load_cache()
    
    def get_cached_data(self, country_name: str) -> Optional[Dict]:
        """Get cached country data if still valid"""
        
        if country_name in self.cache:
            cached_item = self.cache[country_name]
            
            if datetime.now() - cached_item["timestamp"] < self.cache_duration:
                self.log(f"📋 Using cached data for: {country_name}")
                return cached_item["data"]
        
        return None
    
    def cache_data(self, country_name: str, data: Dict):
        """Cache country data with timestamp"""
        
        self.cache[country_name] = {
            "data": data,
            "timestamp": datetime.now()
        }
        
        self.save_cache()
```

## 🔧 Configuration

### **API Settings**

```json
{
  "api": {
    "base_url": "https://restcountries.com/v3.1",
    "timeout": 10,
    "max_retries": 3,
    "retry_backoff": 1.0,
    "cache_duration_hours": 24
  },
  "countries": [
    "india",
    "japan",
    "germany",
    "france",
    "brazil"
  ]
}
```

### **Environment Variables**

```bash
# Optional overrides
export COUNTRIES_API_BASE_URL="https://restcountries.com/v3.1"
export COUNTRIES_API_TIMEOUT="10"
export COUNTRIES_CACHE_DURATION="24"
```

## 📊 Monitoring & Analytics

### **API Metrics**

```python
class APIMetrics:
    def __init__(self):
        self.metrics = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "avg_response_time": 0,
            "countries_processed": 0,
            "cache_hits": 0
        }
    
    def record_request(self, success: bool, response_time: float):
        """Record API request metrics"""
        
        self.metrics["total_requests"] += 1
        
        if success:
            self.metrics["successful_requests"] += 1
        else:
            self.metrics["failed_requests"] += 1
        
        # Update average response time
        current_avg = self.metrics["avg_response_time"]
        total_requests = self.metrics["total_requests"]
        
        self.metrics["avg_response_time"] = (
            (current_avg * (total_requests - 1) + response_time) / total_requests
        )
    
    def get_success_rate(self) -> float:
        """Calculate API success rate"""
        
        if self.metrics["total_requests"] == 0:
            return 0.0
            
        return (
            self.metrics["successful_requests"] / 
            self.metrics["total_requests"] * 100
        )
```

## 🔮 Future API Enhancements

### **Multiple Data Sources**
- **World Bank API**: Economic indicators
- **OpenStreetMap**: Geographic boundaries
- **Wikipedia API**: Additional metadata

### **Enhanced Caching**
- **Redis**: Distributed caching
- **CDN**: Geographic data distribution
- **Smart Invalidation**: Event-driven cache updates

### **Real-time Updates**
- **Webhooks**: Push notifications for data changes
- **WebSockets**: Live data streaming
- **Event Sourcing**: Change tracking

---

## 📚 Related Documentation

- **[System Architecture](ARCHITECTURE.md)** - Overall system design
- **[XML Schema Design](XML_GENERATION.md)** - XML structure and validation
- **[GitHub Actions Setup](GITHUB_ACTIONS.md)** - Automation configuration
- **[Troubleshooting](TROUBLESHOOTING.md)** - Common API issues and solutions 