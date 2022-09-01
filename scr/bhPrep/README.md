
## bhPrep
Der Ordner `bhPrep` beinhaltet folgende Scripts: 
- `bhPrep.py` : Hauptscript 
- `bhUtils.py` : Befehle des Hauptscripts 
- `config.json` : Pfade und Kolonnenauswahl für `output`.csv-Tabellen 

`bhPrep` verwendet Bohrdaten aus GeoDIN, unterscheidet zwischen privaten, öffentlich zugänglichen und 2D Bohrdaten und speichert die Daten in csv-Tabelle mit den wichtigsten Informationen. Die einzelnen Schritte werden in einer log-Textdatei dokumentiert. 
- **Imports** : Die nötigen Module werden importiert. 
- **Load Configuration** : Definitionen der Variablen und dazugehörige Pfade
- **Load data** : Daten werden gelesen via MultiDataLoader und in Tabelle umgewandelt mit Modul `pandas`. Bei Dateiformaten wie .shp, .gpkg, .csv werden die Daten via SingleDataLoader als rawData ausgegeben. Dokumentation der geladenen Files im log-File im Ordner `output`. 
- **Display data** : Anzahl Zeilen (Indexnummern), Spalten, Infos über Datentypen und benötigter Speicherplatz werden gezählt und im Log-File protokolliert. 
- **Statistics** : Berechnungen zur Anzahl Layers pro Bohrung, Dokumentation dazu im log-File im Ordner `output`. 
- **Plot RAW data** : Diagramm der Anzahl Bohrungen pro Tiefenbereich und deren geographische Verteilung wird erstellt und als bh_raw_datum_uhrzeit.jpg gespeichert. Notiz dazu im log-File. 
- **Processing RAW data** : Kolonnen (Columns) werden alphabetisch geordnet, Linien (Lines) werden gemäss Kolonnen `SHORTNAME` und `DEPTHFROM` sortiert. `index` Kolonne wird hinzugefügt und ausgewählte Spalten-Inhalte systematisch gerundet. 
- **Export RAW data** : RAW data file wird als .csv exportiert und im log-File protokolliert. 
- **Process PRIVATE data** : Duplikate werden ausgeschlossen per Kolonne; anschliessend werden gleiche Linien ausgeschlossen und leere Linien übergangen. Die übrig gebliebenen Daten werden gezählt und protokolliert im log-File. 
- **Convert DataFrame to GeoDataFrame** : Sämtliche Daten werden zu `private_bh` benannt und zu einem GeoDataFrame in EPSG 2056 umgewandelt. Memory wird anschliessend wieder gelöscht. 
- **Plot PRIVATE data** : Schweizer Grenze mit 20km Bufferzone wird als Perimeter gesetzt und zusammen mit GeoDataFrame als Diagramm dargestellt. Diagramm wird gespeichert unter private_bh_datum_uhrzeit.jpg. Im Perimeter liegende Bohrungen (private_bh) werden als Clip zu EPSG 4326 umgewandelt und in neuer Kolonne gespeichert. 
- **Export PRIVATE data** : Kolonnen werden umgenannt gemäss config.json für Export und exportiert. Daten werden als private_bh_datum_uhrzeit.csv exportiert.  
- **Process PUBLIC data** : `private_bh` wird in `public_bh` umbenannt. 
- **Delete dataframe and free memory** : `private_bh` wird aus Memory gelöscht. Kolonnen `start` und `end` werden hinzugefügt. `public_bh` wird aufgesplittet gemäss Restriktionen. Layers mit Restriktionen (b und g) werden sortiert nach `DEPTHFROM` und gemäss `SHORTNAME` auf ein Layer gekürzt (Duplikate werden gelöscht, damit nur eine Schicht übrig bleibt). 
	g: Restricted unique data 
	b: Restricted until unique data 
	f: Non-restricted unique data 
	Tiefenangaben bei privaten Bohrungen werden mit `start` und `end` aus zuvor erstellten Spalten überschrieben.
	Details der privaten Bohrungen werden mit `Undefined` überschrieben. 
	Mit pd.concat werden die Bohrungen ohne Restriktionen (f) und die Bohrungen mit Restriktionen (b und g) wieder zusammengefügt. 
	Die nun nicht mehr gebrauchten Kolonnen `start` und `end` werden wieder gelöscht und die Daten im `public_bh` nach `SHORTNAME` und `DEPTHFROM` sortiert. 
- **Export PUBLIC data** : Daten werden als public_bh_datum_uhrzeit.csv exportiert. 
- **Process 2D data** : Kolonnennamen werden wieder zurückgesetzt; public_bh ist noch geordnet und kann darum einfach auf erste Schicht reduziert werden, um die Einträge für map.geo.admin.ch in 2D zu erhalten. URL wird generiert. Die resultierende Tabelle wird als bh_2D_datum_uhrzeit.csv exportiert. 


---


## bhPrep
The folder `bhPrep` contains the following scripts: 
- `bhPrep.py` : Main script 
- `bhUtils.py` : commands of the main script 
- `config.json` : paths and column selection for `output`.csv table

`bhPrep` uses drilling data from GeoDIN, distinguishes between private, public and 2D drilling data and stores the data in csv table with the most important information. The individual steps are documented in a log text file. 
- **Imports** : The necessary modules are imported. 
- **Load configuration** : Definitions of the variables and associated paths.
- **Load data** : Data is read via MultiDataLoader and converted into a table with the module `panda`. For file formats such as .shp, .gpkg, .csv, the data is output as rawData via SingleDataLoader. Documentation of the loaded files in the log file in the `output` folder. 
- **Display data** : Number of lines (index numbers), columns, information about data types and required storage space are counted and logged in the log file. 
- **Statistics** : Calculations of the number of layers per hole, documentation in the log file in the folder `output`. 
- **Plot RAW data** : Diagram of the number of boreholes per depth range and their geographical distribution is created and saved as bh_raw_datum_uhrzeit.jpg. Note in the log file. 
- **Processing RAW data** : Columns are sorted alphabetically, lines are sorted according to columns `SHORTNAME` and `DEPTHFROM`. The `index` column is added and selected column contents are systematically rounded. 
- **Export RAW data** : RAW data file is exported as .csv and logged in the log file. 
- **Process PRIVATE data** : Duplicates are excluded per column; then equal lines are excluded and blank lines are skipped. The remaining data is counted and logged in the log file. 
- **Convert DataFrame to GeoDataFrame** : All data are named `private_bh` and converted to a GeoDataFrame in EPSG 2056. Memory is then deleted again. 
- **Plot PRIVATE data** : Swiss border with 20km buffer zone is set as perimeter and displayed as diagram together with GeoDataFrame. Diagram is saved as private_bh_date_time.jpg. Boreholes lying in the perimeter (private_bh) are converted as a clip to EPSG 4326 and saved in a new column. 
- **Export PRIVATE data** : Columns are renamed according to config.json for export and exported. Data is exported as private_bh_date_time.csv.  
- **Process PUBLIC data** : `private_bh` is renamed to `public_bh`. 
- **Delete dataframe and free memory** : `private_bh` is deleted from memory. Columns `start` and `end` are added. `public_bh` is split according to restrictions. Layers with restrictions (b and g) are sorted by `DEPTHFROM` and shortened to one layer according to `SHORTNAME` (duplicates are deleted so that only one layer remains). 
	g: Restricted unique data 
	b: Restricted until unique data 
	f: Non-restricted unique data 
	Depth details of private boreholes are overwritten with `start` and `end` from previously created columns.
	Details of private boreholes are overwritten with `Undefined`. 
	With pd.concat the boreholes without restrictions (f) and the boreholes with restrictions (b and g) are concatenated again. 
	The columns `start` and `end`, which are now no longer used, are deleted again and the data in the `public_bh` are sorted by `SHORTNAME` and `DEPTHFROM`. 
- **Export PUBLIC data** : Data is exported as public_bh_date_time.csv. 
- **Process 2D data** : Column names are reset; public_bh is still sorted and can therefore simply be reduced to first layer to get the entries for map.geo.admin.ch in 2D. URL is generated. The resulting table is exported as bh_2D_datum_uhrzeit.csv. 
