"""
Mobile Data Service - Loads and queries mobile phone data from JSON
"""
import json
import os
import re
from typing import List, Dict, Any, Optional
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


def _parse_price(price_str: Any) -> Optional[float]:
    """Parse price string and extract numeric value in INR"""
    if not price_str or price_str is None:
        return None
    price_str = str(price_str).replace(',', '').replace('INR', '').replace('PKR', '').replace('CNY', '').replace('USD', '').replace('AED', '').replace('₹', '').replace('$', '').strip()
    try:
        return float(price_str)
    except (ValueError, TypeError):
        return None


def _parse_numeric(value: Any, unit: str = '') -> Optional[float]:
    """Parse numeric value from string (e.g., '6GB' -> 6.0, '3000mAh' -> 3000.0)"""
    if not value or value is None:
        return None
    value_str = str(value).replace(unit, '').replace(',', '').strip()
    try:
        return float(value_str)
    except (ValueError, TypeError):
        return None


class MobileDataService:
    """Service to load and query mobile phone data from JSON"""
    
    def __init__(self, json_path: str):
        self.json_path = json_path
        self.data: List[Dict[str, Any]] = []
        self._load_data()
    
    def _load_data(self):
        """Load JSON data and normalize fields"""
        try:
            with open(self.json_path, 'r', encoding='utf-8') as f:
                raw_data = json.load(f)
            
            # Normalize and clean data
            self.data = []
            for record in raw_data:
                normalized_record = self._normalize_record(record)
                self.data.append(normalized_record)
            
            logger.info(f"Loaded {len(self.data)} mobile phone records from JSON")
            
        except FileNotFoundError:
            logger.error(f"JSON file not found: {self.json_path}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing JSON: {e}", exc_info=True)
            raise
        except Exception as e:
            logger.error(f"Error loading JSON: {e}", exc_info=True)
            raise
    
    def _normalize_record(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize a record by extracting numeric values"""
        normalized = record.copy()
        
        # Parse price (India) - primary price for our use case
        if 'Launched Price (India)' in normalized:
            normalized['Price_INR'] = _parse_price(normalized['Launched Price (India)'])
        
        # Parse numeric fields
        if 'RAM' in normalized:
            normalized['RAM_GB'] = _parse_numeric(normalized['RAM'], 'GB')
        
        if 'Battery Capacity' in normalized:
            normalized['Battery_mAh'] = _parse_numeric(normalized['Battery Capacity'], 'mAh')
        
        if 'Mobile Weight' in normalized:
            normalized['Weight_g'] = _parse_numeric(normalized['Mobile Weight'], 'g')
        
        if 'Screen Size' in normalized:
            normalized['Screen_Size_inches'] = _parse_numeric(normalized['Screen Size'], 'inches')
        
        return normalized
    
    def search_mobiles(
        self,
        brand: Optional[str] = None,
        max_price_inr: Optional[float] = None,
        min_price_inr: Optional[float] = None,
        min_ram_gb: Optional[float] = None,
        min_battery_mah: Optional[float] = None,
        max_weight_g: Optional[float] = None,
        min_screen_size: Optional[float] = None,
        max_screen_size: Optional[float] = None,
        processor_contains: Optional[str] = None,
        camera_contains: Optional[str] = None,
        exclude_apple: bool = False,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Search mobile phones based on filters
        
        Args:
            brand: Company/Brand name (e.g., "Samsung", "Apple")
            max_price_inr: Maximum price in INR
            min_price_inr: Minimum price in INR
            min_ram_gb: Minimum RAM in GB
            min_battery_mah: Minimum battery capacity in mAh
            max_weight_g: Maximum weight in grams
            min_screen_size: Minimum screen size in inches
            max_screen_size: Maximum screen size in inches
            processor_contains: Processor name contains (case-insensitive)
            camera_contains: Camera specs contains (case-insensitive)
            exclude_apple: If True, exclude Apple/iOS phones (for Android-only searches)
            limit: Maximum number of results
        
        Returns:
            List of mobile phone records as dictionaries
        """
        results = []
        
        for record in self.data:
            # Apply filters
            if brand and brand.lower() not in str(record.get('Company Name', '')).lower():
                continue
            
            # Exclude Apple/iOS phones when Android is requested
            if exclude_apple and str(record.get('Company Name', '')).lower() == 'apple':
                continue
            
            # Price filters
            price_inr = record.get('Price_INR')
            if price_inr is not None:
                if max_price_inr and price_inr > max_price_inr:
                    continue
                if min_price_inr and price_inr < min_price_inr:
                    continue
            
            # RAM filter
            ram_gb = record.get('RAM_GB')
            if min_ram_gb and (ram_gb is None or ram_gb < min_ram_gb):
                continue
            
            # Battery filter
            battery_mah = record.get('Battery_mAh')
            if min_battery_mah and (battery_mah is None or battery_mah < min_battery_mah):
                continue
            
            # Weight filter
            weight_g = record.get('Weight_g')
            if max_weight_g and (weight_g is not None and weight_g > max_weight_g):
                continue
            
            # Screen size filters
            screen_size = record.get('Screen_Size_inches')
            if min_screen_size and (screen_size is None or screen_size < min_screen_size):
                continue
            if max_screen_size and (screen_size is not None and screen_size > max_screen_size):
                continue
            
            # Processor filter
            processor = str(record.get('Processor', '')).lower()
            if processor_contains and processor_contains.lower() not in processor:
                continue
            
            # Camera filter
            back_camera = str(record.get('Back Camera', '')).lower()
            if camera_contains and camera_contains.lower() not in back_camera:
                continue
            
            # Build result record (only include original fields + normalized numeric fields)
            result = {
                'Company Name': record.get('Company Name', ''),
                'Model Name': record.get('Model Name', ''),
                'Mobile Weight': record.get('Mobile Weight', ''),
                'RAM': record.get('RAM', ''),
                'Front Camera': record.get('Front Camera', ''),
                'Back Camera': record.get('Back Camera', ''),
                'Processor': record.get('Processor', ''),
                'Battery Capacity': record.get('Battery Capacity', ''),
                'Screen Size': record.get('Screen Size', ''),
                'Launched Price (India)': record.get('Launched Price (India)', ''),
                'Launched Year': record.get('Launched Year', ''),
            }
            # Add normalized numeric fields
            if 'Price_INR' in record:
                result['Price_INR'] = record['Price_INR']
            if 'RAM_GB' in record:
                result['RAM_GB'] = record['RAM_GB']
            if 'Battery_mAh' in record:
                result['Battery_mAh'] = record['Battery_mAh']
            if 'Weight_g' in record:
                result['Weight_g'] = record['Weight_g']
            if 'Screen_Size_inches' in record:
                result['Screen_Size_inches'] = record['Screen_Size_inches']
            
            results.append(result)
            
            # Stop if limit reached
            if len(results) >= limit:
                break
        
        return results
    
    def get_mobile_by_model(self, model_name: str) -> Optional[Dict[str, Any]]:
        """Get a specific mobile phone by model name with fuzzy matching"""
        # Clean and normalize model name for better matching
        normalized_search = model_name.strip()
        
        # Remove common prefixes that might confuse matching
        # e.g., "Samsung Galaxy Xcover 5" -> "Galaxy Xcover 5"
        prefixes_to_remove = ['samsung ', 'apple ', 'iphone ', 'oneplus ', 'xiaomi ', 'vivo ', 'oppo ', 'realme ']
        for prefix in prefixes_to_remove:
            if normalized_search.lower().startswith(prefix):
                normalized_search = normalized_search[len(prefix):].strip()
        
        # Try exact substring match first
        for record in self.data:
            model = str(record.get('Model Name', '')).lower()
            if normalized_search.lower() in model:
                return self._build_result_record(record)
        
        # If no match, try with just the key parts (remove storage variants like "64GB", "128GB")
        key_parts = re.sub(r'\s*\d+gb\s*', '', normalized_search, flags=re.IGNORECASE)
        key_parts = re.sub(r'\s*\d+gb\s*', '', key_parts, flags=re.IGNORECASE)  # Remove all storage variants
        key_parts = key_parts.strip()
        
        if key_parts and key_parts != normalized_search:
            for record in self.data:
                model = str(record.get('Model Name', '')).lower()
                if key_parts.lower() in model:
                    return self._build_result_record(record)
        
        # If still no match, try reverse: check if model name contains search term
        # Split search term into words and try matching any significant word
        words = [w for w in normalized_search.split() if len(w) > 2]  # Ignore short words
        for word in words:
            for record in self.data:
                model = str(record.get('Model Name', '')).lower()
                if word.lower() in model:
                    return self._build_result_record(record)
        
        return None
    
    def _build_result_record(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """Build a result record with original and normalized fields"""
        result = {
            'Company Name': record.get('Company Name', ''),
            'Model Name': record.get('Model Name', ''),
            'Mobile Weight': record.get('Mobile Weight', ''),
            'RAM': record.get('RAM', ''),
            'Front Camera': record.get('Front Camera', ''),
            'Back Camera': record.get('Back Camera', ''),
            'Processor': record.get('Processor', ''),
            'Battery Capacity': record.get('Battery Capacity', ''),
            'Screen Size': record.get('Screen Size', ''),
            'Launched Price (India)': record.get('Launched Price (India)', ''),
            'Launched Year': record.get('Launched Year', ''),
        }
        # Add normalized numeric fields
        if 'Price_INR' in record:
            result['Price_INR'] = record['Price_INR']
        if 'RAM_GB' in record:
            result['RAM_GB'] = record['RAM_GB']
        if 'Battery_mAh' in record:
            result['Battery_mAh'] = record['Battery_mAh']
        if 'Weight_g' in record:
            result['Weight_g'] = record['Weight_g']
        if 'Screen_Size_inches' in record:
            result['Screen_Size_inches'] = record['Screen_Size_inches']
        return result
    
    def compare_mobiles(self, model_names: List[str]) -> List[Dict[str, Any]]:
        """Compare multiple mobile phones by model names (max 3 phones)"""
        results = []
        # Limit to max 3 phones
        model_names = model_names[:3]
        for model_name in model_names:
            mobile = self.get_mobile_by_model(model_name)
            if mobile:
                results.append(mobile)
        return results
    
    def get_brands(self) -> List[str]:
        """Get list of all unique brands"""
        brands = set()
        for record in self.data:
            company = record.get('Company Name')
            if company:
                brands.add(company)
        return sorted(list(brands))
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about the dataset"""
        years = [r.get('Launched Year') for r in self.data if r.get('Launched Year')]
        prices = [r.get('Price_INR') for r in self.data if r.get('Price_INR') is not None]
        
        brands = self.get_brands()
        
        stats = {
            'total_mobiles': len(self.data),
            'total_brands': len(brands),
            'brands': brands,
            'years_range': {
                'min': int(min(years)) if years else None,
                'max': int(max(years)) if years else None,
            }
        }
        if prices:
            stats['price_range_inr'] = {
                'min': float(min(prices)),
                'max': float(max(prices)),
            }
        return stats


# Singleton instance - will be initialized at startup
mobile_data_service: Optional[MobileDataService] = None

def initialize_mobile_data_service(json_path: Optional[str] = None):
    """Initialize the mobile data service"""
    global mobile_data_service
    if json_path is None:
        from app.core.config import settings
        json_path = settings.MOBILE_DATA_JSON_PATH
        # If relative path, try project root
        if not Path(json_path).is_absolute():
            json_path = Path(__file__).parent.parent.parent / json_path
    
    mobile_data_service = MobileDataService(str(json_path))
    logger.info("Mobile data service initialized")
    return mobile_data_service

def get_mobile_data_service() -> MobileDataService:
    """Get the mobile data service instance"""
    if mobile_data_service is None:
        initialize_mobile_data_service()
    return mobile_data_service
