# Reproduzierbarer Unity-Export

> Geltungsbereich: Dieser Bericht beschreibt den UnityFS-Teilbestand. Die zusätzlich exportierten Unity-Data-, Sprach- und Android-Ressourcen stehen in `PACKAGE_COVERAGE.md`.

Die Eingabe enthält UnityFS-Bundles aus einer bereits bereitgestellten APK. Das Skript verändert keine Quelldateien und erzeugt keinen Android-Build. Alle folgenden Pfade beziehen sich auf das Hauptverzeichnis des entpackten `elvenland/`-Pakets.

Das veröffentlichbare Paket enthält ausschließlich die geprüften konvertierten Bilder, Audio- und Metadatendateien sowie die zugehörigen Unterlagen. Unveränderte UnityFS-/FSB-Rohcontainer werden nicht beigelegt. Für eine erneute Extraktion wird eine der in `provenance/SOURCE_INPUTS.json` verifizierten APKs oder ein eigenes privates Eingabeverzeichnis mit den nachgewiesenen Quellen benötigt.

## Installation

```bash
python3 -m venv ../elvenland-tools-venv
../elvenland-tools-venv/bin/python -m pip install -r requirements-extraction.txt
```

Unter Windows lautet der entsprechende Interpreterpfad `..\elvenland-tools-venv\Scripts\python.exe`. Die virtuelle Umgebung liegt bewusst außerhalb des Paketordners, damit sie bei einem erneuten Paketbau nicht mitkopiert wird.

Für die Vorbis-Audiokonvertierung werden zusätzlich `ffmpeg`, `libogg` und `libvorbis` im Betriebssystem benötigt. Diese Programme und Bibliotheken werden durch `pip install` nicht installiert.

## Vollständiger Neubau aus einer verifizierten APK

```bash
../elvenland-tools-venv/bin/python tools/build_package.py --apk /pfad/zur/verifizierten.apk --package-dir ../elvenland-neubau --zip ../Elvenland_Neubau.zip
```

Den Eingabepfad durch die tatsächliche verifizierte APK ersetzen. Das neue Paketverzeichnis darf noch nicht existieren. Die Rohquellen bleiben in der eigenen Eingabe und werden nicht in das veröffentlichbare Paket übernommen. Der ausführliche Ablauf steht in `docs/REPRODUCE.md`.

## Optionaler einzelner Grafikexport mit vorhandenen Rohquellen

Die folgenden Befehle setzen ein eigenes externes Eingabeverzeichnis `../INPUT/` voraus, dessen `assets/android/`-Inhalt aus der verifizierten APK stammt. Dieses Verzeichnis ist kein Bestandteil des Pakets.

```bash
../elvenland-tools-venv/bin/python tools/export_assets.py --input ../INPUT/assets/android --output ../elvenland-visuals-reexport --workers 4
../elvenland-tools-venv/bin/python tools/summarize_animations.py --input ../elvenland-visuals-reexport
```

`--input` wird rekursiv nach der Dateisignatur UnityFS durchsucht. Die Dateiendung ist unerheblich. Alle Abhängigkeiten müssen aus demselben Datenbestand stammen. Externe CAB-Verweise werden anhand des vollständigen Bundlesatzes gezielt aufgelöst. Das Beispiel schreibt in ein separates Ausgabeverzeichnis. Die mitgelieferten Dateien unter `assets/visuals/` und ihr bestehendes Manifest bleiben dadurch unverändert.

## Ausgabe

Unter dem angegebenen Ausgabeverzeichnis enthält `sprites/` einzelne zugeschnittene PNG-Sprites und `textures/` die dekodierten Texturen einschließlich Atlanten. `metadata/` bewahrt die ausgelesenen Unity-Typbäume, darunter Sprite-Pivots, Transform-Daten, AnimationClips und AnimatorController. `bundles_index.csv` enthält pro Objekt Originalname, Quelldatei, Quellhash, Unity-Datei, Objekt-ID, Ausgabepfad, Pixelgröße und PNG-Hash. Fehler stehen in `bundles_errors.json`; die Zusammenfassung steht in `bundles_summary.json`.

Die Originalnamen werden zusätzlich zu sicheren Dateinamen im Index bewahrt. Ein Zahlensuffix und der Quellhash verhindern Kollisionen. Es werden weder Gebäudeleistungen noch Forschungskosten aus Dateinamen abgeleitet.

`animation_reference_catalog.json` verknüpft die nachgewiesenen Sprite-Referenzen der Animationen. Im mitgelieferten Paket liegt diese Datei unter `assets/visuals/animation_reference_catalog.json`. Sie ist keine fertige Godot-Animationsbibliothek: Die kompilierten Zeitkurven sind noch nicht in Godot-Animationsabläufe übertragen.

Die Anforderungen für die Extraktionswerkzeuge stehen in `requirements-extraction.txt`. Der dokumentierte erfolgreiche Prüflauf nutzte Python 3.12.14, UnityPy 1.25.4 und Pillow 13.0.0. Quell-Bundles melden Unity 6000.0.71f1. Aktuelle Paketdateien werden durch `MANIFEST.jsonl` und `SHA256SUMS.txt` im Hauptverzeichnis nachgewiesen.

## Audioergänzung

`tools/decode_vorbis_fsb5.py` verarbeitet die beiden Vorbis-Quellen. `tools/fmod_fsb5_ima_to_wav.py` enthält den Konverter für die 194 IMA-ADPCM-Quellen. Der vollständige Paketbau in `tools/build_package.py` ruft beide Wege auf und legt die aktuellen Dateien unter `assets/audio/` ab.

`catalogs/audio_clip_metadata.json` bewahrt die Unity-AudioClip-Metadaten. `catalogs/audio_inventory_196.json` ist der erhaltene historische Namens- und Prüfkatalog; dort enthaltene alte `wav/`-Pfade sind keine Paketpfade. Für die aktuelle Zuordnung von Clipnamen, Quellen, Ausgabepfaden und Prüfsummen ist `catalogs/audio_asset_links.json` maßgeblich. Der frühere Audio-Prüfbericht liegt unter `docs/AUDIO_REPORT.md`, der aktuelle Konvertierungsnachweis unter `verification/audio_export.json`.

## Grenzen

Die erzeugten Dateien sind exportierte Ressourcen und technische Metadaten. Ein Unity- oder Godot-Spielprojekt, eine vollständige Spielwirtschaft, eine fertige Forschungslogik und ein getesteter Android-Build entstehen daraus nicht automatisch.
