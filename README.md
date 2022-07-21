# Huell - Ultimate Guard
Version: `not yet`

## How to setup development environment


### Prerequisites
* Python 3.10
* PostgreSQL (min v14.4) database (locally or on server)


### First setup
Before you start Huell on a new machine, he has to get used to new environment. To make it easier for him, execute this steps:

Firstly, install pipenv python module
```
pip install pipenv==2022.4.8
```
Secondly, setup pipenv environment
```
cd [path to huell repo]
pipenv shell --python 3.10 
```
Thirdly, install dependence
```
pipenv install
```
Next, **set all environments** - this step is described in other section

After all this steps, you are truly ready to taste the power of Huell! Start local server and run for your life!
```
flask run
```

### Not first setup
If you are after your first time with Huell and you wanna fight him again (poor idea), this section is for you! Just follow this
simple steps:
```
cd [path to huell repo]
pipenv shell
```
**Set all environments** and run `flask run` command to start epic fight!


### About environments
In this section we will talk about what defines Huell - environment variables!

`HUELL_LOGLEVEL` - With this you can decide what do you want to know about Huell actions:
* `DEBUG` - Huell will report you about every step he does - if you can't handle higher levels, this is for you!
* `INFO` - Standard level - Huell reports only about more important stuff, leaving details for him.
* `WARN` - Huell only reports about most important happenings - when it isn't bad yet, but it can be soon.
* `ERROR` - Huell only reports about major problems that somehow stopped Huell's current job.
* `CRITICAL` - Also called `SCREAMS AND SWEARS` - Huell will only talk to you when he needs to stop entire server 
because of you!

`HUELL_USER_PORT` - With this variable you can choose in which diary Huell will write info about users.
For now Huell is fussy and is able to write only in `DATABASE`, but it can change over time :).

`HUELL_DB_URL` - If you choose `DATABASE` as `HUELL_USER_PORT` you also need to give this variable, with
you database URL.\
Database URL model: `DATABASE_SERVICE://USER:PASSWORD@HOSTNAME:PORT/DBNAME`\
Database URL example: `postgresql://huell:huell@huell:8888/huell`\
<sup><sub>**DISCLAIMER** For now only fully tested and 100% working database is POSTGRESQL</sub></sup>



## How to use dockerized Huell
If you don't want to fight with Huell, you just want to accept him and use his help, then this is section for you!
I will show you how to start Huell on your computer without all this horrifying development shit!


### Prerequisites
* Docker and docker-compose


### First setup
If you are stressed just calm down, dockerized Huell isn't so aggressive and furious as in development.
**To set up dockerized Huell** just follow this steps:

Firstly, go to Huell habitat (his repo folder) and go to .docker folder in it 
(don't go anywhere else, or it can end bad for you)
```
cd [path to huell repo]/.docker
```

Then you just need to perform one simple commands to start Huell's work
```
docker-compose up --build
```

**Congratulations!** You just set up you own Huell!


### Not first setup
If you have already done first set up and want Huell's help again, this is what you need to do:
```
cd [path to huell repo]/.docker
docker-compose up
```


### How to get access to dockerized Huell (if you didn't change docker setup)
If you want to communicate with your Huell, you need to connect with specific ports:

* `localhost:5000/api/v1` - this is where you find all of Huell API.
* `localhost:5000/doc` - documentation (also called bestiary) of Huell.
* `localhost:5050` - PGADMIN, you can peek at Huell's diary (for the Holy Mother of God, don't let him see you).


### Default database credentials
* **PGADMIN EMAIL:** codebusters@ironhills.dev
* **PGADMIN PASSWD:** postgres
* **POSTGRES HOST:** huell-postgres:5432 (only accessible through PGADMIN)
* **POSTGRES USERNAME:** huell
* **POSTGRES PASSWD:** huell

