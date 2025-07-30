from flask import Flask, request, render_template, send_from_directory, redirect, url_for
from datetime import datetime
from lxml import etree
import atexit
import os

app = Flask(__name__)
user_comments = {"Krissy":"Wow, this is cool", "Lily":"I think I decrypted the DaVinci code!", "Tanush":"I hate going to the office, but this site picks me up!"}
broken_comments = {"Sebastian":"This site is very bad", "Matin":"OMG! WUT HAPPENED!!!", "Brad W":"My favorite bread is crossaint"}

app_state = {"piece_name":"my_mona_lisa.svg"}

def cleanup():
    print("\nDeleting flag...")
    os.remove('../flag.txt')
    print("Flag deleted")
    print("Deleting uploaded files...")
    for file in os.listdir("./pieces"):
        if file != "my_mona_lisa.svg":
            os.remove(f"./pieces/{file}")
            print(f"Deleted {file}")
    print("Cleanup finished")

def create_flag():
    random_flag = os.urandom(16).hex() 
    open('../flag.txt', 'w').write(f"flag{{{random_flag}}}\n")

atexit.register(cleanup)

@app.route("/api/emergency-restart")
def restart():
    cleanup()
    create_flag()
    app_state['piece_name'] = 'my_mona_lisa.svg'
    return redirect(url_for("index"))

@app.route("/")
def index():
    try:
        piece_name = app_state['piece_name']
        svg_input = open(f'pieces/{piece_name}', 'r').read()
        parser = etree.XMLParser(load_dtd=True, resolve_entities=True)
        tree = etree.fromstring(svg_input.encode(), parser)
        svg_rendered = etree.tostring(tree).decode()
        return render_template("index.html", svg=svg_rendered, comments=user_comments)
    except:
        return render_template("index.html", comments=broken_comments)

@app.route("/api/add", methods=["POST"])
def add():
    if 'file' not in request.files:
        return "Missing 'file' in request\n", 400
    file = request.files['file']
    file.save(f'./pieces/{datetime.now().strftime("%Y-%m-%d-%s")}')
    return "File saved!\n"

@app.route("/api/list")
def list():
    return os.listdir("./pieces/")

@app.route("/api/switch", methods=["POST"])
def switch():
    new_gallery = request.form.get("new_name")
    if not new_gallery:
        return "Missing new_name\n", 400
    app_state['piece_name'] = new_gallery
    return "Gallery changed!\n"

@app.route("/documentation")
def docu():
    return send_from_directory('static', 'documentation.txt')

@app.route("/robots.txt")
def robots():
    return send_from_directory('static', 'robots.txt')

if __name__ == "__main__":
    create_flag()
    app.run(host="0.0.0.0")
