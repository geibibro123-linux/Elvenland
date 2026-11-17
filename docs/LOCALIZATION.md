# Elvenland: extrahierte Sprachdaten

Die 20 im Originalmanifest aufgeführten UnityFS-Bundles wurden mit UnityPy gelesen. Sie enthalten jeweils eine LocalizationDataCollection als MonoBehaviour, keine TextAsset-Objekte. Alle 20 Sprachfassungen und sämtliche Übersetzungsvarianten bleiben erhalten.

`localization_index.json` nennt Quellen, Hashes, Ausgaben und Eintragszahlen. Ausgabepfade sind relativ zu diesem Verzeichnis, im Gesamtpaket `assets/localization/`. `locales/` enthält lesbare Schlüssel-/Werteinträge; `metadata/` die unverändert interpretierten Typbäume. `reference_tables/de_de_key_values.json` und `reference_tables/en_dk_key_values.json` sind kompakte deutsche und englische Referenztabellen. Der Original-Sprachcode `en_dk` wird bewahrt.

Jede Sprache enthält 2.787 Schlüssel. Neun Schlüssel besitzen mehrere Übersetzungsvarianten; die Auswahlregel wurde nicht rekonstruiert. Varianten nicht still auf den ersten Text reduzieren. `de_en_topic_index.json` enthält nur lexikalisch ausgewählte Textbelege zu Forschung, Gebäuden, Produktion und Kampf. Diese Texte sind keine vollständigen Tabellen für Technologien, Abhängigkeiten, Preise oder Produktionsrezepte. Platzhalter wie `%s` und `%d` bleiben erhalten.

Das ursprüngliche Manifest bleibt bytegleich erhalten. Seine CDN-Adresse ist ein Herkunftshinweis; dieser Export hat sie nicht aufgerufen und der Offline-Neubau benötigt sie nicht.
