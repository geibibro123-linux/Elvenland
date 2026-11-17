# Paketbau für Elvenland

Das Repository `geibibro123-linux/Elvenland` ist verbunden. Die lesbaren Projektdateien sind gespeichert und das kleine KI-Startpaket wurde als Release veröffentlicht. Es enthält Unterlagen und Indizes; das große Medienarchiv ist getrennt bereitzustellen.

Für den aktuellen vorbereiteten Ressourcenbau gilt [docs/FULL_RESOURCE_WORKFLOW.md](../docs/FULL_RESOURCE_WORKFLOW.md). Der aktive Workflow liegt unter `.github/workflows/elvenland-resources.yml` und verwendet eine exakt geprüfte Quell-APK im selben Repository. Eine Ausführung dieses vollständigen Ressourcenbaus auf GitHub steht noch aus.

Die Datei `github/elvenland-package.yml` bleibt eine ältere, nicht aktivierte Vorlage für eine öffentlich abrufbare HTTPS-APK-Quelle. Sie ist für den aktuellen Weg nicht erforderlich. Keine geheimen Download-URLs oder Zugriffstokens in ihre Eingaben schreiben.

Der lokal ausgeführte Paketbau ist unter [docs/REPRODUCE.md](../docs/REPRODUCE.md) dokumentiert. Der aktuelle Prüfbericht der vollständigen Wiederherstellung liegt unter `verification/restored_package_20261117.json`.

Diese Abläufe erzeugen Ressourcen-ZIPs. Der Godot-Spielkern und eine neue Android-APK sind nachfolgende Entwicklungsarbeit. Für anonyme Lesbarkeit muss die Sichtbarkeit des Repositorys separat stimmen und ein Abruf ohne Anmeldung geprüft werden.
