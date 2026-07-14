"""Google Sheets client for fetching veterinary services data."""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from typing import List, Dict, Any, Optional
import os
from dotenv import load_dotenv

load_dotenv()


class GoogleSheetsClient:
    """Client for interacting with Google Sheets."""

    def __init__(self):
        self.spreadsheet_id = os.getenv("SPREADSHEET_ID", "1JhSODtviGHzXru6Eb5MhfXfVIF5vtJk3pclzzv7j2l4")
        self.credentials_path = os.getenv("GOOGLE_SHEETS_CREDENTIALS", "credentials/service_account.json")
        self._client = None
        self._worksheet = None

    def _connect(self):
        """Establish connection to Google Sheets."""
        if self._client is None:
            scope = [
                "https://spreadsheets.google.com/feeds",
                "https://www.googleapis.com/auth/drive"
            ]
            credentials = ServiceAccountCredentials.from_json_keyfile_name(
                self.credentials_path, scope
            )
            self._client = gspread.authorize(credentials)
            spreadsheet = self._client.open_by_key(self.spreadsheet_id)
            self._worksheet = spreadsheet.sheet1

    def get_all_services(self) -> List[Dict[str, Any]]:
        """Fetch all veterinary services from the spreadsheet."""
        self._connect()
        records = self._worksheet.get_all_records()
        return records

    def get_service_by_id(self, service_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific service by its ID."""
        services = self.get_all_services()
        for service in services:
            if service.get("service_id") == service_id:
                return service
        return None

    def search_services(self, query: str) -> List[Dict[str, Any]]:
        """Search services by keyword in name or description."""
        services = self.get_all_services()
        query_lower = query.lower()
        results = []
        for service in services:
            name = str(service.get("service_name", "")).lower()
            description = str(service.get("description", "")).lower()
            if query_lower in name or query_lower in description:
                results.append(service)
        return results

    def filter_services(
        self,
        category: Optional[str] = None,
        species: Optional[str] = None,
        price_max: Optional[int] = None,
        requires_appointment: Optional[bool] = None
    ) -> List[Dict[str, Any]]:
        """Filter services by various criteria."""
        services = self.get_all_services()
        results = services

        if category:
            results = [s for s in results if s.get("category", "").lower() == category.lower()]

        if species:
            results = [s for s in results if s.get("species", "").lower() == species.lower()]

        if price_max is not None:
            results = [s for s in results if s.get("price_eur", 0) <= price_max]

        if requires_appointment is not None:
            results = [s for s in results if s.get("requires_appointment") == requires_appointment]

        return results

    def get_categories(self) -> List[str]:
        """Get all unique service categories."""
        services = self.get_all_services()
        categories = list(set(s.get("category", "") for s in services if s.get("category")))
        return sorted(categories)

    def get_species_options(self) -> List[str]:
        """Get all unique species options."""
        services = self.get_all_services()
        species = list(set(s.get("species", "") for s in services if s.get("species")))
        return sorted(species)

    def get_special_offers(self) -> List[Dict[str, Any]]:
        """Get services with special offers."""
        services = self.get_all_services()
        return [s for s in services if s.get("special_offer")]

    def get_available_services(self) -> List[Dict[str, Any]]:
        """Get services with available slots this week."""
        services = self.get_all_services()
        return [s for s in services if s.get("slots_this_week", 0) > 0]

    def update_slots(self, service_id: str, slots_change: int) -> bool:
        """Update available slots for a service."""
        self._connect()
        try:
            services = self.get_all_services()
            for idx, service in enumerate(services):
                if service.get("service_id") == service_id:
                    current_slots = service.get("slots_this_week", 0)
                    new_slots = max(0, current_slots + slots_change)
                    row_number = idx + 2  # +2 because row 1 is header
                    self._worksheet.update_cell(row_number, 8, new_slots)  # Column 8 is slots_this_week
                    return True
            return False
        except Exception as e:
            print(f"Error updating slots: {e}")
            return False
