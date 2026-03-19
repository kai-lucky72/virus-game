# Neural Strike: RCA Cybersecurity Final Project

*Developed for Rwanda Coding Academy - March 2026*

This project demonstrates a multi-stage "Trojan Horse" attack simulation, featuring a custom Dino Jump game, a persistent interactive reverse shell, and a dedicated security cleanup tool.

---

## 1. Installation & Setup

### For the Attacker (Teacher/Attacker Machine)

1. **Requirements**: Python 3.x installed.
2. **Steps**:
    - Copy `attacker.py` to your machine.
    - Open a terminal and run: `python attacker.py`
    - The console will display `[*] Listening for incoming NeuralStrike connections...`.
3. **Network**: Ensure you are on the same Wi-Fi as the target machine. Note your IP (default: `10.12.74.152`).

### For the Target (Victim Machine)

1. **Requirements**: Windows 10/11.
2. **Steps**:
    - Run `dist\NeuralStrike.exe`.
3. **The Trigger**: The backdoor will automatically attempt to "phone home" to the attacker's IP. If it fails, use the **F1** manual override to type the attacker's IP.

---

## 2. The Gaming Process (User Experience)

To the victim, the application appears as a legitimate high-performance game:

- **Phase 1: Disclaimer**: A professional `tkinter` modal notifies the user about the simulation's intent before anyone proceeds.
- **Phase 2: Dependency Staging**: A dynamic progress bar simulates the installation of "required media components" (VLC). This provides cover for the background backdoor initialization.
- **Phase 3: The Game**: A fully playable "Dino Jump" clone. While the user is focused on the gameplay, the shell connection is established silently in a separate non-daemon thread.

---

## 4. Attack Methodology & Persistence

This project satisfies all RCA technical requirements:

- **Interactive Reverse Shell**: Unlike a basic beacon, this shell supports real-time commands, `cd` directory traversal, and robust error handling.
- **Reboot Persistence**: The Trojan copies itself to `%APPDATA%\DinoGame` and creates a **Registry Run Key** (`HKCU\Software\Microsoft\Windows\CurrentVersion\Run\NeuralStrike`).
- **Survivability**: Even if the game window is closed, the backdoor thread continues to run in the background. If the system restarts, the Trojan launches automatically upon user login.

---

## 5. Detection & Prevention (Defensive Measures)

How to defend against attacks like Neural Strike:

- **Registry Monitoring**: Legitimate games rarely need to add themselves to the "Run" keys. Use EDR tools to flag unauthorized registry modifications.
- **Network Filtering**: Block outgoing traffic on non-standard ports (like 4444). Implement a strict "Default Deny" firewall policy.
- **File Integrity**: Modern antivirus (Windows Defender) uses behavioral analysis to detect programs that spawn "hidden" subprocesses or "phone home" to private IP addresses.

---

## 6. Ethical Considerations

- **Intended Use**: This project is strictly for educational purposes within the RCA Cybersecurity curriculum.
- **Consent**: The inclusion of a mandatory pre-execution disclaimer ensures that all participants are informed of the simulation's nature.
- **Safety**: A dedicated `PersistenceRemover.exe` has been provided to ensure the target machine can be restored to a clean state immediately after the demo.

---
**RCA GRADING PROOF**: [Grading Sheet](file:///C:/Users/Lamelo/.gemini/antigravity/brain/2c840330-111b-48fb-a5ed-cc75a838de85/grading_proof.md)
