# Arbeitsauftrag für ChatGPT oder Claude

Den folgenden Auftrag gemeinsam mit dem Elvenland-Paket oder dessen zugänglichem Repository verwenden. Er setzt keine Erinnerung an frühere Chats voraus.

## Auftrag

Arbeite an **Elvenland**, einem neuen, einfach aufgebauten Offline-Spiel für Android, das die wesentlichen lokalen Elvenar-Spielmechaniken mit den im Paket tatsächlich vorhandenen Ressourcen rekonstruiert. Der Nutzer hat einen eigenen Aufbau mit Godot oder Unity ausdrücklich erlaubt. Empfohlen ist **Godot 4.6.3, GDScript und eine isometrische 2D-Darstellung**. Die vorhandenen extrahierten Sprites sollen anhand ihrer Indizes zugeordnet werden.

Die ursprüngliche Unity-App, ihr Client-/Serverprotokoll und ihre native Bridge sind kein zu portierender Laufzeitunterbau. Entwickle einen direkten lokalen Spielkern. Onlinekonto, Cloud-Synchronisation, Gilden, Mehrspielermarkt, Online-Shop und globale Events sind für diesen Offline-Kern entbehrlich.

## Beginne mit den tatsächlichen Dateien

1. Prüfe, ob das Paket oder Repository lesbar ist. Öffne zuerst `START_HERE.md` und `STATUS.json`, dann den dort angegebenen Dateiindex. Verwende keine Daten allein aufgrund eines früheren Chatberichts.
2. Lies die historischen Datenhinweise `README_HISTORICAL_DATA.md`, die Belegliste `evidence_and_coverage.json` und das Transformationsprotokoll `privacy_and_transformations.json` an ihren indexierten Orten.
3. Lies `AGENTS.md`, `docs/ARCHITECTURE.md` und `docs/ROADMAP.md`. Prüfe vorhandenen Code und arbeite am nächsten noch offenen Roadmap-Schritt weiter.
4. Prüfe die benötigten Quellarchive und Dateien gegen vorhandene Hashwerte. Erfinde keine fehlenden Bilder, Audiodateien, Spieltabellen oder Testresultate.
5. Wenn ein Link ohne Anmeldung nicht lesbar ist, behaupte keinen erfolgreichen Abruf. Nutze eine beigefügte ZIP oder benenne genau das fehlende Paket beziehungsweise den fehlenden Zugriff. Fordere keine Passwörter oder veröffentlichten Zugriffstokens an.

## Datenlage und verbindliche Grenzen

Die historische Startreferenz enthält 26 Felder. Sie beschreibt unter anderem zwei Stadtobjekte und bestimmte damalige Ressourcenbestände. Im visuellen Manifest stehen 139 Referenzen, davon 138 mit eigenen Qualitätsvarianten und ein Alias. Die historischen Tabellen enthalten unter anderem 245 Ressourcengruppen, 1.500 Freischaltungseinträge und 13 Feature-/Technologiezuordnungen.

Diese Mengen sind keine Vollständigkeitsbehauptung für das gesamte Spiel. **Der vollständige Forschungsbaum, vollständige Gebäudekosten und Produktionsrezepte sind in den geprüften Tabellen nicht vorhanden.** Die jeweils aktuellen Abdeckungsdateien im Paket haben Vorrang vor dieser Zusammenfassung.

- **FEST** bezeichnet eine ausdrückliche Nutzerentscheidung.
- **BELEGT_HISTORISCH** bezeichnet einen Wert aus einer überprüfbaren früheren Quelle. Er wird dadurch nicht automatisch zum aktuellen Originalwert oder zu einer verbindlichen Elvenland-Regel.
- **ARBEITSWERT** bezeichnet einen vorläufigen, deutlich gekennzeichneten Testwert oder Vorschlag mit dokumentiertem Zweck und Geltungsbereich.
- **OFFEN** bezeichnet eine fehlende Information, Entscheidung oder Prüfung.

Erhalte Originalreferenzen unverändert. In neu normalisierten Spieldefinitionen bleiben unbekannte Werte `null` und OFFEN. Bei 1.493 Freischaltungseinträgen fehlt das Feld `unlocked`; setze es nicht automatisch auf `false`. Auch fehlende Koordinaten und Premiumkoeffizienten nicht still durch numerische Nullwerte ersetzen.

Verwende keine erfundenen Forschungsabhängigkeiten, Baukosten, Produktionszeiten oder Belohnungen als angebliche Originalmechanik. Für einen gesonderten Prototyp darfst du mit klar gekennzeichneten ARBEITSWERTEN weiterarbeiten. Halte diese in einer getrennten Konfiguration und dokumentiere jede Annahme. Unbekannte Originalwerte bleiben OFFEN; bestehende FEST-Werte werden ausschließlich mit ausdrücklicher Nutzerbestätigung ersetzt. Frage nur bei deutlich unterschiedlichen Konsequenzen nach. Gewöhnliche technische Umsetzungsentscheidungen erfordern keine neue Bestätigung.

## Zielarchitektur

Trenne fünf Bereiche:

1. Geprüfte Definitionen für Ressourcen, Gebäude, Produktionsrezepte und Forschung.
2. Einen zentralen lokalen `GameState` mit Ressourcen, Stadt, laufenden Aufträgen und Fortschritt.
3. Lokale Befehle für Platzierung, Produktion, Abholung, Forschung und zulässige weitere Aktionen.
4. Godot-Oberfläche, Stadtanzeige und Audio, die ausschließlich den übernommenen Zustand darstellen.
5. Versionierte Speicherung mit Wiederherstellung sowie externem Export und Import.

Baue einen kleinen vollständigen Ablauf mit belegten Definitionen oder einer ausdrücklich als Prototyp gekennzeichneten ARBEITSWERT-Konfiguration: Stadt öffnen, Gebäude im Baumenü auswählen, gültig platzieren, Kosten genau einmal abbuchen, Bauauftrag fertigstellen, produzieren, genau einmal abholen, speichern und nach Neustart denselben Zustand anzeigen. Benenne im Ergebnis, welche Regeln belegt sind und welche ausschließlich den Prototyp betreffen. Die Oberfläche muss sich nach jeder erfolgreichen Zustandsänderung korrekt aktualisieren.

Die Definitionen müssen später über gut lesbare Datendateien bearbeitbar sein. Plane eine validierte lokale Übernahme solcher Werte ein. Speichere Änderungen als ausdrücklich gekennzeichnete Elvenland-Anpassungen; überschreibe die historischen Referenzen nicht.

Die originalgetreue Forschungsrekonstruktion benötigt vollständige Definitionen für den jeweiligen Teilbaum. Die Mechanik kann unabhängig davon mit einem getrennten synthetischen Testgraphen als ARBEITSWERT geprüft werden. Weder dieser Testgraph noch die vorhandenen Feature-/Technologiezuordnungen dürfen als fertiger Original-Techbaum ausgegeben werden.

## Vier Arbeitsphasen

**Phase 1: Quellen und Abdeckung.** Vorhandene Pakete, Versionen, Herkunft, Hashwerte und offene Datenlücken prüfen. Die Ergebnisse in Status und Index festhalten.

**Phase 2: Daten und eigenes Projekt.** Godot-Projekt eigenständig aufsetzen, Sprites/Audio zuordnen, normalisierte Definitionen mit Herkunft erstellen und eine nutzbare Stadtanzeige sowie ein datenabhängiges Baumenü vorbereiten.

**Phase 3: Lokaler Spielkreislauf.** Transaktionen, gültige Platzierung, Timer, Produktion, belegte Forschung und robuste Speicherung umsetzen. Fehler und doppelte Eingaben dürfen weder Ressourcen erzeugen noch doppelt belohnen. Importierte Daten validieren.

**Phase 4: APK und Android-Prüfung.** Mit passender Exportumgebung eine neue Elvenland-APK bauen und signieren. Installation, Start, Flugmodus, Bedienung, Prozessneustart und Wiederherstellung konkret prüfen. Externen Android-Dokumentexport und Import über Storage Access Framework oder einen belegbar gleichwertigen Android-Weg prüfen. Danach genau einen sinnvollen Samsung-Testauftrag mit Abnahmekriterien geben.

## Tests und Abschluss

Hosttests und simulierte Schnittstellen sind keine Android-Tests. Ein erfolgreicher Build ist kein erfolgreicher App-Start. Benenne jedes Ergebnis mit seinem tatsächlichen Prüfumfang. Gib keine ungeprüfte APK als funktionierende Testversion aus. Der Nutzer wünscht ungefähr 100 Minuten für Auslesen, Analyse, Datenübernahme, Neuaufbau und neue APK insgesamt. Ein vollständiger originalgetreuer Nachbau innerhalb dieses Gesamtbudgets lässt sich nicht belastbar zusagen. Arbeite auf dieses Ziel hin und benenne tatsächlichen Fortschritt und verbleibenden Aufwand; deute den Zeitwunsch nicht als ausschließliches Analysebudget um.

Übernimm keine privaten Rohreferenzen, Besitzer-/Kontodaten, Signierschlüssel oder Zugangsdaten in veröffentlichte Dateien. Dokumentiere die Herkunft von neuem Code und Originalressourcen getrennt. Behaupte keine MIT-Lizenz für Originalgrafiken, Musik oder Originalcode.

Arbeite selbstständig bis zum nächsten konkret überprüfbaren Ergebnis weiter. Beende den Bericht mit **erledigt, nachgewiesen, offen, nächster Schritt und konkreter Nutzertest**. Wenn eine Voraussetzung fehlt, nenne die genaue Datei, den fehlenden Wert oder den fehlenden Zugriff und was bis dahin trotzdem fertiggestellt wurde.
