# Elvenland: vier Phasen bis zur belastbaren Offline-Testversion

Diese Roadmap beschreibt den neuen eigenständigen Aufbau. Der aktuelle Arbeitsstand steht in `STATUS.json`. Abgeschlossene Quellenarbeit nicht erneut als offene Entwicklung behandeln; noch nicht ausgeführte Schritte nicht als erledigt markieren.

Der Nutzer wünscht ungefähr 100 Minuten für die gesamte Kette aus Auslesen, Analyse, Datenübernahme, Neuaufbau und neuer APK. Ein vollständiger originalgetreuer Android-Nachbau innerhalb dieses Gesamtbudgets ist nicht belastbar zusagbar. Der Zeitwunsch wird nicht als ausschließliches Analysebudget umgedeutet. Die folgenden Phasen besitzen überprüfbare Ergebnisse; tatsächlicher Fortschritt und verbleibende Voraussetzungen werden offen dokumentiert.

## Phase 1: Quellen prüfen und ein vollständiges Übergabeverzeichnis erstellen

**Arbeit:** Pakete wiederbeschaffen, verfügbare APK-Versionen und Basis bestimmen, Integrität prüfen, Archive entpacken und Ressourcen zuordnen. Bilder, Audio, Animationen, Kataloge, historische Daten, eigener Code und ursprünglicher Binärcode getrennt indexieren. Persönliche oder geheime Daten aus dem zur Weitergabe bestimmten Bestand ausschließen.

**Ergebnis:** Lesbare Einzeldaten, ein Dateiindex, Herkunfts-/Hashlisten, ein Paket für die Weiterarbeit, ein klarer Status und dieser selbstständige Arbeitsauftrag. Textdateien zusätzlich einzeln lesbar halten. Bei GitHub-Zugriff prüfen, ob externe KI-Systeme die angegebenen Links tatsächlich ohne Anmeldung lesen können.

**Abnahme:** ZIP lässt sich vollständig lesen; erforderliche Dateien existieren und stimmen mit den angegebenen Hashwerten überein. Mengen und offene Datenlücken entsprechen den tatsächlich geprüften Inhalten. Ein nicht vorhandener Forschungsbaum wird nicht als extrahiert ausgegeben.

**Nutzeraktion:** Nur fehlende Quellen oder einen benötigten Zugriff bereitstellen. Hieraus entsteht noch kein notwendiger Telefon-Test.

## Phase 2: Geprüfte Daten und eigenes Godot-Projekt aufsetzen

**Arbeit:** Godot 4.6.3 mit GDScript als empfohlenen Aufbau verwenden. Eigene Projektstruktur, Startszene, Stadtansicht, Kamera, Touch-/Mausauswahl, Sprite-Zuordnung und Audioimport anlegen. Originalreferenzen erhalten und normalisierte Definitionen mit Quellenstatus erstellen.

Das Baumenü wird aus vorhandenen Definitionen erzeugt. Unvollständige Originaleinträge zeigen nachvollziehbar, welche Voraussetzung noch fehlt. Keine Kosten, Grundflächen oder Freischaltungen aus Namen als belegte Werte ableiten. Das erste spielbare Gebäude kann mit einer ausreichend belegten Definition oder einer getrennten, klar als ARBEITSWERT gekennzeichneten Prototypkonfiguration umgesetzt werden.

**Ergebnis:** Eigenständig startendes Godot-Projekt mit sichtbarer Stadt, nachweislich verwendeten Ressourcen und validiertem Datenimport. Kosten, Zeiten und Freischaltungen sind getrennt vom UI-Code organisiert.

**Abnahme:** Godot importiert und öffnet das Projekt ohne relevante Fehler. Die zugeordneten Sprites stimmen mit ihrem Index überein. Aliasreferenzen werden korrekt behandelt. Ungültige oder unvollständige Definitionen werden erkannt; unbekannte Kosten ergeben keinen kostenlosen Bau.

**Nutzeraktion:** Nur bei deutlich unterschiedlichen Konsequenzen eine konkrete Entscheidung einholen. Fehlende Originaldatensätze benennen; ein gesonderter Prototyp darf mit dokumentierten ARBEITSWERTEN fortgesetzt werden. Bestehende FEST-Werte werden dadurch nicht geändert. Technisch unabhängige Arbeit wird selbstständig fertiggestellt.

## Phase 3: Lokalen Spielkreislauf und Speicherung verbinden

**Arbeit:** Zentralen Spielzustand, Baumenüauftrag, gültige Platzierung, gemeinsame Kosten-/Zustandsbuchung, Bauzeit, Produktion, einmalige Abholung und UI-Aktualisierung verbinden. Forschung im jeweils ausreichend definierten Umfang hinzufügen. Spielstand, Revision, Wiederherstellung und validierten Import/Export vorbereiten.

**Erster vollständiger Ablauf:**

1. Eine lokale Stadt öffnen und den gespeicherten Ressourcenstand anzeigen.
2. Ein definiertes Gebäude auswählen und eine gültige freie Position bestätigen.
3. Kosten genau einmal abziehen und einen Bauauftrag mit belegter Dauer anlegen.
4. Fertigstellung korrekt anzeigen und ein definiertes Produktionsrezept starten.
5. Den Ertrag genau einmal abholen.
6. Anwendung beenden und denselben bestätigten Zustand wieder laden.

**Abnahme:** Gültiger Ablauf funktioniert; Überschneidung, unzureichende Ressourcen, unvollständige Definition und doppelte Eingabe werden korrekt behandelt. Ein erzwungener Fehler während Speicherung erzeugt weder Gratisgebäude noch doppelte Ressourcen. Aufträge und Abholstatus bleiben nach Neustart konsistent.

Rekonstruierte Forschung wird anhand eines vollständigen bekannten Teilgraphen geprüft: Voraussetzungen, Investition, Kosten, Freischaltung und Neustart. Fehlt dieser Teilgraph, bleibt die Originalrekonstruktion OFFEN. Die technische Forschungsmechanik kann mit einem getrennten synthetischen Testgraphen als ARBEITSWERT geprüft werden; dieser wird nicht als Originalbaum ausgegeben.

**Nutzeraktion:** Noch kein Samsung-Test allein aufgrund erfolgreicher Hosttests. Offene fachliche Entscheidungen gezielt benennen.

## Phase 4: APK bauen und den tatsächlichen Android-Ablauf prüfen

**Arbeit:** Passende Godot-Exportvorlagen und Android-Bauumgebung verwenden, eine eigenständige Elvenland-Paketkennung einsetzen, APK bauen und mit getrennt verwaltetem Testschlüssel signieren. Vorherige Apps und Spielstände bleiben unangetastet. Version, Dateiname, Paketkennung, Hash und Zertifikatsfingerabdruck dokumentieren.

**Android-Prüfung vor der Testfreigabe:**

| Prüfung | Konkretes Erfolgskriterium |
|---|---|
| Paket und Signatur | APK strukturell gültig, Signatur geprüft, Paket und Version stimmen mit dem Bericht überein. |
| Installation und Start | APK installiert auf der tatsächlich benannten Android-Umgebung und erreicht reproduzierbar die Stadt. |
| Offline-Start | Neuer Prozess startet ohne Originalserverkontakt und ohne erforderliches Onlinekonto. |
| Touchbedienung und Anzeige | Auswahl, Platzierung und Rückmeldung lassen sich tatsächlich bedienen; Ressourcenanzeige folgt dem Modell. |
| Lokaler Ablauf | Angegebener Bau-/Produktionsablauf läuft mit einmaliger Buchung durch. |
| Prozessneustart | Stadt, Ressourcen, Bau-/Produktionsaufträge und Abholstatus werden korrekt wiederhergestellt. |
| Externe Sicherung | Android-Dokument wird außerhalb privater App-Daten exportiert und über den tatsächlichen Android-Dateizugriff importiert. |
| Neuinstallation | Auf einer dafür vorgesehenen Testinstallation lässt sich der vorher extern gesicherte Zustand nach Neuinstallation wiederherstellen. |

Die Neuinstallationsprüfung niemals ungefragt an einer bestehenden App mit dem einzigen Spielstand ausführen. Sie gehört auf eine separate Testinstallation oder ein geeignetes Testgerät mit vorher bestätigter externer Sicherung.

**Ergebnis:** Erst nach den jeweils belegten Prüfungen eine passend bezeichnete Test-APK bereitstellen. Ein fehlender Android-Lauf ist ein offener Nachweis, kein bestandener Starttest. Eine noch fehlende Samsung-Abnahme wird ausdrücklich genannt.

**Konkreter Samsung-Test:** Flugmodus aktivieren, Elvenland starten, den einen dokumentierten Bau-/Produktionsablauf durchführen, App vollständig schließen und erneut starten. Anschließend den exportierten Spielstand über den vorgesehenen Importdialog prüfen. Testdauer und erwartete Werte ergeben sich aus der tatsächlich gebauten Version; keine Platzhalter als ausgeführte Prüfung ausgeben.

## Erweiterungen nach dem ersten vollständigen Ablauf

Weitere Gebäude, Ausbau, zusätzliche Produktionsketten, Forschung, Einheiten und gegebenenfalls lokaler Kampf werden mit ausreichend belegten Definitionen oder getrennten, dokumentierten ARBEITSWERTEN für einen Prototyp ergänzt. Fehlende Originaldaten bleiben OFFEN, bestehende FEST-Werte bleiben verbindlich. Bei deutlich unterschiedlichen Konsequenzen nachfragen. Große fehlende Datensätze sind getrennte Arbeitspakete. Onlinefunktionen werden dadurch nicht still wieder eingeführt.

## Abschlussformat jedes Arbeitsgangs

- **Erledigt:** konkret erstellte oder übernommene Dateien und Funktionen.
- **Nachgewiesen:** tatsächlich ausgeführte Prüfungen mit ihrer Umgebung und Reichweite.
- **Offen:** fehlende Daten, Entscheidungen, Software oder Laufzeitnachweise.
- **Nächster Schritt:** genau der nächste notwendige Roadmap-Schritt.
- **Nutzertest:** eine unmittelbar ausführbare Aufgabe mit erwarteten Ergebnissen oder ausdrücklich „Noch kein sinnvoller Telefon-Test erforderlich“.

Eine neue Testversion muss eine konkrete offene Frage beantworten oder einen tatsächlichen Spielschritt hinzufügen. Reine Wiederholung bereits bekannter Diagnoseergebnisse ist kein Fortschrittsziel.
