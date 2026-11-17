# Elvenland: technische Empfehlung für den Offline-Neuaufbau

Recherche: 17. November 2026. Diese Notiz ist eine Architektur-Empfehlung. Sie bestätigt weder Vollständigkeit noch Qualität der konkreten APK-Ressourcen. Dafür ist die Inventur der tatsächlich zugänglichen Dateien maßgeblich.

## Empfehlung

Für einen neuen, einfach pflegbaren Offline-Aufbaukern ist **Godot 4 mit GDScript und 2D/isometrischer Darstellung** die bevorzugte Arbeitsrichtung. Die konkrete stabile Godot-Version und die dazu passenden Android-Exportvorlagen müssen gemeinsam festgeschrieben werden. Der Vorschlag gilt unter der Bedingung, dass ein ausreichend großer Teil der benötigten Stadtansicht als brauchbare Bilder, Sprites oder Texturatlanten vorliegt. Godot unterstützt isometrische TileSets und TileMapLayer [S1].

Unity bleibt sinnvoll, wenn die tatsächlichen Ressourcen stark von komplexen 3D-Modellen, Skeletten, Unity-Animationen, Materialien oder bereits wiederherstellbaren Unity-Szenen abhängen. Dann kann das Wiederverwenden dieser Strukturen weniger Arbeit verursachen als eine Übertragung in Godot. Ein aus einer APK gewonnenes Asset-Verzeichnis ist jedoch noch kein funktionsfähiges Unity-Projekt.

| Entscheidung | Godot mit GDScript | Unity mit C# |
| --- | --- | --- |
| Neuer lokaler 2D-Aufbaukern | Empfohlene Arbeitsrichtung | Ebenfalls technisch möglich |
| Lesbarer Quelltext und einfache Datenpflege | GDScript, JSON, Textszenen | C#, JSON oder ScriptableObjects |
| Ursprüngliche Unity-Szenen und Animationen übernehmen | Übertragung oder Neuaufbau nötig | Besser passende Engine, soweit Daten vollständig wiederherstellbar sind |
| Backend-Komplexität | Kann vollständig entfallen | Kann in einem neuen Projekt ebenfalls vollständig entfallen |
| Android-Build | Godot, passende Exportvorlagen, Java und Android-Werkzeuge | Unity Hub/Editor und Android-Module |

Die vereinfachte Architektur entsteht durch einen neuen lokalen Spielkern. Der bloße Wechsel des Engine-Namens beseitigt keine fehlenden Regeln, Daten oder Assets.

## Benötigte Software

| Zweck | Werkzeug | Bedingung und Umfang |
| --- | --- | --- |
| Ressourceninventur und wiederholbare Extraktion | Python 3 und festgeschriebene UnityPy-Version | UnityPy kann Unity-Assets, Bundles und APKs lesen; Texturen/Sprites, Audio, Texte und manche Modelle exportieren. Unterstützte Daten müssen tatsächlich vorhanden und lesbar sein [S2]. |
| Komplexe Unity-Objektstruktur prüfen | AssetRipper | Ergänzung für Abhängigkeiten und Unity-native Formate. Projekt nennt versionsabhängig unterschiedliche Unterstützungsqualität [S3]. |
| Neuer Spielkern | Godot 4, Standardausgabe, GDScript | Kein C# für den vorgeschlagenen ersten Android-Aufbau. Die geprüfte Godot-Android-Dokumentation bezeichnet C#-Android-Unterstützung als experimentell [S4]. |
| Android-Ausgabe | Passende Godot-Exportvorlagen | Ein Ressourcen-ZIP oder PCK ist ausdrücklich noch kein ausführbarer Build [S5]. |
| Android-Werkzeuge | OpenJDK 17 und Android SDK | Aktuell geprüfte Godot-Anleitung nennt zusätzlich konkrete Plattform-, Build-Tools-, NDK- und CMake-Versionen. Mit der festgelegten Godot-Version gemeinsam installieren und dokumentieren [S4]. |
| Verwaltung und Installation der Android-Werkzeuge | Android Studio oder SDK Command-line Tools | Android Studio ist ein bequemer Installationsweg, aber nicht der einzige [S4]. |
| Installation und Fehlerprotokolle am Gerät | Android SDK Platform-Tools einschließlich adb | Ein realer Start- und Speichertest ist Voraussetzung für die Aussage, dass die APK auf dem konkreten Samsung funktioniert. |
| Optional: Originale 3D-Ressourcen bearbeiten | Blender | Nur nötig, wenn die Inventur einen tatsächlichen Bedarf an Modell-, Skelett- oder Animationsbearbeitung zeigt. |
| Alternative Unity-Ausgabe | Unity Hub, gewählter Unity Editor, Android Build Support, Android SDK & NDK Tools, OpenJDK | Diese Module nennt Unity offiziell [S6]. |

Alle verwendeten Versionen gehören in eine Toolchain-Datei. Die aktuell abgerufene Godot-Anleitung nennt OpenJDK 17, SDK Platform 35, Build-Tools 35.0.1, Platform-Tools ab 35.0.0, NDK r28b und CMake 3.10.2.4988404 [S4]. Diese Angaben sind kein Freibrief, verschiedene Godot-Versionen und Exportvorlagen zu mischen.

## Was die APK liefern kann und was offen bleibt

1. **Grafiken und Audio:** Nur tatsächlich enthaltene oder separat bereitgestellte Daten sind extrahierbar. Asset-Zähler, Originalnamen, Pfade und Hashes dokumentieren. Ein Sprite-Atlas allein beweist noch keine korrekten Gebäudezuordnungen oder Animationsabläufe.
2. **Texte und Tabellen:** Vorhandene TextAssets, Konfigurationen und Lokalisierungen können lesbare Werte enthalten. Jeder übernommene Wert braucht die konkrete Quelldatei und möglichst einen Datensatz-/Objektbezug.
3. **Client-Code:** IL2CPP wandelt verwalteten Code über C++ in native Binärdateien um. Die APK ist deshalb kein originaler C#-Quellcodebestand [S7]. Eine neue Implementierung ist von einer Rückgewinnung des vollständigen Originalprojekts zu unterscheiden.
4. **Nachgeladene Inhalte:** Unity unterstützt AssetBundles und Addressables, die erst zur Laufzeit von entfernten Quellen geladen werden. Deshalb kann ein APK-Archiv inhaltlich unvollständig sein [S8]. Ob dies in den verfügbaren Elvenar-Versionen zutrifft, muss die konkrete Inventur zeigen.
5. **Serverregeln:** Regeln, die nur auf einem Server vorhanden waren, sind nicht durch Entpacken einer APK wiederherstellbar. Sichtbare Client-Anzeigen beweisen nicht automatisch die zugehörigen Autorisierungs-, Belohnungs- oder Kampfregeln. Fehlende Originalwerte bleiben OFFEN.

## Einfacher lokaler Aufbau

Diese Gliederung ist ein Vorschlag und keine Behauptung über die ursprüngliche Implementierung:

* `data/buildings.json`: Gebäudedefinitionen, Flächen, Stufen, Kosten und belegte Voraussetzungen.
* `data/production.json`: Eingaben, Ausgaben, Dauer und Lagerregeln.
* `data/research.json`: Forschungsknoten, Voraussetzungen, Kosten und Freischaltungen.
* `data/resources.json`: Ressourcen-IDs und Darstellungsinformationen.
* `data/assets.json`: Zuordnung der fachlichen IDs zu lokalen Bild-/Audio-Dateien und Herkunft.
* `data/rules_status.json`: Belegstatus, Quellen, Konflikte und offene Werte, getrennt von lauffähigen Konfigurationen.
* `core/game_state.gd`: Ein zentraler Zustand für Ressourcen, Gebäude, Fortschritt und aktive Vorgänge.
* `core/commands.gd`: Platzieren, Aufwerten, Produzieren, Einsammeln und Forschen als lokale Befehle.
* `core/save_service.gd`: Versionierter Speicherstand, temporäre Schreibdatei, Sicherung und Wiederherstellung.
* `ui/`: Darstellung des Zustands und Eingaben. Die Oberfläche führt keine eigene Ressourcenbuchhaltung.

Ein Bauauftrag prüft zunächst alle Voraussetzungen, verbucht die Kosten genau einmal und legt danach den Vorgang an. Erst eine erfolgreiche Zustandsänderung löst eine UI-Aktualisierung aus. Dieselbe Stelle entscheidet über Forschung und Produktion. Es ist keine nachgebildete HTTP-API und kein lokaler Webserver erforderlich.

Später editierbare Werte werden aus JSON geladen. Eine Android-Funktion zum Importieren einer geprüften Konfigurationsdatei wäre praktischer als das manuelle Bearbeiten versteckter App-Verzeichnisse. Referenzen, Zahlenbereiche und Datenversionen müssen vor Übernahme validiert werden. Ein OFFEN-Wert darf nicht stillschweigend als null oder null Euro spielbar werden.

Normales lokales Speichern übersteht einen App-Neustart. Es übersteht nicht automatisch eine Deinstallation: Android entfernt App-spezifische Dateien [S9]. Für Daniels Ziel braucht es zusätzlich einen ausdrücklich exportierten Spielstand in ein vom Nutzer gewähltes Dokument. Das Android Storage Access Framework ermöglicht solche Dateien außerhalb des App-Verzeichnisses; sie bleiben bei Deinstallation erhalten [S10]. Wiederimport muss zu einer neuen Testversion mit anderer App-ID passen.

## Anonyme Lesbarkeit für ChatGPT und Claude

Ein öffentlich herunterladbares ZIP ist hilfreich, garantiert aber nicht, dass jedes Modell oder jede Sitzung das Archiv direkt entpacken kann. Der Repository-Bestand sollte zusätzlich kleine, unmittelbar lesbare UTF-8-Dateien enthalten:

* `START_HERE.md` mit Aufgabe, Bestand, Status und Lesereihenfolge.
* `MASTER_PROMPT.md` mit Regeln gegen erfundene Originalwerte, klaren Bauetappen und Abnahmekriterien.
* Manifest mit Dateipfad, Größe, SHA-256, Kategorie, Quelle und Status.
* Getrennte JSON-Dateien je Fachsystem sowie bei großem Bestand nachvollziehbare Teildateien.
* Sichtbare Medienübersichten und Kontaktbögen; keine riesigen Base64-Blöcke im Prompt.
* Öffentliche Raw-Links zu den Textdateien sowie ein Release-Download für umfangreiche Medien.

GitHub blockiert einzelne Dateien über 100 MiB im normalen Git-Verlauf. Große ZIP-Dateien passen deshalb eher in Releases; jedes Release-Asset muss unter 2 GiB bleiben [S11, S12]. Anonym erreichbar bedeutet, dass kein Login und kein zeitlich begrenzter Zugriffstoken notwendig ist. Das ist getrennt vom inhaltlichen Datenschutz der veröffentlichten Dateien zu prüfen.

## Einschätzung der 100 Minuten

Ein verbindliches Versprechen, das vollständige Originalspiel in 100 Minuten Analyse, Extraktion, Neuimplementierung und Android-Build zu reproduzieren, ist technisch nicht begründet. Unbekannt sind unter anderem Downloadumfang, Asset-Vollständigkeit, Tabellenqualität, Animationsaufwand, installierte Toolchain und Startverhalten des Builds.

Als Arbeitsfenster für eine belastbare Inventur, automatische Ressourcenextraktion, Quellenzuordnung und ein vollständiges Übergabepaket ist diese Größenordnung plausibel, sofern Dateien zugänglich und Werkzeuge verfügbar sind. Bei günstigen Voraussetzungen kann ein eng begrenzter erster Offline-Spielkreislauf hinzukommen. Das sind Arbeitsziele, keine bereits erbrachten Ergebnisse.

Vier klare Etappen sind ausreichend: **Bestand nachweisen; Ressourcen und Regeln extrahieren; lokalen Kern mit einem vollständigen Spielkreislauf bauen; Android-Build und reale Funktion prüfen.** Die erste APK sollte eine nachgewiesene Stadtansicht, Platzierung mit korrekter Kostenbuchung, einen Produktions-/Erntevorgang und Speichern/Laden enthalten. Weitere Forschungs- und Gebäudestufen folgen auf Grundlage verifizierter Tabellen. Die Bezeichnung „wie das Original“ verlangt deutlich mehr als bloß sichtbare Originalgrafiken.

## Primärquellen

| Kennung | Quelle | URL |
| --- | --- | --- |
| S1 | Godot: Using TileSets | https://docs.godotengine.org/en/stable/tutorials/2d/using_tilesets.html |
| S2 | UnityPy: offizielles Projekt-README | https://github.com/K0lb3/UnityPy/blob/master/README.md |
| S3 | AssetRipper: offizielles Projekt-README | https://github.com/AssetRipper/AssetRipper/blob/master/README.md |
| S4 | Godot: Exporting for Android | https://docs.godotengine.org/en/stable/tutorials/export/exporting_for_android.html |
| S5 | Godot: Exporting projects | https://docs.godotengine.org/en/stable/tutorials/export/exporting_projects.html |
| S6 | Unity: Install dependencies, Android | https://docs.unity.com/en-us/engine/6000.6/manual/platform-specific/android/getting-started/sdksetup/install-dependencies |
| S7 | Unity: IL2CPP Overview | https://docs.unity3d.com/cn/2022.3/Manual/IL2CPP.html |
| S8 | Unity: Introduction to runtime asset management | https://docs.unity3d.com/ja/current/Manual/assets-managing-introduction.html |
| S9 | Android: Access app-specific files | https://developer.android.com/training/data-storage/app-specific |
| S10 | Android: Access documents and other files from shared storage | https://developer.android.com/training/data-storage/shared/documents-files |
| S11 | GitHub: About large files on GitHub | https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github |
| S12 | GitHub: About releases | https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases |

Zusätzliche Implementierungsquellen: https://docs.godotengine.org/en/stable/tutorials/io/saving_games.html und https://docs.godotengine.org/en/stable/classes/class_json.html.
