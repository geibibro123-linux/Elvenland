# Elvenland: geprüfter Gesamtumfang und Grenzen

Stand: 17. November 2026. Diese Übersicht führt die getrennten Exporte zusammen. Die ergänzenden Einzelberichte beschreiben jeweils ihren angegebenen Teilbestand. Die tatsächliche ZIP-Größe, Dateizahl und SHA-256 stehen im abschließenden Prüfbericht neben dem Archiv.

## Grafiken, Audio und Texte

| Inhalt | UnityFS-Bundles | Unity-Data-Dateien | Zusammengeführter Befund |
| --- | ---: | ---: | ---: |
| Sprite-PNGs | 3.735 | 2.859 | 6.594 Dateien |
| Textur-PNGs | 1.591 | 2.604 | 4.195 Dateien |
| Leere Texturobjekte ohne Bildinhalt | 4 | 7 | 11 dokumentierte Quellobjekte |
| AnimationClip-Metadaten | 82 | 345 | 427 JSON-Strukturen |
| AnimatorController-Metadaten | 57 | 116 | 173 JSON-Strukturen |
| AnimatorOverrideController | 0 | 3 | 3 zusätzliche JSON-Strukturen |
| SpriteAtlas-Metadaten | 54 | 35 | 89 Strukturen |
| Eingebettete Schriftdateien | 0 | 6 | 6 Dateien |

Die beiden Grafikbestände stammen aus 317 UnityFS-Bundles und 4.616 logisch rekonstruierten Unity-Data-Dateien. Geteilte Unity-Dateien wurden in ihrer ursprünglichen Reihenfolge zusammengesetzt und mit einem Teilemanifest dokumentiert. Der endgültige Unity-Data-Export hat keine Exportfehler. Die vier im UnityFS-Bericht als Fehler geführten Font-Texture-Objekte sind nachweislich leer; der Data-Export führt sieben weitere leere Quelltexturen gesondert auf.

Diese Zahlen zählen ausgegebene Dateien beziehungsweise Objekte. Sie sind keine Anzahl einzigartiger Gebäude. Bilder können Ebenen, Icons, Kartenfelder, Qualitätsvarianten oder Animationsbilder darstellen. Atlanten und ausgeschnittene Sprites sind teilweise verschiedene Darstellungen derselben Bildinhalte und dürfen nicht zu einer vermeintlichen Zahl unterschiedlicher Spielobjekte addiert werden.

Zusätzlich vorhanden:

- 196 vorhandene Audioquellen vollständig als WAV. Die zwei Vorbis-Musikquellen liegen zusätzlich als OGG vor. Das sind zwei alternative Formate derselben Aufnahmen, keine zwei weiteren Musikstücke.
- 20 Sprachfassungen mit jeweils 2.787 Schlüsseln, insgesamt 55.740 Spracheinträgen. Mehrere Varianten eines Schlüssels bleiben erhalten. `de_de` und der tatsächliche Originalcode `en_dk` liegen zusätzlich als kleine Referenztabellen für KI-Werkzeuge vor.
- 28 geprüfte TextAssets: neun Spine-Skelettdateien mit zusammen 23 benannten Animationen, neun Atlanten, sechs Soundkonfigurationen, Audio-Mix-Einstellungen, das visuelle Manifest und zwei Zeichensätze für Zeilenumbrüche.
- 459 zusätzliche Android-PNG-Referenzen. Darunter befinden sich Android- und SDK-Oberflächenbilder. Diese Dateien sind kein erforderlicher Bestandteil des neuen Spielkerns.

## Wichtige Pfade

| Pfad | Inhalt |
| --- | --- |
| `assets/visuals/` | Export der UnityFS-Bundles einschließlich Sprite-, Textur- und Animationsdaten. |
| `assets/unity_data/` | Zusätzliche Bilder, Schriften, freigegebene TextAssets und grafische Objektstrukturen aus Unity Data. |
| `assets/audio/` | Benannte und indizierte WAV-/OGG-Ausgaben. |
| `assets/localization/` | Alle 20 lesbaren Sprachfassungen, Originalvarianten und Herkunftsbelege. |
| `assets/android_reference/` | Ergänzende Android-PNG-Referenzen. |
| `data/localization/` | Deutsche und englische Referenztabellen sowie lexikalischer Themenindex. |
| `data/reference/` | Bereinigte historische Spielbeobachtungen mit ausdrücklich begrenzter Gültigkeit. |
| `data/definitions/` | Noch offene Definitionen für die neue lokale Wirtschaft, Produktion und Forschung. |
| `indexes/` | Kleine, gezielt lesbare Teile der beiden Grafikindizes. |
| `catalogs/` | Sprachindex, direkte Audiozuordnung und ergänzende Referenzkataloge. |

## Herkunft und tatsächlich geprüfte Versionen

Die Grafik-/Audiogrundlage ist Elvenar 1.244.0, Versionscode 1329. Die ursprünglichen 5.147 statischen Quellmedien und die zusätzlich geprüften 21 Sprachdateien sind bytegleich in der bereitgestellten Original-Basis-APK, der wiedergefundenen Build-02-APK und der vorhandenen Lab-04-Baseline. Diese 5.168 Dateien werden vor einem Paketneubau einzeln geprüft.

Die Android-PNGs besitzen einen getrennten Vergleich: alle 459 stimmen zwischen Build 02 und Lab 04 überein. 450 sind auch in der ursprünglichen Basis-APK bytegleich vorhanden. Neun Android-/SDK-Nine-Patch-Bilder besitzen dort keine identische Bytefassung. Die Unterschiede werden nicht als ursprüngliche Spielgrafiken ausgegeben. APK-interne Android-Ressourcennamen können zwischen den Builds abweichen; der Katalog dokumentiert die Zuordnung über exakte Dateihashes.

Ein späterer Diagnose-Build ist nicht allein wegen seiner höheren Bezeichnung die bessere Medienquelle. Die genannten Vergleiche belegen die konkret überprüften Versionen. Sie behaupten keine Prüfung jedes jemals hochgeladenen Builds.

## Spiellogik und Forschungsbaum

Die bereinigten historischen Daten enthalten 139 visuelle Stadtreferenzen, 245 Ressourcengruppen, 1.500 Freischaltungsbeobachtungen und 13 Feature-/Technologiezuordnungen. Die 139 Referenzen sind keine vollständigen Gebäudedefinitionen. Bei 1.493 Freischaltungsbeobachtungen fehlt das Freischaltungsfeld; ein fehlendes Feld wird nicht als `false` umgedeutet.

Ein vollständiger Forschungsbaum mit Knoten, Abhängigkeiten, Kosten und Wirkungen ist bisher nicht nachgewiesen. Dasselbe gilt für vollständige Gebäudekosten, Produktionsrezepte und Kampfregeln. Forschungstexte und Soundereignisse schließen diese Lücken nicht. Vorhandene Referenzwerte werden nicht automatisch zu verbindlichen Elvenland-Werten.

Neue Prototypkonfigurationen dürfen ausdrücklich als ARBEITSWERTE angelegt werden. Sie bleiben von historischen Originalbeobachtungen getrennt und ersetzen keine bestätigten Werte. Der Hauptprompt beschreibt diese Arbeitsweise und die Abnahmekriterien des ersten vollständigen lokalen Spielablaufs.

## Animationen und ursprünglicher Client

Die Unity-Animationskurven, Controller und Sprite-Pointer liegen lesbar vor. Sie wurden nicht bereits in Godot-Timelines umgebaut oder im neuen Spiel abgespielt. Auch die Spine-Dateien sind Datenquellen, kein nachgewiesener Godot-Animationsimport. Diese Übertragung gehört zur Implementierung.

Grafische Objektstrukturen sind exportiert. Allgemeine benutzerdefinierte MonoBehaviour-Felder, SDK-Laufzeitcode, die ursprüngliche IL2CPP-Laufzeit und Serverprotokolle werden nicht als fertiger eigener Spielkern ausgegeben. Ein Assetexport rekonstruiert kein vollständiges ursprüngliches Unity-Projekt.

## Bereinigung und Integrität

Von 44 TextAssets wurden 28 freigegeben und 16 ausgeschlossen. Neun Spine-Dateien wurden ausschließlich um Editorpfad-Felder bereinigt; 19 Ausgaben bleiben byteidentisch. Quelle, Transformation und Ausgabehash sind im Freigabeindex dokumentiert. Rohquellen werden nur während der lokalen Extraktion verwendet und nicht in das veröffentlichbare Paket kopiert.

Die Haupt-ZIP enthält ein vollständiges Dateimanifest und eine SHA-256-Liste. Sie wird nach dem Schreiben vollständig per CRC geprüft. Das kleine KI-Startpaket besitzt ein eigenes Manifest und enthält keine Grafik-/Audiodateien. Seine übernommenen Fachindizes beschreiben ausdrücklich weiterhin das vollständige Medienpaket.

## Noch nicht nachgewiesen

Es existiert durch diese Lieferung noch kein implementiertes Godot-Spiel, keine gebaute Elvenland-APK, kein Android-Gerätetest und kein anonymer GitHub-Abruf. Die genaue Veröffentlichungslage steht in `STATUS.json` und `docs/GITHUB_PUBLICATION.md`. Diese offenen Punkte dürfen weder durch einen Prompt noch durch erfolgreiche Dateiprüfungen als erledigt gelten.
