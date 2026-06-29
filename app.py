from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory data storage
events = [
    {
        "id": 1,
        "title": "Python Workshop",
        "description": "Learn Flask",
        "date": "2024-07-15"
    },
    {
        "id": 2,
        "title": "Web Dev Meetup",
        "description": "Full-stack discussion",
        "date": "2024-07-20"
    }
]


# Helper function
def find_event(event_id):
    for event in events:
        if event["id"] == event_id:
            return event
    return None


# ==========================
# GET ROUTES
# ==========================

@app.route("/", methods=["GET"])
def welcome():
    return jsonify({"message": "Welcome to the Events API"}), 200


@app.route("/events", methods=["GET"])
def get_events():
    return jsonify(events), 200


@app.route("/events/<int:event_id>", methods=["GET"])
def get_event(event_id):
    event = find_event(event_id)

    if event is None:
        return jsonify({"error": "Event not found"}), 404

    return jsonify(event), 200


# ==========================
# POST ROUTE
# ==========================

@app.route("/events", methods=["POST"])
def create_event():
    data = request.get_json()

    if not data or "title" not in data:
        return jsonify({"error": "Title is required"}), 400

    new_id = max(event["id"] for event in events) + 1 if events else 1

    new_event = {
        "id": new_id,
        "title": data["title"],
        "description": data.get("description", ""),
        "date": data.get("date", "")
    }

    events.append(new_event)

    return jsonify(new_event), 201


# ==========================
# PATCH ROUTE
# ==========================

@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    event = find_event(event_id)

    if event is None:
        return jsonify({"error": "Event not found"}), 404

    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    if "title" in data:
        event["title"] = data["title"]

    if "description" in data:
        event["description"] = data["description"]

    if "date" in data:
        event["date"] = data["date"]

    return jsonify(event), 200


# ==========================
# DELETE ROUTE
# ==========================

@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    event = find_event(event_id)

    if event is None:
        return jsonify({"error": "Event not found"}), 404

    events.remove(event)

    return jsonify({"message": "Event deleted successfully"}), 200


# ==========================
# ERROR HANDLERS
# ==========================

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Route not found"}), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({"error": "Method not allowed"}), 405


if __name__ == "__main__":
    app.run(debug=True)