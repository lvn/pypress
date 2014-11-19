from pypress import Pypress

app = Pypress()

@app.get('/')
def hello (req, res):
    res.send('Hello world!')

app.listen(1337) 