# Pypress
### by [Elvin Yung](https://github.com/elvinyung)

Python web microframework, heavily inspired by Express.js and Sinatra. 

## Installation
Pypress requires Python 3.

### Installing from Pip
1. `sudo pip install pypress`

### Building from source
1. Clone this repo.
2. Run `sudo python setup.py install` at the root of this repo.

## Quickstart
Here's a very simple Hello World app:

```python
from pypress import Pypress

app = Pypress()

@app.get('/')
def hello(req, res):
  res.send('Hello world!')

app.listen(1337)
```
