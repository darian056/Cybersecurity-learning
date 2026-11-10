import socket
import sys
import time
import errno
from scapy.all import *
import logging

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)


def Stealth(target, start_port, ds_port):
    print(f"Scanning {target} for TCP ports (Stealth Mode)")

    if start_port == ds_port:
        ds_port += 1

    for x in range(start_port, ds_port+1):
        p = IP(dst=target) / TCP(dport=x, flags='S')
        response = sr1(p, timeout=0.5, verbose=0)
        
        if response and response.hasLayer(TCP) and "S" in response[TCP].flags and "A" in response[TCP].flags:
            print(f"port {x} is open")

        
            sr(IP(dst=target) / TCP(sport=response[TCP].dport, dport=response[TCP].sport, flags='R'), timeout=0.5, verbose=0)

        time.sleep(0.5)



    print("Stealth Scan complete")


def Scan(target,s, d ):
    try:
        target_ip = socket.gethostbyname(target)

        for port in range(s, d):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            result = s.connect_ex((target_ip, port))

            if result == 0:
                print(f"port {port} is open")
            elif result == errno.ECONNREFUSED:
                print(f"port {port} is closed")
            elif result == errno.ETIMEDOUT:
                print(f"port {port} is filtered")
            else:
                print(f"Error: could not resolve port {port}")
            
            s.close()

        time.sleep(0.05)

    except KeyboardInterrupt:
        print("\nexiting script")
        sys.exit(0)
    except socket.gaierror:
        print("Hostname could not be resolved")
        sys.exit(1)
    except socket.error:
        print("could not connect to the server")
        sys.exit(1)


def main():
    
    if len(sys.argv) == 5:
        target = sys.argv[1]
        start_port = int(sys.argv[2]) 
        ds_port = int(sys.argv[3])    
        
        if sys.argv[4] == "SS":
            Stealth(target, start_port, ds_port)
        elif sys.argv[4] == "S":       
            Scan(target, start_port, ds_port)
        else:
            print("SyntaxError: port_scanner.py <IP> <Start port> <End port> <S(Scan) or SS(Stealth Scan)>")
            sys.exit(1)
    else:
        print("Usage: python3 port_scanner.py <IP> <Start port> <End port> <S|SS>")
        sys.exit(1)


if __name__ == "__main__":
    main()
