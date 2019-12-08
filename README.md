# Haynes-Shockley-Korrektur
Eine kleine Sammlung an Scripten um die Daten des Experimentes auszuwerten

# Vorbereitung
Die Daten (`scope_0.csv`, `scope_1.csv`, ...) müssen in einem Ordner mit dem Namen `data` stehen. Die Python files im gleichen Ordner wie der `data`. 

# Anleitung
Zunächst müssen die ersten drei Zeilen auskommentiert werden, da diese keine oder nur unvollständige Daten enthalten. Dafür wird einfach die Datei `comment-first-three-lines.py` ausgeführt. Dann wird die Datei `analyse.py` ausgeführt. Die korrigierten Daten werden in die entsprechenden Dateien im `data` Ordner geschrieben und es werden ein paar Dateien erstellt, die die charakteristischen Kenngrößen der Experimente zusammenfassen. 

# Modifikationen
Wichtige Dinge, die angepasst werden können, ist der `column_se` in `data_file.py` und die Werte im Array `data` in `analyse.py`. Bei Bedarf kann in der Datei `data_file.py` die letzten zwei Zeilen in der Methode `correct_minority_voltage` einkommentiert werden um ein einzelnes Bild der Regressionsgeraden, der Ausgangsspannung und der korrigierten Spannung zu erhalten.
