from io import BytesIO

from flask import render_template, request, redirect, flash, url_for, session, abort, send_file
from flask import current_app as app
from PIL import Image

from controllers import user_controller, code_controller, purchase_controller


@app.route('/')
def index():
    user_id = session['user'] if 'user' in session else None
    codes = code_controller.get_all_codes()
    return render_template('index.html', codes=codes, user_id=user_id)


@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'GET':
        return render_template('registration.html')
    else:
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')

        if user_controller.check_by_email(email):
            flash('Email is already in use!')
            return redirect(url_for('sign_up'))

        new_user = user_controller.create(email, password, name)
        session['user'] = new_user.id

        return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        email = request.form.get('email')
        password = request.form.get('password')

        usr = user_controller.login(email, password)
        if not usr:
            flash('Wrong email or password!')
            return redirect(url_for('login'))

        session['user'] = usr.id

        return redirect(url_for('index'))


@app.route('/signout')
def sign_out():
    session.pop('user')
    return redirect(url_for('index'))


@app.route('/add-code', methods=['GET', 'POST'])
def add_code():
    if request.method == 'GET':
        if not 'user' in session:
            return redirect(url_for('index'))
        return render_template('codeload.html')
    else:
        if not 'user' in session:
            return redirect(url_for('index'))

        user_id = session['user']
        title = request.form.get('title')
        code = request.files.get('file')
        image = request.files.get('image')

        image_bytes = image.read()
        try:
            img = Image.open(BytesIO(image_bytes))
            img = img.resize([500, 500])
            buf = BytesIO()
            img.save(buf, format='JPEG')
            image_bytes = buf.getvalue()
        except Exception as exc:
            print(exc)
            flash('Wrong data for image!')
            return redirect(url_for('add_code'))

        code_bytes = code.read()
        if code_bytes == b'':
            flash('Wrong zip file!')
            return redirect(url_for('add_code'))

        new_code = code_controller.create(author_id=user_id, title=title, zip_bytes=code_bytes, image_bytes=image_bytes)

        return redirect(url_for('my_code'))


@app.route('/my-code')
def my_code():
    if not 'user' in session:
        return redirect(url_for('index'))

    user_id = session['user']
    codes = code_controller.get_by_user(user_id)

    return render_template('mycode.html', codes=codes)


@app.route('/codes/images/<int:code_id>')
def codes_images(code_id):
    img = code_controller.get_image_by_id(code_id)
    if not img:
        return abort(404)
    return send_file(BytesIO(img[0]), mimetype='image/jpeg')


@app.route('/codes/download/<int:code_id>')
def download_code(code_id):
    if not 'user' in session:
        return redirect(url_for('index'))
    user_id = session['user']
    if code_controller.check_if_available(code_id, user_id):
        code, name = code_controller.get_zip(code_id)
        return send_file(BytesIO(code), mimetype='application/octet-stream', download_name=name+'.zip')
    return redirect(url_for('index'))


@app.route('/purchased')
def purchased():
    if not 'user' in session:
        return redirect(url_for('index'))

    user_id = session['user']
    purchases = purchase_controller.get_by_buyer(user_id)
    codes = [p.code for p in purchases]

    return render_template('purchased.html', codes=codes)


@app.route('/buy/<int:code_id>')
def make_purchase(code_id):
    if not 'user' in session:
        return redirect(url_for('login'))

    user_id = session['user']
    purchase_controller.create(user_id, code_id)

    return redirect(url_for('purchased'))


@app.route('/codes/<int:code_id>')
def code_page(code_id):
    user_id = session['user'] if 'user' in session else None
    code = code_controller.get(code_id)
    return render_template('code.html', code=code, user_id=user_id, check=purchase_controller.check_if_bought)
