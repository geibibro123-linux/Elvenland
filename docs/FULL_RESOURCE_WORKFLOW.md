# Vollständiges Ressourcenpaket direkt auf GitHub erstellen

**Vorbereiteter Ablauf, noch nicht auf GitHub ausgeführt.** Ein gespeicherter Workflow ist kein Nachweis eines erfolgreichen Builds oder Uploads.

## Voraussetzung

Die vollständigen Starter-Inhalte müssen bereits einzeln im Repository stehen. Danach muss der korrigierte `tools/build_package.py` eingespielt werden. Für diese Workflow-Fassung ist dessen SHA-256 festgelegt:

`62fd4facfc1f34ccaae08a129fc0d12b536da03fe9317301bb0a73b6e832cf42`

Der Workflow benutzt ausschließlich das Repository `geibibro123-linux/Elvenland`. Das automatisch für diesen Lauf bereitgestellte `GITHUB_TOKEN` wird mit `contents: write` an die GitHub CLI übergeben. Damit kann der Workflow die Draft-Quelle im selben Repository lesen und das Ergebnis als neues Release erstellen. Ein persönlicher Zugriffstoken und ein Zugriff auf ein anderes Repository sind nicht erforderlich. Repository-Regeln müssen diese Actions-Berechtigung erlauben.

## Quelle als Draft hinterlegen und manuell starten

1. Lege im Repository **Elvenland** ein neues Release mit beispielsweise dem Tag `elvenland-source-lab04` an. Hänge die bereits geprüfte Datei **`Elvenar_Lab04_SkriptTest03.apk`** an und warte, bis der Upload abgeschlossen ist.
2. Wähle **Save draft**. Die Quell-APK bleibt in diesem unveröffentlichten Entwurf. Klicke für diese Quell-Release nicht auf **Publish release**: Sie enthält auch Rohdaten, die bewusst aus dem öffentlichen Übergabepaket ausgeschlossen werden.
3. Öffne **Actions**, wähle **Rebuild verified Elvenland resources**, klicke **Run workflow**, wähle `main` und trage unter `source_release_tag` den tatsächlichen Tag des Drafts ein. Die Workflow-Datei und der korrigierte Builder müssen dafür bereits auf `main` liegen.

Erwartete Dateigröße: **232.466.424 Bytes**.

Erwarteter SHA-256:

`d77de38720bde3c0894493b519cdcca6183d7d020d3377d40e2096516d6d247c`

Der Workflow startet ausschließlich manuell. Er verlangt `isDraft == true`, den exakten Dateinamen, die Dateigröße und die festgelegte APK-Prüfsumme. Eine bereits veröffentlichte Quell-Release wird abgelehnt. Die Quelle wird weder veröffentlicht noch gelöscht.

## Ergebnis

Nach einem erfolgreichen Lauf entsteht ein neues Release **`elvenland-resources-v1`** mit:

- `Elvenland_Offline_Neubaupaket_v1.zip`
- `Elvenland_Offline_Neubaupaket_v1.sha256`
- `Elvenland_Offline_Neubaupaket_v1.verification.json`

Der ZIP-Inhalt umfasst extrahierte Einzeldateien, Daten, Dokumentation und Werkzeuge. Die Quell-APK, GitHub-Transportteile und ausgeschlossene private Rohdaten werden nicht in die neue ZIP übernommen. Dieser Ablauf baut kein spielbares Spiel und keine neue APK.

Die ZIP erhält ihre tatsächlich gemessene eigene Prüfsumme. Sie wird nicht mit dem Hash einer früher auf einem anderen Rechner erstellten ZIP gleichgesetzt. Gemessene Laufzeiten und aktualisierte Dokumentation können die Archivbytes verändern.

## Grenzen und Fehler

Die Workflow-Laufzeit ist auf 20 Minuten begrenzt. Das ist eine technische Abbruchgrenze, keine zugesicherte Fertigstellungszeit. Fehlende Actions-Freigaben, Repository-Regeln, ein ausgeschöpftes GitHub-Kontingent oder eine falsche Quell-APK können den Lauf verhindern.

Ein bereits vorhandenes Ziel-Release oder ein bereits vorhandener Ziel-Tag wird nicht überschrieben. Auch bei einem fehlgeschlagenen Release-Upload wird nicht automatisch gelöscht oder ersetzt; zuerst muss der tatsächliche Zustand geprüft werden.

Die Sichtbarkeit des Repositorys wird nicht verändert. Für anonymes Lesen und Herunterladen der überprüften Dateien und des veröffentlichten Ressourcen-Releases muss Elvenland öffentlich sein. Die Quell-Draft-Release bleibt unveröffentlicht; laut GitHub erhalten nur Personen mit Schreibzugriff die Draft-Release-Daten. Das ist kein allgemeiner Prüfvermerk für beliebige weitere Repository-Dateien oder die Git-Historie. Fehlende Original-Spielregeln werden durch den Ressourcen-Build nicht ergänzt oder erfunden.

## Nachweis zur Draft-Quelle

Geprüft am **17. November 2026** anhand offizieller GitHub-Dokumentation und des GitHub-CLI-Quellcodes:

- [GitHub REST: Releases](https://docs.github.com/en/rest/releases/releases): Öffentliche Releases und Drafts haben unterschiedliche Sichtbarkeit. Die REST-Abfrage über einen Tag ist für veröffentlichte Releases beschrieben.
- [GitHub CLI: gemeinsame Release-Suche](https://github.com/cli/cli/blob/trunk/pkg/cmd/release/shared/fetch.go): `FetchRelease` sucht ausdrücklich auch nach einem Draft mit dem vorgemerkten Tag. Dafür wird der Draft zuerst über GraphQL ermittelt und anschließend über seine Release-ID gelesen.
- [GitHub CLI: Release ansehen](https://github.com/cli/cli/blob/trunk/pkg/cmd/release/view/view.go) und [Release herunterladen](https://github.com/cli/cli/blob/trunk/pkg/cmd/release/download/download.go): Beide Befehle verwenden diese gemeinsame Suche. Der Asset-Download erfolgt authentifiziert über die Asset-API.
- [GitHub Actions: Authentifizierung mit GITHUB_TOKEN](https://docs.github.com/en/actions/tutorials/authenticate-with-github_token): Das bereitgestellte Token kann über `GH_TOKEN` von der GitHub CLI verwendet werden; seine Rechte werden im Workflow festgelegt.

Diese Prüfung belegt den vorgesehenen Zugriffsweg. Der konkrete Ressourcen-Workflow ist noch nicht auf GitHub ausgeführt worden.
