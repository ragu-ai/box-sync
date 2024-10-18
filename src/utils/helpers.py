import requests
from typing import Optional, Dict, Any
import os
from dotenv import load_dotenv
from src.utils.constants import Config

# Load environment variables
load_dotenv()


# Get OAuth2 credentials from environment variables
BOX_CLIENT_ID = os.getenv("BOX_CLIENT_ID")
BOX_CLIENT_SECRET = os.getenv("BOX_CLIENT_SECRET")
BOX_ACCESS_TOKEN = os.getenv("BOX_ACCESS_TOKEN")
BOX_REFRESH_TOKEN = os.getenv("BOX_REFRESH_TOKEN")


class RequestHelper:
    @staticmethod
    def refresh_access_token() -> Optional[str]:
        """Refresh the OAuth2 access token using the refresh token."""
        token_url = Config.API_BASE_URL+Config.OAUTH_PATH
        print(token_url)
        # Update the global token variables (or store in a secure location)
        global BOX_ACCESS_TOKEN, BOX_REFRESH_TOKEN
        
        payload = {
            "grant_type": "refresh_token",
            "client_id": BOX_CLIENT_ID,
            "client_secret": BOX_CLIENT_SECRET,
            "refresh_token": BOX_ACCESS_TOKEN
        }
        print(payload)
        
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        
        try:
            response = requests.post(token_url, data=payload, headers=headers)
            response.raise_for_status()  # Raise an error if the request failed
            
            token_data = response.json()
            
            
            BOX_ACCESS_TOKEN = token_data.get("access_token")
            BOX_REFRESH_TOKEN = token_data.get("refresh_token")
            
            print("Token refreshed successfully!")
            return BOX_ACCESS_TOKEN
        
        except requests.exceptions.RequestException as e:
            print(f"Error refreshing token: {e}")
            return None


    def request_helper_with_token_refresh(
        self,
        method: str,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        timeout: int = 10
    ) -> Optional[Dict[str, Any]]:
        """
        Helper function to handle HTTP requests with OAuth token refresh if token is expired (401).
        
        Args:
            method (str): HTTP method ('GET', 'POST', 'PUT', 'DELETE').
            url (str): The URL for the request.
            headers (dict, optional): Custom headers to include in the request.
            params (dict, optional): URL query parameters.
            data (dict, optional): Form data to send in POST/PUT requests.
            json (dict, optional): JSON data to send in POST/PUT requests.
            timeout (int, optional): Request timeout in seconds.
        
        Returns:
            dict: Parsed JSON response or text content if available, otherwise None.
        """
        if headers is None:
            headers = {}

        # Ensure we have the Authorization header with the current token
        headers.setdefault("Authorization", f"Bearer {BOX_ACCESS_TOKEN}")
        
        # Set default content type to JSON if not specified
        headers.setdefault("Content-Type", "application/json")

        try:
            # Make the initial request
            response = requests.request(
                method=method.upper(),
                url=url,
                headers=headers,
                params=params,
                data=data,
                json=json,
                timeout=timeout
            )
            
            # If the token is expired, refresh and retry
            if response.status_code == 401:
                print("Token expired, refreshing and retrying...")
                new_token = self.refresh_access_token()
                
                if new_token:
                    # Update the Authorization header with the new token
                    headers["Authorization"] = f"Bearer {new_token}"
                    
                    # Retry the request with the new token
                    response = requests.request(
                        method=method.upper(),
                        url=url,
                        headers=headers,
                        params=params,
                        data=data,
                        json=json,
                        timeout=timeout
                    )
            
            # Raise an error if the final request failed
            response.raise_for_status()

            # Return JSON response or text
            try:
                return response.json()
            except ValueError:
                return {"text": response.text}

        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            raise Exception(f"HTTP error occurred: {http_err}")
        except requests.exceptions.RequestException as req_err:
            print(f"Request error occurred: {req_err}")
            raise Exception(f"Request error occurred: {req_err}")


        return None
