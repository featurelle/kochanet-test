Kochanet Test DRF Project - codename Healthpal
===
The lightweight DRF/PostgreSQL app for patient and assessment management.
Done MVP + bonus tasks.

You can see it yourself at http://featurelle-kochanet-healthpal.space
***

Setup
===
Set up the database
---

PostgreSQL
1. Install:
    - `sudo apt install postgresql`
2. Change the auth method to md5 in order to use password authentication in the app [if not done yet]:
    - [Optional] Enter as postgres and change the password:
      - `sudo -i -u -postgres`
      - `psql`
      - `ALTER USER postgres PASSWORD 'your new password';`
      - `\q` to exit psql
      - `exit` to exit postgres session
    - Change the auth method:
      - `sudo nano /etc/postgresql/{postgres version}/main/pg_hba.conf`
      - In the line `local all postgress peer` change `peer` to `md5` and save the file
      - Restart postgres `sudo systemtcl restart postgresql`

3. Create app db:
   - `sudo -i -u -postgres`
   - `psql`
   - `CREATE DATABASE your_db_name;`
   - `\q`
   - `exit`

Set up the project
---

1. Clone and open the project:
   - `git clone git@github.com:featurelle/kochanet-test-drf.git` or use HTTP as you like
   - `cd kochanet-test-drf`
2. Create and enter a virtual environment:
   - `python3 -m venv venv`
   - `source venv/bin/activate`
3. Install requirements:
   - `pip install -r req.txt`
4. Create a config file near settings:
   - `cd healthpal_core/healthpal_core/`
   - `nano settings.ini` or use .env file as you like
   - Write the settings:\
       `[settings]`\
        `HEALTHPAL_DJANGO_DEBUG=True/False`\
        `HEALTHPAL_DJANGO_SECRET=YourSecretCode`\
        `HEALTHPAL_DJANGO_ALLOWED_HOSTS=your_domain_name, localhost or others`\
        `HEALTHPAL_DJANGO_DB_NAME=your_db_name`\
        `HEALTHPAL_DJANGO_DB_USER=your_db_user`\
        `HEALTHPAL_DJANGO_DB_PASS=your_db_pass`\
        `HEALTHPAL_DJANGO_DB_HOST=localhost or other`\
        `HEALTHPAL_DJANGO_DB_PORT=5432 or other`
    
Prepare
---
1. Migrate:
    - `cd ..` to go back to top-level of django project
    - `./manage.py makemigrations`
    - `./manage.py migrate`
2. Create Superuser
    - `./manage.py createsuperuser`
    - Login and pass whatever you like
3. Tests
    - `./manage.py test`
4. Collect statics
    - `./manage.py collectstatic`

Run
---
You can run simply typing `./manage.py runserver` or use nginx (for deploy):
1. Setup nginx:
   - `sudo apt install nginx -y`
   - `sudo nano /etc/nginx/sites-available/{site name}`
   - Enter the basic settings:\
       `server {`\
       `listen 80;`\
       `server_name _;`\
       `location / {`\
       `include proxy_params;`\
       `proxy_pass http://localhost:8000/;` \
       `}`
   - `sudo ln -s /etc/nginx/sites-available/{site name} /etc/nginx/sites-enabled`
   - `nginx -t` check for the errors
   - `sudo systemctl restart nginx`
2. Setup gunicorn:
   - `pip install gunicorn`
   - Create UNIT file to run as service:
     - `sudo nano /etc/systemd/system/{service name}.service`
       - Write the service config:
       `[Unit]`\
       `Description=Whatever you want`\
       `After=network.target`\
       `[Service]`\
       `User={system user}`\
       `WorkingDirectory={django root directory}`\
       `ExecStart={gunicorn path in venv} healthpal_core.wsgi --bind 127.0.0.1:8000 --workers 2`\
       `Restart=always`\
       `RestartSec=3`\
       `[Install]`\
       `WantedBy=multi-user.target`
   - `sudo systemctl daemon-reload`
3. Run:
   - `sudo service {your service} start`
   - `sudo service {your service} status` Check status

Assumptions made
===

**App size:**
- App has less than 5k daily users / up to 100k users overall - we don’t have to optimize it much, and we can concentrate fully on code simplicity and readability

**App format:**
- It’s going to be a mobile app, so no cookies for auth
- The database is only used by this app (app-level constraints for most validations are enough)

**Auth:**
- Only authorized users can access the app
- No email confirmation required
- We don’t need multi-device session control (e.g. raw simplejwt is ok)

**Domain:**
- Overall:
  - App is used in only one country (e.g. no need in country code in phone)
  - We don't generally use cyrillic symbols in that country (except citations)
- Multitenancy:
  - Patients (hence their assessments too) are assigned to particular clinicians (users), others can't access them
  - One clinician per one patient/assessment
  - Admins can access everything via adminpanel
- Patients:
  - A patient still can be processed by admin after the assigned clinician is gone (no cascade deletion)
  - We use Google Places API for obtaining address info (google place id)
  - We don't restrict name format to only first-name/last-name (given europeans and immigrants can have all kinds of names)
  - Phone numbers can be of different lengths (mobile, home, other types), generally maxing at 15 symbols
  - The country we operate in has strong emphasis for 2-gender only gender options in medical software
  - No one ever aged more than 110 years in this country (+10 years span for validation) (though we might have to eventually add "dead/alive" flag in the future in order to store records of patients from the far past)
- Assessments:
  - We don't need to further process assessments after a patient is removed from the system (cascade deletion)
  - We don't have predefined assessment types (free-form assessments)
  - We don't have predefined questions for different assessment types (they are not related)
  - Each assessment must have at least one question-answer round
  - Each question must be answered
  - We don't restrict length/format of questions and answers (even cyrillic citations, special symbols, etc. allowed)
  - Overall score is 0 up to 100

Challenges faced
===

If we consider a technical challenge the state in which I'm desperate having no idea how it works or why it doesn't, there weren't any.
Most of the time stuff required a bit of thinking or googling, mostly on the business-logic side rather than implementation, but since the app is much simpler than what I've done in the past, no notable challenges were faced.

Some bugs, some things won't work right away, some I don't remember right away, the usual stuff. Sorry to disappoint in this regard, but generally it was time-consuming (given that I haven't done it in a while and had to remember stuff) yet overall pretty easy.

Probably the hardest part was to write this documentation and deploy to AWS (my first time) - solved with googling and a bit of practice.

Although if we consider planning a challenge - I had to remember that all the stuff I can come up with might not be doable in a given time (because again, I had to refresh my memories and had other stuff to do) and stick to the MVP version. Solved with googling the possible difficulties, estimating, prioritizing and throwing away ideas that are too time-consuming.

Additional features and improvements
===

None. Did the MVP and bonus tasks in order to be sure the basic code is good and well tested (manual QA done in Postman mostly).

Although it may seem uninterested, my primary goal was to ensure that the app does what's required, I'm on time and I deliver a good and well-tested solution. No cargo cult and no endangering the overall result (well-done test task) for a couple of cool-to-implement features.

Deployment to AWS
===

Given that we assume small to medium size of the app at maximum, and it doesn't have much customization, we can use AWS Lightsail to save time, get simpler deployment process and have better control over the cost of compute and space.

Create an instance
---
1. Create a Linux instance, OS only blueprint, Ubuntu 24.04
2. Enable automatic snapshots for backup
3. Network option - Dual (since IPv4 is still widely used)
4. The cheapest instance plan
5. Name the instance whatever you like
6. Wait until it's running

Set a static IP address
---
1. Go to Networking
2. Select Create static IP
3. Select your instance
4. Name it whatever you want

Set up a domain (assuming domain is already registered)
---
1. Go to Domains&DNS
2. Create DNS Zone
3. Enter your domain
4. Obtain the DNS name servers
5. Put it into your hosting provider panel (the setup here depends on your particular hosting provider)
6. Go to your static IPs and open the IP you created before
7. Select Domains and add your previously registered domain
8. Assign

Set up the instance
---

1. Go back to Instances and click on the instance
2. Connect using SSH
3. Get updates:
   - `sudo add-apt-repository universe`
   - `sudo apt update`
4. Install python3-pip and venv:
   - `sudo apt install python3-pip`
   - `sudo apt install python3-venv`
5. Proceed with instructions from **Setup** section of this documentation
