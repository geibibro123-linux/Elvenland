# Elvenland: nachgewiesene zusätzliche Ressourcenextraktion

> Geltungsbereich: Dieser Bericht beschreibt den UnityFS-Teilbestand. Die zusätzlich exportierten Unity-Data-, Sprach- und Android-Ressourcen stehen in `PACKAGE_COVERAGE.md`.

Prüfdatum: 17.11.2026. Grundlage sind die erneut beschafften Elvenar-Build02-Ressourcenpakete. Die Quellen wurden nicht verändert. Die neuen Ausgaben sind getrennte Dateien, keine APK.

## Ergebnis der Grafikextraktion

| Inhalt im untersuchten Bundlesatz | Erkannt | Erfolgreiche Ausgabe |
| --- | ---: | ---: |
| UnityFS-Bundles | 317 | 317 ausgewertet |
| Sprite-Objekte | 3.735 | 3.735 einzelne PNGs und zugehörige Metadaten |
| Texture2D-Objekte | 1.595 | 1.591 PNGs |
| AnimationClip-Objekte | 82 | 82 vollständige auslesbare Typbäume |
| AnimatorController-Objekte | 57 | 57 Typbäume |
| SpriteAtlas-Objekte | 54 | 54 Typbäume |

Die Sprite-PNGs sind einzeln ausgeschnitten. Darunter befinden sich 262 Namen mit dem Präfix `baseFrame_`. Das sind Referenzen und Varianten, keine Zählung unterschiedlicher baubarer Gebäude. Die insgesamt 5.326 neuen PNG-Dateien bestehen aus 3.735 Sprites und 1.591 Texturen. Sprites und die sie enthaltenden Atlanten sind teilweise dieselbe Grafik in unterschiedlichen Darstellungen und dürfen nicht als unabhängige Inhalte gezählt werden.

Die zuvor fehlenden 53 Texturkonvertierungen sind gelungen. Dazu gehören die beiden Wegtexturen und die mit dem alten Werkzeug nicht dekodierten PVRTC- und Crunched-Formate. Die vier übrigen Texture2D-Einträge heißen `Font Texture` und liegen im `video_ads`-Bundle. Alle vier haben nachweislich 0 × 0 Pixel, 0 Byte Bilddaten und einen leeren Stream-Verweis. Es gibt dort keine eingebetteten Pixel, die noch als PNG extrahiert werden könnten. Der Befund ist in `verification/font_texture_gaps.json` festgehalten.

39 Sprites der Weltkartenränder benötigen Texturen aus einem zweiten Bundle. Der wiederholbare Export löst diese konkrete CAB-Abhängigkeit auf. Danach konnten alle 3.735 Sprite-Objekte ausgegeben werden.

Jedes PNG wurde unmittelbar nach dem Schreiben erneut mit Pillow vollständig eingelesen. Ein Gebäude-Sprite wurde zusätzlich visuell überprüft. Das belegt die Dateilesbarkeit und das korrekte Zuschneiden des überprüften Beispiels, keine umfassende Sichtprüfung jedes einzelnen Spielobjekts.

## Animationen und Szenenbezüge

Die Metadaten unter `assets/visuals/metadata/` bewahren unter anderem Sprite-Pivots, Rechtecke, Pixelmaßstab, Transform-Daten, Renderer-Zuordnungen und die Original-Animationsdaten. `assets/visuals/animation_reference_catalog.json` verknüpft alle 1.608 enthaltenen Sprite-Referenzen der 82 AnimationClips mit exportierten PNGs. Es bleiben dabei keine unaufgelösten Sprite-Zeiger.

Die Zeitkurven liegen weiterhin in der kompilierten Unity-Darstellung vor. Es wurde keine fertige Godot-Animation oder neue Animationsgeschwindigkeit erfunden. Die Pointer-Tabelle ist eine Referenzzuordnung und darf ohne Auswertung der Zeitkurven nicht als fertige Wiedergabereihenfolge behandelt werden.

Zusätzlich wurden Typbäume von 875 GameObjects, 867 Transforms, 323 SpriteRenderern und 57 Animatoren bewahrt. Von 626 MonoBehaviours enthalten zwei nur einen auslesbaren Header. Diese Daten ersetzen keinen rekonstruierten C#-Quelltext und liefern nicht automatisch die vollständige Spielwirtschaft.

## Audio

Alle 196 FSB5-Audioquellen des vorliegenden Pakets sind jetzt in lesbarer Form verfügbar: 194 vorhandene WAV-Dateien plus zwei neu dekodierte Vorbis-Aufnahmen. Die neuen Aufnahmen heißen nachweislich `Onyx_Elf_01` und `Onyx_Human_03`. Sie liegen jeweils als OGG und WAV vor. Das sind zwei Aufnahmen in zwei Formaten.

Alle 196 AudioClip-Namen wurden mit den Ressourcen verknüpft. Die bereits vorhandenen 194 WAVs stimmen bei Sampleanzahl, Abtastrate und Kanälen mit ihren FSB5-Quellen überein. Die beiden neuen Aufnahmen wurden vollständig dekodiert und mit einem unabhängigen Decoder geprüft. Der Bericht dieses Audio-Prüflaufs steht in `docs/AUDIO_REPORT.md`.

Die aktuelle Paketfassung enthält 196 WAV-Dateien und zwei OGG-Dateien unter `assets/audio/`. `catalogs/audio_asset_links.json` ordnet die AudioClip-Namen den aktuellen Quellen, Ausgabepfaden und Prüfsummen zu. `verification/audio_export.json` dokumentiert den Paketbau. Der unverändert erhaltene Katalog `catalogs/audio_inventory_196.json` enthält teilweise historische Dateipfade und ist dafür nicht der aktuelle Pfadindex.

Die Aussage umfasst die 196 vorhandenen Quellen. Sie behauptet nicht, dass keine weiteren Musikstücke oder Sounds vom Online-Spiel nachgeladen werden.

## Dateien und reproduzierbarer Ablauf

`assets/visuals/` enthält den kopierbaren Grafik-/Metadatenbaum. Die genaue Dateianzahl, Größen und Hashwerte der aktuellen Paketfassung stehen in `MANIFEST.jsonl`, `SHA256SUMS.txt` und `verification/package_validation.json`. `assets/visuals/bundles_index.csv` verbindet jeden exportierten Gegenstand mit Quellbundle, Quellhash, Unity-Datei, Objekt-ID, Originalnamen und Ausgabepfad. Die Ausgabepfade innerhalb dieser CSV sind relativ zu `assets/visuals/`; die JSON-Teillisten unter `indexes/` verwenden Paketpfade.

Das CLI `tools/export_assets.py` akzeptiert `--input` und `--output`. Die Anforderungen stehen in `requirements-extraction.txt`. `tools/summarize_animations.py` erstellt den kompakten Referenzkatalog. Aufruf und Ausgabeformat sind in `docs/README_EXPORT.md` beschrieben. `tools/build_package.py` führt Quellenprüfung, Extraktion, Audioverarbeitung, Indizierung und ZIP-Erstellung zusammen.

Die UnityFS-Header melden Unity 6000.0.71f1. Erfolgreich verwendet wurden Python 3.12.14, UnityPy 1.25.4 und Pillow 13.0.0.

## Nicht nachgewiesen

Die Extraktion erzeugt weder einen vollständigen Forschungsbaum mit Originalkosten noch einen vollständigen lokalen Spielkern. Ebenso wurde hier keine installierbare Offline-APK erzeugt. Eine neue Engine muss die Spielregeln, Speichervorgänge, UI-Aktualisierung und Animationen mit diesen Ressourcen gezielt verbinden.
