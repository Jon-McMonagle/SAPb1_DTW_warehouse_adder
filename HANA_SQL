-- This is the query I run in SAP to extract items I want to edit the warehouse listing for.
-- You can also build your own excel file to load into the warehouse adder.

SELECT T0."ItemCode" as "Item", ROW_NUMBER() OVER(PARTITION BY T0."ItemCode" ORDER BY T0."ItemCode", T0."WhsCode") - 1 as "Line",
T0."WhsCode" as "Warehouse"

FROM OITW T0

WHERE T0."ItemCode" BETWEEN '[%0]' and '[%1]'

ORDER BY T0."ItemCode", T0."WhsCode"
