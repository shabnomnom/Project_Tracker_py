"""Hackbright Project Tracker.

A front-end for a database that allows users to work with students, class
projects, and the grades students receive in class projects.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy()


def connect_to_db(app):
    """Connect the database to our Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///hackbright'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


def get_student_by_github(github_input):
    """Given a GitHub account name, print info about the matching student."""

    QUERY = """
        SELECT first_name, last_name, github
        FROM students
        WHERE github = :githubkey
        """

    db_cursor = db.session.execute(QUERY, {'githubkey': github_input})

    row = db_cursor.fetchone() # (first_name, last_name, github)

    print("Student: {} {}\nGitHub account: {}".format(row[0], row[1], row[2]))


def make_new_student(first_name, last_name, github):
    """Add a new student and print confirmation.

    Given a first name, last name, and GitHub account, add student to the
    database and print a confirmation message.
    """

    QUERY = """ 
        INSERT INTO students (first_name, last_name, github)
        VALUES (:first_name, :last_name, :github)

    """

    db.session.execute(QUERY, {'first_name': first_name,
                                'last_name': last_name,
                                'github': github})

    db.session.commit()

    print(f"Successfully added student: {first_name} {last_name}")


def get_project_by_title(title_input):
    """Given a project title, print information about the project."""

    QUERY = """
    SELECT title, description, max_grade
    FROM projects
    WHERE title = :titlekey
    """

    #grab the row 
    db_cursor = db.session.execute(QUERY, {'titlekey': title_input})

    #sectioning the row
    row = db_cursor.fetchone()

    print(f"Project: {row[0]} \ndescription: {row[1]} \nMax_grade: {row[2]}")

def get_grade_by_github_title(github_input, title_input):
    """Print grade student received for a project."""

    QUERY = """ 
        SELECT grade
        FROM grades 
        WHERE student_github = :githubkey AND project_title = :titlekey
    """

    db_cursor = db.session.execute(QUERY, {'githubkey': github_input,
                                    'titlekey': title_input})
    
    row = db_cursor.fetchone() # grade they received

    print(f"{github_input}'s grade for the {title_input} project is {row[0]}")


def assign_grade(github, title, grade):
    """Assign a student a grade on an assignment and print a confirmation."""
    
    QUERY = """
        INSERT INTO grades (student_github, project_title, grade)
        VALUES (:githubkey, :titlekey, :gradekey)

    """
    db.session.execute(QUERY, {'githubkey': github, 'titlekey': title, 'gradekey': grade})

    db.session.commit()

    print(f"Successfully added student github: {github}, project title: {title} and grade: {grade}")

def add_project(title, description, max_grade):
    """Add a new project with its description and max grade """

    QUERY = """
    INSERT INTO projects (title, description, max_grade)
    VALUES (:titlekey, :descriptionkey, :maxgradekey)
    """
    db.session.execute(QUERY, {"titlekey": title, "descriptionkey": description, "maxgradekey":max_grade})

    db.session.commit()

    print(f"Successfully added the new project {title} with {description} and max grade {max_grade}")


def handle_input():
    """Main loop.

    Repeatedly prompt for commands, performing them, until 'quit' is received
    as a command.
    """

    command = None

    while command != "quit":
        input_string = input("HBA Database> ")
        tokens = input_string.split()
        command = tokens[0]
        args = tokens[1:]

        if command == "get_student":
            github = args[0]
            get_student_by_github(github)

        elif command == "new_student":
            first_name, last_name, github = args  # unpack!
            make_new_student(first_name, last_name, github)

        elif command == "project_title":
            project_title = args[0]
            get_project_by_title(project_title)

        elif command == "get_grade":
            github, project_title = args
            get_grade_by_github_title(github, project_title)

        elif command == "assign_grade":
            github, project_title, grade = args
            assign_grade(github, project_title, grade)

        elif command == "add_project":
            title = args[0]
            description = " ".join(args[1:-1])
            max_grade = args[-1]
            add_project(title, description, max_grade)

        else:
            if command != "quit":
                print("Invalid Entry. Try again.")


if __name__ == "__main__":
    connect_to_db(app)

    handle_input()

    # To be tidy, we close our database connection -- though,
    # since this is where our program ends, we'd quit anyway.

    db.session.close()
