import os
import redis
import shortuuid
import secrets
from datetime import timedelta
from flask import Flask, render_template, request, redirect, url_for, abort
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', secrets.token_urlsafe(32))
    
    redis_host = os.getenv('REDIS_HOST', 'localhost')
    redis_port = int(os.getenv('REDIS_PORT', 6379))
    redis_db = int(os.getenv('REDIS_DB', 0))

    try:
        r = redis.Redis(
            host=redis_host,
            port=redis_port,
            db=redis_db,
            decode_responses=True,
            socket_timeout=5,
            health_check_interval=30
        )
        r.ping()
    except redis.exceptions.ConnectionError:
        r = None
    
    PASTE_KEY_PREFIX = "paste:"

    @app.route('/', methods=['GET', 'POST'])
    def create():
        if r is None:
             return render_template('index.html', error="Service Unavailable. Please check backend connection."), 503

        if request.method == 'POST':
            content = request.form.get('content', '').strip()
            expiry_minutes_str = request.form.get('expiry', '60')
            is_private = request.form.get('is_private') == 'on'
            
            if not content:
                return render_template('index.html', error="Paste content cannot be empty."), 400

            try:
                expiry_seconds = int(expiry_minutes_str) * 60
                expiry_seconds = max(expiry_seconds, 60)
            except ValueError:
                return render_template('index.html', error="Invalid expiry time."), 400

            paste_id = shortuuid.ShortUUID().random(length=7)
            key = f"{PASTE_KEY_PREFIX}{paste_id}"
            
            try:
                if is_private:
                    access_token = secrets.token_urlsafe(16) 
                    data = {"content": content, "token": access_token}
                    
                    r.hmset(key, data)
                    r.expire(key, expiry_seconds)
                    
                    paste_url = url_for('view', paste_id=paste_id, token=access_token, _external=True)
                else:
                    r.set(key, content, ex=expiry_seconds)
                    paste_url = url_for('view', paste_id=paste_id, _external=True)

                return render_template('index.html', paste_url=paste_url)

            except redis.exceptions.RedisError:
                return render_template('index.html', error="A database error occurred while saving the paste."), 500

        return render_template('index.html')

    @app.route('/<string:paste_id>')
    def view(paste_id):
        if r is None:
             return "Service Unavailable", 503

        key = f"{PASTE_KEY_PREFIX}{paste_id}"
        
        try:
            type = r.type(key)

            if type == 'none':
                abort(404)

            ttl_seconds = r.ttl(key)
            ttl_formatted = str(timedelta(seconds=ttl_seconds)).split('.', 1)[0]

            if type == 'string':
                content = r.get(key)
                is_private_label = "No (Public)"
                
                return render_template('view.html', 
                                    content=content, 
                                    paste_id=paste_id,
                                    is_private_label=is_private_label,
                                    ttl_formatted=ttl_formatted)

            elif type == 'hash':
                data = r.hgetall(key)
                required_token = data.get('token')
                provided_token = request.args.get('token')
                
                if not required_token or provided_token != required_token:
                    abort(403)
                    
                content = data.get('content', 'Error retrieving content.')
                is_private_label = "Yes (Token Required)"
                
                return render_template('view.html', 
                                    content=content, 
                                    paste_id=paste_id,
                                    is_private_label=is_private_label,
                                    ttl_formatted=ttl_formatted)
            
            else:
                 abort(500)

        except redis.exceptions.RedisError:
            return "Internal Database Error", 500

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

