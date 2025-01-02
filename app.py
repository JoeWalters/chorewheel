from flask import Flask, render_template_string

app = Flask(__name__)

# Path to the text file
TASKS_FILE = 'tasks.txt'

# HTML content with placeholder for tasks
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Chore Wheel</title>
      <!--<link href="{{ url_for('static', filename='main.css') }}" rel="stylesheet" nonce="">-->
    <style>
      body {
        display: flex;
        align-items: center; /*vertical alignement*/
        justify-content: center; /* horizontal alignement*/
      }
      :where(.wheel) {
        --_items: {{ tasks | length }};
        all: unset;
        aspect-ratio: 1 / 1;
        container-type: inline-size;
        direction: ltr;
        display: grid;
        position: relative;
        width: 50%;
        &::after {
          aspect-ratio: 1 / cos(30deg);
          background-color: crimson;
          clip-path: polygon(50% 100%, 100% 0, 0 0);
          content: "";
          height: 4cqi;
          position: absolute;
          place-self: start center;
          scale: 1.4;
        }

        & > * {
          position: absolute;
        }

        button {
          aspect-ratio: 1 / 1;
          background: hsla(0, 0%, 100%, 0.8);
          border: 0;
          border-radius: 50%;
          cursor: pointer;
          font-size: 5cqi;
          place-self: center;
          width: 20cqi;
        }

        ul {
          all: unset;
          clip-path: inset(0 0 0 0 round 50%);
          display: grid;
          inset: 0;
          place-content: center start;

          li {
            align-content: center;
            aspect-ratio: 1 / calc(2 * tan(180deg / var(--_items)));
            background: hsl(
              calc(360deg / var(--_items) * calc(var(--_idx))),
              100%,
              75%
            );
            clip-path: polygon(0% 0%, 100% 50%, 0% 100%);
            display: grid;
            font-size: 5cqi;
            grid-area: 1 / -1;
            padding-left: 1ch;
            rotate: calc(360deg / var(--_items) * calc(var(--_idx) - 1));
            transform-origin: center right;
            user-select: none;
            width: 50cqi;

            {% for task in tasks %}
              &:nth-of-type({{ loop.index }}) {
                --_idx: {{ loop.index }};
              }
            {% endfor %}
          }

        }
      }

      /* for demo */
      * {
        box-sizing: border-box;
      }
      body {
        font-family: system-ui, sans-serif;
        padding: 5cqi;
      }
    </style>
</head>
<body>
<script>
function spin() {


  const node = document.querySelector(".wheel")
  const spin = node.querySelector("button");
  const wheel = node.querySelector("ul");
  let animation;
  let previousEndDegree = 0;
  const randomAdditionalDegrees = Math.random() * 360 + 1800;
  const newEndDegree = previousEndDegree + randomAdditionalDegrees;

  animation = wheel.animate(
    [
      { transform: `rotate(${previousEndDegree}deg)` },
      { transform: `rotate(${newEndDegree}deg)` },
    ],
    {
      duration: 4000,
      direction: "normal",
      easing: "cubic-bezier(0.440, -0.205, 0.000, 1.130)",
      fill: "forwards",
      iterations: 1,
    },
  );

    previousEndDegree = newEndDegree;
}
</script>
<fieldset class="wheel">
  <ul>
    {% for task in tasks %}
    <li>{{ task }}</li>
    {% endfor %}
  </ul>
  <button id="button" onclick="spin(event)">SPIN</button>
</fieldset>
 </body>
</html>
"""

@app.route('/')
def home():
    """Serve the HTML page with tasks injected."""
    try:
        with open(TASKS_FILE, 'r') as file:
            tasks = [line.strip() for line in file.readlines() if line.strip()]
    except FileNotFoundError:
        tasks = []

    # Pass tasks as a JSON-like list to the template
    return render_template_string(HTML_TEMPLATE, tasks=tasks)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
