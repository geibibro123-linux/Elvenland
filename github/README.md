# Vorlage für das eigene Repository elvenland

Diese Dateien sind vorbereitet. Sie wurden nicht auf GitHub ausgeführt. Der GitHub-Zugriff für das angefragte Ziel fehlt derzeit; Einzelheiten stehen in `docs/GITHUB_PUBLICATION.md`.

## Lesbare Projektdateien und vollständiges Medienarchiv

Das kleine KI-Startpaket entpacken und die Dateien innerhalb seines Ordners `elvenland/` als Wurzel des neuen Repositorys verwenden. Prompt, Dokumente, Daten und Indizes können dadurch einzeln gelesen werden. Die Dateien des vollständigen Medienpakets bleiben im vollständigen ZIP und werden als Release-Anhang veröffentlicht. Ein öffentliches Repository und ein tatsächlich öffentliches Release sind für den gewünschten Zugriff ohne Anmeldung erforderlich.

Die vorhandenen ZIP-Dateien lassen sich direkt als Release-Dateien bereitstellen. Ein erneuter Export aus der APK ist dafür nicht nötig. Zusammen mit dem großen ZIP die zugehörige `.sha256` und `.verification.json` veröffentlichen. Den konkreten Release-Link anschließend ohne Anmeldung prüfen; erst danach den Veröffentlichungsstatus ändern.

## Optionaler Neubau mit GitHub Actions

Die Vorlage `github/elvenland-package.yml` ist für ein Repository vorbereitet, dessen Wurzel die Elvenland-Dateien enthält. Zur Aktivierung an `.github/workflows/elvenland-package.yml` kopieren und mit dem Repository speichern. Sie wird ausschließlich manuell über **Run workflow** gestartet.

Der Workflow erwartet eine öffentlich herunterladbare HTTPS-URL zu einer bereits geprüften Quell-APK. Er verwendet keinen privaten Zugriffstoken für das alte Repository. Eine private GitHub-Release-URL funktioniert in dieser Vorlage nicht ohne eine eigene Zugriffslösung. Keine Zugangsdaten oder geheimen Download-URLs in das Eingabefeld schreiben.

`tools/build_package.py` prüft den SHA-256-Wert vor der Extraktion gegen `provenance/SOURCE_INPUTS.json` und akzeptiert nur bekannte Versionen. Eine neue APK-Version muss zuerst unabhängig geprüft und dokumentiert werden. Die Vorlage installiert Python-Abhängigkeiten und Medienwerkzeuge, erzeugt das große Ressourcenpaket und das kleine Startpaket und veröffentlicht beide als Release.

Dieser Workflow baut Ressourcen-ZIPs. Er erstellt keine Godot-Anwendung und keine Android-APK. Seine Ausführung auf GitHub ist noch nicht nachgewiesen. Für den lokalen, tatsächlich ausgeführten Paketbau siehe `docs/REPRODUCE.md` und `verification/`.
