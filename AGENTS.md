# Elvenland: verbindliche Arbeitsregeln

## Projektauftrag

Elvenland ist ein neuer, einfacher aufgebauter Offline-Nachbau der wesentlichen lokalen Elvenar-Spielmechaniken. Der Nutzer hat einen eigenen Godot- oder Unity-Aufbau ausdrücklich erlaubt. Die ursprüngliche Unity-App, ihr nativer Client, ihre Serverabfragen und die frühere Frida-Bridge sind kein zu portierender Laufzeitunterbau dieses Projekts.

FEST sind der Projektname Elvenland, der Offline-Schwerpunkt, die Wiederverwendung tatsächlich vorhandener und nachvollziehbar zugeordneter Ressourcen, später bearbeitbare Spielwerte sowie eine ehrliche Dokumentation der Grenzen. Für die Umsetzung wird Godot 4.6.3 mit GDScript und einer isometrischen 2D-Darstellung empfohlen. Diese konkrete Enginewahl ist eine technische Empfehlung innerhalb des erlaubten Rahmens, keine rückwirkend behauptete Nutzerbestätigung.

## Zuerst lesen

1. `START_HERE.md` und `STATUS.json`.
2. Den dort benannten Dateiindex und die Herkunfts-/Hashlisten.
3. `README_HISTORICAL_DATA.md`, `evidence_and_coverage.json` und `privacy_and_transformations.json` an den im Index angegebenen Orten.
4. `docs/ARCHITECTURE.md` und `docs/ROADMAP.md`.

Eine Datei gilt nur dann als verfügbar, wenn sie tatsächlich geöffnet werden konnte. Ein angekündigter Download oder eine alte Chatbehauptung ersetzt keine vorhandene Datei.

## Status und Werte

| Status | Bedeutung |
|---|---|
| FEST | Vom Nutzer ausdrücklich bestätigte Entscheidung. |
| BELEGT_HISTORISCH | Wert oder Struktur wurde in einer konkreten vorhandenen historischen Quelle gefunden. Keine automatische Bestätigung als aktueller Originalwert oder Elvenland-Regel. |
| ARBEITSWERT | Vorläufiger, deutlich gekennzeichneter Testwert oder Vorschlag. Annahme, Zweck und Geltungsbereich dokumentieren. |
| OFFEN | Information, Entscheidung oder Funktionsnachweis fehlt. |
| VERWORFEN | Durch eine neuere bestätigte Entscheidung ersetzt. |

- Originale Referenzdaten unverändert erhalten. In normalisierten neuen Definitionen unbekannte Werte als `null` mit Status OFFEN darstellen.
- Fehlende Angaben niemals still durch `0`, `false`, kostenlose Kosten, sofortige Fertigstellung oder leere Voraussetzungen ersetzen.
- Historische Werte nicht automatisch zu FEST hochstufen. Eine ausdrückliche bestehende Bestätigung nicht umdeuten.
- Für einen gesonderten Prototyp darf mit deutlich gekennzeichneten ARBEITSWERTEN weitergearbeitet werden. Diese stehen in einer getrennten Konfiguration und ersetzen weder unbekannte Originalwerte noch FEST-Werte. Originalgetreue Regeln mit fehlenden Voraussetzungen bleiben OFFEN. Nur bei deutlich unterschiedlichen Konsequenzen nachfragen; bestehende FEST-Werte ausschließlich mit ausdrücklicher Nutzerbestätigung ersetzen.
- Technische Entscheidungen wie Dateiaufteilung, IDs, Fehlerbehandlung und eine einfache UI selbstständig umsetzen, soweit sie keine neuen Spielregeln festlegen.
- Technische Katalog- und Gebäudecodes bewahren. Begriffe und Preise nicht aus Dateinamen erraten.

## Architektur und Umfang

- Ein lokaler Spielzustand ist die verbindliche Quelle für Ressourcen, Gebäude, Aufträge und Forschungsfortschritt.
- Die Oberfläche zeigt diesen Zustand an. Sie führt keine zweite Ressourcenbuchhaltung.
- Spieldefinitionen und technische Darstellung getrennt halten. Kosten, Zeiten und Voraussetzungen werden aus validierten Datendateien geladen.
- Gebäudeplatzierung prüft reale definierte Grundflächen, Überschneidung, freigeschaltete Flächen, Ressourcen und belegte Voraussetzungen vor der Buchung.
- Kosten und Zustandsänderung gemeinsam übernehmen. Doppelte Eingaben dürfen nicht doppelt abbuchen oder doppelt belohnen.
- Produktions- und Bauaufträge müssen einen Prozessneustart überstehen. Eine Abholung vergütet einen Auftrag höchstens einmal.
- Rekonstruierte Forschung benötigt belegte Knoten, Abhängigkeiten, Kosten und Wirkungen. Die Mechanik darf mit einem getrennten, als ARBEITSWERT gekennzeichneten Testgraphen geprüft werden. Der vorhandene Feature-/Technologieindex und ein solcher Testgraph sind kein vollständiger Original-Forschungsbaum.
- Onlinekonto, Cloud-Synchronisation, Gilden, Mehrspielermarkt, Online-Shop und globale Events gehören nicht zum notwendigen Offline-Kern.
- Keine ursprünglichen Serverendpunkte, Replay-Antworten, Frida-Hooks oder IL2CPP-Abhängigkeiten in den neuen Laufzeitkern aufnehmen.

## Speicherung und Android

Versionierte Spielstände atomar speichern und eine vorherige gültige Fassung zur Wiederherstellung behalten. Export und Import müssen über einen vom Nutzer ausgewählten Dokumentpfad außerhalb privater App-Daten funktionieren. `user://` allein schützt nicht vor dem Datenverlust bei Deinstallation. Für Android ist der Storage Access Framework mit einem passenden Android-Adapter zu prüfen und umzusetzen.

Keine alten Apps deinstallieren und keine alten Spielstände automatisch überschreiben oder migrieren. Ein neuer Test muss als Elvenland erkennbar sein und eine eigene Paketkennung besitzen. Vor Festlegung der konkreten Paket-/Schlüsselstrategie bereits bestätigte Nutzerregeln und vorhandene Projektdateien beachten. Signierschlüssel und Passwörter bleiben außerhalb veröffentlichter Pakete und Repository-Dateien.

## Nachweise und Veröffentlichung

- Statische Prüfung, Hosttests, Android-Installation, Android-Start und Samsung-Abnahme sind unterschiedliche Nachweise. Im Bericht genau angeben, was ausgeführt wurde.
- Erfolgreiche Mock- oder Hosttests nicht als Android-Erfolg darstellen.
- Eine ZIP ist keine APK. Ein kompiliertes APK ist noch kein Nachweis für erfolgreichen Start oder Offline-Spielbarkeit.
- Eine Test-APK erst als sinnvoll testbar anbieten, wenn Integrität, Signatur, Installation und der angegebene lokale Ablauf tatsächlich geprüft wurden. Fehlende Geräteprüfung klar benennen.
- Nur die zur Veröffentlichung vorgesehenen bereinigten Dateien übernehmen. Private Rohreferenzen, Besitzer-/Kontodaten, Sitzungen, Schlüssel und Zugangsdaten ausschließen.
- Herkunft von neuem Code, Originalcode, Grafiken, Musik und sonstigen Ressourcen getrennt dokumentieren. Eine Lizenz des neuen Codes gilt nicht automatisch für Originalressourcen. Originalressourcen nicht pauschal als MIT-lizenziert ausgeben.
- Anonyme Lesbarkeit mit einem Zugriff ohne Sitzung oder Token prüfen. Bei fehlendem öffentlichen Zugriff lokale ZIP-Übergabe verwenden oder die konkrete Zugriffslücke benennen. Ein privater GitHub-Link ist kein anonym abrufbarer Download.

## Arbeitsweise

Der Nutzer wünscht ungefähr 100 Minuten für die gesamte Kette aus Auslesen, Analyse, Datenübernahme, Neuaufbau und neuer APK. Ein vollständiges originalgetreues Spiel ist innerhalb dieses Gesamtbudgets nicht belastbar zusagbar. Den tatsächlichen Fortschritt und die verbleibenden Voraussetzungen benennen, ohne den Zeitwunsch als ausschließliches Analysebudget umzudeuten. Innerhalb einer Sitzung selbstständig bis zum nächsten belegbaren Ergebnis arbeiten. Keine neue Diagnoseserie ohne konkrete offene Frage erzeugen.

Jeder Abschluss nennt knapp: **erledigt, nachgewiesen, offen, nächster Schritt und konkreter Nutzertest**. Wenn nichts sinnvoll auf dem Telefon getestet werden kann, dies direkt sagen und keinen ungeprüften Download als Testversion ausgeben.

## FEST: Auswahl bei widerspruechlichen Forschungskosten (20.11.2026)

Der Nutzer hat festgelegt: **Bei mehreren vergleichbaren, dokumentierten Original-/Community-Werten fuer dieselbe Forschung stets den kleinsten Wert als Elvenland-Auswahlwert nehmen.** Versionen duerfen dabei unterschiedlich sein. Historische Varianten mit jeweiliger Quelle vollstaendig erhalten.

- Nur gleichartige Einheiten und Kosten vergleichen: dieselbe Technologie, Volk, Ressource und Schrittart (WP-Investition versus Forschungsaktivierung versus Gebaeudebau versus Produktion). Elfen- und Menschenwerte **nicht** gegeneinander minimieren.
- Beispiel: Forschungs-KP fuer Elfen-Haendler **12** gemaess Elvenarchy statt frueher gemeldeter **19**. Der 19-WP-Bildbericht ist bislang nicht erneut unabhaengig bestaetigt.
- Diese Auswahlregel ist **FEST**. Die daraus gewaehlt benannten Community-Daten sind als einzeln nachvollziehbare **ARBEITSWERTE** oder historische Quellenwerte gekennzeichnet, solange nicht explizit als FEST-Balance freigegeben.
- Fehlende `parentIds`, Ressourcenmengen und Produktions-/Bauzeiten bleiben OFFEN. Abwesenheit ist kein kostenloser Preis und keine freie Freischaltung. Nicht vorhandene Kosten nicht zusammenphantasieren.
- Quell- und Auswahlstand: `data/reference/community_early_research_ch01_ch05_2026-11-20.json`; Doku `docs/RESEARCH_CH01_CH05_EVIDENCE_2026-11-20.md`. Die 767 Elfen-Forschungen Kapitel VI-XXVI liegen in `data/reference/community_idavis_research_ch06_ch26_2026-11-20.json`.
- Ein direkt lesbarer historischer Screenshot belegt Marmormanufaktur **8 WP und 2.500 Muenzen** als Forschungsaktivierung. Dessen Volk ist nicht gesichert, daher nicht ungeprueft auf beide Voelker anwenden. Separater Gebaeudebau wird nicht mit Forschungspreisen verrechnet.
