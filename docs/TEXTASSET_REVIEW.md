# Prüfung der 44 zusätzlichen Unity-TextAssets

Prüfdatum: 17.11.2026. Quelle: `Elvenar_Build02_04_Unity_Szenen_und_Ressourcen.zip`, ursprüngliche Dateien unter `assets/bin/Data/`. Alle 44 TextAssets wurden über ihre serialisierte Quelldatei und Objekt-ID identifiziert, vollständig gelesen und geprüft. Die 44 Quelldatei-Hashes stimmen mit dem ursprünglichen Build-02-Assetinventar überein.

## Ergebnis

**28 Nutzdateien sind freigegeben, 16 Infrastruktur- oder Entwicklungsdateien ausgeschlossen.** Keine vollständige Gebäudekostentabelle, keine Produktionsrezepttabelle, kein vollständiger Forschungsbaum und keine Übersetzungstabelle wurden in diesen 44 TextAssets gefunden. Die zuvor dokumentierten Lücken bleiben bestehen.

| Freigegebener Inhalt | Dateien | Bedeutung |
|---|---:|---|
| Spine-Skelettdaten | 9 | Knochen, Slots, Skins und zusammen 23 benannte Animationen. Zwei Dateien heißen `gp_won`, besitzen aber unterschiedliche Quellen und Inhalte. |
| Spine-Atlanten | 9 | Texturbereiche und Seiten für die zugehörige Darstellung. |
| Audiokonfigurationen | 6 | Zusammen 214 Einträge für Audioreferenzen und Ereigniszuordnung. Eine Datei ist eine leere Liste. |
| Audio-Mix-Einstellungen | 1 | Numerische Lautstärken und Verzögerungen für Stadt, Kampf, Weltkarte und UI. |
| Visuelles Manifest | 1 | Bereits bekannte Assetzuordnung; keine neue Wirtschaftstabelle. |
| Zeilenumbruch-Zeichensätze | 2 | Führende und folgende Zeichen für Textumbruch, keine Lokalisierungstexte. |

Die Datei `city-collect-buildings-sounds.asset` besitzt 203 Einträge. Diese beschreiben Soundereignisse und Referenzen. Sie belegen keine zusätzlichen vollständigen Gebäudedefinitionen, Baukosten, Laufzeiten oder Erträge.

Die Spine-Dateien enthalten Darstellungsdaten im ursprünglichen Format. Ihre tatsächliche Wiedergabe in Godot ist noch zu integrieren und zu prüfen. Das Vorliegen einer Animation ist kein Beleg für eine fertige Godot-Animationsszene. Die Herkunft und Nutzungsbedingungen der Originalressourcen bleiben getrennt von neuem Projektcode.

## Bereinigung

19 freigegebene Dateien werden byteidentisch ausgegeben. Neun Spine-JSON-Dateien werden kontrolliert bereinigt: ausschließlich die Felder `skeleton.images` und `skeleton.audio` mit Pfaden zur ursprünglichen Editorumgebung werden entfernt. Acht der gefundenen Pfadwerte waren absolute lokale Pfade. Die übrigen Grafik- und Animationsdaten werden unverändert übernommen; nach der definierten JSON-Serialisierung wird der Ausgabehash geprüft.

Die ausgeschlossenen Inhalte sind:

- Drei Objekte der `ClientCredentials`-Familie. Datenbank und Metadaten waren leer; auch der Hashdatensatz wird nicht benötigt.
- Sechs Objekte mit TLS-Zertifikatsdatenbanken, zugehörigen Metadaten oder Hashes.
- Sechs weitere Build-, Modulversions- oder Testeinstellungsobjekte.
- `PerformanceTestRunInfo` mit Hardware-/Gerätenamen und Editor-/Buildmetadaten.

Es wurden keine Inhalte dieser ausgeschlossenen Objekte in öffentliche Ausgabedateien kopiert. Die Freigabeliste enthält ihre technische Identität, Größe, Hashwerte und den Ausschlussgrund, keine Gerätekennungen, Pfadwerte, Geheimnisse oder Rohinhalte.

## Reproduktion

`tools/textasset_approval_index.json` ist die geprüfte Freigabeliste. Sie bindet jede Entscheidung an den Hash der serialisierten Quelldatei, die Unity-Objekt-ID und den Hash der TextAsset-Nutzdaten. Für freigegebene Dateien sind außerdem erlaubte Transformationen und erwartete Ausgabehashes festgelegt.

Der unabhängige Exporthelper liest alle 44 Objekte frisch aus den Eingangsdateien:

```sh
python tools/export_textassets_reviewed.py \
  --source-dir INPUT/assets/bin/Data \
  --output-dir OUTPUT/textassets
```

`INPUT` bezeichnet das entpackte verifizierte Quellenverzeichnis, `OUTPUT` einen neuen Ausgabeort. Der Helper verwendet UnityPy aus der Exportumgebung. Er führt keine Netzwerkabfragen aus und schreibt keine ausgeschlossenen TextAsset-Inhalte. Er verweigert unerwartete Quellbytes, Namen, Objekt-IDs, Transformationen und Ausgabehashes. Vorhandene Zieldateien werden nicht überschrieben.

Dieser Reproduktionslauf wurde mit den echten Quelldateien ausgeführt: **44 Quellen geprüft, 28 Ausgaben erstellt, 16 ausgeschlossen, alle erwarteten Ausgabehashes exakt reproduziert.** Der erzeugte `TEXTASSET_EXPORT_REPORT.json` dokumentiert den Lauf. Der Haupt-Assetexporter kann dieselbe Freigabeliste alternativ über `--approved-text-manifest` verwenden; die Buildpipeline soll einen Exportweg wählen.

## Abdeckung

Die Prüfung erfasst sämtliche 44 inventarisierten TextAssets. Sie ersetzt keine semantische Analyse aller übrigen MonoBehaviour-Objekte oder des nativen Originalcodes. Unbekannte Originalregeln bleiben deshalb OFFEN. Neue Sound- und Animationszuordnungen verbessern die Darstellung des Nachbaus, schließen aber die fehlende Wirtschafts- und Forschungsdatenlage nicht.
