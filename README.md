# Haynes-Shockley-Korrektur
Eine kleine Sammlung an Scripten um die Daten des Experimentes auszuwerten

# Vorbereitung
Erstelle eine Datei `settings.txt`, die den Dateipfad zur Messung, die Laser-Kontakt distanz und die Laserspannung enthält. Der Dateipfad kann absolut oder relativ sein. Alle Werte müssen durch Kommata getrennt sein. Fließkommazahlen können wie in der englischen Schreibweise mit einem Punkt als Dezimaltrennzeichen angegeben werden.

# Anleitung
Das Programm kann von der Kommandozeile unter Windows mit `python auto_correction.py` und unter Linux mit `python3 auto_correction.py` aufgerufen werden. Es gibt Argumente, die übergeben werden können um die Ausgabe für Excel mit deutschen Einstellungen, Excel mit englischen Einstellungen und gnuplot zu vereinfachen. Diese können mit `python3 auto_correction.py help` oder `python auto_correction.py` angezeigt werden.
