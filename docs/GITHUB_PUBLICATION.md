# GitHub-Veröffentlichung und anonymer KI-Zugriff

Stand: 17. November 2026.

## Tatsächlich abgeschlossen

Das bestätigte Ziel [geibibro123-linux/Elvenland](https://github.com/geibibro123-linux/Elvenland) ist verbunden und weiterhin **privat**.

* 253 Tabellen, Indizes, Referenzmodule und Werkzeuge wurden einzeln importiert. Alle 253 Git-Blob-Hashes stimmen mit dem geprüften Startpaket überein. Die 13 vorhandenen Kerndateien wurden erhalten.
* Der [Importlauf](https://github.com/geibibro123-linux/Elvenland/actions/runs/44181480446) wurde erfolgreich abgeschlossen. Sein Inhaltscommit lautet `74a254ee1ed47ee0926ba1a7aec1ed80d22f1714`.
* Das [KI-Startpaket v1](https://github.com/geibibro123-linux/Elvenland/releases/tag/elvenland-ki-startpaket-v1) ist mit 4.686.083 Bytes und SHA-256 `3aea47b37907ea7bf168139f6d10957deffdca933afe8870325b17524898169b` als Release gespeichert.
* Der vollständige Medienbestand wurde lokal erneut erzeugt. Die aktuelle ZIP enthält 25.662 Dateien bei 673.087.419 Bytes. Alle 11.452 Medien-Dateien sind byte-identisch zum vorherigen geprüften Paket. Belege stehen unter `verification/restored_package_20261117.json` und `verification/restored_package_file_comparison_20261117.json`.

## Noch offen

Die große ZIP ist noch nicht als GitHub-Release gespeichert. Die GitHub-Anbindung stellte keinen direkten Upload für binäre Release-Dateien bereit. Die zusätzliche Browser-Anmeldung wurde abgebrochen; danach war keine angemeldete Browser-Sitzung verfügbar. Der zusätzliche dauerhafte Dateispeicherversuch lieferte kein erfolgreiches Ergebnis. Die kleine ZIP und die GitHub-Dateien sind davon getrennt erfolgreich gespeichert.

Das Repository ist privat. Ein erfolgreicher Upload ist deshalb noch kein anonymer Zugriff. `anonymous_github_access_verified` bleibt `false`. Die Sichtbarkeit kann mit den vorhandenen GitHub-Werkzeugen nicht geändert werden.

## Vorbereiteter Weg zum vollständigen Medien-Release

Die Anleitung steht unter [FULL_RESOURCE_WORKFLOW.md](FULL_RESOURCE_WORKFLOW.md). Der neue Workflow `.github/workflows/elvenland-resources.yml` liest die exakt geprüfte Datei `Elvenar_Lab04_SkriptTest03.apk` als Anhang eines **unveröffentlichten Release-Entwurfs** aus demselben Repository Elvenland. Er wird ausschließlich manuell gestartet und verlangt, dass die Quell-Release ein Entwurf bleibt. Er benötigt keinen zusätzlichen dauerhaften Zugriffsschlüssel. Er prüft den APK-Hash, erzeugt die Medien-ZIP und veröffentlicht ihre tatsächlich gemessene Prüfsumme. Er wurde noch nicht auf GitHub ausgeführt.

Die Quell-APK liegt bisher in der wiederhergestellten Dateisammlung und im anderen privaten Quellrepository. Das kurzlebige Token von Elvenland kann nicht automatisch das andere private Repository lesen. Daher muss die Quell-APK zunächst als Anhang eines unveröffentlichten Release-Entwurfs in Elvenland liegen. Die Quell-APK bleibt im Entwurf, während das geprüfte erzeugte Ressourcenpaket separat veröffentlicht wird. Draft-Releases sind nur für Konten mit Push-Zugriff sichtbar [3]. Die vorhandene Vorlage `github/elvenland-package.yml` bleibt eine ältere Alternative für öffentlich abrufbare APK-URLs; für den aktuellen Weg gilt die neue Anleitung.

Der Workflow erstellt ein Ressourcenpaket. Eine neue spielbare Android-App wurde nicht erstellt.

## Anonymen Zugriff abschließen

Nach Umstellung des Repositorys auf Public müssen die tatsächlichen Text- und Downloadlinks ohne Anmeldung geprüft werden. Erst dann darf der anonyme Zugriff als bestätigt gelten. Keine Zugangstokens in Prompts oder Dokumente aufnehmen. Die bestehenden Hinweise zur Herkunft und zu Rechten an Originalmedien bleiben unter `THIRD_PARTY_NOTICE.md` erhalten.

GitHub blockiert einzelne Dateien über 100 MiB im normalen Git-Verlauf. Release-Assets dürfen jeweils unter 2 GiB groß sein; die große ZIP passt daher als Release-Datei [1][2].

## Archivstände und Prüfsummen

Das kleine Startpaket bleibt ein unveränderter Erstellungssnapshot vom 17. November 2026. Damalige Zugangshinweise im ZIP sind historisch. Für den aktuellen Veröffentlichungsstand gelten diese Datei, README und STATUS im Repository. Medienindizes beschreiben den vollständigen Bestand, auch wenn die Medien nicht im kleinen Git-Dateibestand liegen.

Die aktuelle wiederhergestellte lokale Medien-ZIP hat SHA-256 `651d0600107835b45ecac198a858aed5f21bd1335764c436d10d1c5035aca822`. Der ältere Hash `595290ed0ffc7b78440605f802df514c3aede50ee83f8647628df7fe58c3d797` gehört zur früheren ZIP und darf nicht dafür verwendet werden. Gemessene Laufzeiten und geänderte Dokumentation können bei weiteren Builds andere Archiv-Hashes erzeugen. Maßgeblich ist immer der Prüfbericht der tatsächlich gelieferten Datei.

## Quellen

1. https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github
2. https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases

3. https://docs.github.com/en/rest/releases/releases
