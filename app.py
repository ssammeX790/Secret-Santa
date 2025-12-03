from flask import Flask, render_template, request
import random

app = Flask(__name__)

def generate_assignments(participants, restrictions):
    givers = participants[:]

    # Feasibility check
    for g in givers:
        blocked = set(restrictions.get(g, [])) | {g}
        if len(blocked) >= len(participants):
            return None  # impossible setup

    receivers = participants[:]

    # Shuffle until valid
    for _ in range(10000):
        random.shuffle(receivers)
        valid = True

        for g, r in zip(givers, receivers):
            if g == r or r in restrictions.get(g, []):
                valid = False
                break

        if valid:
            return dict(zip(givers, receivers))

    return None


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        participants_raw = request.form["participants"]
        restrictions_raw = request.form["restrictions"]

        participants = [p.strip() for p in participants_raw.split(",") if p.strip()]

        restrictions = {}
        if restrictions_raw.strip():
            for line in restrictions_raw.split("\n"):
                if ":" in line:
                    person, blocked = line.split(":")
                    p = person.strip()
                    blocked_list = [b.strip() for b in blocked.split(",") if b.strip()]
                    restrictions[p] = blocked_list

        assignments = generate_assignments(participants, restrictions)

        return render_template("result.html", assignments=assignments)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)