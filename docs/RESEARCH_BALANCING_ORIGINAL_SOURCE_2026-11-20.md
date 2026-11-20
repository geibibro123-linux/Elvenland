# Elvenland: Quelle der vollstaendigen Forschungs-Konfiguration identifiziert

**Datum:** 20. November 2026  
**Ergebnis:** Original-Datenformat und Ladepfad **nachgewiesen**; vollstaendige originale Forschungen Kapitel I-V **noch nicht als Datenfile heruntergeladen**.

## 1. Befund und Original-Provenienz

Im oeffentlich lesbaren Erweiterungscode [paviad/elvenar-helper-extension](https://github.com/paviad/elvenar-helper-extension) ist der Original-Ladepfad der Forschungsdaten dokumentiert:

`/frontend//static/{locale}/xml.balancing.research.ResearchTechnologies{Elves|Humans}_{32-stelliger-Hash}.json`

**Belege:**
- [nonSpecificMatchers.ts](https://github.com/paviad/elvenar-helper-extension/blob/master/src/inject/nonSpecificMatchers.ts), Matcher `RESEARCH_TECHNOLOGIES`, Name und URL-Struktur der vom Webspiel angeforderten Datei.
- [researchTechnology.ts](https://github.com/paviad/elvenar-helper-extension/blob/master/src/model/researchTechnology.ts), Originalstruktur `ResearchTechnologyConfigVO` mit IDs, Kapiteln, Kosten und Vorgangern.
- [processResearchTechnologies.ts](https://github.com/paviad/elvenar-helper-extension/blob/master/src/elvenar/processResearchTechnologies.ts), Umformung von JSON `requirements.resources`, `maxSP`, `gate.completedProvinces`, `rewards`.
- [processResearchStatus.ts](https://github.com/paviad/elvenar-helper-extension/blob/master/src/elvenar/processResearchStatus.ts), persoenlicher Fortschritt kommt *separat* aus `ResearchService/startup` und wird nicht als universeller Forschungsbaum behandelt.
- [buildChapterResearchGraph.ts](https://github.com/paviad/elvenar-helper-extension/blob/master/src/elvenar/buildChapterResearchGraph.ts), verbindet Kosten- und Kantenwerte mit dem lokalen Spielerstatus.

**Nicht mit Unity-Szenendaten gleichsetzen.** Dass die originale Android-APK `TechTreeTechnologyView` usw. enthaelt, beweist nur, dass sie den Baum darstellt. Der vollstaendige, durch den Browser genutzte Balancing-Datensatz liegt in einer separaten versionsgebundenen JSON-Quelle.

## 2. So sieht eine valide einzelne Technologie-Konfiguration aus

`ResearchTechnologyConfigVO` kann diese Felder liefern:

| Originalfeld | In Elvenland benoetigt fuer | Interpretation |
|---|---|---|
| `id` | stabiler technischer Knotencode | Originalcode nicht umbenennen |
| `race` | Elfen- oder Menschenvariante | Quellen/Voelker getrennt |
| `section` | Kapitel I bis XXVI | Kapitelzuordnung |
| `name` | Name, Lokalisierung spaeter | Anzeigename |
| `maxSP` | Wissenspunktekosten | Original teilweise als Textzahl |
| `requirements.resources` | Muenzen, Vorraete und einzelne Gueter | research unlock costs |
| `parentIds` und `childrenIds` | gerichtete Kanten | Eltern als primaere Voraussetzungen |
| `rewards` | Gebaeude, Einheit, Erweiterung, Feature | Historische Wirkung |
| `gate.completedProvinces` | Weltkarten-Kapitel-Gate | Nicht mit Elternkanten verwechseln |
| `gate.rewards.resources` | Gate-Belohnung | Einnahmen, keine Kosten |
| `category` | Forschungstyp | getrennte Anzeige-/Wirkungsart |
| `featureFlag` | versions-/freigabegesteuerter Knoten | nicht als immer aktiv ausgeben |

Es kann auch einen Root-Knoten ohne `maxSP` geben. Dieser ist ein **technischer Anker**, keine frei zu erforschende kostenlose Technologie. Fehlende `requirements` bedeuten nicht automatisch Gratisaktivierung, ausser die Originalquelle oder eine ausdrueckliche Elvenland-Entscheidung bestaetigt dies.

Die genaue Struktur wurde in [maschinenlesbarer Schema-Referenz](../data/reference/research_balancing_schema_provenance_2026-11-20.json) festgehalten.

## 3. Der erste echte Linktest

Die Quell-Erweiterung nennt als Beispiel:

`https://oxen.innogamescdn.com/frontend//static/en_DK/xml.balancing.research.ResearchTechnologiesHumans_9fa701953369071f3962fd3ffe897522.json`

[GitHub-Actions-Test 44832391105](https://github.com/geibibro123-linux/Farm-elvenar-/actions/runs/44832391105) wurde erfolgreich durchgefuehrt. Die Datei selbst antwortet mit **HTTP 404** (Beispielhash nicht mehr aktuell/verfuegbar), deshalb wurden **0 Datensaetze** heruntergeladen.

[Maschinenlesbarer Probebericht](https://github.com/geibibro123-linux/Farm-elvenar-/blob/main/docs/research_apk_scans/public_balancing_source_probe_2026-11-20.json).

Der 404 belegt ausschliesslich, dass **dieses alte Hash-Objekt** nicht mehr an dieser Adresse liegt. Er belegt **nicht**, dass es keinen aktuellen Original-Balancing-Datensatz gibt.

## 4. Aktuelle Quelle spaeter beschaffen, ohne Spielstand oder Geheimnisse

Wenn Zugriff auf das normale Browser-Spiel besteht, kann eine einmalige, *lesende* Untersuchung der bereits vom Spiel angeforderten oeffentlichen Forschungs-Datei genuegen:

1. Elvenar ganz normal im Browser spielen/oeffnen; keine Kontodaten weitergeben.
2. Am Computer im Browser die Entwicklertools oeffnen, Register **Network/Netzwerk**.
3. Die Seite normal laden, im Filter `ResearchTechnologies` eingeben.
4. Eine Datei nach dem Muster `ResearchTechnologiesElves_<hash>.json` oder `ResearchTechnologiesHumans_<hash>.json` ermitteln.
5. **Nur den oeffentlichen `innogamescdn.com`-Dateilink** oder die Datei selbst bereitstellen; keine Cookies, Authorization-Header, Session-Tokens, Kontodaten oder den persoenlichen `ResearchService/startup`-Response kopieren.
6. Fuer beide Voelker getrennt und Quellenversion/URL samt SHA-256 archivieren. Falls ein URL nur mit Autorisierung erreichbar waere, nicht unautorisierte Umgehungen nutzen.

Der Datenbestand kann danach gefiltert werden: `section in {1,2,3,4,5}`; IDs, `maxSP`, `requirements.resources`, `parentIds`, `rewards` und `gate` ohne stille Werteveraenderungen archivieren. Danach erkannte Bild- und Community-Konflikte dokumentieren und **FEST**-Kostenminimum je Volk/Art im getrennten Elvenland-Auswahlstand anwenden.

**Hinweis:** Eine Web-Browser-Recherche setzt nicht voraus, dass der Nutzer jetzt einen PC hat. Diese Anleitung ist eine Option fuer den spaeteren Fall; kein aktueller Nutzertest ist noetig.

## 5. Was trotz neuer Quelle weiterhin OFFEN ist

- Ein aktueller und frei zugaenglicher Dateihash der originalen Balancing-Datei fuer Elfen und Menschen.
- Die echten 124 Einzelkonfigurationen der Kapitel I-V sowie die korrekten technischen IDs, Elternbeziehungen und Kosten.
- Ob die originalen Android-Test-APKs dieselbe Balancing-Datei direkt herunterladen oder sie ueber einen anderen Service erhalten.
- Die korrekte Quellenversion fuer die eigenstaendige Offline-Elvenland-APK.
- Lokale Alternativen fuer rein onlinebezogene Features: **Konzept ausarbeiten, APK-Aktivierung bleibt OFFEN**, keine stillen Ausnahmen.
- Lizenz-/Nutzungsfreigabe fuer eine etwaige externe Verbreitung kompletter proprietaerer Originaldaten.

## 6. Warum der vorherige APK-Scan trotzdem nuetzlich war

Zwei voneinander unabhaengige GitHub-Action-Laeufe konnten die APKs tatsaechlich lesen und per SHA-256 pruefen. Die Resultate sind in [RESEARCH_CH01_CH05_EVIDENCE_2026-11-20.md](RESEARCH_CH01_CH05_EVIDENCE_2026-11-20.md) dokumentiert. Der dort sichtbare VO- und Klassenstand ist mit dem hier gefundenen Original-Balancing-Schema konsistent. **Es sind weiterhin keine vollstaendigen 124 Forschungsknoten direkt aus der APK dekodiert.**

**Naechstes fachliches Gate:** Erster vollstaendiger Original-Balancing-Datensatz fuer ein Volk. Dann Quellenvalidierung, Kapitel-I-V-Extraktion, Konfliktminimum und erst nach gesonderter Freigabe aktiver Godot-Import.
