# 2400Lab
## Task1: Import CSV Files into PostgreSQL
The first lab is designed to let students learn how to import outfiles into databases.

### 1) Download the Data
First, you need to download the files to your computer. 

You can either:

Use the green **Clone or Download** button in the top right corner and then unzip it;

Or use the `git` commands:

In **Linux**:

1. Click the terminal to open the Terminal
2. In the terminal, use commands `mkdir <directory name>` to make a directory storing the data
3. Use `cd <directory name>` to enter the directory
4. Use `git clone https://github.com/sjmsjmdsg/2400Lab.git` to download the data to your directory 


In **Windows**:

1. Click the **Windows** button in the bottom left corner in your computer, and find the **search** button
2. Search **CMD**, which represents command prompt, and press enter, this will open the cmd.exe, which will help you transform the data to the partch server.
3. In the cmd.exe, use commands `mkdir <directory name>` to make a directory storing the data
4. Use `cd <directory name>` to enter the directory
5. Use `git clone https://github.com/sjmsjmdsg/2400Lab.git` to download the data to your directory

</br>

### 2) Link to the Partch
We need to use partch to use the database. 

In **Linux**:

Open the terminal and use command

    ssh u1234567@partch.anu.edu.au

to log in the partch.


</br>


In **Windows**:

1. Search the **putty** in the search window, which is introduced in the last step, and open the PuTTY.exe, which can help you establish a ssh connection between your computer and the partch server.
2. In the HostName blank, enter your student ID: *u1234567@partch.anu.edu.au*, choose SSH for connection type, click *open*

</br>

Then input your password, and you can link to the partch

</br>

### 3) Load Data to PostgreSQL
To load the data, we first need to copy the data to the partch server. To do this, you can:

- Use the `git` commands introduced before in the linux terminal/putty command window to clone the files to the server

Or:

In **Linux**:

- Open a new terminal, enter command:

      scp <path stored csv data> u1234567@partch.anu.edu.au:<path in the server that you want to store the data>
      
    For example:
    
      scp /students/u1234567/2400Lab-master/data/basics.csv u1234567@partch.anu.edu.au:~/comp2400lab
      
    If you want to copy the whole directory, then:
    
      scp -r /students/u1234567/2400Lab-master/data u1234567@partch.anu.edu.au:~/comp2400lab
      
</br>

In **Windows**:

- Open cmd.exe, enter command:

      pscp <path stored csv data> u1234567@partch.anu.edu.au:<path in the server that you want to store the data>

    For example: 

      pscp D:\2400Lab-master\data\basics.csv u1234567@partch.anu.edu.au:~\comp2400lab

The scp/pscp command can copy the file from your computer to the remote server, you can enter `man scp`/`pscp` to see other options.

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

**Note**: If you don't know how to create those two table, the answer is in the `answer` file.

Finally, we can use `\copy` command to load the csv files into the table. An example could be:

    \copy ratings from '~/comp2400lab/data/ratings.csv' delimiter ',' CSV Header;

You can find more specific details about `copy` command [here](http://www.postgres.cn/docs/9.3/sql-copy.html)[1]

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

## Task4: Use SQL to Answer Simple Questions

## Reference


