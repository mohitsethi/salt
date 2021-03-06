'''
Return data to a mongodb server

Required python modules: pymongo


This returner will send data from the minions to a MongoDB server. To 
configure the settings for your MongoDB server, add the following lines
to the minion config files::

    mongo.db: <database name>
    mongo.host: <server ip address>
    mongo.user: <MongoDB username>
    mongo.password: <MongoDB user password>
    mongo.port: 27017

'''

# Import python libs
import logging

# Import third party libs
try:
    import pymongo
    has_pymongo = True
except ImportError:
    has_pymongo = False


log = logging.getLogger(__name__)


def __virtual__():
    if not has_pymongo:
        return False
    return 'mongo_return'


def _remove_dots(d):
    output = {}
    for k, v in d.iteritems():
        if isinstance(v, dict):
            v = _remove_dots(v)
        output[k.replace('.', '-')] = v
    return output


def _get_conn():
    '''
    Return a mongodb connection object
    '''
    conn = pymongo.Connection(
            __salt__['config.option']('mongo.host'),
            __salt__['config.option']('mongo.port'))
    db = conn[__salt__['config.option']('mongo.db')]

    user = __salt__['config.option']('mongo.user')
    password = __salt__['config.option']('mongo.password')

    if user and password:
        db.authenticate(user, password)
    return conn, db


def returner(ret):
    '''
    Return data to a mongodb server
    '''
    conn, db = _get_conn()
    col = db[ret['id']]
    back = {}

    if isinstance(ret['return'], dict):
        back = _remove_dots(ret['return'])
    else:
        back = ret['return']

    log.debug(back)
    sdata = {ret['jid']: back, 'fun': ret['fun']}
    if 'out' in ret:
        sdata['out'] = ret['out']
    col.insert(sdata)


def get_jid(jid):
    '''
    Return the return information associated with a jid
    '''
    conn, db = _get_conn()
    ret = {}
    for collection in db.collection_names():
        rdata = db[collection].find_one({jid: {'$exists': 'true'}})
        if rdata:
            ret[collection] = rdata
    return ret


def get_fun(fun):
    '''
    Return the most recent jobs that have executed the named function
    '''
    conn, db = _get_conn()
    ret = {}
    for collection in db.collection_names():
        rdata = db[collection].find_one({'fun': fun})
        if rdata:
            ret[collection] = rdata
    return ret
