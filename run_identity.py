from http.server import ThreadingHTTPServer

from myota_logging import configure_logging

configure_logging("myota-identity", component="api")

from identity import IdentityHandler, bootstrap_admin, seed

seed()
bootstrap_admin()
ThreadingHTTPServer(("0.0.0.0", 8001), IdentityHandler).serve_forever()
