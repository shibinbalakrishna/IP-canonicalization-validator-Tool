import socket
import requests
import ast
from colorama import Fore, Style, init
init()

def get_ip_address(url):
    """Get the IP address from the URL.

    Args:
        url (str): The URL to retrieve the IP address for.

    Returns:
        tuple: The hostname and IP address.
    """
    try:
        hostname = url.replace("http://", "").replace("https://", "").split('/')[0]
        ip_address = socket.gethostbyname(hostname)
        return hostname, ip_address
    except socket.gaierror as e:
        print(f"Error retrieving IP address for {url}: {e}", )
        return None, None


def get_hostname(ip_address):
    """Perform a reverse DNS lookup to get the hostname.

    Args:
        ip_address (str): The IP address to lookup.

    Returns:
        str: The resolved hostname.
    """
    try:
        hostname, _, _ = socket.gethostbyaddr(ip_address)
        return hostname
    except socket.herror as e:
        print(f"Error performing reverse DNS lookup for {ip_address}")
        return None


def get_status_code(url):
    """Get the HTTP status code for the given URL.

    Args:
        url (str): The URL to check.

    Returns:
        int: The HTTP status code.
    """
    try:
        response = requests.get(url, allow_redirects=False)
        return response.status_code
    except requests.RequestException as e:
        print(f"Error fetching status code for {url}: {e}", )
        return None


def get_web_status(ip_address):
    """Check the web status of the given IP address.

    Args:
        ip_address (str): The IP address to check.

    Returns:
        int: The HTTP status code.
    """
    try:
        url = "http://" + ip_address
        response = requests.head(url)
        return response.status_code
    except requests.RequestException as e:
        print(f"Error fetching web status for {ip_address}: {e}", )
        return None


def is_using_cloudflare(url):
    """Check if the URL is using Cloudflare.

    Args:
        url (str): The URL to check.

    Returns:
        bool: True if using Cloudflare, False otherwise.
    """
    try:
        response = requests.get(url)
        headers = response.headers
        cloudflare_headers = ['CF-RAY', 'Server']
        for header in cloudflare_headers:
            if header in headers and 'cloudflare' in headers[header].lower():
                return True
        return False
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}", )
        return False


def ip_canonicalization(url):
    """Perform IP canonicalization for the given URL.

    Args:
        url (str): The URL to canonicalize.
    """
    try:
        original_hostname, ip_address = get_ip_address(url)
        if not original_hostname or not ip_address:
            print(f"Unable to retrieve IP address for {url}")
            return

        status_code = get_status_code(url)
        web_status_code = get_web_status(ip_address)
        resolved_hostname = get_hostname(ip_address)

        print(f"The IP address of {original_hostname} is {ip_address}")
        print(f"The hostname resolved from IP address {ip_address} is {resolved_hostname}")

        if resolved_hostname or resolved_hostname is None:
            if is_using_cloudflare(url):
                print("The IP address and domain name resolve to the same URL.")
            elif (status_code == 301 or status_code == 302) and (web_status_code != 200 or web_status_code == 403):
                print("The IP address and domain name resolve to the same URL.")
            elif status_code in {301, 302, 200} and (web_status_code not in {200, 302, 301} or web_status_code == 403):
                print("The IP address and domain name resolve to the same URL.")
            elif original_hostname == resolved_hostname:
                print("The IP address and domain name resolve to the same URL.")
            else:
                print(Fore.CYAN +"The IP address and domain name do NOT resolve to the same URL"+Style.RESET_ALL)
                data = {
                    "original_hostname": original_hostname,
                    "ip_address": ip_address
                }
                print(f"{data}")
        else:
            print(Fore.CYAN +"The IP address and domain name do NOT resolve to the same URL."+Style.RESET_ALL)
            data = {
                "original_hostname": original_hostname,
                "ip_address": ip_address
            }
            print(f"{data}")
    except Exception as e:
        print(f"An unexpected error occurred during IP canonicalization for {url}: {e}", )


def main():
    """Main function."""
    try:

    
        url=input("Enter url:")
        if url.startswith('https://') or url.startswith('http://'):
            ip_canonicalization(url)
        elif "." not in url:
            print(print(Fore.RED+"Recheck your entered URL:"+url+Style.RESET_ALL))
        else:
            print(Fore.RED+"Ensure your URL contain http:// or https:// schema"+Style.RESET_ALL)
    except Exception as e:
        print("An unexpected error occurred: {}".format(e))



if __name__ == "__main__":
    main()
