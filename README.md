# Assignment 2 - Kanban Board

In this second assignment, you will write an API for a
[`Kanban Board`](https://leankit.com/learn/kanban/kanban-board/) to be used by
a single person to manage tasks they have yet `todo`, tasks that are `in
progress`, and tasks that are `done`.  This application has a front-end web
app that will be useful as both a debugging tool, as well as a visualization
of how your API contributes to a successful product that a user can interact

![Kanban Board View](board.png)

## Learning Objectives

This assignment, unlike the first assignment, involves the complete application-
layer backend development experience.  The skills honed in this project are those
you'd use day-to-day when developing any backend supporting an app, be it web
or mobile.  As a result, it involves several tools / technologies / concepts:

* `Python` as a language and `Flask` as a framework
* [`JSON`](http://www.json.org/) as a means of sending and receiving data
* `HTTP` requests / responses
* `MySQL` system configuration and usage
* `SQL-esque` data-modeling
* [`ORM`](http://flask-sqlalchemy.pocoo.org/2.1/) usage and data-modeling
* [`Object Serialization`](http://marshmallow-sqlalchemy.readthedocs.io/en/latest/)
* `SQL` querying
* Writing an `API` to fit a specification given by front-end

## Table of Contents

* [Academic Integrity and Collaboration](#academic-integrity-and-collaboration)
* [System Configuration](#system-configuration)
* [Organization](#organization)
* [Front-end](#front-end)
* [Expected Functionality](#expected-functionality)
* [Testing Your Code](#testing-your-code)
* [Project Submission](#project-submission)

## Academic Integrity and Collaboration

#### Academic Integrity

Note that these projects should be completed **individually**. As a result, all University-standard AI guidelines should be followed.

#### Code Attribution and Collaboration

One of the reasons we chose `Flask` as an initial backend framework for students to use is because of its phenomenal support online. Looking up framework documentation and adapting the docs' sample code to suite your own needs in something we expect and want you to do, as it allows you to explore and increase your self-sufficiency regarding backend development. However, if you find code in a `StackOverflow` post or in an open source Github repository, then you should cite it accordingly. See the [project submission](#project-submission) section for guidelines as to where to include those citations.

## System Configuration

The following initial [**4** steps](https://github.com/Cornell-PoBE/A1/blob/master/README.md#system-configuration)
from `A1` are required in order to interact with this project.  

In addition to the above steps, we expect you to have `MySQL` installed.  
A guide to do so can be found [here](https://dev.mysql.com/doc/mysql-getting-started/en/#mysql-getting-started-installing).  
In addition, you should be able to access your `MySQL` system's terminal via the command-line
easily.  We recommend setting up your `$PATH` in order for you to access the `mysql` console.
To do so, add the following line to your `.bashrc`, `.zshrc`, or whatever other shell you
might use (these configuration files are found at your `root user directory: ~`):

````bash
export PATH="/path/to/my/mysql/bin_folder/bin:$PATH"
````
As an example, I'm on a `Mac` and my `MySQL` bin is located at the following path:

````bash
/usr/local/mysql-5.7.17-macos10.12-x86_64/bin
````

In addition, we we expect your backend to parameterized with [`environment variables`](https://en.wikipedia.org/wiki/Environment_variable) so that we can run the
code on our systems with these variables set to our own environment's configurations.  In
order to make dealing with environment variables easier, we recommend you install
[`autoenv`](https://github.com/kennethreitz/autoenv).  `autoenv` allows for environment
variable loading on `cd-ing` into the base directory of the project.  You can declare
environment variables in a `.env` file of the following format:

````bash
export APP_SETTINGS=config.DevelopmentConfig
export DB_NAME=pobe_a2_db
...
````

On `cd-ing` into your project directory, you can ensure that these variables are, in fact,
loaded into your environment by running the following argument, with `VARIABLE_NAME` replaced
with a variable you're setting in your `.env` file:

````bash
echo $VARIABLE_NAME
````

## Organization

TODO
