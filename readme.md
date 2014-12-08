# Pypress
### by [Elvin Yung](https://github.com/elvinyung)

Python web microframework, heavily inspired by Express.js and Sinatra. 

## Installation
### Installing from Pip
1. `sudo pip install pypress`

### Building from source
1. i dunno lol, clone the thing

## Quickstart
Here's a very simple Hello World app:

```python
from pypress import Pypress

app = Pypress()

@app.get('/')
def hello (req, res):
  res.send('Hello world!')

app.listen(1337)
```
