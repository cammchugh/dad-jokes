# dad-jokes
Django web-app to demo some refactoring stuff

virtualenv -p python3 venv

pip install django

pip install requests

Had to install psycopg2 using:

env LDFLAGS="-I/usr/local/opt/openssl/include -L/usr/local/opt/openssl/lib" pip --no-cache install psycopg2

https://stackoverflow.com/questions/26288042/error-installing-psycopg2-library-not-found-for-lssl

# Branches

1. initial
- An early django project
- Everything is in the view
- All tests use the testing client
- lots of test setup, super slow
- Nothing is mocked, not even the joke API
2. mock-enternal-service
- Introduce mocking of the joke API
- Not hitting an API anymore, but still really slow
- Tests depend on so many things.
  - routing
  - middleware
  - auth
  - templating
  - database
  - etc.
- Test failures don't indicate cause of failure.
3. testing-view-functions-directly
- Testing View methods directly, mocking request.
- Eliminates routing, middleware, auth, templating.
- Still have to assert against values in context.
- Still quite slow.
- Still very little feedback on cause of failure.
4. adding-domain-class
- Pull joke fetching logic into a domain class.
- No longer need fine grained client/view tests.
- Domain class method is still too big, as are it's tests.
5. wrapping-external-service
- Wrap requests to joke API in a service method
- Only need to mock requests in small number service tests.
- Domain class now only needs to mock our (simpler) interface.
6. remove-db-queries-from-domain-logic
- Hide ORM stuff behind class methods on DadJoke
- Could also go into a separate class.
- Could go into a manager or query set, but then the ORM leaks into domain logic.
- Mock the wrapper methods.
- Now we can test the joke fetcher without the database.
