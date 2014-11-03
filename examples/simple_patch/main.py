import endpoints_local

from google.appengine.ext import ndb
from protorpc import remote

from endpoints_proto_datastore.ndb import EndpointsModel


class MyModel(EndpointsModel):
  _message_fields_schema = ('id', 'attr1', 'created')

  attr1 = ndb.StringProperty(repeated=True)
  created = ndb.DateTimeProperty(auto_now_add=True)


DEFAULT_FIELDS = MyModel._DefaultFields()


@endpoints_local.api(name='myapi', version='v1', description='My Little API')
class MyApi(remote.Service):

  @MyModel.method(request_fields=DEFAULT_FIELDS,
                  path='mymodel', http_method='POST', name='mymodel.insert')
  def MyModelInsert(self, my_model):
    my_model.put()
    return my_model

  @MyModel.method(path='mymodel/{id}', request_fields=DEFAULT_FIELDS,
                  http_method='PATCH', name='mymodel.update')
  def MyModelPatch(self, my_model):
    if not my_model.from_datastore:
      raise endpoints_local.NotFoundException('MyModel not found.')
    my_model.put()
    return my_model

  @MyModel.method(request_fields=('id',),
                  path='mymodel/{id}', http_method='GET', name='mymodel.get')
  def MyModelGet(self, my_model):
    if not my_model.from_datastore:
      raise endpoints_local.NotFoundException('MyModel not found.')
    return my_model

  @MyModel.query_method(path='mymodels', name='mymodel.list')
  def MyModelList(self, query):
    return query


application = endpoints_local.api_server([MyApi], restricted=False)
