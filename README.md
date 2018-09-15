# 2400Lab
## Task1: Import CSV Files into PostgreSQL
The first lab is designed to let students learn how to import outfiles into databases.

### 1) Link to the Partch
We need to use partch to execute the whole lab. 

In **Linux**:

Open the terminal and use command

    ssh u1234567@partch.anu.edu.au

to log in the partch.

</br>

Then input your password, and you can link to the partch

</br>

### 2) Download the Data
Then, you need to download the files to your computer. 

You can use the `git` commands:

In **Partch Shell**:

1. Use commands `mkdir <directory name>` to make a directory storing the data, for example, `mkdir 2400lab`
2. Use `cd <directory name>` to enter the directory
3. Use `git clone https://github.com/sjmsjmdsg/2400Lab.git` to download the data to your directory 

The whole file is about 500MB.

</br>

### 3) Load Data to PostgreSQL
To load the data, we first use `psql` to enter the database. Then, we need to create tables for loading csv files in to the database, so we should firstly create a new table named *basics*, the schema is shown below:

|Column|Type|
|------|------|
| tconst         | character varying(50)   |
| titletype      | character varying(20)   |
| primarytitle   | character varying(600)  |
| originaltitle  | character varying(600)  |
| isadult        | boolean                 |
| startyear      | smallint                |
| endyear        | character varying(10)   |
| runtimeminutes | character varying(10)   |
| genres         | character varying(20)[] |

with primary key *tconst*

Then we create a table named *ratings*, the schema is shown below:

|Column|Type|
|------|------|
| tconst        | character varying(50) |
| averagerating | numeric(3,1)          |
| numvotes      | integer               |

with primary key *tconst*

**Note**: If you don't know how to create those two table, the answer is in the [answer](https://github.com/sjmsjmdsg/2400Lab/blob/master/answer/answer.txt) file.

Finally, we can use `\copy` command to load the csv files into the table. An example could be:

    \copy ratings from '~/comp2400lab/data/ratings.csv' delimiter ',' CSV Header;

You can find more specific details about `copy` command [here](https://www.postgresql.org/docs/9.2/static/sql-copy.html)[1]

</br>

## Task2: Check Functional Dependencies
The second lab is to learn about functional dependencies.

There is a simple python program named *FDchecker.py*, you should clone or download it to your computer (not the partch server).

**Note**: it can only run under python3 rather than python2.

In the linux terminal/cmd.exe, use command `python3` to run it, the specific command is:

    python3 FD_checker.py [-p <path>] num,num...-num,num...
    
For example,

    python3 FD_checker.py -p D:\Downloads\title.ratings.tsv\ratings.csv 1,2-3
    
This will let program find csv file in the giving path and try to check whether the column 1 and 2 can decide column or not.

You can change the default path in the program, so that you don't need to enter the path every time，the default path is oriented to the basics table in the data file.

It allows user to input several times, input `exit` to exit.

## Task3: Query Processing and Optimisation
The third lab is to learn about index.

Through psql documentation, index is a method that can improve the searching speed of database []. Basically, the index will let database management system stores the disk address or data itself in special structure that can save the time of reading info from disk. Without index, the DBMS has to search the data by sequence so it will be very slow when searching the data among millions of rows. Through psql document, by default, the `CREATE INDEX` command will create B-tree index, but it also supports many other structures, which can be check [here](https://www.postgresql.org/docs/9.2/static/indexes-types.html) [].  Meanwhile, because index requires data storing in structure, it will also decrease the performance of inserting/updating/deleting the rows. We will try to see the effect of index in the following lab.

### 1) Searching Operation

In this part, we will see the effect of index in searching.

First, use `\timing` command to open the timer, so you can see the sql operation time now. You can type it again to close the timer.

Second, let's create an index. You can use following command to create an index. 

    CREATE [ UNIQUE ] INDEX [ CONCURRENTLY ] [ name ] ON table [ USING method ]
        ( { column | ( expression ) } [ COLLATE collation ] [ opclass ] [ ASC | DESC ] [ NULLS { FIRST | LAST } ] [, ...] )
        [ WITH ( storage_parameter = value [, ... ] ) ]
        [ TABLESPACE tablespace ]
        [ WHERE predicate ]
        
In this part, we first create an index on `genres` attribute of table basics. It is varchar[] type and the content is long, so we can see the effect of index clearly. For example:

    CREATE INDEX ON basics(genres);
    
Since the DBMS has to generate the specific data format for storing data, this process can spend some time. 

Then we use the following command to search amount of rows that genres is '{Action,Adventure,Animation}':

    SELECT COUNT(genres) FROM basics WHERE genres = '{Action,Adventure,Animation}';
    
How much time does DBMS need to search the result? Remember that time.

Now let's drop the index. using the following command:

    DROP INDEX [ IF EXISTS ] name [, ...] [ CASCADE | RESTRICT ]

First, we need to search the *name* of the index we just created, we can use `\d` command.

    \d basics
    
By default, the name of index is "table_name + attr_name + idx", so here the index name can be "basics_genres_idx". We just drop it:

    DROP INDEX basics_genres_idx;
    
Now, let's do the same searching again. Could you find the difference between two times? This table is small, assume we have a table will millions of rows that needs about an hour to search an outcome, how much time do we need after using index? 

**Extra Info:** we can use command `EXPLAIN ANALYZE` to anslyse the process:

    EXPLAIN ANALYZE SELECT COUNT(startyear) FROM basics WHERE startyear < 2009;
    
Then we may see a tree structure like below:

      Finalize Aggregate  (cost=23503.24..23503.25 rows=1 width=8) (actual time=187.940..187.940 rows=1 loops=1)
       ->  Gather  (cost=23503.02..23503.23 rows=2 width=8) (actual time=187.932..187.937 rows=3 loops=1)
             Workers Planned: 2
             Workers Launched: 2
             ->  Partial Aggregate  (cost=22503.02..22503.03 rows=1 width=8) (actual time=100.149..100.149 rows=1 loops=3)
                   ->  Parallel Seq Scan on basics  (cost=0.00..21903.18 rows=239936 width=2) (actual time=0.095..89.823 rows=193081 loops=3)
                         Filter: (startyear < 2009)
                         Rows Removed by Filter: 120338
     Planning time: 0.079 ms
     Execution time: 205.960 ms
     
This command can show the sql executing process from bottom to top. From *actual time* column, we can see the executing time in ms. If you see *Parallel Seq Scan*, that means the index is not used. If you see *Index Cond*, that means index is used.

### 2) Insert/Delete Operation

In this part, we will see the effect of insert/delete rows of index.

You can find a file named *insert_delete.sql*, it is PL/pgSQL code which can insert and delete 100,000 rows to the basic. For the details of PL/pgSQL code, you can find info [here](https://postgres.cz/wiki/PL/pgSQL_(en)#Introduction_into_PL.2FpgSQL_language) []. However, it is not included in this course.

Now, lets move all the indexes, and type `\i insert/delete.sql`. Remember the execute time.

Then, we add index to attribute `genres`, and execute the code again. Does the insert/delete time change?

Finally, we add another index to attribute `titletype`, and execute the code again. Does the insert/delete time change again?

From the experiment above, we can see that index will slow the insert/delete process for it should maintain the index structure when the insert operation is executed. This will consume extra time.

Consequently, using index when it can truly improve the performance of the database operation, like when the table size is large and searching sql is required a lot!

### 3） Multiple Indexes

In this part, we will try to see how multiple indexes are different from single index.

Now, drop all the indexes and create a multi-indexes on basics's attributes `genres` and `titletype`:

    CREATE INDEX ON basics(genres, titletype);
    
Now, try to execute five commands below:

    EXPLAIN ANALYZE SELECT * FROM basics WHERE genres = '{Animation,Short}' AND titletype = 'short';

    EXPLAIN ANALYZE SELECT * FROM basics WHERE genres = '{Animation,Short}';

    EXPLAIN ANALYZE SELECT * FROM basics WHERE titletype = 'short';

    EXPLAIN ANALYZE SELECT * FROM basics WHERE titletype = 'short' AND genres = '{Animation,Short}';
    
    EXPLAIN ANALYZE SELECT * FROM basics WHERE genres = '{Animation,Short}' OR titletype = 'short';
    
Which sql uses index and which are not?

In fact, for the multi-indexes like above, the index of titletype is dependent on the index of genres. Thus, the index of genres can work along but index of titletype cannot.

Then, how about to create two independent indexes for the two attributes? 

Now, let's drop the multi-indexes above and create two indexes on the two attributes independently. Then, execute the above 5 commands again. What happened now?

Through the psql documentation, the multiple indexes have lots of limits []. The first one is what we have mentioned. The multi-indexes (x, y) cannot work when you want to just search under condition y. When you search the info under condition x, because multi-indexes (x, y)'s structure is complex than the single index, so it is still slower compared to use single index x. Besides, multi-indexes (x, y) cannot work under `OR` operation, but psql can combine single indexes x and y to do that. However, if your searching operations are mainly about both x and y, then multiple indexes are more effecient than the two single indexes. You can find more details [here](https://www.postgresql.org/docs/10/static/indexes-bitmap-scans.html).

Therefore, you should consider your tasks and index conditions before you set up the index!

## Task4: Use SQL to Answer Simple Questions

## Reference


