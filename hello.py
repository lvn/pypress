from pypress import Pypress

# A basic Pypress app that displays Hello World.

app = Pypress()


@app.get('/')
def hello(req, res):
    res.send('Hello world!')

app.listen(1337)
