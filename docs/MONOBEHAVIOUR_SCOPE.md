# Begrenzte semantische Prüfung der MonoBehaviour-Objekte

Prüfdatum: 17.11.2026. Quelle ist Paket 04, `assets/bin/Data`. `data/reference/monobehaviour_scope.json` enthält Archivhash, Prüfumfang, Klassenzählung sowie technische Referenzen der erkannten benannten Konfigurationsobjekte. Für direkt vorliegende serialisierte Dateien sind zusätzlich Datei-Hashes enthalten. Die ursprünglichen Quelldateien bleiben unverändert.

## Belastbares Ergebnis

Alle **45.620 MonoBehaviour-Header** wurden ohne Lesefehler geprüft. Über die zugehörigen MonoScript-Verweise wurden **45.617 Instanzen insgesamt 1.351 Scriptklassen** zugeordnet. Bei drei Instanzen blieb die Klasse mit der verwendeten Referenzauflösung offen. Zusätzlich wurden 9.798 MonoScript-Definitionen gelesen. Eine Klassendeklaration allein wurde nicht als vorhandene Spieldatentabelle gewertet.

Bereits **34.844 Instanzen** gehören zum Namensraum `UnityEngine.UI`, etwa Image, Text, LayoutElement und Button. Weitere zahlreiche Klassen sind eigene UI-Komponenten, Tooltips, Fenster und Mediatoren. Damit ist der große Objektbestand überwiegend eine Quelle für Darstellung und Clientstruktur.

Der Filter `Config|Definition|Balance|Research|Technology|Production|Building|Cost|CityEntity` identifizierte **138 Kandidatenklassen mit 501 Instanzen**. Für eine Instanz je Kandidatenklasse wurde ein vollständiger TypeTree-Leseversuch durchgeführt. 14 Exemplare ließen sich vollständig lesen, enthalten jedoch ausschließlich die vier Unity-Basisfelder `m_GameObject`, `m_Enabled`, `m_Script` und `m_Name`. Bei den übrigen 124 Exemplaren reichen die verfügbaren Typinformationen nicht zur vollständigen Dekodierung der individuellen Nutzdaten: UnityPy konnte nur den Basisbereich lesen, nicht die gesamte Objektlänge.

**Dies ist keine vollständige semantische Dekodierung aller 45.620 Objekte.** Insbesondere ist die Aussage, im übrigen Datenbestand seien sicher keine Wirtschafts- oder Forschungsdaten vorhanden, durch diesen Überblick nicht belegt.

## Konkrete Datenkandidaten

Die folgenden Klassen besitzen tatsächlich ein benanntes serialisiertes Objekt. Das sind gezielte Anknüpfungspunkte für eine spätere Typrekonstruktion. Die Namen belegen die Existenz der Objekte; Kosten, Einheitenwerte, Forschungskanten oder andere Nutzdaten sind dadurch noch nicht validiert.

| Instanzierte Klasse | Serialisierte Quelldatei | Objekt-ID | Bytes |
|---|---|---:|---:|
| `Onyx.Engine.Effects.BuildingOutlineGlowSettings` | `sharedassets3.assets` | 239 | 144 |
| `Onyx.Game.SharedModel.Units.Data.UnitClassDefinitions` | `3ad369655591d40418316377e6346ce2` | 1 | 456 |
| `Onyx.ScriptableObjects.Rarities.RarityDefinitions` | `00796b5659fd7477182a6a4b89fb14e5` | 1 | 756 |
| `Onyx.Game.PremiumShop.View.CashShopGroupConfig.CashShopGroupConfig` | `eb2426e33b82745eb826be720f0e7bb9` | 1 | 176 |
| `Onyx.Game.HUD.Mediator.SidePanel.Configuration.SidePanelConfiguration` | `a7c83bc30a402428c8f064fe0dd06352` | 1 | 736 |
| `Onyx.Game.City.Weather.WeatherEffectObjectsConfiguration` | `9e7118cac7ea1499d9f5e5f024b5557f` | 1 | 96 |
| `Onyx.ShopHighlightConfig` | `8a64b05d0a7ea43ab9aebc82513cbdd2` | 1 | 76 |
| `Onyx.ScriptableObjects.ConsentManagement.ConsentManagementConfig` | `af53aa5d615a74e4fab4a6401494a84f` | 1 | 76 |

`UnitClassDefinitions` und `RarityDefinitions` sind die deutlichsten Kandidaten für kleine fachliche Definitionen. Aus ihren Namen folgt kein vollständiger Einheitenkatalog. Die übrigen Namen deuten überwiegend auf Darstellung, Wetter, Shop oder Einwilligungsinfrastruktur. Das ist eine begrenzte Einordnung anhand der Typnamen, keine Rekonstruktion ihrer Werte.

Die gefundenen Klassen `TechTreeTechnologyView`, `TechTreeTechnologyMediator`, `TechTreeTechnologyConnectionsView` und `ResearchWindowMediator` belegen die ursprüngliche Forschungsoberfläche. Sie belegen keinen vollständig ausgelesenen Technologiegraphen. Entsprechend belegen ProductionView-, Component- und Tooltip-Klassen keine vollständigen Produktionsrezepte.

## Grenze und nächster sinnvoller Schritt

Vollständige Gebäudekosten, Produktionsrezepte und Forschungsvoraussetzungen bleiben **OFFEN**. Für die genannten benutzerdefinierten Datenobjekte wäre als gesonderter Untersuchungsschritt zuerst eine passende Typstruktur aus verifizierten Assembly- oder IL2CPP-Metadaten erforderlich. Danach wären einzelne Objekte feldweise zu dekodieren, auf private Informationen zu prüfen und erst anschließend fachliche Tabellen abzuleiten. Ohne passende Struktur werden keine Binärzahlen als Preise, Zeiten oder andere Originalwerte interpretiert.

Der separat bestätigte Exporterfolg für Grafiken, Audio und andere unterstützte Assettypen ist davon unabhängig. Keine Fehler bei diesen Exporten bedeutet keine vollständige Dekodierung der Spiellogik oder sämtlicher MonoBehaviour-Nutzdaten.

Es wurden ausschließlich Typnamen, technische Referenzen, Objektgrößen, Zählwerte und Basisfeldnamen in diesen Bericht übernommen. Vollständige Rohobjekte und individuelle Nutzdaten wurden nicht veröffentlicht. Es gab keine Anfragen an Spielserver.
