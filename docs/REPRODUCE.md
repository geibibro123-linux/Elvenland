# Ressourcenpaket wiederholt erzeugen

Der Paketbau erstellt ein Daten-/Medienarchiv. Er kompiliert keine Android-App.

## Voraussetzungen

- Python 3.12.
- Die festgeschriebenen Python-Abhängigkeiten aus `requirements-extraction.txt`.
- FFmpeg sowie die Systembibliotheken libogg und libvorbis.
- Eine der in `provenance/SOURCE_INPUTS.json` anhand SHA-256 belegten APK-Dateien.
- Genügend freier Speicher für Eingabe, entpackte Quellen, exportierte Medien und die abschließende ZIP.

Beispiel für eine isolierte Python-Umgebung auf Linux. Die Befehle werden im übergeordneten Verzeichnis ausgeführt, das den Projektordner `elvenland/` enthält. Die virtuelle Umgebung und die Ausgabe liegen damit außerhalb dieses Projektordners:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r elvenland/requirements-extraction.txt
.venv/bin/python elvenland/tools/build_package.py \
  --apk Eingabe.apk \
  --package-dir build/elvenland \
  --zip dist/Elvenland_Offline_Neubaupaket_v1.zip
```

`build/elvenland` darf noch nicht existieren. Das Skript überschreibt kein vorhandenes Arbeitspaket. `--workers 2` ist der Standard für parallele Unity-Exporte. Das Skript prüft zuerst den vollständigen APK-Hash und danach jede in der aktuellen Quellenliste ausgewählte statische Quelldatei einzeln.

Bei Bedarf installieren Ubuntu-/Debian-Systeme `ffmpeg`, `libogg0` und `libvorbis0a` mit ihrem normalen Paketmanager.

## Vorbereitete GitHub-Vorlage

Die Datei `github/elvenland-package.yml` ist eine vorbereitete Workflow-Vorlage und wurde noch nicht auf GitHub ausgeführt. Sie startet ausschließlich manuell über `workflow_dispatch`. Beim Start muss der Nutzer eine öffentlich abrufbare HTTPS-URL zur Eingabe-APK angeben. Nach dem Download wird der APK-Hash gegen die zugelassenen Quellen geprüft; eine beliebige andere APK wird dadurch nicht automatisch akzeptiert.

Die Vorlage liest keine private APK-Quelle und benötigt keinen privaten Quelltoken. Ein öffentlich nicht abrufbarer Downloadlink erfüllt ihre Eingabeanforderung nicht. Der obige lokale Aufruf bleibt unabhängig davon möglich und benötigt nur die tatsächlich vorhandene verifizierte APK. Hinweise zum noch fehlenden Veröffentlichungsziel stehen in `docs/GITHUB_PUBLICATION.md`.

## Ablauf

1. Die geprüften Dokumente und bereinigten Daten werden in ein neues Zielverzeichnis kopiert.
2. Die statischen Medien werden vorübergehend im Arbeitsbereich extrahiert und einzeln mit dem Herkunftsmanifest verglichen. Dieser Rohdatenbestand ist kein Bestandteil des veröffentlichbaren Pakets.
3. UnityPy erzeugt Sprite-PNGs, Texture-PNGs und JSON-Metadaten. Dateiverweise zwischen Worldmap-Bundles werden ausdrücklich aufgelöst. Die 20 vorhandenen Sprachfassungen werden als lesbare JSON-Daten exportiert; deutsche und englische Referenztabellen werden zusätzlich für den KI-Einstieg bereitgestellt.
4. Audio wird in 194 IMA-WAVs und zwei Vorbis-Aufnahmen als WAV/OGG umgewandelt. Samplezahl, Kanäle und Abtastrate werden geprüft.
5. Kleine KI-lesbare Teilindizes, Assetverknüpfungen und eine lokale Bildübersicht werden erzeugt.
6. Die Rohcontainer werden vor der Paketbildung aus dem neuen Ausgabeverzeichnis entfernt. Die Eingabe-APK bleibt unverändert. Das veröffentlichbare Paket übernimmt ausschließlich die geprüften konvertierten Ausgaben und zugehörigen Unterlagen.
7. JSON-Dateien werden eingelesen, Dateihashes berechnet und das ZIP danach mit vollständiger CRC-Prüfung erneut gelesen.

Ausgaben neben der ZIP sind eine SHA-256-Datei und ein maschinenlesbarer Prüfbericht. Die ZIP enthält zusätzlich ihr eigenes Dateimanifest. Dieses Manifest schließt sich selbst, die alternative SHA-Liste und den Paketprüfbericht aus, um zirkuläre Hashbezüge zu vermeiden.

## Android-Werkzeuge sind ein späterer Schritt

Der hier installierte Godot-Editor ist 4.6.3. Die ursprüngliche Sitzung hatte keine passenden Android-Exportvorlagen und kein eingerichtetes Android SDK. Das ist im Paketbau kein Hindernis. Für die spätere App werden Godot mit passenden Exportvorlagen, OpenJDK 17 und Android SDK benötigt. Die konkrete Versionenkombination ist vor dem ersten APK-Build festzuschreiben; siehe `docs/SOFTWARE_AND_ENGINE.md`.
