# Elvenland

Geprüftes Ressourcen- und Datenpaket für einen neuen, einfach aufgebauten Offline-Städtebau auf Android.

**Einstieg: [START_HERE.md](START_HERE.md)**  
**Arbeitsauftrag: [MASTER_PROMPT.md](MASTER_PROMPT.md)**  
**Prüfstand: [STATUS.json](STATUS.json)**

Der zusammengeführte Bestand enthält 6.594 Sprite-PNGs, 4.195 Textur-PNGs, 196 Audioquellen, sechs Schriftdateien und 20 Sprachfassungen. Animations- und Objektmetadaten sind lesbar exportiert. Die genaue Bedeutung dieser Zahlen und die verbleibenden Grenzen stehen in [docs/PACKAGE_COVERAGE.md](docs/PACKAGE_COVERAGE.md).

**Übergabe an KI-Chats: [docs/AI_HANDOFF.md](docs/AI_HANDOFF.md)**

Der Nutzer erlaubt einen eigenen Aufbau mit Godot oder Unity. Empfohlen ist Godot 4.6.3 mit GDScript und einer isometrischen 2D-Darstellung. Das Projekt übernimmt keine Pflicht zur ursprünglichen Unity-Serverkommunikation.

Die für dieses Repository vorbereiteten Projektdateien enthalten die lesbaren Unterlagen, geprüften Tabellen und wiederholbaren Werkzeuge. Die großen dekodierten Medien liegen in der Gesamt-ZIP als einzelne Dateien. Ihre Rohquellen bleiben anhand der ursprünglichen APKs und Hashlisten nachvollziehbar. Die kompakte Gesamt-ZIP verdoppelt diese Medien nicht durch zusätzlich beigelegte Rohcontainer.

Die Projektdateien sind in **Elvenland** gespeichert. 253 importierte Dateien wurden gegen ihre Git-Hashes geprüft; die 13 vorhandenen Kerndateien blieben erhalten. Das [KI-Startpaket v1](https://github.com/geibibro123-linux/Elvenland/releases/tag/elvenland-ki-startpaket-v1) ist als geprüftes 4,69-MB-Release vorhanden. Es enthält die Unterlagen und Indizes. Das vollständige Medienarchiv ist noch nicht als GitHub-Release bereitgestellt. Das Repository ist weiterhin **privat**, daher ist anonymer Zugriff noch nicht verfügbar. Der aktuelle Stand steht in [docs/GITHUB_PUBLICATION.md](docs/GITHUB_PUBLICATION.md).

Dieses Paket ist kein spielbares Offline-Spiel. Ein vollständiger Original-Forschungsbaum, vollständige Gebäudekosten und Produktionsrezepte sind noch nicht nachgewiesen. Unbekannte Werte bleiben offen. Die genaue Datenlage steht in [data/reference/README_HISTORICAL_DATA.md](data/reference/README_HISTORICAL_DATA.md).

Die Originalgrafiken und Originalmusik behalten ihre Herkunft und ihre Rechte. Eine Freigabe als Open Source oder eine Rechteübertragung wird durch diesen Export nicht behauptet. Siehe [THIRD_PARTY_NOTICE.md](THIRD_PARTY_NOTICE.md).

## Repository und Archivstand

Die Quellarchive sind unveränderte Erstellungssnapshots vom 17. November 2026. Der Materialumfang bleibt unverändert. Diese Repository-Fassung aktualisiert den Veröffentlichungsstand. `INDEX.json` und die Medienindizes beschreiben weiterhin das vollständige Medienpaket; die großen Medien liegen nicht im kleinen Git-Dateibestand. Archivbezogene SHA-Listen und Archivmanifeste werden hier nicht als aktuelle Repository-Prüfsummen übernommen. Die im kleinen ZIP enthaltene Datei `KI_START_HERE.md` erläutert dessen Umfang; im Repository gelten diese README, `START_HERE.md` und `STATUS.json`.


## Vollständiges Medienpaket erneut erstellen

Der vorbereitete [Ressourcen-Workflow](docs/FULL_RESOURCE_WORKFLOW.md) kann die gesamte ZIP aus der geprüften Quell-APK als Release-Anhang in diesem Repository erzeugen. Er wurde noch nicht auf GitHub ausgeführt. Er baut keine neue Android-App. Die korrigierten Werkzeuge wurden lokal für die vollständige Wiederherstellung verwendet; siehe [Prüfbericht](verification/restored_package_20261117.json).
