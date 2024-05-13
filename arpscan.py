import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)  # Masquer les avertissements scapy
from scapy.all import *

def discover_devices():
    # Créer une requête ARP pour découvrir les appareils sur le réseau local
    arp_request = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst="192.168.1.0/24")
    
    # Envoyer la requête ARP et attendre les réponses
    devices = srp(arp_request, timeout=2, verbose=False)[0]
    
    # Afficher les adresses IP des appareils découverts
    print("Devices discovered on the local network:")
    for _, device in devices:
        print(device[ARP].psrc)

if __name__ == "__main__":
    discover_devices()