# Elvenland an ChatGPT oder Claude übergeben

Geprüfter Informationsstand: **17. November 2026**. Dateiannahme, Entpacken und vollständige Verarbeitung sind getrennte Fähigkeiten. Ein erfolgreicher Upload beweist noch nicht, dass eine Sitzung sämtliche enthaltenen Medien lesen kann.

Die vollständig wiederhergestellte lokale Medien-ZIP hat 673.087.419 Bytes. Ihr aktueller Prüfbericht liegt unter `verification/restored_package_20261117.json`. Das kleine KI-Startpaket hat 4.686.083 Bytes und ist als GitHub-Release vorhanden. **Das Hauptarchiv wird deshalb nicht als direkt in einen KI-Chat hochladbare Datei zugesagt. Das kleine KI-Startpaket ist der empfohlene Einstieg.**

## Empfohlener Einstieg

1. Das kleine **KI-Startpaket** und den separat bereitgestellten `MASTER_PROMPT.md` verwenden. Zuerst `START_HERE.md`, `STATUS.json` und die Datenabdeckung lesen lassen. Die deutschen und englischen KI-Referenztabellen sind für diesen Einstieg zusätzlich separat vorgesehen.
2. Ein ZIP nur anhängen, wenn die konkrete Sitzung diesen Dateityp annimmt und Werkzeuge zum Entpacken besitzt. Falls das nicht funktioniert, die benötigten Text- und JSON-Dateien einzeln anhängen oder über tatsächlich zugängliche Raw-Links bereitstellen.
3. Das vollständige Medienpaket getrennt bereithalten. Es enthält die exportierten Bilder, WAV-/OGG-Dateien, technischen Metadaten und alle 20 gefundenen Sprachfassungen. Benötigte Medien anhand der Indizes auswählen, statt alle Dateien gleichzeitig in den Gesprächskontext zu laden. Ein externer Download setzt tatsächlich verfügbaren Datei- und Netzwerkzugriff der jeweiligen Sitzung voraus.
4. Vor der Weiterarbeit die tatsächlich geöffneten Dateien, ihre Prüfsummen und fehlende Zugriffe feststellen lassen. Ein privater GitHub-Link wird durch einen Prompt nicht anonym erreichbar. Keine Passwörter oder Zugriffstokens in den Prompt schreiben.

Das kleine Paket erleichtert Übertragung und gezieltes Lesen. **Seine geringere Größe garantiert keine ZIP-Unterstützung.** Es ersetzt nicht die Medien und ist ebenso wenig wie das Gesamtpaket eine installierbare APK.

## Offiziell dokumentierte Grenzen

| Oberfläche | Dokumentierter Stand | Bedeutung für Elvenland |
| --- | --- | --- |
| ChatGPT.com | Die Uploadhilfe nennt 512 MB pro Dokument-/Präsentationsdatei. ZIP-Verarbeitung wird ausdrücklich für Sitzungen mit verfügbarer Data Analysis beschrieben. Text-/Dokumentdateien besitzen zusätzlich eine Grenze von zwei Millionen Tokens [1]. | Ein Hauptarchiv über 512 MB liegt oberhalb dieser dokumentierten Größe. Zum direkten Einstieg das kleine Paket beziehungsweise unterstützte Einzeldateien verwenden. Auch dann ZIP-Annahme und Entpacken konkret prüfen. |
| Claude.ai, direkter Chat | Die allgemeine Uploadhilfe nennt 500 MB pro Datei und bis zu 20 Dateien pro Chat. ZIP ist in ihrer Standardformatliste nicht ausdrücklich aufgeführt [2]. | Ein Hauptarchiv über 512 MB überschreitet auch diese Grenze. Das kleine Startpaket oder passende Einzeldateien verwenden; die Größe allein beweist keine ZIP-Unterstützung. |
| Claude Project-Dateien | Die Uploadhilfe nennt 30 MB pro Datei; der Gesamtinhalt muss in das Kontextfenster passen [2]. | Das große Medienarchiv ist dafür zu groß. Kleine unterstützte Text-/JSON-Dateien gezielt verwenden. |
| Claude Codeausführung und Dateierstellung | Die gesonderte Hilfeseite nennt weiterhin 30 MB für Uploads und Downloads. Codeausführung und Netzwerkzugriff können von den Einstellungen abhängen [3]. | Die offiziellen Angaben sind für große Archive nicht einheitlich. Deshalb keinen sicheren Groß-ZIP-Upload oder externen Download versprechen. |

Die genannten Größen sind die Angaben der jeweiligen Hilfeseiten. Die genaue Größe des ausgelieferten Elvenland-Archivs steht in seinem Prüfbericht. Konto-, Speicher-, Nutzungs- und Werkzeuggrenzen können zusätzlich gelten.

## Was im Standardpaket fehlt

Das veröffentlichbare Paket enthält ausschließlich die geprüften konvertierten Ausgaben und zugehörigen Unterlagen. Unveränderte UnityFS- und FSB-Rohcontainer werden nicht beigelegt. Ihre Herkunft und Prüfsummen stehen unter `provenance/`. Für eine erneute Extraktion wird die eigene verifizierte APK beziehungsweise ein externes privates Eingabeverzeichnis benötigt; siehe `docs/REPRODUCE.md`.

Für das Lesen der bereits exportierten PNG-, WAV-, OGG- und JSON-Dateien ist diese erneute Extraktion nicht erforderlich. Ein kleines KI-Startpaket enthält die Unterlagen und Indizes, aber nicht automatisch die gesamten Mediendateien.

Alle 20 Sprachen bleiben im Vollpaket erhalten. Die kompakten Referenztabellen für `de_de` und `en_dk` werden zusätzlich für das KI-Startpaket bereitgestellt. Der ursprüngliche Sprachcode `en_dk` und sämtliche Übersetzungsvarianten bleiben erhalten. Diese Tabellen enthalten Anzeige- und Erklärungstexte, keinen vollständigen Technologiebaum oder verbindliche Wirtschaftstabellen.

## Offizielle Quellen

1. OpenAI, **Uploading files and audio to ChatGPT**: https://help.openai.com/en/articles/8555545-uploading-files-and-audio-to-chatgpt
2. Anthropic, **Upload files to Claude**, Seitendatum 23. Juli 2026: https://support.claude.com/en/articles/8241126-upload-files-to-claude
3. Anthropic, **Create and edit files with Claude**: https://support.claude.com/en/articles/12111783-create-and-edit-files-with-claude

