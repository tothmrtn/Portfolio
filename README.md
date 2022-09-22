# Task Management Webapp
### Description: This is a basic task management web application made with:

>Python

>Javascript

>HTML, CSS & Jinja

>Flask

>SQLite

# **How it works**
## **Check/Remove button**

#### By default there are four random task listed on the "check-list" which can be marked by the user.
#### If a box, or multiple boxes are marked, the "CHECK TASK" button changes to "REMOVE TASK"
#### and it can be removed from the "check-list".

## **Reset Button**

#### With the help of the "Reset" button, the user can reset the tasks, and four
#### random new task appears on the "check-list".

## **Add Task button**

#### Selecting the drop-down menu, the user can see all the listed tasks that can be added
#### to the "check-list". Clicking on the "ADD TASK" button will add the selected one to the list.

## **Add button**

#### If the desired task is not found in the drop-down menu, unique tasks can be added.

## **What cannot be done**

- More than 10 task cannot be pushed to the "check-list".
- An item that's already in the "check-list" cannot be added twice.
- At the "Add new task" section, the input cannot be empty.
- If a task is already available in the drop-down menu, it cannot be added one more time.
- The text cannot contain any special character.

# **Implementation**

## **Client Side**
### For the front-end, the application uses HTML with Jinja, CSS, and Javascript.
### **CSS**

> ../project/static/css/main.css

#### The CSS file starts with a :root selector where all the necessary colors and actions are
#### defined. This way, if any modification is needed in the style, we can simply just re-write
#### the color's hexadecimal value within the mentioned selector.
#### Below there's the Body section, then the Buttons, Button hovers, Input, the Clock, and finally
#### the style of the flashed messages. I decided to have blue color and its variants on the site.
#### Originally it was menta, but I believe this is a more modern design. The hovering effects over
#### the buttons are also eye catching in my opinion. At the check-list section, the color is nor
#### gray or white, it's very slight bone color. I think it's pretty elegant.
#### Everything is positioned to the middle. Straightforward, I think that was the
#### best choice for this web app.

## **Javascript**
> ../project/static/js/main.js

#### The Javascript file contains four functions:
- **check_me()**
  #### This function receives a dinamically created input_id from the HTML.
  #### It changes the appearance both the CHECK/REMOVE button
  #### and the selected/de-selected item from the check-list.
  #### The item's are selected based on their current ID's,
  #### this way we can manipulate the button and the currently selected item.
  ```
  document.querySelector('input[id=' + input_id + ']');
  ```

  #### In this for loop, the number of the checked boxes are
  #### stored in an array.

  ```
  var checkBoxes = document.getElementsByName('check');
  var selected = [];

  for (var i=0; i<checkBoxes.length; i++) {
    if (checkBoxes[i].checked) {
           selected.push(checkBoxes[i].value);
    }
  }
  ```

  #### If an array is empty, there is no checked box, hence the REMOVE button
  #### should be changed to it's default appearance. The first if/else if statement
  #### ensures that if multiple boxes are selected, and the user de-select one,
  #### the line-through appearance of the de-selected item should disappear,
  #### but the REMOVE button should remain the same.
  ```
  if (selected.length != 0 && check_input.checked){
    ...
  }else if (!(check_input.checked)){
    ...
  if (selected.length == 0)
  ```

- **mouseOver()** & **mouseOut()**
  #### These two functions ensures that mouse hovering over the "CHECK TASK" button
  #### still works after the first check. In the CSS there is a :hover selector
  #### for that button, but in Javascript you can't call that.

- **displayTime()**
  #### That's just handle the fancy clock's mechanism.

## **HTML**
> ../project/static/templates/index.html

#### Basic HTML, displays the buttons, inputs, check-boxes, background, and the clock on the top of the page.
#### It's pretty short and straightforward. The only thing that's worth mentioning is the Jinja loop within the
#### Remove task section. First time when the app ran, the check_me() function didn't work on all the tasks,
#### then I figured out it's only not working on item's that has multiple words, like "Take a walk".
#### I found out that the querySelector can't handle whitespaces, so I had to use the .replace method
#### on the ID's and Label names, before the check_me() function receives it.

```
{% for item in all_task %}
....id="{{ item.replace(' ', '') }}" value="{{ item }}" onchange="check_me( '{{ item.replace(' ', '') }}' )">

```
## **Server Side**
### For the back-end, the application uses Python with Flask and SQLite.
### **Python**

> ../project/app.py

#### Top of the code there are the imports, underneath the class inicialisation of the application.
#### Below, just in case, there's a defined secret key in order to encrypt the cookies, and a session cookie name.

#### The file contains seven functions:
- **def index()**
  #### This is the main root. It returns the index.html from the HTML, the all_data and all_items
  #### that's defined in the Jinja loop. The application uses sessions, in order to load variables globally.

- **def add_items()**
  #### It handles the mechanism of the "ADD TASK" button. When the button clicked, the
  #### selected item from the **select_items** list is being added to the **all_task** list.
  #### The function also restricts the user from doing certain things:
  #### - Adding the same item twice to the **all_task** list.
  #### - Adding more than ten task to the **all_task** list.
  ```
  if request.form["select_items"] in session["all_task"]:
      flash("You cannot add one task twice!", "info")
  elif len(session["all_task"]) > 9:
      flash("You cannot add more task!", "info")
  ```
- **def add_new()**
  #### With this function, the user can add new tasks to the database. In order to prevent any malicious
  #### activity, this function also has some restriction:
  #### - User cannot include any special character in the textfield.
  #### - The field cannot be empty.
  #### - One task can be added once to the database, case sensitively.
  ```
  SELECT name FROM todo WHERE name = ? COLLATE NOCASE
  ```

- **def remove_items()**
  #### If one box is checked, it can be removed from the **all_task** list.
  #### It stores the actual checked box in the check_boxes variable.
  #### A loop checks whether the item in all_task is checked or not.
  #### If so, the pop method will be called and it removes from the **all_task** list.
  #### Lastly, the session will be updated.
  ```
  check_boxes = request.form.getlist("check")

  for item in check_boxes:
      if item in session["all_task"]:
          idx = session["all_task"].index(item)
          session["all_task"].pop(idx)
          session.modified = True
  ```

- **def reset_task()**
  #### This basically acts the same as the Index function. Only difference it's assigned
  #### to the "reset" button in the HTML, so the user can manually reset the tasks without
  #### reloading the actual page.

- **def get_db()**
  #### This connects the SQLite database to the application. It fetches all the tasks names
  #### from the database and print it to the page, up to four task, randomly.

- **def close_connection(exception)**
  #### These block of code are responsible for terminating the database connection
  #### once the user is done using it.


### **SQLite**

> ../project/todo_db.db

#### This is the database that stores all the task names with their ID's.
- Table name: "todo"
- Columns: "id", "name"

#### The database is assigned to the variable "db" at the top of the app.py file.
```
db = SQL("sqlite:///todo_db.db")
```

#### Selecting the "Gym" from the db in the python file example
```
db.execute("SELECT name FROM todo WHERE name = 'Gym'")
```