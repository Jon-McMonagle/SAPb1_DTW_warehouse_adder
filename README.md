Add_Warehouses is a program that takes a 3 column excel (csv or xlsx) file in the format: Item | Line | Warehouse.
Example: 
Item    Line  Warehouse
Test1   0     Main
Test1   1     Extra
Test2   0     Main
Test2   1     Extra

It will then ask the user to input a space separated list of warehouses you would like to add to these items.
Example: Proxy Remote
End result:
Test1   0     Main
Test1   1     Extra
Test1   2     Proxy
Test1   3     Remote
Test2   0     Main
Test2   1     Extra
Test2   2     Proxy
Test3   3     Remote

This end result file can be uploaded into SAP B1's data transfer workbench under Inventory > Item Warhouse Info.

The SQL code is for SAP HANA and will extract the necessary information to put into an excel file that can then be processed by the Python program.

Future updates:
- The python program currently will duplicate warehouses if an item already has the warehouse you are trying to add. This will be fixed.
