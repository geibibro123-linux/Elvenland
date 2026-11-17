# Elvenland: Architektur des eigenständigen Offline-Spiels

## Entscheidung und Reichweite

Der Nutzer erlaubt einen neuen, einfacheren Godot- oder Unity-Aufbau. Für die vorhandenen Sprite-Ressourcen wird Godot 4.6.3 mit GDScript und isometrischem 2D empfohlen. Die Original-APK dient als nachvollziehbare Ressourcen- und Analysequelle. Die neue Anwendung führt ihre Regeln direkt lokal aus.

Die folgende Architektur ist eine Umsetzungsempfehlung. Sie legt keine neuen wirtschaftlichen Originalwerte fest. Die alte Architektur aus Original-Unity-Oberfläche, Frida und nativer Bridge bleibt historische Referenz des früheren Elvenar-Projekts.

## Datenverantwortung

| Bereich | Verantwortlich für | Darf nicht übernehmen |
|---|---|---|
| Definitionen | IDs, belegte Kosten, Voraussetzungen, Grundflächen, Zeiten, Erträge und Herkunft. | Laufende Bestände oder eine unbemerkte Umwandlung unbekannter Werte in gültige Regeln. |
| `GameState` | Ressourcen, platzierte Gebäude, laufende Aufträge, Forschungsfortschritt und Revision. | Darstellungsdetails oder Netzwerksitzungen. |
| Lokale Befehle | Prüfung und gemeinsame Übernahme einer zulässigen Zustandsänderung. | Separate Buchungen durch die UI oder Erfolg bei unvollständigen Definitionen. |
| Oberfläche | Baumenü, Platzierungsvorschau, Stadt, Timer und verständliche Rückmeldung. | Eigenständige Ressourcen- oder Produktionsberechnung. |
| Speicherung | Versionen, atomare Dateien, Wiederherstellung, Import und Export. | Zugangsdaten, automatische Migration fremder Spielstände oder irreversible Überschreibung ohne bestätigten Auftrag. |

Die Oberfläche und der Speicher verwenden denselben übernommenen Spielzustand. Eine Bildschirmaktualisierung erfolgt über ein Signal nach erfolgreicher Zustandsübernahme. Ein sichtbarer Wert darf nicht unabhängig vom gespeicherten Modell verändert werden.

## Empfohlene Projektstruktur

Die folgenden Pfade sind die Struktur des zu implementierenden Spiels. Ihr Vorhandensein wird dadurch noch nicht behauptet. Der tatsächliche Übergabebestand steht im Dateiindex.

| Pfad | Inhalt |
|---|---|
| `godot/project.godot` | Eigene Godot-Projektkonfiguration. |
| `godot/scenes/` | Stadtansicht, Menüs und Dialoge. |
| `godot/scripts/model/` | Zustand und Datendefinitionen. |
| `godot/scripts/commands/` | Lokale Spielaktionen. |
| `godot/scripts/persistence/` | Speicheradapter, Migration und Export/Import. |
| `data/reference/` | Unveränderte bereinigte historische Referenzen. |
| `data/definitions/` | Normalisierte, für das Spiel ausgewählte Definitionen mit Status und Herkunft. |
| `assets/sprites/` und `assets/audio/` | Tatsächlich zugeordnete Bild- und Audiodateien. |
| `tools/` | Reproduzierbare Datenaufbereitung und Prüfwerkzeuge. |
| `docs/` | Architektur, Datenlücken, Entscheidungen und Nachweise. |

## Datenmodell und Veränderbarkeit

Eine Gebäudedefinition enthält mindestens technische ID, Darstellung, definierte Grundfläche, Kosten, Bauzeit und erforderliche Freischaltungen. Produktionsrezepte enthalten Gebäudezuordnung, Eingaben, Erträge, Dauer und belegte Regeln für Aufträge. Forschung enthält ID, Elternabhängigkeiten, Punktbedarf, Ressourcenbedarf und Wirkung.

Nicht vorhandene Angaben werden in der normalisierten Definition als `null` und OFFEN geführt. Die ursprüngliche Referenz bleibt unverändert. Die Laufzeitvalidierung muss zwischen einer belegten leeren Liste und einer unbekannten Liste unterscheiden. Eine unbekannte Kostenliste darf keinen kostenlosen Bau ergeben.

Jede Definition verweist auf ihre Herkunft, etwa Quelldatei, JSON-Pfad oder Katalogeintrag, und auf ihren Status. Historische Beobachtung und gewünschte Spielregel bleiben getrennt. Ein Editor oder Import für geänderte Werte schreibt eine eigene Elvenland-Anpassung. Er verändert nicht die historischen Ausgangstabellen.

Für Android liegen gebündelte Definitionen im Anwendungspaket. Spätere Nutzeranpassungen können als validierte lokale Überschreibung geladen werden. Eine exportierte und anschließend wieder importierte Konfigurationsdatei ist dafür eine mögliche einfache Bedienform. Unbekannte IDs, ungültige Zahlen, fehlende Abhängigkeiten und zyklische Forschungsgraphen werden vor Übernahme zurückgewiesen. Es werden keine ausführbaren Skripte aus Konfigurationsdateien geladen.

## Stadtansicht und Platzierung

Die isometrische Darstellung bildet lokale Rasterkoordinaten auf die Bildschirmfläche ab. Kameraposition, Zoom, Sprite-Pivot und Bildgröße sind Darstellungsparameter. Die logische Grundfläche wird aus einer geprüften Gebäudedefinition gelesen. Ein Grafikname wie `2x2` oder die PNG-Abmessung allein belegt diese Grundfläche nicht.

Die Platzierungsvorschau zeigt nur, ob ein Auftrag nach den vorhandenen Regeln zulässig wäre. Sie zieht keine Ressourcen ab und verändert die Stadt nicht. Erst die bestätigte Platzierung erzeugt einen lokalen Befehl. Dabei werden freigeschaltete Fläche, Grenzen, Überschneidung, Ressourcen und belegte Voraussetzungen erneut geprüft.

Eine Straßenverbindung wird nur dann als Regel ausgewertet, wenn die benötigte Verbindungslogik feststeht. Eine unbekannte Straßenpflicht darf weder unbegründet aktiviert noch pauschal ignoriert und als originalgetreu bezeichnet werden.

## Transaktionen und Fehler

Ein Befehl besitzt eine lokale Auftragskennung. Eingabe und aktuelle Definitionen werden geprüft, bevor eine Änderung entsteht. Kosten und neue Gebäude-/Auftragsdaten werden in einem vorbereiteten Folgezustand gemeinsam berechnet. Der Folgezustand wird validiert und dauerhaft gespeichert. Danach erhält die Oberfläche die Erfolgsmeldung und den neuen Zustand.

Bei einem Speicherfehler bleibt der vorherige bestätigte Zustand maßgeblich. Die UI darf weder ein fertiges Gebäude noch einen erfolgreichen Kauf anzeigen. Doppelte Übermittlung desselben Auftrags liefert dasselbe Ergebnis, ohne erneut abzubuchen. Eine Kennung mit abweichendem Inhalt wird als Konflikt abgelehnt.

Dieser Ablauf benötigt keine ursprüngliche Backend-Anfrage, kein ResponseVO und keinen nativen Client-Callback. Die alten Hostmodule können als Referenz für Fehlerfälle und Zwei-Slot-Speicherung dienen; ihre Versions-, Paket- und Bridge-Abhängigkeiten werden nicht übernommen.

## Timer und Produktion

Bau- und Produktionsaufträge speichern Start, Dauer, Fertigstellungszustand und Abholstatus. Während einer laufenden Sitzung kann monotone Zeit verwendet werden; für einen Neustart ist zusätzlich ein persistenter Zeitbezug nötig. Ein rückwärts springendes Gerätedatum darf keine negativen Laufzeiten oder zusätzliche Belohnungen erzeugen.

Offline-Zeitfortschritt wird auf Grundlage des konkreten Auftrags berechnet. Ohne belegte Wiederholungsregel erzeugt eine fertiggestellte Produktion nicht automatisch beliebig viele weitere Durchläufe. Eine neue Begrenzung des Offline-Ertrags oder eine neue Strafe für Zeitänderungen wäre eine Spielregel und benötigt eine entsprechende Entscheidung.

Ein Auftrag wird genau einmal fertiggestellt und genau einmal vergütet. Abholung, Ressourcenänderung und Auftragsabschluss bilden eine gemeinsame Transaktion. Neustart und wiederholtes Tippen dürfen daran nichts ändern.

## Forschung

Die historischen Feature-/Technologiezuordnungen dienen als Quellenhinweise. Sie enthalten keinen vollständigen gerichteten Forschungsgraphen. Der neue Forschungsteil benötigt für seinen aktivierten Umfang vollständige Knoten und Abhängigkeiten sowie Kosten und Wirkungen.

Vor Übernahme eines Forschungsdatensatzes werden eindeutige IDs, vorhandene Elternknoten, Zyklen, Kosten und Wirkungsreferenzen geprüft. Forschungspunkte und Ressourcen werden nur bei zulässiger Transaktion verändert. Eine gesperrte oder unbekannte Forschung darf keine Folgeknoten freischalten.

Ein rekonstruierter Teilbaum benötigt belegte Grenzen und Werte. Für die technische Prüfung darf ein getrennter synthetischer Testgraph als ARBEITSWERT verwendet werden. Er ersetzt keine Originaldaten oder FEST-Werte und darf nicht als vollständiger Original-Techbaum bezeichnet werden. Nur bei deutlich unterschiedlichen Konsequenzen ist eine zusätzliche Nutzerentscheidung erforderlich.

## Speicherung und externe Sicherung

Ein Spielstand enthält mindestens Schema- und Definitionsversion, Revision, lokalen Zustand und die für Wiederholungs-/Abholschutz erforderlichen Auftragsinformationen. Die Speicherung erfolgt über temporäre Datei und atomare Übernahme mit einer erhaltenen vorherigen gültigen Fassung. Beim Laden wird die jüngste gültige Fassung ausgewählt. Beschädigte Dateien dürfen keinen stillen Neustart mit neuen Ressourcen auslösen.

Eine Prüfsumme erkennt unbeabsichtigte Beschädigung. Sie ist kein Schutzversprechen gegen absichtliche Änderung. Import prüft Format, Version, Größen, Datentypen, IDs, Referenzen und Zustandskonsistenz. Nicht unterstützte Versionen werden nachvollziehbar zurückgewiesen.

Ein externer Export muss die Android-App-Deinstallation überstehen. Dazu wird ein Dokument über Android Storage Access Framework angelegt und beim Import erneut gewählt. Die konkrete Godot-/Android-Anbindung ist ein eigener technischer Nachweis. Ein Desktop-Dateidialog oder eine Datei in `user://` belegt diese Android-Funktion nicht.

## Prüfgrenzen

Statische Prüfung und Hosttests sichern Daten und Algorithmen ab. Android-Prüfungen sichern Export, Installation, Start, Touchbedienung und tatsächlichen Dateizugriff ab. Samsung-Prüfungen bestätigen das Verhalten auf dem Zielgerät. Der konkrete Nachweis wird separat dokumentiert.

Erstes Ziel ist ein belegbarer lokaler Spielkreislauf mit Neustart. Eine große Anzahl importierter Grafiken, erfolgreiche Hosttests oder ein signiertes APK allein belegen diesen Kreislauf nicht.
