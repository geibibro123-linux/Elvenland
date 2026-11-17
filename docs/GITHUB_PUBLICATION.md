# GitHub-Veröffentlichung und anonymer KI-Zugriff

Stand: 17. November 2026.

## Aktuelle Verbindung

Das vom Nutzer bestätigte Ziel [geibibro123-linux/Elvenland](https://github.com/geibibro123-linux/Elvenland) existiert und ist mit dem GitHub-Zugang verbunden. Schreibzugriff wurde bestätigt. Das Repository ist derzeit **privat**; der Standardbranch heißt `main`.

Der Upload der vorbereiteten Projektdateien läuft. Ein Elvenland-Release ist noch offen. Ein erfolgreicher Upload oder ein vorhandener Repository-Link allein bestätigt keinen anonymen Zugriff. `anonymous_github_access_verified` bleibt `false`.

Die Archive bleiben unveränderte Erstellungssnapshots vom 17. November 2026. Der Materialumfang wurde nicht geändert. Die aktuelle Repository-Fassung aktualisiert ausschließlich die Publikationsangaben und enthält die kleinen lesbaren Projektdateien. Große Medien werden getrennt bereitgestellt.

Das frühere private Repository `geibibro123-linux/Farm-elvenar-` bleibt eine historische Quelle. Der jetzt autorisierte Upload hat das ausdrücklich benannte Ziel `geibibro123-linux/Elvenland`.

## Dateiablage und gewünschter anonymer Zugriff

- `README.md`, `START_HERE.md`, `MASTER_PROMPT.md`, `STATUS.json`, `INDEX.json`, `AGENTS.md`, Daten, Dokumente und Teilindizes als gewöhnliche lesbare Dateien.
- Die große ZIP als Release-Datei, mit passender SHA-256-Datei und Prüfbericht.
- Keine Signaturschlüssel, Kontodaten, Zugangstokens oder unbearbeiteten privaten Startantworten veröffentlichen.
- Einzelne Text-/JSON-Dateien über ihre tatsächlichen Raw-URLs prüfen. ZIP-Download ohne Anmeldung prüfen und dessen SHA-256 gegen das Release-Manifest abgleichen.
- Nur bei tatsächlichem erfolgreichen anonymen Abruf `anonymous_github_access_verified` auf `true` setzen.

GitHub blockiert einzelne Dateien über 100 MiB im normalen Git-Verlauf. Release-Assets dürfen laut der am 17.11.2026 geprüften Dokumentation jeweils unter 2 GiB groß sein. Für die spätere Veröffentlichung ist die Medien-ZIP deshalb als Release-Asset vorgesehen [1][2]. Die Erstellung dieses Releases ist noch offen.

## Wiederholbarer Paketbau

Die konkrete Vorlage liegt unter `github/elvenland-package.yml`. Sie wurde noch nicht auf GitHub ausgeführt und startet ausschließlich manuell über `workflow_dispatch`. Der Nutzer muss beim Start eine öffentlich abrufbare HTTPS-URL zur Eingabe-APK angeben. Anschließend wird der APK-Hash gegen die verifizierten Quellen geprüft. Das Paketskript verwendet die in `provenance/source_media_files.json` ausgewählten Quelldateien.

Diese Vorlage greift nicht auf das private Baseline-Release zu und benötigt keinen privaten Quelltoken. Die angegebene HTTPS-Quelle muss ohne Anmeldung tatsächlich erreichbar sein. Das bloße Vorhandensein der Workflow-Datei ist kein Nachweis eines erfolgreichen Downloads oder eines ausgeführten GitHub-Builds.

Für einen lokalen Neubau kann eine der in `provenance/SOURCE_INPUTS.json` verifizierten APKs unmittelbar als Eingabedatei übergeben werden. Dieser Weg benötigt keinen öffentlichen APK-Link. Die Gesamt-ZIP enthält die dekodierten Medien bereits und benötigt für den neuen Spielbau keine erneute Verbindung zum Spielserver.

Der lokale Paketbau ist der unmittelbar verfügbare Weg. Die veröffentlichbare ZIP enthält ausschließlich die geprüften konvertierten Ausgaben und zugehörigen Unterlagen. Unveränderte Rohcontainer bleiben in der eigenen verifizierten APK beziehungsweise im privaten Eingabeverzeichnis. Hinweise zur Übergabe der vorbereiteten Dateien an KI-Chats stehen in `docs/AI_HANDOFF.md`.

Laufzeit-, Kompressions- und Werkzeugmetadaten können zwischen zwei erneuten Paketbauten variieren. Maßgeblich ist die SHA-256-Datei der jeweils tatsächlich heruntergeladenen ZIP und das darin enthaltene Dateimanifest. Keinen Hash einer lokalen ZIP für ein unabhängig neu erzeugtes Release-Archiv ausgeben.

## Quellen

1. https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github
2. https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases
