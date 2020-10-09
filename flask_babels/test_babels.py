
from flask import Flask, request, render_template, flash
from flask_babel import Babel
from flask_babel import gettext as _

def app_cfg_init():
    # export FLASKR_SETTINGS="./setting.cfg"
    # app.config.from_envvar('FLASKR_SETTINGS', silent=True)
    fk_app = Flask(__name__)
    fk_app.secret_key = 'abc'  # 设置表单交互密钥
    fk_app.debug = True
    return fk_app

def babel_cfg_init(app):
    app.config['BABEL_DEFAULT_LOCALE'] = 'zh_Hans_CN'
    b = Babel(app)
    return b

app = app_cfg_init()
babel = babel_cfg_init(app)



@app.route('/', methods=['GET', 'POST'])
def index():
    p = {
        "author" : {
            "nickname": "Micro"
        },
        "timestamp" : 10000
    }
    flash(_('Invalid login. Please try again.')) #gettext()
    flash(_("Test for Test"))
    return render_template("index.html", post=p, Home="Test for Labels")


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=80)