# Secure-Login-Page
Secure Login in Python (Flask) with TOTP

Dieses Repository enthält eine einfache Login-Seite mit TOTP-Authentifizierung. 
Secure-Login-Page wurde in Python geschrieben und verwendet die Framework Flask.

Installation

Erstellen Sie einen RSA-Schlüssel, indem Sie den folgenden Befehl ausführen:

    python generate_rsa_key.py


Kopieren sie den RSA-Schlüssel

    cp secret_key.pem static/img/secret_key.pem

Secure-Login-Page Starten

    python3 main.py

Nun regestriren sie sich hierzu öffnen sie den Webbrowser und geben die IP ihres gerätes ein.

    z.b. 192.168.178.5

Daneben mit Doppelpunkten getrennt den Port was hier 8080 wäre.
    
    z.b. 192.168.178:5:8080
    
Nun noch die seite register öffnen.
   
    z.b. 192.168.178.5:8080/register
