# Big Data Analytics Project

## Database Connection - Necessary!!!
```bash
# install drivers
pip install psycopg2-binary python-dotenv
```
Check **.env** in project root (with correct credentials) exists.

The main.py attempts a Database connection on start. If the connection fails the program exits.

## Setting up Database Schema
This is **useful** for testing and writing sql-queries!

For the next steps use the credentials from the **.env** file in your project root.
1) In **DataGrip** or PyCharm (**DataGrip** preferred) click on the Plus - chose Data Source - chose **PostgreSQL**
2) For **Host** use **PGHOST**
3) For **Port** use **PGPORT**
4) For **User** use **PGUSER**
5) For **Password** use **PGPASSWORD**
6) For **Database** use **PGDATABASE**
7) Open the **SSH/SSL** tab
8) Check **Use SSL**
9) Set **Mode** to **Require**
10) Click **Test Connection** and then **OK**

Now you can test around and write sql-queries!
