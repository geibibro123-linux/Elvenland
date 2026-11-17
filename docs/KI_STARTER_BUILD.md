# Kleines KI-Startpaket erzeugen

Das vollständige Elvenland-Paket zuerst aufbauen und prüfen. Danach:

```bash
python tools/create_starter.py \
  --package-dir /pfad/zum/geprueften/elvenland \
  --zip /pfad/zur/ausgabe/Elvenland_KIStart.zip
```

Der Aufruf erstellt eine ZIP mit genau einer obersten Ebene `elvenland/` und daneben `MASTER_PROMPT.txt`. Mit `--prompt-output` lässt sich der separate Promptpfad ändern. Beide Ausgaben müssen außerhalb des Eingabeverzeichnisses liegen.

Enthalten sind ausgewählte UTF-8-Texte aus dem Hauptverzeichnis sowie `docs/`, `data/`, `catalogs/`, `provenance/`, `verification/`, `indexes/`, `tools/`, `reference_code/` und `github/`. Dazu gehören `.yml`-/`.yaml`-Workflowvorlagen und `.gitignore`-Dateien. Medien, APKs, Archive, andere versteckte Dateien, Symlinks und Python-Caches werden ausgeschlossen. Bekannte sensible Dateinamen werden ausgelassen; erkannte private Schlüssel oder GitHub-Zugangstokens führen zum Abbruch. Das Skript ersetzt keine vorherige Datenschutzprüfung des Eingabepakets.

`INDEX.json` und Ursprungsmanifeste bleiben unverändert und beschreiben weiterhin das Vollpaket. Die zusätzlich erzeugte Datei `KI_START_HERE.md` erklärt diesen Unterschied. Ausschließlich `KI_STARTER_MANIFEST.json` beschreibt die tatsächlich enthaltenen Startpaketdateien mit Pfad, Bytezahl und SHA-256.

Der Aufbau nutzt feste ZIP-Zeitstempel, liest das fertige Archiv vollständig zur CRC-Prüfung und veröffentlicht keine ZIP ab 30 MB. Zu große oder nicht als UTF-8 lesbare Einzeldokumente werden gezählt und ausgelassen. Fehlt eine der vier Pflichtdateien `INDEX.json`, `MASTER_PROMPT.md`, `START_HERE.md` oder `STATUS.json`, bricht der Ablauf ab.

Das Skript verändert keine Quelldatei und führt keine enthaltenen Projektwerkzeuge aus. Es erstellt kein APK und ändert keine GitHub-Freigabe. Eine enthaltene Workflowvorlage belegt weder einen ausgeführten GitHub-Build noch einen veröffentlichten Release.
