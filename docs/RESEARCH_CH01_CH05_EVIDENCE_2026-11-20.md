# Elvenland | Forschungsbaum Kapitel I-V | Quellen- und Rekonstruktionsstand

**Stand:** 20. November 2026  
**Status:** HISTORISCHE REFERENZ; **NICHT** als FEST-Balance uebernommen.  
**Ziel:** Den fruehen Original-Forschungsbaum fuer Elfen und Menschen nachvollziehbar erfassen. Keine erfundenen Kosten, Kanten, Zeiten, IDs oder Freischaltungen.

## 1. Verwendbarer Datenbestand

- `data/reference/community_early_research_ch01_ch05_2026-11-20.json`: 5 Kapitelgesamtwerte, neun einzeln bezifferte Forschungsbeispiele, ihre Mindestpfade, Zusatzbeobachtungen aus Kapitelguides und dokumentierte Luecken.
- `data/reference/historical_feature_technology_links.json`: 13 historische Feature-zu-Technologie-Beziehungen, 11 eindeutige Technologie-IDs aus einem historischen eingebetteten Referenzstand, teilweise in fruehen Kapiteln.
- `data/reference/research_tree_status.json`: Herkunft und technische Feldnamen aus dem Altprojekt; die dortigen Aussagen ueber einen fehlenden vollstaendigen Baum gelten **nur fuer den alten eingebetteten Referenzstand**.
- `data/reference/community_idavis_research_ch06_ch26_2026-11-20.json`: 767 strukturierte Elfen-Technologien ab Kapitel VI, mit ID, KP, Ressourcen und `parentIds`. Sie sind **nicht** Teil der 124 fruehen Eintraege.
- `data/definitions/research_nodes.json`: weiterhin bewusst **OFFEN und ohne aktivierte Originaldefinitionen**. Historische Quellen werden nicht automatisch als spielbereite Regeln eingesetzt.

## 2. Kapitelumfang

| Kapitel | Elfen-Forschungen laut Quelle | WP-Summe | Stand Einzeldefinitionen |
|:--|--:|--:|:--|
| I: Die Ankunft | 21 | 155 | Einzelne WP und Themen; Gesamtgraph OFFEN |
| II: Entwicklung | 25 | 275 | Einzelne WP und Themen; Gesamtgraph OFFEN |
| III: Aufsteigende Magie | 27 | 578 | Einzelne WP und Themen; Gesamtgraph OFFEN |
| IV: Weisheit und Wunder | 25 | 747 | Einzelne WP und Themen; Gesamtgraph OFFEN |
| V: Weg in die Vergangenheit | 26 | 1.030 | Einzelne WP und Themen; Gesamtgraph OFFEN |
| **Gesamt** | **124** | **2.785** | **Keine 124 vollstaendigen Originalkonfigurationen** |

Quelle fuer Anzahl und Elfen-WP-Summen: [Elvenarchy, die ersten fuenf Kapitel](https://elvenarchy.fuzzalab.pt/en/guides/primeiros-capitulos-estrategia), aktualisiert 23.10.2026. Die dortigen Mindestpfade sind *kumulative Abhaengigkeitspfade* und nicht die vollen Kosten des jeweiligen Kapitels.

## 3. Bezifferte einzelne Forschungsbeispiele

| Kap. | Forschung | Eigene WP (Elfen) | Menschen WP | Mindestpfad ab Beginn: Forschungen / WP | Historische Feature-ID |
|:--:|:--|--:|--:|:--|:--|
| I | Nachbarschaftshilfe | 5 | OFFEN | 13 / 70 | `elves_neighbourlyhelp` |
| I | Haendler | 12 | OFFEN | 8 / 39 | OFFEN |
| I | Magische Akademie | 12 | OFFEN | 16 / 107 | OFFEN |
| II | Gemeinschaften | 6 | OFFEN | 21 / 155 | `elves_fellowships` |
| II | Gemeinschaftsabenteuer | 8 | OFFEN | 28 / 227 | `elves_fellowship_adventures` |
| III | Handwerk | 28 | 21 | 48 / 493 | `elves_crafting` |
| IV | Turniere | 32 | 35 | 73 / 1.119 | `elves_tournaments` |
| V | Turm der Ewigkeit | 50 | 45 | 90 / 1.684 | `elves_spire` |
| V | Hexenkessel | 30 | OFFEN | 96 / 1.914 | `elves_cauldron` |

**Begrenzung:** Fuer diese neun Beispiele liegen die Ressourcenpreise und vollstaendigen `parentIds` noch nicht als konsistente Originalzeilen vor. `OFFEN` ist niemals 0 oder kostenlos. Quellen: Elvenarchy und archivierte Featurezuordnungen.

## 4. Weiter rekonstruierte Kapitelstruktur

Die folgenden Bausteine sind **Quellenhinweise auf Forschungsinhalte oder Wirkungen**, keine komplette Liste eindeutiger Technologiezeilen. Reihenfolgen aus Spieler-Guides duerfen nicht als programmierte `parentIds` interpretiert werden.

### Kapitel I: Die Ankunft

- Fruehe Guide-Reihenfolge: Hauptgebaeude, Werkstatt, Leuchtender Wegweiser (Kultur).
- Danach: Marmor-, Stahl- und Holz-/Brettermanufaktur sowie produktionsbezogener Bonus.
- Haendler; Nachbarschaftshilfe; Magische Akademie; verbesserte Kundschafter als Kapiteluebergang.
- Bonusgut der ersten Stufe wird stadtabhaengig zugewiesen; kein universeller fixer Warenbonus.
- Gebaeudebezogene, **nicht als Forschungskosten zu lesende** Masse aus dem Forum: Haendler Elfen 3x4, Menschen 4x4; Magische Akademie Elfen 5x5, Menschen 5x4.

### Kapitel II: Entwicklung

- Kristall-, Schriftrollen- und Seidenmanufakturen, Trainingsgelaende und Gebaeudeausbauten.
- Gemeinschaften 6 WP, Gemeinschaftsabenteuer 8 WP laut Elvenarchy.
- Onlinegebundene Gemeinschaftssysteme bei Offline-Rekonstruktion als historisches Freischaltthema dokumentieren, nicht ohne Entscheidung online implementieren.

### Kapitel III: Aufsteigende Magie

- Elixier-, Magiestaub- und Edelsteinmanufakturen; Bonus fuer das stadtindividuell festgelegte wertvolle Gut.
- Handwerk: laut Guide eigener Zugriff in der Magischen Akademie.
- Magische Inspiration: laut deutschsprachigem Kapitelguide **zwei zusaetzliche Verzauberungen** in der Akademie.
- Weitere Stadt- und Truppenentwicklungen (z. B. Golems / Zauberinnen) als Themen belegt; technische IDs und exakte Kosten hier noch OFFEN.

### Kapitel IV: Weisheit und Wunder

- Verbesserte Kundschafter, fortgeschrittene Manufakturen, Turniere und Antike Wunder.
- Geheime Antike Wunder: Waelzer der Geheimnisse, Goldener Abgrund.
- Antike Wunder des Sturms: Endlose Ausgrabung, Nadeln des Sturms.
- Volksspezifische Wunder: Kloster der Kampfkünste und Kristall-Leuchtturm (Elfen); Das Heiligtum und Der grosse Glockenturm (Menschen).
- **Achtung:** Namen mehrerer Wunder bedeuten nicht zwingend ebenso viele einzelne Technologien. Fuer IDs und `parentIds` noch Bild-/Konfigurationsabgleich noetig.

### Kapitel V: Weg in die Vergangenheit

- Verbesserte Kundschafter, Turm der Ewigkeit und Hexenkessel.
- Vergessene Antike Wunder: Ruinen des Wachstums; Throne der Hohen Wesen (Guide-Bezeichnungen).
- Die Folge zu Kapitel VI ist im iDavis-Datensatz noch nur ueber den **externen Elternverweis `elves_all3_aw`** belegt. Seine vollstaendige Konfiguration aus Kapitel V fehlt.
- Der originale Turm ist ein Community-/Online-Feature; ob und wie er lokal ersetzt wird, ist eine getrennte Elvenland-Entscheidung.

## 5. Spielmechanik: belegte Regeln und Grenzen

1. **Wissenspunkte (WP):** Offiziell 1 WP je Stunde, regulaere Speichergrenze 10, temporaer erweiterbar auf 20. Historischer APK-Auszug: `producingTime: 3600`, `currentSP: 10`, `maxSP: 10`. Dies ist eine **Erzeugungsrate**, keine feste technologiebezogene Forschungsdauer.
2. **Zweistufige Freischaltung:** Erst WP investieren, anschliessend Ressourcen fuer die Aktivierung bezahlen. Fehlende Zahlungsanforderungen duerfen nicht als Gratisfreischaltung gelesen werden.
3. **Vorgaenger:** Technologieknoten werden durch abgeschlossene Vorganger freigeschaltet. Fuer Kapitel I-V fehlen die exakten Kanten.
4. **Kapitelgrenze:** Nach Community-Beschreibung wird die erste Technologie eines Folgekapitels zudem durch die Zahl abgeschlossener Provinzen begrenzt. Konkrete Kapitel-I-V-Schwellen bleiben OFFEN.
5. **Stadterweiterung:** Forschung der Erweiterung und **gesonderte Platzierungsgebuehr in Muenzen** sind unterschiedliche Transaktionen. Keine Doppelbelastung oder kostenlose Platzierung annehmen.
6. **Volk:** Elfen und Menschen koennen sich in Kosten, Technik-Anordnung und Gebaeudeformen unterscheiden; keine blinde 1:1-Uebertragung.
7. **Statuslogik:** Vorschlag fuer die Implementierung aus *bereits nachgewiesener* Mechanik: Vorgaenger-/Kapitel-Gate, WP-Fortschritt, Ressourcenaktivierung, Effekt anwenden, Persistenz. Dies ist keine Behauptung einer bereits implementierten und getesteten Godot-Forschung.
8. **Quellenstatus:** `HISTORICAL_EMBEDDED_REFERENCE`, `COMMUNITY_PUBLIC_GUIDE` oder `OFFEN` erhalten; spaeter erst mit expliziter Nutzerfreigabe nach `FEST` ueberfuehren.

## 6. Nicht uebernehmen, bevor verifiziert

- In einem frueheren Chat wurden **8 WP / 2.500 Muenzen fuer die Marmormanufaktur** und **19 WP fuer den Haendler** einem historischen Screenshot zugeschrieben. Die Bildquelle wurde bei dieser Recherche **nicht erneut in einer dauerhaft pruefbaren Form** gesichert. Diese Hinweise sind deshalb nur als *unverifizierter Bildbericht* konserviert.
- Die Elvenarchy-Quelle nennt dagegen **12 WP fuer den Haendler**. Moegliche historische Balanceaenderung: Dokumentieren, nicht still ueberschreiben.
- Weder die Guide-Reihenfolge noch Gruppenbeschreibungen belegen alle 124 `parentIds`.
- Recherche ergibt **keine** zusammenhaengenden Ressourcenanforderungen fuer Kapitel I-V; keine Nullpreise erzeugen.
- Die iDavis-Datei zu Kapitel VI-XXVI hat 767 eindeutige Nodes, aber nicht Kapitel I-V. Sie ersetzt diese Luecke nicht.

## 7. Naechste konkrete Datenarbeit

**P1:** Original-Spielbildschirm oder Original-Konfigurationsdatei mit den 21 Zeilen und Kanten von Kapitel I sichern, inklusive Quelle / Versionsstand. Exakte `parentIds`, `maxSP` bzw. WP und `requirements` per Knoten erfassen.

**P2:** Kapitel I gegen die neun bekannten Quelleneinzelwerte und sichtbare historische Screenshots pruefen; Kostenkonflikte als getrennte Quellenstufen archivieren.

**P3:** Kapitel II bis V nacheinander auf denselben Erfassungsgrad bringen. Dabei den Kapitelsprung `elves_all3_aw` zu `elves_scouting_6` nachweisen.

**P4:** Menschenbaum getrennt erfassen und verknuepfte Offline-Ersatzwirkungen fuer reine Onlinesysteme nur nach Designentscheidung anlegen.

**P5:** Erst dann validierte Knoten in `data/definitions/research_nodes.json` uebernehmen; deren Aktivierung und Tests sind noch OFFEN.

## 8. Direkte Quellen

- [Elvenarchy: Kapitel I-V Gesamt- und Einzel-WP](https://elvenarchy.fuzzalab.pt/en/guides/primeiros-capitulos-estrategia)
- [Elvenarchy: Kapitel I](https://elvenarchy.fuzzalab.pt/en/guides/capitulo-1-a-chegada)
- [Elvenarchy: Kapitel II](https://elvenarchy.fuzzalab.pt/en/guides/capitulo-2-a-evolucao)
- [Elvenarchy: Kapitel III](https://elvenarchy.fuzzalab.pt/en/guides/capitulo-3-descoberta-da-magia)
- [Elvenarchy: Kapitel IV](https://elvenarchy.fuzzalab.pt/en/guides/capitulo-4-sabedoria-e-conhecimento)
- [Elvenarchy: Kapitel V](https://elvenarchy.fuzzalab.pt/en/guides/capitulo-5-caminho-para-o-passado)
- [Elvenar-Fan-Forum: Kapitel I, mit Originalbildanlagen](https://www.elvenar-fan-forum.de/t674f64649-Kapitel.html)
- [Elvenar-Fan-Forum: Kapitel III](https://www.elvenar-fan-forum.de/t676f64649-Kapitel.html)
- [Elvenar-Fan-Forum: Kapitel IV](https://www.elvenar-fan-forum.de/t677f64649-Kapitel.html)
- [Elvenar-Fan-Forum: Kapitel V](https://www.elvenar-fan-forum.de/t678f64649-Kapitel.html)
- [Offizielle InnoGames-Hilfe: Wissenspunkte](https://support.innogames.com/kb/Elvenar/de_DE/218)
- [Offizielle InnoGames-Hilfe: Technologie freischalten](https://support.innogames.com/kb/Elvenar/de_DE/219)
- [Offizielle InnoGames-Hilfe: Stadterweiterungen](https://support.innogames.com/kb/Elvenar/en_DK/627)
- [Community: Forschungs-Menue und Kapitelgrenzen](https://www.santastoybox.net/elvenar.htm)

**Hinweis zur Nutzung:** Externe Bilder sind nicht in dieser Datei kopiert, sondern ueber die Quellseiten referenziert. Fuer veroeffentlichte Eigennutzung gelten die jeweiligen Rechte der Medien. Das GitHub-Repository bleibt privat.
