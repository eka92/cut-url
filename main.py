from bottle import *
import pymongo
import random
import string

def generate_url():
    global urls
    size = 5
    rand_str = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(size))
    doc = {"tiny_url": rand_str}
    if urls.find_one(doc):
        return generate_url()
    else:
        return rand_str
    

@post('/create')
def create_link():
    long_url = request.forms.get('url').strip()
    if long_url.startswith("http://"):
        pass
    else:
        long_url = "http://"+long_url

    cut_url = generate_url()
    global urls
    urls.insert({"long_url": long_url, "cut_url": cut_url})
    return template('main', you_url=base_site + cut_url)


@route("/")
def main():
    name = 'world'
    return template('main', you_url=None)


@route("/:url")
def redirect_to_page(url):
    global urls
    url_page = urls.find_one({"cut_url": url})
    if url_page:
        redirect(url_page["long_url"])
    else:
        return template('main',you_url = 'Sorry...')

#config
base_site = "http://localhost:8080/"
name_db = "chuv_su"
mongo_connect = pymongo.Connection('localhost', 27017)
mongo_data = mongo_connect[name_db]
users = mongo_data["users"]
urls = mongo_data["urls"]

run(reloader=True)