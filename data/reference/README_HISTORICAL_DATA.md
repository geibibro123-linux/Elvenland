# Elvenland: tatsächlich wiedergefundene Spieldaten

Stand der Prüfung: 17.11.2026. Die Daten stammen aus der in Build 02 eingebetteten Datei `assets/offline_lab/reference_start_v4_v5.json` und dem damaligen visuellen Assetmanifest. Der SHA-256-Wert der Referenz wurde gegen das wiedergefundene Inventar geprüft und stimmt überein:

`3c4a3ef6a6bb3da5ff6da32480d6cea05052b908479b6e814b49faab952ec4cb`

**Diese Dateien sind historische Referenzen. Sie sind keine erneut vom Originalserver bestätigten aktuellen Spielwerte und keine automatisch verbindlichen Elvenland-Balancingentscheidungen.** In den JSON-Dateien wird dies durch `HISTORICAL_EMBEDDED_REFERENCE`, `current_server_values_verified: false` und `approved_elvenland_balance: false` ausgedrückt. Das sind Herkunftskennzeichnungen, keine Spielparameter.

## Vorhandener Inhalt

| Inhalt | Tatsächlich gefunden | Dateiname |
|---|---|---|
| Minimaler Stadt- und Ressourcenstand | 2 Stadtobjekte, Kartengröße 80 × 80, 12.000 Münzen, 1.200 Vorräte und 200 Premiumeinheiten in dieser Referenz. Forschungspunkte 10 von 10. | `historical_initial_state_minimal.json` |
| Visuelle Stadtreferenzen | 139 Referenzen im Manifest. 138 besitzen insgesamt 272 Qualitätsvarianten. `E_Province_1` ist ein zusätzlicher Alias auf `City_Expansion_Fence`. | `city_visual_catalog.json` |
| Ressourcengruppen | 245 Gruppen mit zusammen 557 unterschiedlichen technischen Ressourcen-IDs. | `historical_resource_sets.json` |
| Beobachtete Freischaltungsfelder | 1.500 Einträge. 7 enthalten ausdrücklich `unlocked: true`; bei 1.493 fehlt das Feld. | `historical_item_unlock_observations.json` |
| Feature-/Forschungszuordnungen | 13 Zuordnungen mit 11 unterschiedlichen Technologie-IDs. | `historical_feature_technology_links.json` |
| Forschungspunkte-Pakete | 6 historische Kosten-/Ertragsdatensätze. | `historical_knowledge_point_packages.json` |
| Produktionsbonus-Stufen | 61 Bonusstufen, überwiegend mit Reliktbedarf. Keine Produktionsrezepte. | `historical_production_boost_steps.json` |
| Premiumkoeffizienten | 31 Einträge. In zwei Einträgen fehlt der Wert `premium_price`. | `historical_premium_coefficients.json` |
| Armee-Referenz | Beobachtete Einheitenbestände und technische Referenzwerte aus diesem Startzustand. Keine vollständige Einheitentabelle. | `historical_army_reference.json` |
| Abdeckung und Herkunft | Hashwerte der Eingangsarchive, geprüfte Mengen und konkrete Lücken. | `evidence_and_coverage.json` |
| Datenschutz und Transformationen | Dokumentiert ausgelassene Bereiche und entfernte Instanzkennungen. | `privacy_and_transformations.json` |

Die minimalen Stadtobjekte sind `H_Elves_Townhall_1` und `Z_Elves_WorkerHut_1`. Die ursprünglichen Instanz-IDs wurden entfernt. Technische Gebäudecodes bleiben erhalten. Die enthaltenen Bestände sind eine historische Beobachtung eines Startzustands, keine allgemeingültige Zusage für jedes Volk, Kapitel oder jede Spielversion.

## Was für einen originalgetreuen Neubau noch fehlt

- Vollständige Gebäudeökonomie mit Kosten, Bauzeiten, verifizierten Grundflächen, Bevölkerungs-/Kulturwirkung und Ausbaupfaden.
- Produktionsrezepte mit Gebäudezuordnung, Eingabemengen, Erträgen, Laufzeiten und Warteschlangenregeln.
- Der vollständige Forschungsbaum mit Knoten, Elternabhängigkeiten, Punktkosten, Ressourcenanforderungen, Torbedingungen und Freischaltungen.
- Vollständige Einheitentabellen, Kampfregeln und deren konkrete Werte.
- Vollständige Zuordnung sämtlicher Grafiken und Animationen zu einer spielbaren Definition.

`research_tree_status.json` dokumentiert die belegten Technologie-IDs und die offenen Bestandteile. Es enthält absichtlich keinen erfundenen Ersatzbaum.

Die Klassen-/Feldnamen eines Forschungsdatensatzes sind im historischen Engineering-Checkpoint dokumentiert. Dessen `original_research_planner.js` verlangt echte Konfigurationen als Eingabe. Er liefert diese nicht selbst. Ein vorhandener Klassenname oder ein Icon ist deshalb kein Beleg für Kosten oder Abhängigkeiten.

## Regeln für ChatGPT, Claude und weitere Importer

1. Fehlende Felder unverändert als fehlend behandeln. Nicht automatisch `false`, `0`, einen kostenlosen Bau oder eine leere Abhängigkeit daraus machen.
2. Bei 1.493 Freischaltungseinträgen fehlt `unlocked`. Daraus darf weder „freigeschaltet“ noch „gesperrt“ als belegte Originalregel abgeleitet werden.
3. Bei beiden Stadtobjekten und dem freigeschalteten Bereich fehlt die y-Koordinate. Die Originalserialisierung könnte einen Standardwert verwenden; dieser wurde hier nicht nachgewiesen. `y=0` daher nicht still ergänzen.
4. In Konstruktionsgrafiknamen wie `C_Elves_2x2` enthaltene Größen sind zunächst visuelle Bezeichnungen. Sie ersetzen keine geprüfte spielmechanische Kollisions- oder Grundflächendefinition.
5. Die 13 Feature-/Technologiezuordnungen sind kein vollständiger Forschungsbaum. Ein Technologiecode belegt noch keine Elternkante oder Punktkosten.
6. Premiumkoeffizienten allein ergeben keine vollständige Preisformel. Fehlende Werte sind nicht automatisch null.
7. Forschungspunkte-Pakete sind historische Daten. Sie sind weder automatisch genehmigte Elvenland-Preise noch ein Auftrag zur Übernahme von Onlinekaufmechanismen.
8. Armee-Referenzmaxima wie `maxBaseDamageReference` nicht jedem Einheitentyp als Schaden zuordnen. Die Datei ist keine Einheitendatenbank.
9. Alle Onlinefeatures aus historischen Tabellen nur als Beleg aufbewahren. Das neue Offline-Spiel benötigt sie nicht automatisch. Ihr Auftreten in einer Referenz autorisiert keinen neuen Onlineumfang.

## Technische Grenzen dieser Prüfung

Die ausgewählten JSON- und Katalogdateien wurden vollständig gelesen. Zusätzlich wurden alle 44 TextAssets aus den Unity-Szenen/Ressourcen vollständig exportiert und geprüft. Ihre 44 Quelldateien stimmen mit den SHA-256-Werten des ursprünglichen Inventars überein. Gefunden wurden weitere Darstellungs- und Audiokonfigurationen, aber keine vollständige Forschungs-, Gebäudekosten-, Produktionsrezept- oder Übersetzungstabelle. Eine vorherige gezielte Bytesuche erfasste außerdem sämtliche 4.633 Archiveinträge. Das ist weiterhin keine vollständige semantische Dekodierung aller Unity-MonoBehaviour-Objekte. Weitere noch nicht dekodierte binäre Konfigurationen bleiben OFFEN.

## Ergänzung: 44 geprüfte Unity-TextAssets

28 Nutzdateien sind zur Weitergabe freigegeben: neun Spine-Skelettdateien mit zusammen 23 benannten Animationen, neun zugehörige Atlanten, sechs Audiokonfigurationen mit 214 Einträgen, eine Audio-Mix-XML, das visuelle Manifest und zwei Zeichensätze für Zeilenumbrüche. Die 203 Einträge der Gebäudesammel-Audiokonfiguration sind Soundereignisse, keine 203 vollständigen Gebäudedefinitionen. Die Zeichensätze sind keine Übersetzungstabelle.

19 Dateien bleiben byteidentisch. Bei neun Spine-Dateien wurden die reinen Editorpfade unter `skeleton.images` und `skeleton.audio` entfernt; darunter waren acht absolute lokale Pfade. Knochen, Slots, Skins und Animationskurven wurden nicht verändert. Die Wiedergabe der Spine-Daten in Godot ist ein eigener, noch offener Integrationsnachweis.

16 Dateien aus TLS-/Credential-Infrastruktur sowie Build-/Testmetadaten werden nicht veröffentlicht. Darunter ist ein Performance-Testbericht mit Geräte-/Entwicklungsumgebungsangaben. Die Hash-basierte Freigabeliste und der reproduzierbare Exporthelper dokumentieren für alle 44 Quellen die Entscheidung und für die 28 Nutzdateien den erwarteten Ausgabehash. Der Helper erzeugte alle freigegebenen Ausgaben erneut aus den Quelldateien mit exakt passenden Hashwerten.

Es wurden keine Originalserver-Anfragen ausgeführt, keine Spielwerte erfunden und keine APK gebaut. Die öffentlichen Datentabellen enthalten keine Profile, Einstellungen, Besitzerkennungen, Gerätekennungen, Sitzungen oder Zugangsdaten. Die unveränderte Rohreferenz gehört nicht in dieses öffentliche Teilpaket.

## Reproduzierbarkeit

Das ergänzende Skript `prepare_historical_tables.py` nimmt ein Verzeichnis mit den wiedergefundenen Eingangsarchiven und ein Ausgabeverzeichnis entgegen. Es prüft den erwarteten Referenzhash, exportiert nur die aufgeführten Datenbereiche und erhält fehlende Felder. Es arbeitet vollständig lokal und ruft keinen Spielserver auf.

## Begrenzter Überblick über MonoBehaviour-Objekte

Alle 45.620 Objekt-Header wurden geprüft. 45.617 Instanzen wurden 1.351 Scriptklassen zugeordnet, bei drei Instanzen blieb die Klassenzuordnung offen. Der Überblick enthält 138 fachlich benannte Kandidatenklassen. Eine repräsentative Instanz je Kandidatenklasse wurde auf vollständige Lesbarkeit geprüft: 14 enthalten nur die vier Unity-Basisfelder, bei 124 fehlt eine vollständig verwendbare Typstruktur für die individuellen Nutzdaten. Unter den benannten Datenobjekten befinden sich `UnitClassDefinitions` und `RarityDefinitions`. Ihre fachlichen Werte sind damit noch nicht dekodiert oder als Spieltabellen freigegeben. Die Methode und konkreten Quellobjekte stehen in `monobehaviour_scope.json` und `docs/MONOBEHAVIOUR_SCOPE.md`. Vollständige Kosten, Produktionsrezepte und der Forschungsgraph bleiben OFFEN. Der Überblick beweist nicht, dass solche Daten in den noch nicht dekodierten Nutzdaten fehlen.

## Nachtrag zur Forschung, Stand 20.11.2026

**Abgrenzung:** Die obige Bestandsliste und der Stand vom 17.11.2026 beschreiben *nur* die damalige eingebettete Original-/Lab-Referenz. Diese Liste ist nicht die Gesamtheit der inzwischen gefundenen externen Forschungskonfigurationen.

- **Kapitel VI-XXVI:** 767 strukturierte historische/community Elfen-Definitionen mit `id`, `kp`, `requirements`, `parentIds`, `childrenIds` in [`community_idavis_research_ch06_ch26_2026-11-20.json`](community_idavis_research_ch06_ch26_2026-11-20.json). Ihre 21 Kapitel ergeben 82.540 Wissenspunkte. Ein fehlender Anschluss an Kapitel V (`elves_all3_aw`) und fuenf nicht-reziproke Kanten sind dokumentiert. **Nicht** automatisch als aktuell originalgueltige Elvenland-Regeln uebernehmen.
- **Kapitel I-V:** Laut aktualisiertem Elvenarchy-Guide 124 Elfen-Technologien insgesamt 2.785 WP, neun einzelne WP-Daten und einige Human-Vergleichswerte, siehe [`community_early_research_ch01_ch05_2026-11-20.json`](community_early_research_ch01_ch05_2026-11-20.json). 26 zusaetzliche *historische Bildbeobachtungen*, keine 26 sicher zusaetzlichen IDs, in den drei `community_*screenshot*.json`-Referenzen. Vollstaendige Preise und `parentIds` OFFEN.
- **Jetzt lauffaehiger technischer APK-Scan:** GitHub Actions untersuchte zwei voneinander getrennte Testversionen, `Lab04` und `Lab09`, SHA-256-geprueft mit UnityPy und 44 TextAssets je APK. Forschungs-UI-/ConfigVO-Klassen sichtbar, **0 vollstaendige Forschungsdatenzeilen dekodiert**. [Quellenbericht](../../docs/RESEARCH_CH01_CH05_EVIDENCE_2026-11-20.md).
- **Original-Balancingquelle gefunden:** Die oeffentliche Erweiterung `paviad/elvenar-helper-extension` belegt die Struktur `xml.balancing.research.ResearchTechnologiesElves_<hash>.json` und `ResearchTechnologiesHumans_<hash>.json`, mit originalen `maxSP`, `requirements.resources`, `parentIds`, `rewards`, `gate`. Die dokumentierte Beispiel-URL lieferte HTTP 404; ein gueltiger aktueller Hash fehlt noch. [Technische Beschaffungsanleitung](../../docs/RESEARCH_BALANCING_ORIGINAL_SOURCE_2026-11-20.md).
- **Fuer UI schon normalisiert:** [`compiled_research_readonly_preview_2026-11-20.json`](compiled_research_readonly_preview_2026-11-20.json) mit **776 Vorschauknoten**, davon 9 fruehe unvollstaendige Community-Knoten und 767 spaetere strukturierte Datensaetze. Wurde [in GitHub Actions erfolgreich validiert](https://github.com/geibibro123-linux/Elvenland/actions/runs/44832731386). Alle bleiben **read-only** und `activation_ready: false`; aktive `data/definitions/research_nodes.json` bleibt leer.
- **FEST als Nutzerentscheidung:** Bei widerspruechlichen vergleichbaren Forschungskosten den kleinsten dokumentierten Wert fuer Elvenland auswaehlen. Die urspruenglichen Quellenkosten getrennt archivieren. Elfen und Menschen, Technologie-Forschung und Gebaeudebau, sowie Graphversionen voneinander trennen.
- **Onlinefeatures:** Nur lokales Konzept erarbeiten, fuer aktuelle APK OFFEN. [Konzept](../../docs/ONLINEFUNKTIONEN_OFFLINE_KONZEPT_OFFEN_2026-11-20.md).
- **Gesamte Build-Schnittstelle und Sicherheits-Gates:** [`RESEARCH_IMPORT_READINESS_2026-11-20.md`](../../docs/RESEARCH_IMPORT_READINESS_2026-11-20.md).

Dieser Nachtrag aendert die Originaldaten vom 17.11.2026 nicht. Insbesondere werden fehlende Forschungswerte **niemals** als Nullpreis oder leere Voraussetzung interpretiert.
