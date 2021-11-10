Der Ordner "bhPrep" beinhaltet folgende Scripts: 
- bhPrep.py : Hauptscript 
- bhUtils.py : Befehle des Hauptscripts 
- config.json: Pfade 

"bhPrep" verwendet Bohrdaten aus GeoDIN, unterscheidet zwischen privaten, öffentlich zugänglichen und 2D Bohrdaten und speichert die Daten in csv-Tabelle mit den wichtigsten Informationen. Die wichtigsten Schritte werden in einer log-Textdatei dokumentiert. 
- Imports: Die nötigen Module werden importiert. 
- Load Configuration: Definitionen der Variablen und dazugehörige Pfade
- Load data: Daten werden gelesen via MultiDataLoader und in Tabelle umgewandelt mit Modul "panda". Bei Dateiformaten wie .shp, .gpkg, .csv werden die Daten via SingleDataLoader als rawData ausgegeben. Dokumentation der geladenen Files im log-File im Ordner "output". 
- Display data: 
- Statistics: Berechnungen zur Anzahl Layers pro Bohrung, Dokumentation dazu im log-File im Ordner "output". 
- Plot RAW data: Diagramm der Anzahl Bohrungen pro Tiefenbereich und deren geographische Verteilung wird erstellt und als bh_raw_datum_uhrzeit.jpg gespeichert. Notiz dazu im log-File. 
- Processing RAW data: Kolonnen (Columns) werden alphabetisch geordnet, Linien (Lines) werden gemäss Kolonnen "SHORTNAME" und "DEPTHFROM" sortiert. "index" Kolonne wird hinzugefügt und ausgewählte Spalten-Inhalte systematisch gerundet. 
- Export RAW data: RAW data file wird als .csv exportiert und im log-File protokolliert. 
- Process PRIVATE data: Duplikate werden ausgeschlossen per Kolonne; anschliessend werden gleiche Linien ausgeschlossen und leere Linien übergangen. Die übrig gebliebenen Daten werden gezählt und protokolliert im log-File. 
- Convert DataFrame to GeoDataFrame: Sämtliche Daten werden zu "private_bh" benannt und zu einem GeoDataFrame in EPSG 2056 umgewandelt. Memory wird anschliessend wieder gelöscht. 
- Plot PRIVATE data: Schweizer Grenze mit 20km Bufferzone wird als Perimeter gesetzt und zusammen mit GeoDataFrame als Diagramm dargestellt. Diagramm wird gespeichert unter private_bh_datum_uhrzeit.jpg. Im Perimeter liegende Bohrungen (private_bh) werden als Clip zu EPSG 4326 umgewandelt und in neuer Kolonne gespeichert. 
- Export PRIVATE data: Kolonnen werden umgenannt gemäss config.json für Export und exportiert. Daten werden als private_bh_datum_uhrzeit.csv exportiert.  
- Process PUBLIC data: "private_bh" wird in "public_bh" umbenannt. 
- Delete dataframe and free memory: "private_bh" wird aus Memory gelöscht. Kolonnen "start" und "end" werden hinzugefügt. "public_bh" wird aufgesplittet gemäss Restriktionen. Layers mit Restriktionen (b und g) werden sortiert nach "DEPTHFROM" und gemäss "SHORTNAME" auf ein Layer gekürzt (Duplikate werden gelöscht, damit nur eine Schicht übrig bleibt). 
	g: Restricted unique data 
	b: Restricted until unique data 
	f: Non-restricted unique data 
	Tiefenangaben bei privaten Bohrungen werden mit "start" und "end" aus zuvor erstellten Spalten überschrieben.
	Details der privaten Bohrungen werden mit "Undefined" überschrieben. 
	Mit pd.concat werden die Bohrungen ohne Restriktionen (f) und die Bohrungen mit Restriktionen (b und g) wieder zusammengefügt. 
	Die nun nicht mehr gebrauchten Kolonnen "start" und "end" werden wieder gelöscht und die Daten im "public_bh" nach "SHORTNAME" und "DEPTHFROM" sortiert. 
- Export PUBLIC data: Daten werden als public_bh_datum_uhrzeit.csv exportiert. 
- Process 2D data: Kolonnennamen werden wieder zurückgesetzt; public_bh ist noch geordnet und kann darum einfach auf erste Schicht reduziert werden, um die Einträge für map.geo.admin.ch in 2D zu erhalten. URL wird generiert. Die resultierende Tabelle wird als bh_2D_datum_uhrzeit.csv exportiert. 