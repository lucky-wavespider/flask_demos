#!/bin/bash

pybabel --list-locales

##generate template
pybabel extract -F babel.cfg -o messages.pot .


##generate Target templage
pybabel init -i messages.pot -d translations -l zh_Hans_CN


####when translated, then exec 
pybabel compile -d translations


#Update template and translations
pybabel update -i messages.pot -d translations
