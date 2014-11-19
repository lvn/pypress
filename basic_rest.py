from pypress import Pypress
import json

app = Pypress()

things = []

@app.use()
def json_body_parser (req, res, after):
    # parse json here
    req.body = json.loads(req.body)
    after(req, res)

@app.get('/')
def hello (req, res):
    res.send('Hello world!')

@app.get('/thing')
def query_thing (req, res):
    res.send(json.dumps(things))

@app.get('/thing/:id')
def get_thing (req, res):
    res.send(json.dumps(things[req.params.id]))

@app.post('/thing')
def query_thing (req, res):
    things.append(req.body.thing)
    res.send('done')

@app.put('/thing/:id')
def query_thing (req, res):
    things[req.params.id] = req.body.thing
    res.send('done')

@app.delete('/thing/:id')
def query_thing (req, res):
    things.pop(req.params.id)
    res.send('done')

app.listen(1337) 