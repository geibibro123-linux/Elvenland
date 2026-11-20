# Elvenland | Forschungsdaten fuer den spaeteren Android-Bau

**Quellenpruefstand:** 20.11.2026. **Keine Aenderung an der spielbaren APK.**  
**Status:** HISTORISCHES REFERENZMATERIAL mit einzelnen ARBEITSWERT-Auswahlen; nicht als vollstaendiger neuer Forschungsbaum freigegeben.

## A. Quellen, die im Build-Prozess verwendet werden koennen

| Daten | Datei | Status |
|---|---|---|
| Kapitel I-V, Elfen: 124 Forschungen, 2.785 Kapitel-Gesamt-WP | `data/reference/community_early_research_ch01_ch05_2026-11-20.json` | Kapitelzahlen und 9 einzelne Technologie-WP belegt; exakte Kosten-/Eltern-Zeilen OFFEN |
| Kapitel I, alter Screenshot: 11 sichtbare Technologietitel und WP | `data/reference/community_ch01_historical_spieletrend_screenshot_2026-11-20.json` | HISTORISCHES BILDDATUM, ohne technische IDs und Version |
| Kapitel IV, alter Screenshot: 5 Einzelanforderungen, davon 1 mit geringerer Lesesicherheit | `data/reference/community_ch04_historical_forum_screenshot_2026-11-20.json` | HISTORISCHES BILDDATUM; alter Graph nicht automatisch modern |
| Groesserer historischer Screenshot: 10 sichtbare Forschungspunktanforderungen | `data/reference/community_historical_gameguide_fr_research_screen_2026-11-20.json` | Historische Version vermutlich 2015, Kapitel der Einzelknoten nicht verifiziert |
| Kapitel VI-XXVI: 767 strukturierte Elfen-Technologieeintraege | `data/reference/community_idavis_research_ch06_ch26_2026-11-20.json` | Community-Quelle mit ID, WP, `requirements`, `parentIds` und `childrenIds`; Abweichungen dokumentiert |
| Historische Client-Sidecar-Featurezuordnung: 13 Links / 11 IDs | `data/reference/historical_feature_technology_links.json` | Provenienz aus Altarchiv, kein kompletter Forschungsbaum |
| Aktivierte Spieldaten | `data/definitions/research_nodes.json` | OFFEN / leere `definitions`; keinerlei automatisch erfundene Preise |
| Gemeinsamer Status | `data/reference/research_tree_status.json` | Quellenstand und Luecken |

Die Bildquellen ergeben **26 Beobachtungen**, nicht 26 zusaetzliche eindeutig nachgewiesene moderne Technologieknoten. Namen koennen doppelt, veraltet oder aus verschiedenen Kapiteln stammen. Nicht als 124+26 zaehlen.

## B. Technischer APK-Nachweis, jetzt erfolgreich

Die lokale Containerumgebung war mit `ClientError` auch fuer `pwd` blockiert. In GitHub Actions wurde der Scan daher erfolgreich und reproduzierbar ausgefuehrt:

- [Run 44831049326](https://github.com/geibibro123-linux/Farm-elvenar-/actions/runs/44831049326): SHA-256-gepruefte `Elvenar_Lab09_RequestRoute02.apk`, 231.770.000 Bytes, 6.492 Eintraege.
- 44 Unity-TextAssets geprueft; 232 unterschiedliche technologieaehnliche **Text-Tokens**, keine 232 echten Konfigurationszeilen.
- Klartext-Indikatoren `ResearchTechnologyConfigVO`, `parentIds`, `requirements` in Metadaten und Sidecar gefunden. **Vollstaendig dekodierte Technologien aus dem APK-Binaerinhalt: 0.**
- [JSON-Scanbericht](https://github.com/geibibro123-linux/Farm-elvenar-/blob/main/docs/research_apk_scans/lab09_route02_structural_scan_2026-11-20.json).
- Ein weiterer [GitHub-Actions-Scan](https://github.com/geibibro123-linux/Farm-elvenar-/actions/runs/44831608464) konnte die oeffentliche Elvenarchy-Seite `/research` lesen. Das HTML enthaelt keine Inline-Definitionen; zugehoerige JS-Dateien lieferten 403. Daher kein rechtmaessig verfuegbarer API-Komplettdatensatz aus diesem Versuch. Die normalen Kapitel-Guides bleiben lesbar.

**Versionsrisiko:** Die vorherige APK Lab04, die bereitgestellte Google-Drive-Lab09-Route01 und die jetzt gepruefte Release-Lab09-Route02 sind unterschiedliche Dateien. Aussage des Nutzers: Die Original- und veraenderte APK haben denselben Forschungsbaum. Das wird als Nutzerwissen aufgenommen, nicht als binarer Identitaetsnachweis ausgegeben.

## C. Pflichtvertrag fuer normalisierte Forschungsdefinitionen

Fuer einen spaeteren Import je Technologie mindestens vorsehen:

| Feld | Typ | Regel |
|---|---|---|
| `tech_id` | String oder null | Originalcode erhalten, fehlende IDs nicht generieren und als original ausgeben |
| `race` | `elves`, `humans` oder `unknown` | Elfen und Menschen nicht verwechseln |
| `chapter` | Integer oder null | Historische Screenshot-Zuordnung darf offen sein |
| `name` | String | Quelltextname, ggf. lokalisierte Anzeige separat |
| `kp_cost` | Integer oder null | Nutzerregel: kleinster belegter vergleichbarer WP-Wert; Varianten getrennt archivieren |
| `activation_requirements` | Resource->Integer oder null | **null = OFFEN, nicht kostenlos** |
| `parentIds` | Stringarray oder null | **null = unbekannt, nicht frei erforschbar** |
| `unlock_effects` | Liste oder null | Originalfunktion von spaeterer lokaler Offline-Wirkung trennen |
| `source_version` | String oder null | Alte Bilder nicht als neuer 2026-Graph ausgeben |
| `source_url` | String | Herkunft jedes importierten Werts |
| `data_status` | `HISTORISCH`, `ARBEITSWERT`, `OFFEN` | FEST nur bei explizit bestaetigter Regel |
| `import_ready` | Boolean | true erst wenn Kosten und Kanten fuer geplante Funktion ausreichen |

**FEST**: Fuer *vergleichbare* Kosten derselben Technologie, desselben Volks und derselben Ressourcenart den kleinsten belegten Wert verwenden. **Nicht** die alte Topologie mit dem modernen Baum mischen. In der Community berichteten Spieler im Juli 2023 von einer frueheren Kapitel-I-V-Baumaenderung und Migration alter Konten, siehe [Quellenbericht](RESEARCH_CH01_CH05_EVIDENCE_2026-11-20.md).

## D. Stand der Graphpruefung und kritische Warnungen

- Die 767 iDavis-Knoten aus VI-XXVI lassen sich laut bereits durchgefuehrter Referenzpruefung als gerichteter `parentIds`-Graph topologisch ordnen. Es gibt jedoch **einen fehlenden externen Elternknoten**: `elves_scouting_6` verlangt `elves_all3_aw` aus Kapitel V.
- `childrenIds` und `parentIds` sind an Kapiteluebergaengen **nicht durchgehend gegenseitig konsistent**. Die originalen `parentIds` als primaere Abhaengigkeit verwenden, nicht blind beide Richtungen zusammenfuehren.
- Die ersten fuenf Kapitel haben keine nachgewiesenen vollstaendigen `parentIds` oder `requirements`. 2.785 WP ist ein historischer Kapitel-Gesamtwert und muss nach Kosten-Minimierung gegebenenfalls neu berechnet werden.
- **KEINE automatische Gratis-Forschung** bei fehlendem `requirements`-Feld. **KEINE angenommene Wurzelforschung** bei unbekanntem `parentIds`-Feld.
- Original-Onlinesysteme wie Gemeinschaften, Turniere und Turm bleiben fuer die aktuelle APK **OFFEN**. Konzeption getrennt in [Offline-Konzept](ONLINEFUNKTIONEN_OFFLINE_KONZEPT_OFFEN_2026-11-20.md).

## E. Naechste Bau-/Forschungsaufgaben

1. **Kapitel I-V:** Fehlende Einzelzeilen mit ID, WP, Kosten und Vorgangern aus weiteren Quellen sammeln. Fruehe Knoten nicht durch fehlende Preise freischalten.
2. **Kapitel V-VI:** `elves_all3_aw` korrekt zuordnen. Ohne Brueckeneintrag ist der volle Graph nicht geschlossen.
3. **Normalisieren und validieren:** Alle Quellen pro Volk und Versionsfamilie trennen; Konfliktminimum nur innerhalb vergleichbarer Kostenfelder.
4. **Erste Darstellung:** Auf Wunsch eine nicht freischaltende, referenzbasierte Forschungsvorschau im Godot-Build umsetzen. Unbekannte Knoten/Kosten deutlich als OFFEN markieren.
5. **Aktivierter Spielkreislauf:** Erst nach Quellenvollstaendigkeit oder einer ausdruecklich bestaetigten lokalen Alternativregel den Forschungszustand und Ressourcenabbuchungen implementieren und automatisiert testen.

**Abschluss:** Kein neuer Android-Test aus dieser Recherche. GitHub-Datenbasis und reproduzierbare technische Scans sind bereit; vollstaendige historische Fruehkapitel-Kosten sind weiterhin OFFEN.

## F. Neuer Original-Balancing-Quellenbeleg: Dateiformat statt geratenem Baum

Am 20.11.2026 wurde im oeffentlichen Quellcode `paviad/elvenar-helper-extension` eine **nicht-personenbezogene Original-Konfigurationsquelle** identifiziert:
`xml.balancing.research.ResearchTechnologiesElves_<hash>.json` bzw.
`ResearchTechnologiesHumans_<hash>.json`. Das erklaert den Befund, warum in den beiden APK-Schnellscans zwar TechTree-UI- und ConfigVO-Klassen, aber nicht die 124 echten Kostenzeilen nachgewiesen wurden. Es ist **noch nicht belegt**, dass die Android-App exakt denselben Dateipfad nutzt.

Das nachgewiesene Original-Schema enthaelt die bisher fehlenden Felder `section`, `maxSP`, `requirements.resources`, `parentIds`, `childrenIds`, `rewards` und `gate.completedProvinces`.

- [Ausfuehrliche Quellenanalyse und datensparsame Beschaffungsanleitung](RESEARCH_BALANCING_ORIGINAL_SOURCE_2026-11-20.md)
- [Maschinenlesbare Schema-/Provenienzreferenz](../data/reference/research_balancing_schema_provenance_2026-11-20.json)
- [Quell-Code fuer das Modell](https://github.com/paviad/elvenar-helper-extension/blob/master/src/model/researchTechnology.ts)
- [Quell-Code fuer den Balancing-Datei-Matcher](https://github.com/paviad/elvenar-helper-extension/blob/master/src/inject/nonSpecificMatchers.ts)

Der direkte [GitHub-Actions-Abrufversuch](https://github.com/geibibro123-linux/Farm-elvenar-/actions/runs/44832391105) der historisch im Matcher belegten Menschen-Datei mit dem 32-stelligen Hash `9fa701953369071f3962fd3ffe897522` erhielt **HTTP 404**. Dies bedeutet: dieser eine Dateistand ist unter der historischen URL nicht mehr abrufbar. Keine aktuellen Elfen- oder Menschenzeilen aus dem Originalnetz gefunden.

**Fuer einen wirklichen Build relevant:** Wenn ein aktueller URL-Hash einmal ermittelt ist und die Datei legal zugaenglich bleibt, kann ein automatisierter Import die 124 fruehen Konfigurationsobjekte aus einem konsistenten Originalstand extrahieren. Fehlende Kinder-/Elternbeziehungen weiterhin als OFFEN behandeln, solange keine Quellzeile sie belegt. **Keine** Inventar-, Konten-, Forschungsfortschritts- oder Sessiondaten mit dem Forschungsreferenzbestand vermischen.

## G. Zwei reale APK-Scans statt Infrastrukturfehler

[GitHub Actions Lab04-Vergleich](https://github.com/geibibro123-linux/Farm-elvenar-/actions/runs/44832009895) jetzt ebenfalls **erfolgreich**: 232.466.424 Bytes Lab04, 6.494 ZIP-Eintraege, 44 TextAssets, 240 technologieaehnliche Tokens, 0 vollstaendige Forschungszeilen. Die Lab09-Reihe hatte 231.770.000 Bytes, 6.492 ZIP-Eintraege, 44 TextAssets, 232 Tokens, ebenfalls 0 komplette Zeilen. Alle genannten Forschungs-VO-Klassen haben in beiden Scans gleiche Fundzahlen. Der Screenshot-/Clientklasse-Nachweis ist vom Origial-Gesamtschema getrennt.

Alle Rohberichte und Versionsgrenzen: [Forschungsbaum-Bericht Kapitel I-V](RESEARCH_CH01_CH05_EVIDENCE_2026-11-20.md).
