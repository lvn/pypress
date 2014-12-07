from pypress import Pypress
import json

# A basic Pypress REST API.

app = Pypress()

things = []


@app.use()
def json_body_parser(req, res, after):
    # parse json here
    req.body = json.loads(req.body)
    after(req, res)


@app.get('/thing')
def query_thing(req, res):
    res.send(json.dumps(things))


@app.get('/thing/:id')
def get_thing(req, res):
    res.send(json.dumps(things[req.params.id]))


@app.post('/thing')
def create_thing(req, res):
    things.append(req.body.thing)
    res.send('done')


@app.put('/thing/:id')
def replace_thing(req, res):
    try:
        things[req.params.id] = req.body.thing
        res.send('done')
    except:
        res.send(404)


@app.delete('/thing/:id')
def destroy_thing(req, res):
    try:
        removed = things.pop(req.params.id)
        res.send(removed, 204)
    except:
        res.send(403)


app.listen(1337)
