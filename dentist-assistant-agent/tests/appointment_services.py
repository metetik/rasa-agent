from unittest.mock import patch
from actions.services.appointment_services import check_dentist_availability
from datetime import datetime
import requests

def test_check_dentist_availability():
    # Mock the requests.get() function to return a list of appointments
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [
            {
                "start_date": "2022-01-01T09:00:00",
                "end_date": "2022-01-01T09:30:00",
            },
            {
                "start_date": "2022-01-01T10:00:00",
                "end_date": "2022-01-01T10:30:00",
            },
        ]

        # Test case where the dentist is available
        dentist = {"id": 1}
        start_date = datetime.fromisoformat("2022-01-01T11:00:00")
        end_date = datetime.fromisoformat("2022-01-01T11:30:00")
        assert check_dentist_availability(dentist, start_date, end_date) == True

        # Test case where the dentist is not available
        start_date = datetime.fromisoformat("2022-01-01T09:00:00")
        end_date = datetime.fromisoformat("2022-01-01T09:30:00")
        assert check_dentist_availability(dentist, start_date, end_date) == False

        start_date = datetime.fromisoformat("2022-01-01T09:00:00")
        end_date = None
        assert check_dentist_availability(dentist, start_date, end_date) == False

        start_date = datetime.fromisoformat("2022-01-01T08:45:00")
        end_date = datetime.fromisoformat("2022-01-01T09:15:00")
        assert check_dentist_availability(dentist, start_date, end_date) == False
        
        start_date = datetime.fromisoformat("2022-01-01T09:10:00")
        end_date = datetime.fromisoformat("2022-01-01T09:25:00")
        assert check_dentist_availability(dentist, start_date, end_date) == False

        # Test case where the API request fails
        mock_get.side_effect = requests.exceptions.RequestException
        assert check_dentist_availability(dentist, start_date, end_date) == False