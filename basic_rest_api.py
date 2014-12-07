from pypress import Pypress

# A basic Pypress REST API.

app = Pypress()

things = []


app.use(Pypress.Middleware.json_body_parser)


@app.get('/thing/:id')
def get_thing(req, res):
    res.json(things[req.params.id])


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
