
# German:
# blackfrog
Blackfrog-Lock: Ein Python-Skript, das sich als Benutzer-Shell in der Registrierung registriert, nach dem Neustart eine Vollbildsperre anzeigt und den Task-Manager/das Herunterfahren blockiert. Die Entsperrung ist nur durch das Lösen eines Rätsels möglich. Malware-ähnliches Verhalten – nur für Bildungszwecke in einer VM verwenden.

# Blackfrog-Lock (Demonstration) — README & Disclaimer

**Kurz:** Dieses Repository enthält eine *Demonstration* eines Shell-Hijack-Lockers.  
**WICHTIG:** Dieses Projekt darf **nur** zu Forschungs- oder Lehrzwecken in isolierten Umgebungen (z. B. Virtual Machine) verwendet werden.
# Warnung!!!
unser team übernimmt keine haftung bei sach oder personschäden bei ausführen der skripte

---

## Warnung — lesen bevor du irgendetwas machst
Dieses Programm verändert System-Registry-Einstellungen und kann Rechner unbrauchbar machen. Veröffentlichung, Verbreitung oder Einsatz auf fremden Systemen **ohne ausdrückliche Zustimmung** ist illegal und kann strafrechtlich verfolgt werden. Nutze dieses Repo **nur** in einer VM, die du selbst kontrollierst.

# installation
natürlich musst du python auf dem pc haben
um zu starten musst du den installer skript ausführen (import pywin32.py)
nun musst du im code ''your question'' und ''your answer'' durch deine fragen und antworten austauschen
dann kannst du blackfrog starten
---

## Nutzungsempfehlung (sicher)
. Verwende eine frische Windows-VM (Snapshot vor Änderungen).   


---

## Wiederherstellung (wenn du aus Versehen gesperrt wirst)
Starte Windows im **Abgesicherten Modus mit Eingabeaufforderung** und gehe in cmd und schreibe: reg add "HKCU\Software\Microsoft\Windows NT\CurrentVersion\Winlogon" /v Shell /d explorer.exe /f
     dann den pc neustarten und alles ist gut:)

  # English:

  # blackfrog
Blackfrog-Lock: A Python script that registers itself as a user shell in the registry, displays a full-screen lock after rebooting, and blocks Task Manager/Shutdown. Unlocking is only possible by answering a puzzle. Malware-like behavior—use only for educational purposes in a VM.
  # Blackfrog-Lock (Demonstration) — README & Disclaimer

**In Brief:** This repository contains a *demonstration* of a shell hijack lock.
**IMPORTANT:** This project may **only** be used for research or teaching purposes in isolated environments (e.g., virtual machines).

# Warning!!!
Our team assumes no liability for property damage or personal injury resulting from the execution of the scripts.

---

## Warning — Read before you do anything
This program modifies system registry settings and can render computers unusable. Publishing, distributing, or using it on third-party systems **without explicit consent** is illegal and may result in criminal prosecution. Use this repo **only** in a VM under your control.

# Installation
To start, you must run the installer script (import pywin32.py).
Now, in the code, you must replace ''your question'' and ''your answer'' with your questions and answers.
Then you can start Blackfrog.
---

## Recommended Use (Safe)
. Use a fresh Windows VM (snapshot before changes).

---

## Recovery (if you accidentally get locked out)
Start Windows in **Safe Mode with Command Prompt** and go to cmd and type: reg add "HKCU\Software\Microsoft\Windows NT\CurrentVersion\Winlogon" /v Shell /d explorer.exe /f
then restart the PC and everything will be fine :)

  

