## xmlPrep
Das Python-Script `Replacements_in_xml` liest eine xml Datei und entschlüsselt ihre hierarchische Auffächerung in einen Objektbaum mit den Modulen `lxml.tree` und `xml`. Hierbei anzumerken gilt, dass im Modul `xml` einfach auf spezifische Elementnamen gewechselt werden kann, Kind-Eltern Beziehungen aber nur im `lxml` abgerufen werden können. Im Ordner befindet sich ebenfalls die GeolCode Liste mit alphanumerischen, sowie dazugehörigem numerischen Code ( `ReplaceList_UUID.xlsx`).
- **Generating UUID** : Excel-Liste wird eingelesen, indexiert und als Liste formatiert. Neue Kolonne mit UUID wird angehängt und Excel exportiert. 
- **Reading input files** : Bereits vorbereitetes Excel mit UUIDs und xml-Datei werden eingelesen.
- **Replace GeolCode: Alphanumeric to numeric** : Mit Modul `xml` wird nach GeolCode gesucht und dessen Text gemäss Excel-Liste mit numerischen Code ersetzt. 
- **Replace TID: alphanumeric to UUID** : Mit Modul `lxml` wird nach GeolCodes gesucht. Mittels der Funktion element.getparent() kann das Attribut `TID` im Parent-Element mit der UUID aus dem Excel-File ersetzt werden. 
- **Replace REF: alphanumeric to UUID** : Die Werte der Tabellen Lithologie, Lithostrat, Tecto und Chrono werden mit Parent-IDs verlinkt. Diese müssen mit den neu generierten UUIDs ersetzt werden. Mit dem Modul `xml` können alle `Parent`-Attribute gesucht werden und die Attribute `REF` ersetzt werden. 

---

The Python script `Replacements_in_xml` reads an xml file and decodes its hierarchical fan-out into an object tree with the modules `lxml.tree` and `xml`. It should be noted that in the `xml` module it is easy to switch to specific element names, but child-parent relationships can only be retrieved in the `lxml`. The folder also contains the GeolCode list with alphanumeric and numeric codes (`ReplaceList_UUID.xlsx`).
- **Generating UUID** : Excel list is read in, indexed and formatted as a list. New column with UUID is appended and Excel exported. 
- **Reading input files** : Excel already prepared with UUIDs and xml file are read in.
- **Replace GeolCode: Alphanumeric to numeric** : The module `xml` is used to search for GeolCode and its text is replaced with numeric code according to the Excel list. 
- **Replace TID: alphanumeric to UUID** : The module `lxml` is used to search for GeolCodes. Using the function element.getparent(), the attribute `TID` in the parent element can be replaced with the UUID from the Excel file. 
- **Replace REF: alphanumeric to UUID** : The values of the tables Lithology, Lithostrat, Tecto and Chrono are linked with Parent-IDs. These must be replaced with the newly generated UUIDs. With the module `xml` all `Parent` attributes can be searched and the attributes `REF` can be replaced. 
