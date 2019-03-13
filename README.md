I have created two separate files: one for table generation and other for data transfer

<h1>Python Database Table Replication:</h1>

Here is the code file: table_generation.py

Here are steps to run:
1. Download and extract chinook db from this link: 

	http://www.sqlitetutorial.net/sqlite-sample-database/

2. Copy chinook.db file on your system. Copy table_generation.py file also in same folder.
3. Install MS-SQL server from this link:

	https://www.microsoft.com/en-in/sql-server/sql-server-downloads

4. Create database in MS-SQL named as "testdb"
5. Run command from anaconda prompt:

	python table_generation.py -f sqlite:///chinook.db -t mssql+pymssql://username:password@hostname:port/testdb

6. Table will generate in MS-SQL database.

<h1>Python Database Data Replication:</h1>

Here is the code file: data_transfer.py

Here are steps to run:
1. Copy data_transfer.py also in same folder.
2. Run command from anaconda prompt:

	python data_transfer.py -f sqlite:///chinook.db -t mssql+pymssql://username:password@hostname:port/testdb

3. Data will transfer in tables in MS-SQL database.
