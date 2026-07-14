"""MCP server tools for VetCare chatbot."""

from typing import Optional, List, Dict, Any
from .sheets_client import GoogleSheetsClient


# Initialize the sheets client
sheets_client = GoogleSheetsClient()


def search_services(query: str) -> str:
    """
    Search for veterinary services by keyword.
    
    Args:
        query: Search term to find in service names or descriptions
        
    Returns:
        JSON string with matching services
    """
    import json
    try:
        results = sheets_client.search_services(query)
        if not results:
            return json.dumps({"message": "No services found matching your query.", "results": []})
        return json.dumps({"count": len(results), "results": results[:10]}, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)})


def filter_services(
    category: Optional[str] = None,
    species: Optional[str] = None,
    price_max: Optional[int] = None,
    requires_appointment: Optional[bool] = None
) -> str:
    """
    Filter veterinary services by criteria.
    
    Args:
        category: Service category (e.g., 'Vaccination', 'Dental', 'Surgery')
        species: Animal species (e.g., 'Dog', 'Cat', 'Rabbit')
        price_max: Maximum price in EUR
        requires_appointment: Whether appointment is required
        
    Returns:
        JSON string with filtered services
    """
    import json
    try:
        results = sheets_client.filter_services(
            category=category,
            species=species,
            price_max=price_max,
            requires_appointment=requires_appointment
        )
        if not results:
            return json.dumps({"message": "No services found matching your criteria.", "results": []})
        return json.dumps({"count": len(results), "results": results[:10]}, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)})


def get_service_details(service_id: str) -> str:
    """
    Get detailed information about a specific service.
    
    Args:
        service_id: The service ID (e.g., 'MVC-001')
        
    Returns:
        JSON string with service details
    """
    import json
    try:
        service = sheets_client.get_service_by_id(service_id)
        if not service:
            return json.dumps({"error": f"Service with ID {service_id} not found."})
        return json.dumps(service, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)})


def check_availability(service_id: str) -> str:
    """
    Check availability for a specific service.
    
    Args:
        service_id: The service ID (e.g., 'MVC-001')
        
    Returns:
        JSON string with availability information
    """
    import json
    try:
        service = sheets_client.get_service_by_id(service_id)
        if not service:
            return json.dumps({"error": f"Service with ID {service_id} not found."})
        
        availability_info = {
            "service_id": service_id,
            "service_name": service.get("service_name"),
            "slots_this_week": service.get("slots_this_week", 0),
            "availability": service.get("availability"),
            "requires_appointment": service.get("requires_appointment"),
            "price_eur": service.get("price_eur"),
            "duration_min": service.get("duration_min")
        }
        return json.dumps(availability_info, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)})


def get_categories() -> str:
    """
    Get all available service categories.
    
    Returns:
        JSON string with list of categories
    """
    import json
    try:
        categories = sheets_client.get_categories()
        return json.dumps({"categories": categories})
    except Exception as e:
        return json.dumps({"error": str(e)})


def get_species_options() -> str:
    """
    Get all available species options.
    
    Returns:
        JSON string with list of species
    """
    import json
    try:
        species = sheets_client.get_species_options()
        return json.dumps({"species": species})
    except Exception as e:
        return json.dumps({"error": str(e)})


def get_special_offers() -> str:
    """
    Get all current special offers and promotions.
    
    Returns:
        JSON string with services that have special offers
    """
    import json
    try:
        offers = sheets_client.get_special_offers()
        if not offers:
            return json.dumps({"message": "No special offers available at this time.", "offers": []})
        return json.dumps({"count": len(offers), "offers": offers}, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)})


def get_available_services() -> str:
    """
    Get services with available appointment slots this week.
    
    Returns:
        JSON string with services that have available slots
    """
    import json
    try:
        services = sheets_client.get_available_services()
        if not services:
            return json.dumps({"message": "No services have available slots this week.", "services": []})
        return json.dumps({"count": len(services), "services": services[:10]}, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)})


def book_appointment(service_id: str, pet_name: str, owner_name: str, pet_species: str) -> str:
    """
    Book an appointment for a service.
    
    Args:
        service_id: The service ID (e.g., 'MVC-001')
        pet_name: Name of the pet
        owner_name: Name of the pet owner
        pet_species: Species of the pet
        
    Returns:
        JSON string with booking confirmation
    """
    import json
    try:
        service = sheets_client.get_service_by_id(service_id)
        if not service:
            return json.dumps({"error": f"Service with ID {service_id} not found."})
        
        if service.get("slots_this_week", 0) <= 0:
            return json.dumps({"error": "Sorry, no slots available for this service this week."})
        
        # Decrease available slots
        success = sheets_client.update_slots(service_id, -1)
        if not success:
            return json.dumps({"error": "Failed to book appointment. Please try again."})
        
        booking = {
            "status": "confirmed",
            "service_id": service_id,
            "service_name": service.get("service_name"),
            "pet_name": pet_name,
            "owner_name": owner_name,
            "pet_species": pet_species,
            "price_eur": service.get("price_eur"),
            "duration_min": service.get("duration_min"),
            "availability": service.get("availability"),
            "message": f"Appointment booked successfully for {pet_name}!"
        }
        return json.dumps(booking, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)})


# Tool definitions for MCP
TOOLS = [
    {
        "name": "search_services",
        "description": "Search for veterinary services by keyword in name or description",
        "function": search_services,
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search term to find in service names or descriptions"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "filter_services",
        "description": "Filter veterinary services by category, species, price, or appointment requirement",
        "function": filter_services,
        "parameters": {
            "type": "object",
            "properties": {
                "category": {
                    "type": "string",
                    "description": "Service category (e.g., 'Vaccination', 'Dental', 'Surgery')"
                },
                "species": {
                    "type": "string",
                    "description": "Animal species (e.g., 'Dog', 'Cat', 'Rabbit')"
                },
                "price_max": {
                    "type": "integer",
                    "description": "Maximum price in EUR"
                },
                "requires_appointment": {
                    "type": "boolean",
                    "description": "Whether appointment is required"
                }
            }
        }
    },
    {
        "name": "get_service_details",
        "description": "Get detailed information about a specific service by ID",
        "function": get_service_details,
        "parameters": {
            "type": "object",
            "properties": {
                "service_id": {
                    "type": "string",
                    "description": "The service ID (e.g., 'MVC-001')"
                }
            },
            "required": ["service_id"]
        }
    },
    {
        "name": "check_availability",
        "description": "Check availability and slots for a specific service",
        "function": check_availability,
        "parameters": {
            "type": "object",
            "properties": {
                "service_id": {
                    "type": "string",
                    "description": "The service ID (e.g., 'MVC-001')"
                }
            },
            "required": ["service_id"]
        }
    },
    {
        "name": "get_categories",
        "description": "Get all available service categories",
        "function": get_categories,
        "parameters": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "get_species_options",
        "description": "Get all available animal species options",
        "function": get_species_options,
        "parameters": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "get_special_offers",
        "description": "Get all current special offers and promotions",
        "function": get_special_offers,
        "parameters": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "get_available_services",
        "description": "Get services with available appointment slots this week",
        "function": get_available_services,
        "parameters": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "book_appointment",
        "description": "Book an appointment for a veterinary service",
        "function": book_appointment,
        "parameters": {
            "type": "object",
            "properties": {
                "service_id": {
                    "type": "string",
                    "description": "The service ID (e.g., 'MVC-001')"
                },
                "pet_name": {
                    "type": "string",
                    "description": "Name of the pet"
                },
                "owner_name": {
                    "type": "string",
                    "description": "Name of the pet owner"
                },
                "pet_species": {
                    "type": "string",
                    "description": "Species of the pet"
                }
            },
            "required": ["service_id", "pet_name", "owner_name", "pet_species"]
        }
    }
]
