# Elvenland: Beweissichere Screenshots des Forschungsbaums

**Stand:** 21.11.2026. **Zweck:** Kapitel I-V mit Originalansichten rekonstruieren, ohne Spielwerte zu erfinden.

## Prioritaet 1: Kapitel I, komplette Baumansicht

1. In Elvenar den **Forschungsbaum**, Kapitel I, oeffnen.
2. **Volk (Elfen/Menschen)** und ungefaehre Spielversion/Datum notieren. Bitte keine Konto-, Kontakt-, Sitzungs- oder Zugangsdaten mitsenden.
3. Ganz nach links scrollen und Screenshot aufnehmen. Danach **horizontal** stueckweise verschieben und weitere Screenshots machen.
4. Die benachbarten Screenshots sollen **mindestens ein bis zwei Forschungsknoten ueberlappen**, damit die Verbindungen und die Reihenfolge zweifelsfrei zusammengesetzt werden koennen.
5. Bis zum **ersten Knoten von Kapitel II** fortsetzen. Danach Kapitel II bis V auf die gleiche Weise.

Bitte Namen, Fortschrittsanzeigen wie 0/8, die Kapitelueberschrift und die gezeichneten Verbindungslinien nicht abschneiden. Originalaufloesung beibehalten. Abbildungen nicht zusaetzlich verkleinern oder zu einer einzigen unscharfen Gesamtgrafik zusammenkleben.

**Empfohlene Namen:** `Elvenland_K01_Elfen_Baum_01.png`, `..._02.png`; bei Menschen `Elvenland_K01_Menschen_Baum_01.png`.

## Prioritaet 2: Einzelkosten und Aktivierung

Einzelne **noch nicht aktivierte** Technologien anklicken und deren Informationsfenster fotografieren, wenn dort **Wissenspunkte, Aktivierungskosten und Freischaltwirkung** stehen.

Fuer jeden Knoten getrennt erfassen:
- Name, Kapitel, Volk, sichtbare WP, Forschungsfortschritt.
- Aktivierungskosten: Muenzen, Vorraete, Gut-ID bzw. deutsches Gut und Menge.
- Sichtbare Forschungsvorgaenger/Kanten, gegebenenfalls angeklickte Verbindung.
- Wirkungen (Gebaeudestufe, Einheit, Ausbau, Kultur, Zauber, Funktion).
- Falls Weltkarten-Provinzbedingung erkennbar: Text `x/y` und Kontext.

**Empfohlener Dateiname:** `Elvenland_K01_Elfen_Marmormanufaktur_Aktivierung.png`.

Ist eine Technologie bereits abgeschlossen und zeigt das Spiel den damaligen Preis nicht mehr, bleiben deren historischen Aktivierungskosten **OFFEN**. Bitte nicht zurueckrechnen oder einen spaeteren Baupreis als Forschungskosten eintragen.

## Prioritaet 3: Kapitel V -> VI

Den **letzten Bereich von Kapitel V** und den **ersten Bereich von Kapitel VI** mit Ueberlappung aufnehmen. Besondere Aufmerksamkeit gilt der noch nicht aufgeloesten historischen Elternreferenz `elves_all3_aw`. Aus einer sichtbaren Linie allein wird keine technische ID abgeleitet.

## Datenschutz und Belegstatus

Persoenliche Profilinformationen, Chatfenster, Nachrichten, Spielernamen und Kontodaten nach Moeglichkeit ausblenden oder vor der Uebergabe zuschneiden. Keine Cookies, Token, Spielstandantworten oder Login-Daten weitergeben.

Historische Screenshots (z.B. YouTube oder 2022) und aktuelle Spielbilder duerfen als **verschiedene Quellversionen** verglichen werden. Nie die Elternkanten unterschiedlicher Generationen still mischen. Unlesbare Werte sind **OFFEN**. Nach bestaetigter Gegenpruefung werden Daten ausschliesslich in `data/reference/` dokumentiert. Die spielwirksame Datei `data/definitions/research_nodes.json` bleibt unveraendert, bis konkrete Daten und Integration gesondert freigegeben sind.

## Bereits verifizierte Bearbeitungsgrundlagen

- Video: https://www.youtube.com/watch?v=tF7h1gaTfes, oEmbed-Titel `Elvenar All research`. Direkter Videoabruf am 21.11.2026 durch Bot-Schutz blockiert, daher keine daraus abgelesenen Einzeltechnologien.
- Nutzerregel **FEST**: innerhalb vergleichbarer Forschungskosten desselben Volks, derselben Ressource und Technik den kleinsten belegten Wert waehlen, Historienversionen erhalten.
- Reproduzierbarer Originaldaten-Importer: `tools/extract_research_balancing_reference.py`; **nur Referenzdateien**, keine Aktivierung.
