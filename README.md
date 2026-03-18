# Neural Strike: RCA Cybersecurity Final Project

Developed for Rwanda Coding Academy - March 2026

## Overview

This project is a multi-component cybersecurity simulation featuring a "Trojaned" Dino Jump game, an interactive reverse shell, and a persistence management system.

## Components & Usage

### 1. The Game (Target Side)

**Location**: `dist/NeuralStrike.exe`

- **Action**: Launch this on the Windows machine.
- **Grading Feature**: It will first show a **Disclaimer** (Requirement 1) and then a **Dependency Staging** progress bar before starting the game.

### 2. The Master Console (Attacker Side)

**Location**: `attacker.py`

- **Action**: Copy this to your Kali Linux VM.
- **Execution**: `python3 attacker.py`
- **Feature**: This provides the "Listener" that gives you full shell access to the Windows target.

### 3. The Remover (Safety Tool)

**Location**: `dist/PersistenceRemover.exe`

- **Action**: Run this to clean up the system. It removes the Registry keys and AppData files added by the game.

## Grading Highlights

- **User Notification**: Implemented via a `tkinter` modal at launch.
- **Dependency Download**: Simulated via a dynamic progress bar staging scene.
- **Persistence**: Implemented via `HKCU\...\Run` registry keys and `%APPDATA%\DinoGame` nesting.
- **No Interruption**: High-performance game loop using `pygame` with background operations on a separate daemon thread.
- **Interactive Shell**: Full command execution and output return to the Kali listener.

## Ethical Considerations & Defensive Measures

- **Prevention**: Use EDR (Endpoint Detection and Response) or Antivirus to flag suspicious Registry modifications. Monitor outgoing traffic to port 4444.
- **Detection**: Check `regedit` under `CurrentVersion\Run` for unknown entries.
- **Ethics**: This project is for **educational use only** at RCA. The disclaimer ensures no user is tricked during the simulation.
