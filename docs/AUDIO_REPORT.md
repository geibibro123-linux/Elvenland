# Elvenland: vervollständigte Audioextraktion

Prüfdatum: 17.11.2026. Dieser Bericht beschreibt die damalige Audioergänzung. Die anschließend zusammengeführte Standardfassung enthält alle 196 WAV-Dateien und die beiden zusätzlichen OGG-Dateien unter `assets/audio/`. Unveränderte FSB-Rohcontainer bleiben in der eigenen verifizierten APK beziehungsweise im privaten Eingabeverzeichnis und werden nicht beigelegt.

## Ergebnis

Alle 196 in dem früheren Audiopaket enthaltenen FSB5-Ressourcen liegen jetzt in lesbarer Audioform vor. Die bereits vorhandenen 194 WAV-Dateien wurden gegen die FSB5-Header geprüft. Kanäle, Abtastrate und Sampleanzahl stimmen bei allen 194 Dateien überein. Die zwei zuvor fehlenden Vorbis-Dateien wurden neu als Ogg und WAV erstellt.

| Belegter AudioClip-Name | Quellenhash im Dateinamen | Kanäle | Abtastrate | Sampleanzahl | Dauer |
| --- | --- | --- | --- | --- | --- |
| `Onyx_Elf_01` | `454f395b4395d46988325bf5289e959b` | 1 | 44.100 Hz | 5.663.232 | 128,417959 Sekunden |
| `Onyx_Human_03` | `f4eda84e578b34bb7b7ed6dcea105b37` | 1 | 44.100 Hz | 5.101.056 | 115,670204 Sekunden |

Die ursprünglichen AudioClip-Namen aller 196 Ressourcen wurden inzwischen aus den Unity-Objekten zugeordnet. Grundlage ist `catalogs/audio_clip_metadata.json`; die historische Zuordnung mit Quelldatei und Objekt-ID ist in `catalogs/audio_inventory_196.json` dokumentiert. Die aktuellen Paketpfade und Hashwerte stehen in `catalogs/audio_asset_links.json`. Abtastrate, Kanäle und Dauer passen zu den FSB5-Daten. Die konkrete Abspielsituation im Spiel wurde nicht untersucht.

## Dateien

Die beiden `.ogg`-Dateien enthalten die rekonstruierten Vorbis-Pakete ohne verlustbehaftete Neukodierung. Die beiden `.wav`-Dateien sind dekodiertes 16-Bit-PCM für einen einfachen Import. Beide Formate enthalten denselben jeweiligen Clip. Bei der Zählung sind es zwei neue Aufnahmen, nicht vier.

`catalogs/audio_inventory_196.json` erhält die Metadaten, belegten Namen und historischen Ausgabehashes. Seine alten Pfade sind keine aktuellen Paketpfade. `assets/audio/vorbis_rebuild_manifest.json` dokumentiert den aktuellen Vorbis-Export; `verification/audio_export.json` dokumentiert die Audioverarbeitung beim Paketbau.

Die 194 früheren WAV-Dateien wurden aus `Elvenar_Build02_06_Audio_WAV_konvertiert.zip` wiedergefunden. Der neue Gesamtpaketbau erzeugt die WAV-Dateien aus den verifizierten Quellen erneut und führt alle 196 Aufnahmen unter `assets/audio/` zusammen. Der aktuelle Namens-/Dateiindex ist `catalogs/audio_asset_links.json`.

## Technische Prüfung

FSB5 wurde mit `fsb5 1.0` gelesen. Der erste Ogg-Export enthielt bei beiden Clips 832 zusätzliche Padding-Samples. Der letzte Ogg-Granulewert wurde deshalb auf die im FSB5-Header belegte Sampleanzahl gesetzt und die Seitenprüfsumme neu berechnet. Die komprimierten Audiopakete blieben unverändert.

Die WAV-Dateien wurden zusätzlich direkt aus FSB5 mit `vgmstream r2168` ohne zusätzliche Schleifen dekodiert. FFmpeg 7.1.5 dekodierte beide korrigierten Ogg-Dateien vollständig ohne Fehlermeldung. Die resultierende Sampleanzahl stimmt mit FSB5 und WAV überein. Die unabhängigen PCM-Dekoder unterscheiden sich maximal um zwei 16-Bit-Quantisierungsstufen. Diese geringe Differenz wird in der Prüfung offengelegt; Bytegleichheit verschiedener Dekoder wird nicht behauptet.

Keine Aufnahme wurde abgespielt oder inhaltlich durchgehört. Die Prüfung belegt Dateiintegrität, Dekodierbarkeit, technische Länge und Audioformat.

## Reproduzieren

Benötigt werden Python, `fsb5==1.0`, `libogg`, `libvorbis` und FFmpeg. Für dieselbe WAV-Ausgabe wie im historischen Vergleich wird zusätzlich vgmstream r2168 benötigt. Dieses Programm ist nicht im Paket enthalten. Der normale Paketbau verwendet FFmpeg; unterschiedliche Decoder können leicht unterschiedliche WAV-Prüfsummen erzeugen.

Die folgenden Befehle beziehen sich auf das Paket-Hauptverzeichnis. `../INPUT/assets/bin/Data` muss als tatsächliches externes Eingabeverzeichnis aus der eigenen verifizierten APK bereitgestellt werden. Es ist kein Bestandteil des veröffentlichbaren Pakets; siehe `docs/REPRODUCE.md`.

```bash
python -m pip install -r requirements-extraction.txt
python tools/decode_vorbis_fsb5.py --input ../INPUT/assets/bin/Data --output ../elvenland-audio-reexport
```

`--input` akzeptiert entweder ein Rohdatenverzeichnis oder das ursprüngliche ZIP. Es werden ausschließlich die zwei Vorbis-Aufnahmen umgewandelt. Die übrigen 194 IMA-ADPCM-Aufnahmen meldet das Skript als übersprungen; sie werden durch den vorhandenen IMA-Konverter beziehungsweise die bereits konvertierten WAV-Dateien abgedeckt. Der Ablauf benötigt keinen speziellen Workspacepfad.

Optional ergänzt `--audio-metadata catalogs/audio_clip_metadata.json` die belegten AudioClip-Namen in das neu erzeugte Manifest. Mit `--vgmstream /path/to/vgmstream-cli` wird WAV direkt aus FSB5 dekodiert. Ohne diese Option erzeugt FFmpeg die WAV-Dateien aus den normierten Ogg-Dateien. Rundungsbedingt können sich deren WAV-Prüfsummen von den historischen vgmstream-WAVs unterscheiden.

## Werkzeugquellen

* https://github.com/HearthSim/python-fsb5
* https://github.com/vgmstream/vgmstream
* https://github.com/vgmstream/vgmstream/releases/tag/r2168
* https://ffmpeg.org/

Die Originaldateien wurden bei der Extraktion nicht verändert. Historische Arbeitsverzeichnisse wie `source_downloads` sind keine mitgelieferten Paketpfade.
