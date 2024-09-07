#IPcanonicalization.

IP canonicalization validator Tool



IP canonicalization ensures that domain names resolve to their corresponding IP addresses accurately. 
Failures in this process could lead to misidentification of web resources, potential security vulnerabilities, 
and erroneous actions taken based on incorrect IP-to-hostname mappings, possibly resulting in unauthorized access, 
data manipulation, or unintended operations.




1. IP Canonicalization Process
     For each URL in the subdomains list:
       Get IP Address
         Extract the hostname from the URL.
         Retrieve the IP address using
   `socket.gethostbyname()`.
       
       Check Status Code
         Get the HTTP status code of the URL using `requests.get()`.
       
       Check Web Status
         Get the HTTP status code of the IP address using `requests.head()`.
         
       Resolve Hostname
         Perform a reverse DNS lookup to get the hostname from the IP address using `socket.gethostbyaddr()`.
         
       Cloudflare Check
         Check if the site uses Cloudflare by inspecting response headers.
         
       Comparison and Logging
         Compare the original hostname and the resolved hostname.
         
         Log the results based on the comparison:
           If matching or specific conditions are met (e.g., Cloudflare detected, status codes match/mismatch).
Result:
    The tool detected discrepancies between IP addresses and domain names in the analyzed subdomains'
