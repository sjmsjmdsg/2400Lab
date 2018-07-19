# 2400Lab
## 1.Import CSV Files into PostgreSQL
The first lab is designed to let students learn how to import outfiles into databases.
### Download the Data
First, you need to download the files to your computer. 

You can either:

Use the green **Download** button in the top right corner;

Or use the `git` commands:

1. Click the **Windows** button in the bottom left corner in your computer, and find the **search** button
2. Search **CMD**, which represents command prompt, and press enter, this will open the cmd.exe, which will help you transform the data to the partch server.
3. In the cmd.exe, use commands `mkdir <directory name>` to make a directory storing the data
4. Use `cd <directory name>` to enter the directory
5. Use `git clone <url>` to download the data to your directory
  
### Link to the Partch
We need to use partch to use the database. To load the data to the PostgreSQL, you need to:

1. Search the **putty** in the search window, which is introduced in the last step, and open the PuTTY.exe, which can help you establish a ssh connection between your computer and the partch server.
2. In the HostName blank, enter your student ID: *u1234567@partch.anu.edu.au*, choose SSH for connection type, click *open*

Then input your password, and you can link to the partch

### Load Data to PostgreSQL
To load the data, we first need to copy the data to the partch server. To do this, you can:

- Use the `git` commands introduced before in the putty command window to clone the files to the server

Or:

- Open cmd.exe, enter command:

      pscp <path stored csv data> u1234567@partch.anu.edu.au:<path in the server that you want to store the data>

    For example: 

      pscp D:\2400Lab\data\basics.csv u1234567@partch.anu.edu.au:~\comp2400lab

The pscp command can copy the file from your computer to the remote server, you can enter `pscp` to see other options.

After copying the data, we use `psql` to enter the database. In this lab, we need to copy two csv file in to the database, so we firstly create a new table named *basics*, the schema is shown below:

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

Finally, we can use `\copy` command to load the csv files into the table. An example could be:

    \copy ratings from '~/comp2400lab/data/ratings.csv' delimiter ',' CSV Header;

You can find more specific details about `copy` command [here](http://www.postgres.cn/docs/9.3/sql-copy.html)

## 2.Check Functional Dependencies
The second lab is to learn about functional dependencies.

There is a simple python program named *FDchecker.py*, you should clone or download it to your computer (not the partch server).

In the cmd.exe, use command `python` to run it, the specific command is:

    python FDchecker.py [-p <path>] num,num...->num,num...
    
For example,

    python FDchecker.py -p D:\Downloads\title.ratings.tsv\ratings.csv 1,2->3
    
This will let program find csv file in the giving path and try to check whether the column 1 and 2 can decide column or not.

You can change the default path in the program, so that you don't need to enter the path every time.

## 3.Query Processing and Optimisation

## 4.Use SQL to Answer Simple Questions
