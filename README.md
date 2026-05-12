### Quick Fix

Service center management system

### Installation

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch develop
bench install-app quickfix
```
-----------------------------------------------------
A2 
-----------------------------------------------------
1.what each config file is for, and what breaks if you accidentally put a secret in common_site_config.json ?
 ----> site_config contain site specific configurations like db credentials , dev mode and site level secrects on the other hand the common_site_config file contains db_host , redis config etc 
 if the secrets are accidentally put a secret in common_site_config.json then all the sites in the bench can access the secret so security break.

2.List the 4 processes bench start launches and explain what happens to background jobs if the worker process crashes ?
 ----> web, worker, scheduler, socketio and if the worker process crashes , the rq jobs wont execute , it will just queued.

------------------------------------------------------------
C3 
------------------------------------------------------------
1.Rename one of your test Technician records using the Rename Document feature.Then check: does the assigned_technician field on linked Job Cards automatically update? Why or why not? What does "track changes" mean in this context?
 ----> Yes , it got Automatically Update in the Job Card too , as the link field maintains the referencial integrity it will updated in all the places. The Track Changes logs who (User) renamed the doc , to what name and time .
 
 2.Explain unique constraints: what is the difference between setting a field as "unique" in the DocType vs doing a frappe.db.exists() check in validate()?
 ---->  Unique in the Docfield make the field unique in db level (Unique Constrain) and doing a frappe.db.exists() check in validate() is doing manually logic written in python 

------------------------------------------------------------
C1
------------------------------------------------------------
1.When you append a row to Job Card.parts_used and save, what 4 columns does
Frappe automatically set on the child table row?
----> ParentField , ParentType , Parent , Idx

2.What is the DB table name for the Part Usage Entry DocType?
----> tabPart Usage Entry

3.If you delete row at idx=2 and re-save, what happens to idx values of remaining rows?
----> The Index values will be updated , such that frappe reindex all the rows

------------------------------------------------------------
B1
------------------------------------------------------------
Step1 - Routing 
1.When a browser hits /api/method/quickfix.api.get_job_summary - what Python
function handles this request and how does Frappe find it?
---->get_job_summary this python fn handels the req and it should whitelisted . quickfix.api will be imported automatically and frappe parses the url and identify the app , file and the method 

2.When a browser hits /api/resource/Job Card/JC-2024-0001 - what happens
differently compared to /api/method/?
----> it is a rest api for doctype and /api/resource its a custom fn
/api/method/ --> fetch document and internally runs frappe.get_doc()

------------------------------------------------------------
D2
------------------------------------------------------------
What is the issues in using frappe.get_all in a whitelisted method that is exposed to guests or low-privilege users. Explain it in the context of permission_query_conditions ?
 
----> get_all() fetches all the records without applying the permissions so that even the low-privilege or guest user can retrive the records. So the permission_query_conditions used to check the user perm when we call the get_list() fn it automatically calls it .

------------------------------------------------------------
E1
------------------------------------------------------------
Recursion Pitfall in on_update() ----> using save() fn in on_update() will create a loop as that save fn invoke the on_update() fn so it will lead to crash or max recursion exceeded err. Alternatively frappe.db.set() can be used in such cases.

------------------------------------------------------------
E3
------------------------------------------------------------
part 1 : 
MRO ---> MRO defines the order of method execution during the python inheritance (class hierarchy)
super().validate() is non negotiable cause it is used to call the original validation funtion which is defined in the super class(parent class)
override_doctype_class is preferred when we need to change the core logic fn and override the existing methods deoc_events is preferred to add addtional functionalities without modification.

part 2 :
doc_events is safer because it wont replaces the core logic (Original class) like the override doctype class does.

------------------------------------------------------------
F1
------------------------------------------------------------
Task - B
1.TWO validate handlers on Job Card - one in your main controller and one in
doc_events . in what order do they run? What happens if
both raise a frappe.ValidationError?

----> The main controller handler will run first and then the doc_events handler execute. if both raise a error , the execution will stop at first when the main handler raised the err so the second one wont execute.

2.what happens when you register "*" AND a specific DocType handler
for the same event? Do both run?
----> yes, Both will run but the specifi doc handler will execute first.

------------------------------------------------------------
F3
------------------------------------------------------------
Assest hooks 
1.what DocType would use a tree view and why,explain what bench build --app quickfix does and why assets need cache-busting after JS changes

---->Tree view is used for hierarchial data (parent , child relationships) ,
cache busting is needed because browser caches the old data so that to reload the newversion cache busting is used

Jinja hooks
1.what is the difference between a Jinja context available in Print Formats vs one available in Web Pages? Are they the same? 
Jinja context available in Print Formats has limited context like doc objects only. In webpages full context -> user , frappe, session , custom methods So both are not same.

------------------------------------------------------------
F4
------------------------------------------------------------

1.explain the difference between override_whitelisted_methods (hook-based reversible, explicit) vs monkey patching (import-time, brittle, invisible). When would you use each?

----> override whitelisted method is safe and hook based , whereas monkey patching is an unsafe runtime modification hard to debug and maintain.
override whitelisted method is used during api call , auditing or logging and monkey patching when no hooks availabe

2.What happens if TWO apps both register override_whitelisted_methods for the same method? Write the answer

---->if TWO apps both register override_whitelisted_methods for the same method then the last installed app verride_whitelisted_methods will be executed.

3.Explain about the Signature mismatch and not having exactly the same arguments as the original and in what case would you get a TypeError.

----> When overriding the frappe method the custom method should have the same args as the original method otherwise typeError will occcur.

------------------------------------------------------------
F5
------------------------------------------------------------
1.Explain fieldname collision risk: what happens if your Custom Field has the same fieldname as a field added by a future Frappe update?

----> Collision will occur , migration failure ,field override conflict will occur .

2.Explain patching order: if Patch 1 creates a Custom Field and Patch 2 reads it, why must they be separate entries in patches.txt and never merged?

----> if we gives the patches in the same file the order of execution we will never know , so that we give it in seperate files as that frappe will run the files in sequencial order.

------------------------------------------------------------
H1
------------------------------------------------------------
1.Making a frappe.call inside the validate client event (before_save handler) - explain why this does not work ?
----> frappe.call is async function and validate will not wait for it to complete so inconsistent validation and unreliable logic these things will occur.

2.Using onload or refresh for async data fetches  ----> implementing frappe.call is in onload and referesh is best practice cause these are ui oriented event can safly wait.

------------------------------------------------------------
K3
------------------------------------------------------------
Task - A (N+1 query detection and fix)

----> SELECT jc.name, t.technician_name, t.phone FROM `tabJob Card` jc LEFT JOIN `tabTechnician` t ON jc.assigned_technician = t.name


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
