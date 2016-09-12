from wsgiref.simple_server import make_server
from tg import expose, TGController, AppConfig
import numbergen
import random

random.seed()

def cleanup_textarea_value ( val ):
	return '\n'.join( val.splitlines() )

class RootController(TGController):
	@expose('tpl/index.xhtml')
	def index( self, lang = None ):
		example_numbers = None
		lang_base_clean = None
		if None != lang:
			lang_base_clean = cleanup_textarea_value( lang )
			possible_numbers = numbergen.get_possible_numbers( lang_base_clean )
			example_numbers = {}
			while len( example_numbers ) < 5 and len( possible_numbers ) != 0:
				index = random.randrange( len( possible_numbers ) )
				num = possible_numbers.pop( index )
				example_numbers[ num ] = numbergen.get_number_name( lang_base_clean, num )

		return {
			'lang_base': lang_base_clean,
			'example_numbers': example_numbers,
		}


config = AppConfig( minimal = True, root_controller = RootController() )
#enable kajiki templating engine
config.renderers = ['kajiki']
#enable static files
config.serve_static = True
config.paths['static_files'] = 'static'



print("Serving on port 8080...")
httpd = make_server('', 8080, config.make_wsgi_app() )
httpd.serve_forever()