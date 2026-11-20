# Elvenland | Onlinebezogene Originalfunktionen: lokales Konzept (OFFEN)

**Projektentscheidung am 20.11.2026:** Die originale Funktionsweise und moegliche lokale Alternativen werden analysiert und fuer die spaetere Produktentscheidung ausgearbeitet. **Nicht** in die aktuelle APK uebernehmen. Die hier aufgefuehrten Loesungen sind **OFFEN**, keine bestaetigten Spielfunktionen, keine implementierten Regeln und keine genehmigten Zahlen.

## Rahmen

- Original-Forschungsbaum und belegte historische Kosten/Kapitelzuordnungen als Forschungsreferenz erhalten.
- Die Entscheidung, ein Onlinesystem spaeter lokal zu ersetzen, separat von dessen historischer Forschungskonfiguration treffen.
- Kein Onlinekonto, keine Originalserver, keine Cloud-Synchronisation, kein Multiplayerzwang fuer den Offline-Kern.
- Eine gesperrte Onlinefunktion darf nicht versehentlich wichtige lokale Grundsysteme oder Kapitelzugang dauerhaft blockieren. Die konkreten Ersatz-Gates bleiben OFFEN.
- Lokale Simulation ist keine belegte Originalmechanik. Sie muss als **Elvenland-Eigenloesung** gekennzeichnet sein.
- Die Regel **FEST** "bei mehreren vergleichbaren Kosten den kleinsten dokumentierten Wert waehlen" bleibt unabhaengig von einer Funktionsdeaktivierung gueltig.
- Keine fehlenden Forschungskosten oder Abhaengigkeiten durch 0, leere Listen oder willkuerliche Werte ersetzen.

## Kandidaten fuer spaetere Offline-Abbildung

| Originalfunktion | Online-/Serveranteil (Forschungsaufgabe) | Moegliches lokales Konzept, noch OFFEN | Auswirkung auf Forschung |
|---|---|---|---|
| Nachbarschaftshilfe | echte Nachbarstadt / Besuch | fiktive Nachbarstaedte oder lokale Hilfebelohnungen | Historische `elves_neighbourlyhelp`-Freischaltung bewahren; lokale Wirkung OFFEN |
| Gemeinschaften | Mitgliedschaft, sozialer Fortschritt | nur historische Forschung belassen, oder lokale NPC-Gruppe | `elves_fellowships` nicht vorschnell entfernen; Folge-Gates OFFEN |
| Gemeinschaftsabenteuer | gemeinsame Aufgaben / globale Synchronisation | lokale optionale Abenteuerkette oder deaktiviert | `elves_fellowship_adventures` dokumentieren; keine unbestimmte Belohnung |
| Handel / Haendler | Austausch und moegliche globale Marktangebote | lokaler NPC-/Stadthandel mit separat beschlossener Preis- und Angebotslogik | Haendlerforschung 12 WP als gewaehlter Elfen-ARBEITSWERT; Warenpreise OFFEN |
| Turniere | Rankings/Gemeinschaftswettbewerb mit PvE | lokale Kaempfe ohne globales Ranking | `elves_tournaments`; Gegnerwerte, Belohnung, Zugang OFFEN |
| Turm der Ewigkeit | Server-Spielzustand und Fortschritt, teils sozial | lokale PvE-Begegnungen mit persistiertem Zustand | `elves_spire`; nicht als rein multiplayerabhaengig behandeln |
| Hexenkessel | Serverzustand und persoenlicher Fortschritt | lokales, unabhaengiges System oder erst spaeter | `elves_cauldron`; Preise/Rezepte/Abklingzeiten OFFEN |
| Weltkarte / Provinzen | Originaldaten und Fortschritt teilweise servergebunden | lokale Provinzkarte mit bestandenen Begegnungen | Provinz-Gates fuer Kapiteluebergang nur anhand belegter Schwellen uebernehmen |
| Handwerk / Magische Akademie | urspruenglich serverpersistierte Rezepte/Angebote | lokales Rezept-/Gegenstandssystem | `elves_crafting`; Rezepte und Ressourcen OFFEN |

**Wichtig:** Die Spalte "Online-/Serveranteil" ist eine technische Pruefkategorie. Sie behauptet nicht, dass jede genannte Funktion zwingend Mehrspielerfunktionen braucht. Auch ein Einzelspielermodus kann serverseitig gespeicherte Daten benoetigen.

## Technischer Entwurf: Trennung von Forschung und Spielwirkung

Historischer Technologieeintrag (Originalquelle, unveraenderter Referenzstand) -> definierte Forschungskosten und Voraussetzungen -> lokaler, persistierter Forschungsabschluss -> separate, spaeter beschlossene `unlock_effect`-Zuordnung.

Wenn eine reine Onlinefunktion spaeter bewusst nicht umgesetzt wird, muss der Spielzustand technisch unterscheiden zwischen:
- Technologie als historischer Forschungsgraph-Knoten,
- Forschungspunkten bezahlt,
- ggf. Ressourcen zur Freischaltung bezahlt,
- Forschung abgeschlossen,
- Offline-Wirkung vorhanden, ausgesetzt oder noch OFFEN.

Die App darf eine Forschung mit unbekannten Kosten nicht unbeabsichtigt als kostenlos behandeln. Welche der onlinebezogenen Knoten im lokalen Spiel sichtbar, aktiv oder ausgegraut sind, bleibt eine spaetere ausdrueckliche Designentscheidung.

## Original-APK-Quellenkontrolle, 20.11.2026

Der im Chat neu gesendete Google-Drive-Link lieferte erfolgreich Google-Dateimetadaten und eine rohe APK-Dateireferenz:
- Datei auf Drive laut Metadaten: `Elvenar_Lab09_RequestRoute01.apk`
- Groesse: **231.769.998 Bytes**
- MIME: `application/vnd.android.package-archive`
- Das ist anhand des Dateinamens ein **Lab09-Test-/Diagnosestand**, keine nachweislich unmodifizierte Original-APK.
- Historische Projektanalysebasis in der Datei-Library: `Elvenar_Lab04_SkriptTest03.apk`, **232.466.424 Bytes**, ebenfalls ein Lab-Teststand.
- Der SHA-256 der frueheren Lab04-Referenz lautet laut Altbefund `d77de38720bde3c0894493b519cdcca6183d7d020d3377d40e2096516d6d247c`; ein neuer Byte-fuer-Byte-Abgleich scheiterte, daher kein aktuell bestaetigter Identitaetsnachweis.
- Der Roh-APK-Download via den verbundenen Drive-Zugriff war moeglich. Programmausfuehrung zur Binäranalyse scheiterte hingegen weiter an `ClientError`. **Keine neuen Forschungskonfigurationen aus der APK gelesen.**
- Aus dem historischen Sidecar sind 13 Feature-zu-Technologie-Verknuepfungen mit 11 individuellen IDs dokumentiert. Diese sind **nicht automatisch direkt aus dem Lab09-APK-Binaerinhalt nachgewiesen**.
- In einem separaten frueheren Asset-Audit wurden Forschungs-UI-Klassen wie `TechTreeTechnologyView` und `ResearchWindowMediator` ermittelt. Das beweist ein Forschungsmenue, nicht die vollstaendigen konfigurierten Technologiepreise.

**Noch sinnvollste Originalquelle:** Eine unveraenderte Installations-APK (oder Original-APK/Split-Paket mit klarer Herkunft) mit dokumentierter Paketversion und Pruefsumme. Vor einem weiteren Binary-Workflow muessen Container-/Dateiwerkzeuge wieder funktionsfaehig sein.

## OFFEN und naechste Schritte

1. Vollstaendige fruehe Kapitel-I-V-Technologiezeilen aus APK oder externen Listen nachweisen: `id`, `maxSP`, `requirements`, `parentIds`, `unlock_effects`.
2. APK-Paketidentitaet, Signatur, Version und SHA-256 fuer alte Lab04- und neu gelieferte Lab09-Datei separat pruefen; daraus allein keine Originalkonfiguration ableiten.
3. Fuer jeden onlinebezogenen Forschungszweig Originalfunktion, konkrete lokal notwendige Funktionen, minimalen Offline-Ersatz und UI-Konsequenzen mit der Nutzerschaft entscheiden.
4. Erst nach expliziter Entscheidung eigenstaendige Offline-Effektdefinitionen anlegen und auf Deadlocks, Ressourcenbuchung, Persistenz und mobile Bedienbarkeit testen.

**Status:** Konzeption dokumentiert, technische APK-Binaeranalyse weiterhin blockiert, **keine Implementierung**.
