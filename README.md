# Double Agent

Experimentation with 2 "agents":
* a UI agent that does requirement gathering
* a background agent that does code generation, here HTML

to start do

```
python double.py
```

One available, open the `outputs/app.html` file in your browser.
For this demo you will have to reload manually when you are notified of an html update


Note: there seems to be a bug with some duplicates in the message history, but the concept still works

## running the tests

```
pytest
```
