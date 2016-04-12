import os
import betamax
from betamax_serializers import pretty_json

betamax.Betamax.register_serializer(pretty_json.PrettyJSONSerializer)

user = os.environ.get('FOOBOT_USER', '')
password = os.environ.get('FOOBOT_PASSWORD', '')
uuid = os.environ.get('FOOBOT_UUID', '123456789ABCDEF')
userid = os.environ.get('FOOBOT_USERID', '1234')
mac = os.environ.get('FOOBOT_MAC', '1234')

with betamax.Betamax.configure() as config:
    config.cassette_library_dir = 'tests/cassettes'
    config.default_cassette_options['record_mode'] = 'once'
    config.default_cassette_options['serialize_with'] = 'prettyjson'

    config.define_cassette_placeholder('USERNAME', user)
    config.define_cassette_placeholder('PASSWORD', password)
    config.define_cassette_placeholder('123456789ABCDEF', uuid)
    config.define_cassette_placeholder('1234', userid)
    config.define_cassette_placeholder('1234', mac)
