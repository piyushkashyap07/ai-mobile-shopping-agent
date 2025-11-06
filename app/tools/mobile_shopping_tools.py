"""
Mobile Shopping Tools - Tools for searching, comparing, and recommending mobile phones
"""
from typing import List, Dict, Any, Optional
from llama_index.core.tools import FunctionTool
from llama_index.core.workflow import Context
from app.services.mobile_data_service import get_mobile_data_service
import logging

logger = logging.getLogger(__name__)


async def search_mobile_phones(
    ctx: Context,
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
) -> Dict[str, Any]:
    """
    Search for mobile phones based on various criteria.
    
    Use this tool when users ask for phones matching specific criteria like:
    - "Best camera phone under ₹30,000"
    - "Samsung phones under ₹25,000"
    - "Android phones" (set exclude_apple=True)
    - "Compact Android phones" (set exclude_apple=True, max_screen_size=5.5)
    - "Phones with good battery"
    - "Compact phones with small screen"
    
    **CRITICAL**: When user asks for "Android" phones, you MUST set exclude_apple=True.
    Apple phones run iOS, not Android. Only non-Apple brands run Android.
    
    Args:
        brand: Company/Brand name (e.g., "Samsung", "Apple", "OnePlus")
        max_price_inr: Maximum price in Indian Rupees (INR)
        min_price_inr: Minimum price in Indian Rupees (INR)
        min_ram_gb: Minimum RAM in GB
        min_battery_mah: Minimum battery capacity in mAh
        max_weight_g: Maximum weight in grams (for compact/lightweight phones)
        min_screen_size: Minimum screen size in inches
        max_screen_size: Maximum screen size in inches (for compact phones)
        processor_contains: Processor name contains (e.g., "Snapdragon", "A17")
        camera_contains: Camera specs contains (e.g., "MP", "OIS")
        exclude_apple: MUST be True when user asks for Android phones. Excludes Apple/iOS phones.
        limit: Maximum number of results (default: 10)
    
    Returns:
        Dictionary with 'results' list containing mobile phone records
    """
    try:
        # Log CSV data source usage
        logger.info("=" * 60)
        logger.info("📊 DATA SOURCE: JSON Database")
        logger.info(f"🔍 Tool: search_mobile_phones")
        logger.info(f"📋 Parameters: brand={brand}, max_price={max_price_inr}, min_price={min_price_inr}, "
                   f"ram={min_ram_gb}, battery={min_battery_mah}, exclude_apple={exclude_apple}, limit={limit}")
        logger.info("=" * 60)
        
        service = get_mobile_data_service()
        results = service.search_mobiles(
            brand=brand,
            max_price_inr=max_price_inr,
            min_price_inr=min_price_inr,
            min_ram_gb=min_ram_gb,
            min_battery_mah=min_battery_mah,
            max_weight_g=max_weight_g,
            min_screen_size=min_screen_size,
            max_screen_size=max_screen_size,
            processor_contains=processor_contains,
            camera_contains=camera_contains,
            exclude_apple=exclude_apple,
            limit=limit
        )
        
        logger.info(f"✅ JSON Query Result: Found {len(results)} phones from JSON database")
        
        return {
            "success": True,
            "count": len(results),
            "results": results,
                    "data_source": "JSON"  # Add data source indicator
        }
    except Exception as e:
        logger.error(f"Error searching mobile phones: {e}", exc_info=True)
        return {
            "success": False,
            "error": str(e),
            "results": []
        }


async def compare_mobile_phones(
    ctx: Context,
    model_names: List[str]
) -> Dict[str, Any]:
    """
    Compare multiple mobile phone models side by side.
    
    Use this tool when users explicitly ask to compare phones, e.g.:
    - "Compare Pixel 8a vs OnePlus 12R"
    - "Compare iPhone 15 Pro vs Samsung Galaxy S24"
    
    Args:
        model_names: List of model names to compare (e.g., ["iPhone 15 Pro", "Samsung Galaxy S24"])
    
    Returns:
        Dictionary with comparison results
    """
    try:
        # Log CSV data source usage
        logger.info("=" * 60)
        logger.info("📊 DATA SOURCE: JSON Database")
        logger.info(f"🔍 Tool: compare_mobile_phones")
        logger.info(f"📋 Models to compare: {model_names}")
        logger.info("=" * 60)
        
        service = get_mobile_data_service()
        results = service.compare_mobiles(model_names)
        
        if len(results) == 0:
            logger.warning(f"❌ JSON Query Result: No matching phones found for comparison")
            return {
                "success": False,
                "error": "No matching phones found for comparison",
                "results": [],
                "data_source": "CSV"
            }
        
            logger.info(f"✅ JSON Query Result: Comparing {len(results)} phones from JSON database")
        
        return {
            "success": True,
            "count": len(results),
            "results": results,
                    "data_source": "JSON"  # Add data source indicator
        }
    except Exception as e:
        logger.error(f"Error comparing mobile phones: {e}", exc_info=True)
        return {
            "success": False,
            "error": str(e),
            "results": []
        }


async def get_mobile_details(
    ctx: Context,
    model_name: str
) -> Dict[str, Any]:
    """
    Get detailed information about a specific mobile phone model.
    
    Use this tool when users ask about a specific phone, e.g.:
    - "Tell me about iPhone 15 Pro"
    - "Details of Samsung Galaxy S24 Ultra"
    - "I like this phone, tell me more details"
    
    Args:
        model_name: Model name (can be partial, e.g., "iPhone 15 Pro", "Galaxy S24")
    
    Returns:
        Dictionary with mobile phone details
    """
    try:
        # Log CSV data source usage
        logger.info("=" * 60)
        logger.info("📊 DATA SOURCE: JSON Database")
        logger.info(f"🔍 Tool: get_mobile_details")
        logger.info(f"📋 Model: {model_name}")
        logger.info("=" * 60)
        
        service = get_mobile_data_service()
        result = service.get_mobile_by_model(model_name)
        
        if result is None:
            logger.warning(f"❌ JSON Query Result: Phone '{model_name}' not found in JSON database")
            return {
                "success": False,
                "error": f"Phone '{model_name}' not found. Try a different name or check spelling.",
                "result": None,
                "data_source": "CSV"
            }
        
            logger.info(f"✅ JSON Query Result: Found phone details for '{model_name}' from JSON database")
        
        return {
            "success": True,
            "result": result,
                    "data_source": "JSON"  # Add data source indicator
        }
    except Exception as e:
        logger.error(f"Error getting mobile details: {e}", exc_info=True)
        return {
            "success": False,
            "error": str(e),
            "result": None
        }


async def get_brand_list(
    ctx: Context
) -> Dict[str, Any]:
    """
    Get list of all available mobile phone brands/companies.
    
    Use this tool when users ask about available brands or want to filter by brand.
    
    Returns:
        Dictionary with list of brands
    """
    try:
        # Log CSV data source usage
        logger.info("=" * 60)
        logger.info("📊 DATA SOURCE: JSON Database")
        logger.info(f"🔍 Tool: get_brand_list")
        logger.info("=" * 60)
        
        service = get_mobile_data_service()
        brands = service.get_brands()
        
        logger.info(f"✅ JSON Query Result: Found {len(brands)} brands from JSON database")
        
        return {
            "success": True,
            "brands": brands,
            "count": len(brands),
                    "data_source": "JSON"  # Add data source indicator
        }
    except Exception as e:
        logger.error(f"Error getting brand list: {e}", exc_info=True)
        return {
            "success": False,
            "error": str(e),
            "brands": []
        }


def create_mobile_shopping_tools() -> List[FunctionTool]:
    """Create all mobile shopping tools"""
    tools = [
        FunctionTool.from_defaults(
            fn=search_mobile_phones,
            name="search_mobile_phones",
            description="Search for mobile phones based on criteria like brand, price, RAM, battery, camera, etc."
        ),
        FunctionTool.from_defaults(
            fn=compare_mobile_phones,
            name="compare_mobile_phones",
            description="Compare multiple mobile phone models side by side"
        ),
        FunctionTool.from_defaults(
            fn=get_mobile_details,
            name="get_mobile_details",
            description="Get detailed information about a specific mobile phone model"
        ),
        FunctionTool.from_defaults(
            fn=get_brand_list,
            name="get_brand_list",
            description="Get list of all available mobile phone brands/companies"
        ),
    ]
    
    return tools
