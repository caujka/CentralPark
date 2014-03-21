# Technical spec


## Database

Table1: ParcingLot (Id_Lot, Name_Lot, Decribe, Adress);
Tabble2: ParcingPlace (Id_Lot, Id_place, Number)

## Dataflow

## Requests diagrams
Дані запиту оплати замовлення пересилаютсья на контролер, що формує запит у базу даних, створює новий запис у таблиці транзацій, створює транзакції, виконує її, передає відповідному темплейту необхідні дані та робить відповідь на запит. 
