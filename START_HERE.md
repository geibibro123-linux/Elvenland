# Elvenland: Einstieg für ChatGPT, Claude und Entwickler

Materialstand: 17. November 2026. Die Archive bleiben historische Erstellungssnapshots dieses Stands. Das bestätigte Zielrepository [geibibro123-linux/Elvenland](https://github.com/geibibro123-linux/Elvenland) existiert, ist verbunden und derzeit privat. Die lesbaren Projektdateien und das kleine KI-Startpaket sind auf GitHub gespeichert. Das vollständige Medien-Release und anonymer Zugriff sind noch offen. Der Materialumfang bleibt unverändert. Es handelt sich noch nicht um ein spielbares Spiel; eine installierbare Elvenland-APK ist nicht enthalten.

## In dieser Reihenfolge lesen

1. `STATUS.json`: aktueller Umfang, belegte Ergebnisse und offene Systeme.
2. `MASTER_PROMPT.md`: vollständiger Arbeitsauftrag für eine neue ChatGPT- oder Claude-Sitzung.
3. `INDEX.json`: zentrale Wegweisung zu Daten, Medienindizes und Herkunft.
4. `data/reference/README_HISTORICAL_DATA.md`: Bedeutung und Grenzen der echten historischen Startdaten.
5. `docs/ARCHITECTURE.md` und `docs/ROADMAP.md`: einfacher lokaler Aufbau und vier Arbeitsphasen.
6. `docs/SOFTWARE_AND_ENGINE.md`: benötigte Werkzeuge, geprüfte Primärquellen und Engine-Empfehlung.
7. `docs/AI_HANDOFF.md`: Übergabe an ChatGPT/Claude, dokumentierte Dateigrenzen und Voraussetzungen für ZIP-Verarbeitung.
8. `docs/PACKAGE_COVERAGE.md`: zusammengeführte Zähler, Quellenabdeckung und verbleibende Grenzen aller Teilbestände.

## Was das vollständige Medienpaket enthält

Dieses Repository übernimmt Texte, Datentabellen, Kataloge, Teilindizes und Werkzeuge aus dem kleinen KI-Startpaket. Die nachfolgenden `assets/`-Pfade und die Medienangaben in `INDEX.json` gehören zum separaten Vollpaket. Ein indexierter Pfad bedeutet nicht, dass die große Mediendatei im Git-Dateibestand liegt.

| Pfad | Zweck |
| --- | --- |
| `assets/visuals/sprites/` | Direkt verwendbare PNG-Einzelbilder aus den Unity-Bundles. Ein Bild kann ein Gebäude, eine Ebene, ein Icon oder ein Animationsschritt sein. |
| `assets/visuals/textures/` | Dekodierte Texturen und Atlanten als PNG. |
| `assets/visuals/metadata/` | Lesbare JSON-Strukturen für Sprite-Rechtecke, Pivots, AnimationClips, Controller, Transformations- und Objektverknüpfungen. |
| `assets/unity_data/` | Zusätzliche 2.859 Sprite-PNGs, 2.604 Textur-PNGs, sechs Schriftdateien sowie Animations-, Struktur- und freigegebene TextAssets aus Unity Data. |
| `assets/audio/` | Alle 196 vorhandenen Audioquellen als WAV; die beiden Musikquellen zusätzlich als OGG. |
| `assets/localization/` | Alle 20 Sprachfassungen mit jeweils 2.787 Schlüsseln und erhaltenen Übersetzungsvarianten. |
| `assets/android_reference/` | 459 ergänzende Android-PNG-Referenzen, teilweise SDK-/Systemoberfläche. |
| `data/localization/` | Kleine deutsche und englische Referenztabellen für den Einstieg. |
| `catalogs/audio_asset_links.json` | Geprüfte AudioClip-Namen, direkte aktuelle WAV-/OGG-Pfade und Quelldateihashes. |
| `data/reference/` | Bereinigte historische Beobachtungen und visuelle Kataloge. Keine automatisch verbindlichen neuen Spielwerte. |
| `data/definitions/` | Leere, ausdrücklich offene Eingabedateien für die neue lokale Wirtschaft. |
| `indexes/` | Kleine JSON-Teillisten für selektives Lesen durch KI-Werkzeuge. |
| `provenance/source_media_files.json` | Herkunfts- und Hashliste der 5.147 geprüften statischen Quelldateien. Die redundanten Rohcontainer werden im kompakten Standardpaket nicht nochmals beigelegt. |
| `provenance/additional_static_media_files.json` | Ergänzende Hashliste der 21 verifizierten Sprachquellen. |
| `provenance/` | Herkunft, Quell-Hashes und Vergleich mit Original-APK und GitHub-Baseline. |
| `verification/` | Nachweise für Quellen, Export und Paketprüfung. |
| `catalogs/historical_20261114/` | Historische Kataloge. Alte Exportlücken sind keine aktuellen Fehlermeldungen. |
| `reference_code/javascript/` | Vorhandene lokale Transaktions-/Speicherideen als technische Referenz, kein fertiger Godot-Spielkern. |
| `tools/` | Wiederholbare Extraktion, Audio-Dekodierung, Indizierung und Paketbau. |

Im vollständigen Medienarchiv liegen außerdem `MANIFEST.jsonl`, `SHA256SUMS.txt` und eine lokale Bildübersicht `ASSET_PREVIEW.html`. Diese Archivdateien sind kein aktuelles Repository-Manifest. Die vollständige ZIP enthält eine einzige oberste Ebene `elvenland/`. Medien liegen als einzelne Dateien vor; es gibt keine verschachtelten Ressourcen-ZIPs. Für erneute Extraktion bleiben die eigene verifizierte APK beziehungsweise externe private Eingabedateien die Quelle. Das veröffentlichbare Paket enthält ausschließlich die geprüften konvertierten Ausgaben und zugehörigen Unterlagen, keine unveränderten Unity-/FSB-Rohcontainer.

## Zentrale Fakten

Die Quelle ist Elvenar 1.244.0, Versionscode 1329. Die 5.147 ausgewählten statischen Medien und 21 Sprachquellen sind bytegleich in der bereitgestellten Original-APK, der wiedergefundenen Build-02-Grundlage und der vorhandenen GitHub-Lab-04-Baseline. Eine neuere Diagnose-APK ist deshalb für diese Medienextraktion nicht automatisch die bessere Quelle. Der gesonderte Android-PNG-Vergleich und seine neun Abweichungen stehen in `docs/PACKAGE_COVERAGE.md`.

Zusammengeführt sind 6.594 Sprite-PNGs, 4.195 Textur-PNGs, 196 Audioquellen, 427 AnimationClip-Strukturen, 173 AnimatorController, drei OverrideController und sechs Schriftdateien vorhanden. Das sind Datei-/Objektzahlen; daraus folgt keine entsprechende Anzahl eigenständiger Gebäude oder spielbereiter Animationen.

Der Katalog enthält 139 visuelle Stadtreferenzen: 138 mit 272 Qualitätsvarianten und einen Alias. Daraus folgen weder 139 vollständige Gebäudedefinitionen noch Baukosten. Die historische Referenz enthält 245 Ressourcengruppen und 1.500 Freischaltungsbeobachtungen. Bei 1.493 Einträgen fehlt das Freischaltungsfeld. Der vollständige Forschungsbaum, Gebäudekosten und Produktionsrezepte bleiben offen.

## Zugriff ohne Anmeldung

Unverschlüsselte UTF-8-Dateien, PNG, WAV, OGG und JSON sind technisch vorbereitet. Anonymer Abruf ist zusätzlich eine Eigenschaft des Hosting-Zugriffs. Ein privates GitHub-Repository wird durch eine passende ZIP-Struktur nicht öffentlich.

Das verbundene Ziel `geibibro123-linux/Elvenland` ist derzeit privat. Die Projektdateien und das kleine Release `elvenland-ki-startpaket-v1` sind geprüft vorhanden. Das vollständige Medienarchiv ist noch nicht als Release gespeichert. Für anonymes Lesen müsste das Ziel öffentlich erreichbar sein, und die tatsächlichen Raw-/Downloadlinks müssten ohne Anmeldung geprüft werden. Die aktuelle Veröffentlichungslage steht in `STATUS.json` und `docs/GITHUB_PUBLICATION.md`. Niemals einen privaten Link als anonym geprüft bezeichnen und niemals Zugriffstokens in den Prompt schreiben.

Ein KI-Chat kann eine ZIP nur verarbeiten, wenn die Datei in seiner Sitzung zugänglich ist und Werkzeuge zum Entpacken vorhanden sind. Deshalb werden die Startdateien, der Prompt, Daten und Teilindizes zusätzlich einzeln bereitgestellt. Zum Einstieg das kleine KI-Startpaket oder einzelne Text-/JSON-Dateien verwenden. Auch eine kleine ZIP muss vom jeweiligen Chat unterstützt werden. Die dokumentierten Größenlimits und ihre Grenzen stehen in `docs/AI_HANDOFF.md`. Es gibt keine Garantie, dass jede ChatGPT- oder Claude-Sitzung automatisch alle Medien lesen kann.

## Nächster sinnvoller Entwicklungsschritt

Ein kleiner vollständiger lokaler Spielkreislauf: Stadt anzeigen, Gebäude platzieren, Kosten gemeinsam mit der Zustandsänderung buchen, Produktion starten und einsammeln, speichern und nach Neustart fortsetzen. Dafür belegte Definitionen oder eine getrennte, klar als ARBEITSWERT gekennzeichnete Prototypkonfiguration verwenden. Fehlende Originalwerte bleiben OFFEN; Prototypwerte ersetzen weder Originaldaten noch bestehende FEST-Werte. Forschung und weitere Gebäude folgen auf derselben Datenstruktur. Nur bei deutlich unterschiedlichen Konsequenzen nachfragen, sonst mit dokumentierten Annahmen weiterarbeiten.


## Aktueller Übergabestand

Das kleine Release enthält 270 Dateien und hat 4.686.083 Bytes. Es ist der unveränderte Erstellungssnapshot. Die laufenden Publikationsangaben im Repository haben Vorrang vor damaligen Zugangshinweisen im ZIP. Die vollständige lokal wiederhergestellte ZIP enthält 25.662 Dateien bei 673.087.419 Bytes; alle 11.452 Mediendateien sind byte-identisch zum vorherigen vollständigen Paket. Ihr aktueller Hash und die belegten Grenzen stehen in `verification/restored_package_20261117.json`.

Der neue Ablauf unter `docs/FULL_RESOURCE_WORKFLOW.md` kann das große Paket aus der exakt geprüften Quell-APK im selben Repository erzeugen. Er ist vorbereitet, aber noch nicht auf GitHub ausgeführt.
