### Quick Fix

Service center management system

### Installation

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch develop
bench install-app quickfix
```

A2 - 
1.what each config file is for, and what breaks if you accidentally put a secret in common_site_config.json ?
 ----> site_config contain site specific configurations like db credentials , dev mode and site level secrects on the other hand the common_site_config file contains db_host , redis config etc 
 if the secrets are accidentally put a secret in common_site_config.json then all the sites in the bench can access the secret so security break.

2. List the 4 processes bench start launches and explain what happens to background jobs if the worker process crashes ?
 ----> web, worker, scheduler, socketio and if the worker process crashes , the rq jobs wont execute , it will just queued.

C3 - 
1.Rename one of your test Technician records using the Rename Document feature.Then check: does the assigned_technician field on linked Job Cards automatically update? Why or why not? What does "track changes" mean in this context?
 ----> Yes , it got Automatically Update in the Job Card too , as the link field maintains the referencial integrity it will updated in all the places. The Track Changes logs who (User) renamed the doc , to what name and time .
 
 2.Explain unique constraints: what is the difference between setting a field as "unique" in the DocType vs doing a frappe.db.exists() check in validate()?
 ---->  Unique in the Docfield make the field unique in db level (Unique Constrain) and doing a frappe.db.exists() check in validate() is doing manually logic written in python 

C1 - 
1.When you append a row to Job Card.parts_used and save, what 4 columns does
Frappe automatically set on the child table row?
----> ParentField , ParentType , Parent , Idx

2.What is the DB table name for the Part Usage Entry DocType?
----> tabPart Usage Entry

3.If you delete row at idx=2 and re-save, what happens to idx values of remaining rows?
----> The Index values will be updated , such that frappe reindex all the rows

B1 -
Step1 - Routing 
1.When a browser hits /api/method/quickfix.api.get_job_summary - what Python
function handles this request and how does Frappe find it?
---->get_job_summary this python fn handels the req and it should whitelisted . quickfix.api will be imported automatically and frappe parses the url and identify the app , file and the method 

2.When a browser hits /api/resource/Job Card/JC-2024-0001 - what happens
differently compared to /api/method/?
----> it is a rest api for doctype and /api/resource its a custom fn
/api/method/ --> fetch document and internally runs frappe.get_doc()

### Contributing

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/quickfix
pre-commit install
```

Pre-commit is configured to use the following tools for checking and formatting your code:

- ruff
- eslint
- prettier
- pyupgrade

### CI

This app can use GitHub Actions for CI. The following workflows are configured:

- CI: Installs this app and runs unit tests on every push to `develop` branch.
- Linters: Runs [Frappe Semgrep Rules](https://github.com/frappe/semgrep-rules) and [pip-audit](https://pypi.org/project/pip-audit/) on every pull request.


### License

mit
