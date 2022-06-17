# CSV To DGF

This small program was designed to help out the transition between third-party systems to Digifort, where the customer has the ability to produce a .CSV file
with the devices they wish to register on the system. The program will first validate that all necessary information is correctly registered, as well as do a
quick check on the manufacturer/models provided and if any of them can't be found on Digifort's library it'll prompt the user to register them as ONVIF (a 
generic protocol).

The system will also automatically assign a recording directory to each camera in case a directory isn't provided on the .CSV file. Once the program runs it'll
generate a backup file so that the user can apply to any server they want.

You'll also find a example CSV to demonstrate the program usage.
