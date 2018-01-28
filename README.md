# Bandwidth Monitor

This projects allows to continuously monitor the bandwidth of your home network
and visualize the results over time. It can be useful to make sure that your
provider gives you what you pay for!

Ideally, you could make this run on a raspberry pi at home, plugged on your box
via Ethernet.

The project is made of two parts:

1. `speed.py`, which will measure the bandwidth and store the results in a
   sqlite3 database, every time you run the file. For a very simple setup, you
   could make it run every N minutes from a `screen`, using the `watch` command.
2. `app.py` is a simple Flask API which allows for visualizing the results. You
   should run it in the same folder as the `speed.py` script so that it can
   access the database (it can be in a separate `screen`).
