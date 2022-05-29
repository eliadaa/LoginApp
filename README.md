# LoginApp
Final Individual project for AC Labs - Continental 
Manage Login application
Coordinator Continental: MG
Main scope of this project is to create an application capable to manage first login of a new employee
Application should contain two parts: Management and Login Window
Management:
1.	This is responsible to generate a temporary password for a provided username. This app is used by an administrator to generate a set of username + temporary password for a new employee  for first day into company. 
2.	Username must be composed only from alphanumeric characters. A warning needs to be provided if check failed
3.	Password must contains 8 random characters from next string string validChars = "ABCDEFGHJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*?
4.	Username + temporary password must be stored encrypted into “database.txt” file. MD5 algorithm can be a solution, but candidate if free to choose. 
Login Window:
1.	This is responsible for login action. New company employee receives his/her username + temporary password and he/she needs to perform his/her first login on company network. 
2.	He/she will enter into Login window the received username  + temporary password and click Login
3.	If username  + temporary password is not found into “database.txt” next warning must be displayed “User or password invalid”.
4.	If username  + temporary password is found into “database.txt” next message will be displayed: “New password mut be created”.
5.	User will be asked to enter:
a.	Old password 
b.	New password 
c.	Confirmation of new password (new password added twice)
6.	After new password was enter, then username + new password will replace existing username + temporary password into “database.txt”.
7.	A new login with temporary password should not be able, only using password define at step 5.
Note: candidate will create only one application, example for User Interface. 
