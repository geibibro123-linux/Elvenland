# Elvenland: Prüfung des bisherigen Offline-Kerns

Prüfdatum: 17.11.2026. Quelle: privates Repository `geibibro123-linux/Farm-elvenar-`, gelesener Zweig `main`. Die Blob-Hashes der geprüften Dateien stehen im Paket unter `provenance/previous_core_provenance.json`. Diese Notiz bewertet nur die hier geprüften Repository-Dateien. Über getrennt gespeicherte Originaldaten oder weitere APK-Ressourcen trifft sie keine Vollständigkeitsbehauptung.

## Ergebnis

**Wiederverwendbar sind die Grundsätze für Transaktionen, Zustandsverwaltung und robuste Speicherung. Ein vollständiger Elvenar-Spielkern, ein Forschungsbaum und vollständige Wirtschafts- oder Gebäudetabellen liegen in diesen Dateien nicht vor.** Die frühere native Unity-Integration ist für Elvenland nicht erforderlich, wenn das Spiel wie jetzt ausdrücklich gewünscht neu aufgebaut wird.

Die hier erneut ausgeführten 111 Hosttests bestanden. Sie prüfen JavaScript mit synthetischen Eingaben und simulierten Adaptern. Sie beweisen weder die Originalwerte noch die Funktionsfähigkeit einer Android-App. Auch ein Test mit dem Namen „real 26-field startup reference“ verwendet hier eine synthetische Ersatzdatei.

## Was konkret vorhanden ist

Die folgende Tabelle nennt die ursprünglichen Pfade im geprüften Repository. Im Elvenland-Paket liegen die drei übernommenen Referenzmodule unter `reference_code/javascript/offline_core.js`, `reference_code/javascript/dual_slot_store.js` und `reference_code/javascript/local_session_coordinator.js`. Die übrigen dort geprüften Module und die Tests gehören nicht zum neuen Laufzeitkern und sind nicht als Paketdateien enthalten.

| Datei | Tatsächlich implementiert | Grenze und Nutzung für Elvenland |
|---|---|---|
| `implementation/offline_core.js` | Kosten aus einer übergebenen Definition lesen; ausreichende Ressourcen prüfen; Bauplan vorbereiten; Gebäude und Kosten in einem kopierten Zustand gemeinsam ändern; wiederholte Transaktions-IDs abweisen oder erkennen. | Kein Baukatalog, keine eigene Kollisions-/Straßenprüfung, keine Produktion oder Forschung. Die Platzierungsprüfung und Gebäudeerzeugung kommen aus einem externen Adapter. Als Logikvorlage brauchbar, nicht unverändert als neuer Spielkern. |
| `implementation/dual_slot_store.js` | Zwei Speicherdateien, Revisionen, SHA-256-Prüfsumme, Rückfall auf die letzte gültige Datei, Export und Import eines JSON-Umschlags, Ablehnung bestimmter Zugangsdatenfelder. | Benötigt einen echten atomaren Dateischreibadapter. Noch kein Android-Dateiauswahldialog und keine Sicherung außerhalb des App-Verzeichnisses. Für Godot die Grundidee mit dessen Dateifunktionen umsetzen. |
| `implementation/local_session_coordinator.js` | Speicherzustand zuerst laden; einen unterstützten Bauauftrag abwickeln; Speicherung vor Erfolgsmeldung; fehlerhafte native Übernahme sperrt weitere Aktionen; doppelte Aufträge nicht zweimal abbuchen. | Eng an die alte Unity-Bridge und 37 Startup-Felder gebunden. Diese Abhängigkeiten im Neubau weglassen. Das Modul stellt keine echten Startdaten bereit. |
| `implementation/network_guard.js` | Lokaler Router mit ausdrücklicher Freigabe einzelner Aktionen; nicht unterstützte Aktionen scheitern. | Ein reiner Aufrufrouter und keine nachgewiesene Sperre aller Netzwerkverbindungen der Original-APK. Im Neubau sind keine ursprünglichen Request-/Response-Formate nötig. |
| `implementation/verified_reply_engine.js` | Strenger Abgleich extern verifizierter Anfrage-/Antwortpaare für erlaubte Leseaktionen. | Enthält keine Originalmitschnitte. Verbietet Startup und zustandsändernde Bau-/Produktionsoperationen. Für einen direkten lokalen Godot-Spielkern entbehrlich. |
| `implementation/frida_file_store_adapter.js` | Frida-Zugriffe auf privaten Android-Speicher mit temporärer Datei, Synchronisierung und Umbenennung. | Auf `org.elvenar.offline.lab3` festgelegt. Kein echter Godot-Adapter, kein SAF-Export und keine bestätigte Unity-Persistenz. Für Elvenland nicht übernehmen. |

## Originaldaten und Testwerte strikt trennen

Die ursprüngliche Repository-Datei `tests/fixtures/startup_shape_26.json` enthält ausdrücklich `"season": "SYNTHETIC_TEST_ONLY"`. Die Stadtliste ist leer; `featureTechnologies`, `unlocked_items` und weitere Listen sind ebenfalls leer. `premium=100` und `money=5` dienen den Tests. Sie sind keine belegten Elvenar-Startressourcen und dürfen nicht als Elvenland-Spielwerte übernommen werden.

Die Testdateien erfinden außerdem eine Gebäudedefinition mit beispielsweise 2 × 2 Feldern, Bevölkerung 123 und einer Produktion von vier Einheiten in 100 Sekunden. Der native Adapter in den Tests gibt eine Platzierung pauschal frei. Diese Werte und Adapter sind ausschließlich Prüfeingaben, keine aus der APK extrahierte Spielmechanik.

Die echte Datei `references/reference_start_v4_v5.json` ist laut `docs/PROJECT_STATUS.md` absichtlich nicht im Repository. Beide Testdateien wählen, wenn diese Datei fehlt, die synthetische 26-Feld-Fixture. Deshalb beweisen erfolgreiche Tests hier nur, dass eine 26-Feld-Struktur unverändert gespeichert werden kann und der alte Koordinator elf fehlende Felder erkennt. Sie beweisen weder die Werte eines ursprünglichen Spielstands noch dessen Vollständigkeit.

Das alte Kernmodul enthält eine besondere Preisänderung für `R_Elves_Premium_Residential_1` von 80 auf 2 Premiumeinheiten, nur bei gesetzten externen Verifikationsmarkierungen. Diese Regel ist ein historischer Modifikationswunsch. Der Quelltext allein belegt keinen aktiven Originalpreis. Für Elvenland darf diese Sonderregel nicht stillschweigend zum Originalwert oder zur neuen allgemeinen Preisregel werden.

## Historische Nachweise und ihre Reichweite

Die Dokumente berichten statisch geprüfte IL2CPP-Methoden und einen Server-Fallback im Tutorial. Die am 17.11.2026 fortgeschriebene Roadmap berichtet außerdem zehn installierte Hooks und 38 beobachtete Anfrageklassen auf Samsung. Diese Nachweise sind Beobachtungen des Originalclients. Die gleiche Roadmap lässt Offline-Start, lokalen Bau, Persistenz, Produktion, Forschung und Android-Abnahme funktional offen.

Der neue Neubauauftrag erlaubt eine andere Architektur. Die frühere Entscheidung „Original-Unity-UI + native Bridge“ bleibt als Historie des alten Elvenar-Projekts erhalten. Sie ist keine Vorgabe, mit der der ausdrücklich gewünschte Elvenland-Neubau blockiert werden sollte. Alte AGENTS.md-Dateien daher nur als historische Referenz ablegen und nicht ungeprüft als aktive Anweisung in das neue Projekt kopieren.

## Empfehlung für den neuen Kern

1. Einen eigenen `GameState` für Stadtfelder, platzierte Gebäude, Ressourcen, Produktionsaufträge und Forschungsfortschritt definieren. Gebäude- und Forschungsdefinitionen getrennt als JSON laden.
2. Direkte lokale Befehle wie `place_building`, `start_production`, `collect_production` und `unlock_technology` verwenden. Der neue Code braucht keine originalen Backend-Anfragen oder simulierten Serverantworten.
3. Zuerst Definition, Freischaltung, freie Felder und verfügbare Ressourcen prüfen. Danach Kosten und neue Entität gemeinsam übernehmen. Ein Fehler darf keinen halben Bauvorgang hinterlassen.
4. Die Oberfläche liest ausschließlich den übernommenen Zustand. Keine zweite Ressourcenwirtschaft in UI-Skripten führen.
5. Wiederholte Nutzeraktionen mit stabilen Auftrags-IDs oder gleichwertiger lokaler Zustandssicherung gegen Doppelbuchungen absichern.
6. Versionierte Spielstände atomar schreiben, eine vorherige gültige Fassung behalten und einen expliziten Export außerhalb privater App-Daten anbieten. Der Export muss nach einer Deinstallation wieder importierbar sein.
7. Originaldaten, vom Nutzer bestätigte Änderungen und vorläufige Testwerte in den Daten jeweils mit Herkunft und Status kennzeichnen. Fehlende Originalwerte bleiben OFFEN.

Dies ist eine technische Umsetzungsempfehlung, keine neue Festlegung von Spielpreisen, Ressourcenmengen, Forschungsabhängigkeiten oder Zeiten.

## Erneute Hostprüfung

Ausgeführt mit Node.js v24.22.1 aus den unverändert abgerufenen relevanten Dateien. Die Befehle beziehen sich auf das damalige Prüfverzeichnis des alten Repositorys, nicht auf das Elvenland-Paket:

| Prüflauf | Ergebnis | Was er belegt |
|---|---|---|
| `node tests/test_host.js` | 52/52 bestanden | Preisregel als Code, einmalige Buchung, Speicherumschlag, Wiederherstellung, simulierte Frida-Dateizugriffe. |
| `node tests/test_local_session.js` | 22/22 bestanden | Koordinator mit simuliertem nativen Adapter, Fehlerfälle und Reihenfolge von Speicherung und Zustandsübernahme. |
| `node tests/test_verified_reply_engine.js` | 37/37 bestanden | Abgleich synthetischer Anfrage-/Antwortpaare und Ablehnung unzulässiger Eingaben. |

Vollständige Ausgaben im Paket: `verification/previous_host_tests.json`. Kein Android-Prozess und kein Unity-Client wurden in dieser Prüfung gestartet.

## Quellen

- [Offline-Kern](https://github.com/geibibro123-linux/Farm-elvenar-/blob/main/implementation/offline_core.js)
- [Zwei-Slot-Speicher](https://github.com/geibibro123-linux/Farm-elvenar-/blob/main/implementation/dual_slot_store.js)
- [Session-Koordinator](https://github.com/geibibro123-linux/Farm-elvenar-/blob/main/implementation/local_session_coordinator.js)
- [Synthetische Startup-Fixture](https://github.com/geibibro123-linux/Farm-elvenar-/blob/main/tests/fixtures/startup_shape_26.json)
- [Historischer Projektstatus](https://github.com/geibibro123-linux/Farm-elvenar-/blob/main/docs/PROJECT_STATUS.md)
- [Roadmap mit Fortschreibung vom 17.11.2026](https://github.com/geibibro123-linux/Farm-elvenar-/blob/main/docs/ROADMAP_OFFLINE_MVP_2026-11-15.md)
- [Historische Architekturentscheidung](https://github.com/geibibro123-linux/Farm-elvenar-/blob/main/docs/ARCHITEKTUR_ENTSCHEIDUNG_LOCAL_BRIDGE.md)

Diese GitHub-Quellen liegen zum Prüfzeitpunkt in einem privaten Repository. Die Links sind deshalb kein Nachweis anonymer Lesbarkeit.
