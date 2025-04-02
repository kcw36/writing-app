"""A simple API to track writing"""

from flask import Flask, request

from entry_functions import load_all_entries, save_new_entry, is_valid_entry

api = Flask(__name__)


@api.get("/")
def index():
    return {
        "message": "Welcome to the writing app"
    }


@api.route("/entry", methods=["GET", "POST"])
def get_or_create_entries():
    if request.method == "GET":
        args = request.args.to_dict()
        entries = load_all_entries()

        if "author" in args:
            author = args["author"]
            entries = [e for e in entries if e["author"].lower() ==
                       author.lower()]

        return entries
    else:
        new_entry = request.json
        entries = load_all_entries()
        if is_valid_entry(new_entry):
            created_entry = save_new_entry(new_entry)
            return created_entry, 202
        else:
            return {
                "error": "Invalid entry given."
            }


if __name__ == "__main__":
    api.run(port=8080, debug=True)
