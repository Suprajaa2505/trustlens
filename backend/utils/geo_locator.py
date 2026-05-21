import socket, requests

def resolve_ip(domain):
    try:
        return socket.gethostbyname(domain)
    except:
        return None

def locate_country(domain):
    ip = resolve_ip(domain)
    if not ip:
        return {"domain": domain, "ip": None, "country": "Unknown", "lat": None, "lon": None}
    try:
        res = requests.get(f"http://ip-api.com/json/{ip}", timeout=5).json()
        return {
            "domain": domain, "ip": ip,
            "country": res.get("country", "Unknown"),
            "lat": res.get("lat"), "lon": res.get("lon")
        }
    except:
        return {"domain": domain, "ip": ip, "country": "Unknown", "lat": None, "lon": None}