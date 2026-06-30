import requests

def make_request(method, url, **kwargs):
    """
    Wrapper around requests to handle common errors.
    """
    try:
        response = requests.request(method, url, timeout=30, **kwargs)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {str(e)}")