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

## 9. Auswahlregel FEST: niedrigster vergleichbarer Quellenwert (Nutzerentscheidung 20.11.2026)

Der Nutzer hat verbindlich entschieden, bei mehreren dokumentierten Forschungswerten den **kleinsten Wert** als Elvenland-Auswahlwert zu verwenden, auch wenn die Belege aus unterschiedlichen Originalspiel-Versionen stammen. Die Regel gilt nur bei *vergleichbaren* Kosten: identische Forschung, identisches Volk, identische Waehrung/Ressource und derselbe Zahlvorgang. Es ist **kein** Beleg dafuer, dass dieser niedrigste Wert im gesamten historischen Originalzeitraum gueltig war.

| Forschung / Vergleich | Belege | Elvenland-Auswahl |
|---|---|---|
| Haendler, Elfen, Forschung-WP | 12 WP: [Elvenarchy](https://elvenarchy.fuzzalab.pt/en/guides/primeiros-capitulos-estrategia); 19 WP: ungesicherter frueherer Bildbericht | **12 WP** |
| Handwerk, Kapitel III | Elfen 28 WP, Menschen 21 WP: unterschiedliche Voelker | **28 WP Elfen**, **21 WP Menschen** |
| Turniere, Kapitel IV | Elfen 32 WP, Menschen 35 WP: unterschiedliche Voelker | **32 WP Elfen**, **35 WP Menschen** |
| Turm der Ewigkeit, Kapitel V | Elfen 50 WP, Menschen 45 WP: unterschiedliche Voelker | **50 WP Elfen**, **45 WP Menschen** |

Der ausgewaehlte Wert ist zunaechst **ARBEITSWERT** fuer die Spielentwicklung. Die Auswahlregel selbst ist **FEST**. Die oeffentlichen/community Quellen und alle abweichenden historischen Werte werden erhalten. Unbekannte `requirements` und `parentIds` bleiben OFFEN; sie werden niemals als Nullpreis bzw. leere Elternliste gedeutet. Die neun belegten Einzel-WP-Werte sind in der Referenz-JSON einzeln als Arbeitsauswahl gespiegelt.

## 10. Direkt verifizierter Screenshot: Marmormanufaktur

Bildbeleg: [Original-Spielansicht auf Malavida](https://imag.malavida.com/mvimgbig/download-fs/elvenar-28484-12.jpg), [Quellseite](https://elvenar.fr.malavida.com/android/).

- Technologie: `Marble Manufactory` (Marmormanufaktur), fruehes Kapitel I.
- Forschung: **8 Wissenspunkte** (Anzeige `0/8`).
- **Forschungs-Aktivierungskosten: 2.500 Muenzen**.
- Die sichtbare Sofortfreischaltung mit 360 Diamanten ist eine separate Premiumoption, **nicht** die regulaere Forschungskosten-Summe.
- Volk und exakter Screenshot-Build sind im Bild nicht sicher identifiziert. Deshalb ist der technische Anschluss an eine Elf-/Mensch-ID weiterhin OFFEN.
- Zum Vergleich nennt [Elvenar Tools](https://elvenar-tools.com/buildings/manufactories) fuer den Neubau einer **Marmormanufaktur Stufe 1** 200 Muenzen, 10 Vorraete und 40 Sekunden Bauzeit. **Diese Bauwerte duerfen nicht mit den 2.500 Muenzen fuer die Technologiefreischaltung verwechselt werden.**

Zusaetzlicher [Screenshot von BlueStacks](https://cdn-www.bluestacks.com/bs-images/Tips-and-tricksElvenar-5.png) zeigt vier fruehe Forschungen mit je `0/8` Wissenspunkten. Die Knotennamen sind dort nicht ablesbar. Daher wird daraus **keine** Zuweisung zu bestimmten IDs erstellt.

## 11. Original-APK: vorhanden, erneute Binaerpruefung unterbrochen

Die Datei `Elvenar_Lab04_SkriptTest03.apk` wurde am 20.11.2026 in der verbundenen Dateibibliothek mit **232.466.424 Bytes** gefunden und zur lokalen Analyse materialisiert. Die in einem frueheren GitHub-Release gemeldete SHA-256 lautet `d77de38720bde3c0894493b519cdcca6183d7d020d3377d40e2096516d6d247c`. **Eine erneute SHA-256-Berechnung auf den jetzt gefundenen Bibliotheksbytes ist nicht gelungen.**

Alle lokalen Shell- und Python-Versuche brachen mit `ClientError` ab. Deshalb wurden **keine neuen Original-Technologiezeilen direkt aus der APK gewonnen** und keine Negativaussage ueber den Inhalt getroffen.

Bestehende belegte Ergebnisse frueherer APK-/Archivuntersuchungen:
- 13 Feature-Technologie-Zuordnungen zu 11 eindeutigen technischen IDs in `data/reference/historical_feature_technology_links.json`.
- `ResearchTechnologyConfigVO` verlangt `id`, `maxSP`, `parentIds`, `requirements`, der historische Offline-Planer liefert aber keine vollstaendigen Konfigurationszeilen.
- `TechTreeTechnologyView`, `TechTreeTechnologyMediator`, `TechTreeTechnologyConnectionsView` und `ResearchWindowMediator` belegen Client-UI-Komponenten, **keinen** vollstaendigen Kosten-/Kantensatz.
- Die bisherige [MonoBehaviour-Pruefung](MONOBEHAVIOUR_SCOPE.md) erfasste 45.620 Objekt-Header, konnte aber zahlreiche nutzdatentragende TypeTrees nicht vollstaendig dekodieren.
- [Offizielle Versionshinweise 1.244](https://support.innogames.com/kb/Elvenar/en_DK/7006/Release-Notes-1244) datieren den Originalclient auf Oktober 2020. Spaetere Kapitel-22-Featurelinks in einem historischen Referenz-Archiv duerfen **nicht** ungeprueft als eingebettete Daten dieser APK-Version ausgegeben werden.

**Fortsetzung der Binaerpruefung:** Erneut SHA-256 und ZIP-Inventar der materialisierten APK ausfuehren; enthaltene Unity-Assets und IL2CPP-Metadaten nach Forschungsdefinitionen/Typen durchsuchen; echte Konfigurationszeilen, falls vorhanden, mit Provenienz gesondert exportieren. Fehlt eine clientseitige Konfiguration, offen als moeglichen serverseitigen Inhalt behandeln.

## 12. Verifizierte externe Spielregeln fuer die Offline-Abbildung

- [InnoGames](https://support.innogames.com/kb/Elvenar/de_DE/218): 1 WP je Stunde, Speicher regulär 10, temporaer 20; weitere WP ueber alternative Quellen.
- [InnoGames](https://support.innogames.com/kb/Elvenar/en_DK/297): ein zugewiesenes Produktionsbonus-Gut je Gueterklasse. Forschungsbonus gilt erst nach Freischaltung der jeweiligen Technologie.
- [Elvenarchy](https://elvenarchy.fuzzalab.pt/en/guides/menus-das-manufaturas): Urspruengliche Gueterproduktion bietet 3 h, 9 h, 1 Tag und 2 Tage. **Das sind Produktionsdauern, keine Forschungslaufzeiten.**
- Ein Forschungsbaum ohne bewiesene Ressourcenanforderungen darf keine unbeabsichtigte Gratisaktivierung zulassen.

**Roadmap:** Zuerst die verbliebenen Kapitel-I-Knoten und deren freigegebene Zahlen, dann Kapitel II-V, dann den Anschluss `elves_all3_aw` zu `elves_scouting_6` aufbauen; die aktualisierte Original-APK nach Wiederherstellung der Ausfuehrungsumgebung gesondert pruefen.

## 13. Erfolgreicher APK-Ausweichscan ueber GitHub Actions, 20.11.2026

**Warum fruehere Versuche scheiterten:** Die lokale Ausfuehrungsumgebung gab `ClientError` selbst auf einfache Shellbefehle wie `pwd` zurueck. Dieser Test beweist eine Ausfuehrungs-/Infrastrukturstoerung; er beweist weder eine kaputte APK noch eine bestimmte Ursache des Fehlerdienstes. Wiederholte identische Containeraufrufe allein konnten das nicht beheben.

**Erfolgreiche Alternative:** GitHub Actions im privaten Repository `geibibro123-linux/Farm-elvenar-`. Beleg: [erfolgreicher Lauf 44831049326](https://github.com/geibibro123-linux/Farm-elvenar-/actions/runs/44831049326). Pinning: `Elvenar_Lab09_RequestRoute02.apk`, SHA-256 `d9e36fa4beef2c6c5e3b196caa3eca9cc128af03a8d4add1290f4c6034fe0bf1`. APK-Groesse 231.770.000 Bytes. **Nicht** identisch mit der urspruenglich materialisierten Lab04-Datei oder mit der zuvor verlinkten Lab09 RequestRoute01 auf Google Drive.

- 6.492 ZIP-Eintraege; 451.253.390 Bytes unkomprimierter Inhalt.
- 4.830 Unity-Daten-Dateien; UnityPy hat erfolgreich **44 TextAssets** geprueft, jedoch **0 TextAsset-Namen mit Forschung/Technologie-Bezug** gefunden.
- Der einfache Stringscan fand 232 unterschiedliche **technologieaehnliche Textkennungen**, darunter viele UI-/Lokalisierungs-/Weltnamen und einige historische `elves_...`-Featurebezeichnungen. **Nicht mit 232 echten Forschungen verwechseln.**
- Technische Strings: `ResearchTechnologyConfigVO` 6 Treffer, `ResearchTechnologyProgressVO` 6, `TechTreeTechnology` 115, `parentIds` 1, `requirements` 45, `technologySection` 6. Fundorte liegen vorwiegend in IL2CPP-Metadaten, UI-Assets und im historischen beigefuegten Referenz-JSON.
- `elves_all3_aw` und `elves_scouting_6` wurden als rohe Klartextkennungen **nicht** gefunden. Dies ist kein Beweis fuer die Abwesenheit aus versteckten / serverseitigen / kodierten Daten.
- **Vollstaendige Konfigurationszeilen aus APK: 0.** Der Scan ist bewusst eine Bestandsaufnahme der Datenorte und nicht der Nachweis einer vollstaendigen Forschungsdatenbank.

Dauerhaft lesbare Rohberichte in privatem GitHub:
[JSON-SCAN](https://github.com/geibibro123-linux/Farm-elvenar-/blob/main/docs/research_apk_scans/lab09_route02_structural_scan_2026-11-20.json),
[MARKDOWN-SCAN](https://github.com/geibibro123-linux/Farm-elvenar-/blob/main/docs/research_apk_scans/lab09_route02_structural_scan_2026-11-20.md).

**Folgerung:** Ein weitergehender Versuch muss gezielt die originalen ConfigVO-Datenquellen (ggf. Serverantwort statt APK-Assets), IL2CPP-Binaer-Layouts und Graphformate identifizieren. Ein UI-Klassenname reicht nicht aus. Keine fehlenden Aktivierungspreise erfinden.

## 14. Zusaetzliche historische Kapitel-I-Knoten mit Bildquelle

Neu gespeichert:
[`data/reference/community_ch01_historical_spieletrend_screenshot_2026-11-20.json`](../data/reference/community_ch01_historical_spieletrend_screenshot_2026-11-20.json)

Primaerbeleg: [Spieletrend, historischer Forschungsbaum](https://spieletrend.com/medien/elvenar-wissen-forschung.jpg), [urspruengliche Artikelseite](https://spieletrend.com/spiele/elvenar/).

Einzelne eindeutig erkennbare sichtbare Forschungsanforderungen:
`Leuchtender Wegweiser 5 WP`; `Kaserne 8 WP`; `Marmormanufaktur 8 WP`; `Stahlmanufaktur 8 WP`; `Holzmanufaktur 8 WP`; `Stadterweiterung I 10 WP`; `Erweiterung der Truppgroesse I 11 WP`; `Bogenschuetzen 15 WP`; `Marmor-Produktionsbonus 14 WP`; `Haendler 19 WP`. `Ruestkammer 13 WP` ist zusaetzlich notiert, **mit mittlerer Lesesicherheit**.

Das Bild liefert fuer einige Knoten sichtbare Verbindungslinien. Diese wurden **nur** als visuelle historische Hinweise abgelegt, nicht als technische `parentIds`.

**Wichtiges Versionsrisiko:** In [einer Elvenar-Redditdiskussion vom 18.07.2023](https://www.reddit.com/r/Elvenar/comments/152i8a1) berichten mehrere Spieler, dass die Forschungen der Kapitel I bis V zuvor umgestaltet und alte Konten Mitte Juli 2023 auf die neue Struktur migriert wurden. Dies ist ein **Communitybericht**, keine direkt bestaetigte InnoGames-Migrationsliste. Er erklaert moegliche Unterschiede wie `Haendler 19 WP` im alten Bild versus `12 WP` im modernen Elvenarchy-Guide, beweist aber nicht allein die Ursache dieses konkreten Unterschieds.

**FEST bleibt:** Bei vergleichbaren Kosten den kleinsten belegten Zahlenwert auswaehlen; die abweichenden historischen Werte und Quellen erhalten. **NICHT FEST:** Kombination unterschiedlicher Topologien, denn diese darf spaeter zu unspielbaren oder unhistorischen Voraussetzungen fuehren.

## 15. Vorbereiten fuer Build-Integration

Bestaetigte Quellenwerte und ihr Provenienzstatus bleiben in `data/reference/`; die aktive Laufzeitdatei `data/definitions/research_nodes.json` bleibt unveraendert ohne freie Original-Erfindungen.

Die Datenpipeline muss kuenftig diese Felder getrennt erhalten: `source_version`, `race`, `tech_id` (nullable), `name`, `knowledge_points` (nullable), `activation_requirements` (nullable), `parentIds` (nullable), `unlock_effect` (nullable), `source_url`, `source_confidence`, `user_selected_cost`, `import_ready`.

Ein Knoten darf nur dann als originalgetreu freischaltbar in den Laufzeitbaum importiert werden, wenn seine benoetigten Kosten und Kanten bekannt oder als separate, vom Nutzer freigegebene Elvenland-Alternative vorhanden sind. Onlinefunktionen bleiben fuer die aktuelle APK **OFFEN**, siehe [separates Offline-Konzept](ONLINEFUNKTIONEN_OFFLINE_KONZEPT_OFFEN_2026-11-20.md).

## 16. Direktvergleich von zwei APK-Testversionen, 20.11.2026

Zweiter GitHub-Actions-Lauf [44832009895](https://github.com/geibibro123-linux/Farm-elvenar-/actions/runs/44832009895) **erfolgreich**. Nun wurden zwei APK-Dateien durch denselben reproduzierbaren, read-only Scanner untersucht und vorab per SHA-256 gegen den jeweiligen Release-Beleg geprueft.

| Messwert | Lab04 SkriptTest03-1 | Lab09 RequestRoute02 |
|---|---:|---:|
| APK-Dateigroesse in Bytes | 232.466.424 | 231.770.000 |
| ZIP-Eintraege | 6.494 | 6.492 |
| Unity-Daten-Dateien geprueft | 4.830 | 4.830 |
| Gelesene Unity-TextAssets | 44 | 44 |
| TextAssets mit Forschung/Technologie im Namen | 0 | 0 |
| unterschiedliche technologieaehnliche Text-Tokens | 240 | 232 |
| Vorkommen `ResearchTechnologyConfigVO` | 6 | 6 |
| Vorkommen `ResearchTechnologyProgressVO` | 6 | 6 |
| Vorkommen `TechTreeTechnology` | 115 | 115 |
| Vorkommen `parentIds` | 1 | 1 |
| Vorkommen `requirements` | 45 | 45 |
| Vollstaendige Technologie-Konfigurationszeilen dekodiert | **0** | **0** |

Hashes:
- Lab04: `d77de38720bde3c0894493b519cdcca6183d7d020d3377d40e2096516d6d247c`
- Lab09: `d9e36fa4beef2c6c5e3b196caa3eca9cc128af03a8d4add1290f4c6034fe0bf1`

Berichte:
- [Lab04 JSON](https://github.com/geibibro123-linux/Farm-elvenar-/blob/main/docs/research_apk_scans/lab04_baseline_structural_scan_2026-11-20.json)
- [Lab09 JSON](https://github.com/geibibro123-linux/Farm-elvenar-/blob/main/docs/research_apk_scans/lab09_route02_structural_scan_2026-11-20.json)

**Interpretation:** Die textuell identifizierten TechTree-/ResearchVO-Klassen und der TextAsset-Umfang sind gleich. Die acht Differenz-Tokens **beweisen keine acht geaenderten Forschungsknoten**, weil der Scanner zahlreiche UI-, Text- und Provinzkennungen mitzaehlt. Die Aussagen des Nutzers, dass modifizierter Client und Original denselben Forschungsbaum zeigen, passen hierzu, sind durch den Klasse-/Tokenvergleich aber **noch nicht als Voll-Datenidentitaet nachgewiesen**. Die modifizierten APKs wurden nicht mit einer unveraenderten Original-APK im Binärvergleich abgeglichen.

**Naechste sinnvolle APK-Quelle:** fuer reale `id/maxSP/requirements/parentIds` zuerst pruefen, ob die Forschungskonfiguration im Server-Response `StartupService.getData` bzw. in weiteren durch den Originalclient empfangenen Definitionen vorkommt. Vorher ein sauberes Response-Schema gewinnen und personenbezogene Felder entfernen. Klassennamen und UI-Assets allein reichen nicht, um Kostenzeilen zu rekonstruieren. Kein live-Spielserverzugriff wird durch diesen Vergleich behauptet.
