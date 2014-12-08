from pypress import Pypress

# A basic Pypress REST API.

app = Pypress()
app.use(Pypress.Middleware.json_body_parser)
things = []


@app.use()
def convert_id_to_int(req, res, next):
    if 'id' in req.params:
        req.params['id'] = int(req.params['id'])
    next()


@app.get('/things/:id')
def get_thing(req, res):
    print(req.params['id'])
    if req.params['id'] < len(things):
        res.json(things[req.params['id']])
    else:
        res.send(404)


@app.get('/things')
def get_things(req, res):
    res.json(things)


@app.post('/things')
def create_thing(req, res):
    things.append(req.body['thing'])
    res.send('done')


@app.put('/things/:id')
def replace_thing(req, res):
    try:
        things[req.params['id']] = req.body['thing']
        res.send('done')
    except:
        res.send(404)


@app.delete('/things/:id')
def destroy_thing(req, res):
    try:
        removed = things.pop(req.params['id'])
        res.send(removed, 204)
    except:
        res.send(403)


app.listen(1337)
