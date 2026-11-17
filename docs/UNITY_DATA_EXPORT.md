# Zusätzlicher Export der Unity-Data-Dateien

## Ergebnis und Reichweite

Der Export von `assets/bin/Data` ergänzt die separat bearbeiteten 317 UnityFS-Bundles. Er wurde mit UnityPy 1.25.4 und Pillow 13.0.0 aus dem wiedergefundenen Paket `Elvenar_Build02_04_Unity_Szenen_und_Ressourcen.zip` erstellt. Die SerializedFiles melden Unity 6000.0.71f1. Diese Zahlen sind historische Quellbefunde, keine neuen Spielwerte.

| Objektart | In der Quelle | Ausgegeben |
|---|---:|---|
| Sprite | 2.859 | 2.859 einzelne PNGs und Objektmetadaten |
| Texture2D | 2.611 | 2.604 PNGs, Metadaten aller 2.611 Objekte |
| AnimationClip | 345 | 345 vollständige Typbaum-JSONs |
| AnimatorController | 116 | 116 Typbaum-JSONs |
| AnimatorOverrideController | 3 | 3 Typbaum-JSONs |
| SpriteAtlas | 35 | 35 Typbaum-JSONs |
| Font | 6 | 6 eingebettete TTF-Dateien und Metadaten |
| AudioClip | 196 | 196 Metadatensätze; das eigentliche Audio liegt im gesonderten Audioexport |
| TextAsset | 44 | 28 freigegebene Nutzdateien, davon 9 bereinigt; 16 ausdrücklich zurückgehalten |
| Ausgewählte Grafikstruktur | 82.398 | In 963 JSON-Dateien nach Quelldatei zusammengefasst |

Die 7 Texture2D-Objekte ohne PNG enthalten bereits in der Quelle keine Pixel: sechs heißen `Font Texture`, eines `LiberationSans SDF Atlas`. Breite, Höhe und Stream-Größe sind jeweils null. `source_empty_textures.json` verweist auf die erhaltenen Metadaten. Sie sind keine fehlgeschlagenen Bildexporte.

Der finale Lauf hat **0 Exportfehler**. Sämtliche erzeugten PNGs wurden nach dem Speichern vollständig mit Pillow geladen. Alle sechs TTF-Dateien lassen sich durch FreeType laden. Eine zuvor im parallelen Zugriff fehlerhafte Stadtgrafik wurde außerdem visuell geprüft. Die Fontnamen sind Source Sans Pro Bold, Italic, Regular und Black sowie zweimal Liberation Sans in unterschiedlichen Quelldateien.

Der Medienindex umfasst 7.178 Zeilen. Das Hashmanifest erfasst 12.637 Dateien mit zusammen 361.203.923 Bytes, jeweils ohne die Manifestdatei selbst. Diese Zahlen gelten ausschließlich für diesen zusätzlichen Data-Export. Dateien aus dem UnityFS-Export, Android-PNGs und Audio sind darin nicht enthalten. Objektzahlen lassen keine Aussage über die Anzahl einzigartiger Gebäude zu; verschiedene Quellen können inhaltlich gleiche Darstellungen enthalten.

## Wiederholbarer Aufruf

Die Eingabe ist ein vollständiges, lokal vorhandenes Unity-Verzeichnis `assets/bin/Data`, einschließlich aller `.splitN`-Teile und abhängigen Ressourcen. Die freigegebenen Anforderungen aus `requirements-unitypy.txt` müssen zuvor installiert sein.

```bash
python tools/export_data_assets.py \
  --input /pfad/zur/privaten/eingabe/assets/bin/Data \
  --output /pfad/zur/ausgabe/assets/unity_data \
  --workers 4 \
  --approved-text-manifest tools/textasset_approval_index.json
```

Ohne `--approved-text-manifest` bleiben sämtliche TextAsset-Inhalte zurückgehalten. Der optionale Parameter `--review-text-dir` schreibt unbearbeitete TextAssets in einen ausdrücklich getrennten privaten Prüfordner und ist für den normalen Paketbau nicht erforderlich. Ein neues Ausgabeverzeichnis vermeidet alte, nicht mehr verwendete Dateien.

Die Bildverarbeitung lädt die Quelldateien vor dem Start der parallelen Prozesse als Bytes. Dadurch teilen Linux-Prozesse keine veränderlichen Dateipositionen. Dieser Punkt ist wesentlich: Ein früherer Zwischenlauf mit geteilten Datei-Handles erzeugte vorübergehende Parsefehler; dieselben unveränderten Quellen ließen sich nach der Korrektur vollständig lesen. Der endgültige Fehlerbericht ist leer.

## Dateien und Herkunft

Alle folgenden relativen Pfade beziehen sich auf `assets/unity_data/`:

| Datei oder Ordner | Bedeutung |
|---|---|
| `sprites/` | Einzelbilder, benannt nach Quelle, Quellhash, Objektname und Objekt-ID |
| `textures/` | Dekodierte Texturen, einschließlich Atlanten |
| `fonts/` | Eingebettete Original-Schriftdateien |
| `text_assets/` | Nur die 28 geprüften und gegebenenfalls bereinigten Inhalte |
| `metadata/` | Typbäume für Medien, Animationen und ausgewählte Grafikstruktur |
| `data_index.csv` | Objektidentität, Herkunft, Zielpfade, Status, Größe, Bildmaße und SHA-256 |
| `data_source_manifest.json` | Herkunft der 4.616 logischen SerializedFiles, einzelne physische Quelldateien, Split-Reihenfolge, Hashes und externe Unity-Dateiverweise |
| `data_summary.json` | Vollständige Objektzählung, Exportstatus und bewusst nicht exportierte Typen |
| `data_errors.json` | Fehlerliste; im geprüften Lauf leer |
| `animation_reference_catalog.json` | Überblick über 345 Clips und nachgewiesene Sprite-Pointer |
| `source_empty_textures.json` | Nachweis der 7 bereits leeren Quelltexturen |
| `SHA256_MANIFEST.json` | Ausschließlich die öffentlichen Dateien dieses Exports mit Größe und SHA-256 |

`data_index.csv` enthält die Spalten `source`, `source_sha256`, `source_content_sha256`, `serialized_file`, `unity_version`, `type`, `object_id`, `name`, `status`, `output_path`, `metadata_path`, `width`, `height`, `bytes`, `sha256` und `error`. Strukturdateien enthalten zusätzlich für jedes ihrer Objekte Typ, Objekt-ID, Name und Typbaum. Ihr Indexeintrag verwendet `StructuralMetadata` und `object_id=multiple`.

Bei zusammengefügten Unity-Split-Dateien bezeichnet `source` den logischen Dateinamen. `source_sha256` bezieht sich auf die Konkatenation `split0 + split1 + ...` in numerischer Reihenfolge. Die sieben betroffenen Dateiserien sind lückenlos vorhanden und im Quellenmanifest mit den Hashes aller physischen Teile dokumentiert. `external_files` ordnet die Unity-Datei-IDs ihren unveränderten Quellverweisen zu. Ein Unity-Pointer ist stets zusammen mit der jeweiligen SerializedFile zu interpretieren; eine Objekt-ID allein ist nicht global eindeutig.

## Animationen und verbleibende Entwicklungsarbeit

Der Clip `NHelp_fx_animation` enthält 20 Sprite-Pointer. Alle 20 sind auf konkrete exportierte PNGs aufgelöst. Die übrigen Data-Clips enthalten keine entsprechende Sprite-Pointertabelle; darunter befinden sich zahlreiche Animationen für Oberflächen, Transformationen und Effekte.

Die Pointertabelle ist keine bewiesene Bildfolge mit Zeitangaben. Die kompilierten Unity-Kurven, Bindungen, Abspielraten und verfügbaren Clip-Metadaten sind erhalten. Eine Godot-Timeline oder vollständige Rekonstruktion der Unity-Animator-Zustandslogik wurde hier nicht behauptet oder automatisch erzeugt. Dieser Import bleibt eine spätere Aufgabe bei der Neuentwicklung.

## Bewusste Inhaltsgrenzen

Die TextAsset-Freigabe bindet jede Veröffentlichung an den SHA-256 der Quelldatei, die Objekt-ID, den Hash der unbearbeiteten Nutzdaten und den erwarteten Hash der Ausgabe. Neun Spine-JSONs wurden ausschließlich um die freigegebenen Felder `skeleton.images` und `skeleton.audio` bereinigt. Dabei entfernte die Prüfung acht absolute Editorpfade. Die 19 anderen freigegebenen Inhalte sind unverändert. Die 16 ausgeschlossenen SDK-, Zertifikats-, Build- und Testinhalte werden als zurückgehalten protokolliert.

Es werden keine beliebigen MonoBehaviour-Felder exportiert. Die 45.620 gefundenen MonoBehaviour-Objekte sowie Unity-Shader, allgemeine Player-/Build-Einstellungen und weitere nicht übernommene Typen sind in `data_summary.json` gezählt. Die ausgegebene Grafikstruktur besteht aus GameObject, Transform, RectTransform, SpriteRenderer, Animator, CanvasRenderer, Canvas, CanvasGroup, Animation, Material, ParticleSystem und ParticleSystemRenderer. Vollständige Spielskripte, Forschungsregeln, Kosten oder Produktionsrezepte entstehen dadurch nicht.

Für die Paketintegration werden ausschließlich `files[].path` aus `SHA256_MANIFEST.json` und die Manifestdatei selbst kopiert. Prüfordner wie `textassets_private/` oder `textassets_approved/` gehören nicht zum Medienpaket. Die unbearbeiteten Quellen verbleiben in der privaten Eingabe, damit entfernte Editorpfade und zurückgehaltene TextAssets nicht über eine zusätzliche Rohkopie wieder in die Ausgabe gelangen.
