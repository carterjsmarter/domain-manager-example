# Steps for project setup
1. Create a virtual environment
    $ python3.8 -m venv venv
2. Activate the virtual env.
    $ source venv/bin/activate
3. Install packages from requirements.txt
    $ pip install -r requirements.txt
4. Create a new postgres database
    $ sudo -u postgres psql
    $ sudo -u postgres createuser <username>
    $ sudo -u postgres createdb <database_name>
    $ alter user <username> with encrypted password '<password>'
    $ grant all privileges on database <database_name> to <username> ;

5. Copy your databse_name, username and password, that you have just created in step 6 and put these in the settings.py file under DATABASES (Name, USER, PASSWORD)

6. Run migrate command (In the directory where manage.py file exists)
    $ python manage.py migrate

7. Run your application
    $ python manage.py runserver