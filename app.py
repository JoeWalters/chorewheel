from flask import Flask, render_template_string
import math

app = Flask(__name__)

# Path to the text file containing tasks
TASKS_FILE = 'tasks.txt'

# HTML Template with fixed desktop and mobile sizes
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chore Wheel</title>
    <style>
        body {
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: Arial, sans-serif;
            height: 100vh;
            background-color: #f0f0f0;
            overflow: hidden;
        }

        .wheel-container {
            position: relative;
            width: 80vmin; /* Default size for most devices */
            height: 80vmin;
            border-radius: 50%;
            overflow: hidden;
        }

        /* Desktop-specific size adjustment */
        @media (min-width: 1024px) {
            .wheel-container {
                width: 500px;
                height: 500px;
            }
        }

        .wheel {
            position: relative;
            width: 100%;
            height: 100%;
            border-radius: 50%;
            border: 5px solid #ccc;
            overflow: hidden;
        }

        .wheel svg {
            width: 100%;
            height: 100%;
        }

        .spin-button {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 15%;
            height: 15%;
            border: none;
            border-radius: 50%;
            background-color: crimson;
            color: white;
            font-size: 1.2rem;
            font-weight: bold;
            cursor: pointer;
            z-index: 2;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
        }

        .indicator {
            position: absolute;
            top: -20px;
            left: 50%;
            transform: translateX(-50%);
            width: 0;
            height: 0;
            border-left: 15px solid transparent;
            border-right: 15px solid transparent;
            border-bottom: 25px solid crimson;
            z-index: 3;
        }
    </style>
</head>
<body>
    <div class="wheel-container">
        <div class="indicator"></div>
        <div class="wheel">
            <svg id="wheel" viewBox="0 0 500 500">
                <g id="wheel-group" style="transform-origin: 250px 250px;">
                    {% for task in tasks %}
                    {% set index = loop.index0 %}
                    {% set total = tasks|length %}
                    {% set angle = 360 / total %}
                    {% set start_angle = index * angle %}
                    {% set end_angle = (index + 1) * angle %}
                    {% set radius = 250 %}
                    <path d="M250,250 L{{ 250 + 250 * math.cos(math.radians(start_angle)) }},{{ 250 + 250 * math.sin(math.radians(start_angle)) }} 
                             A250,250 0 {{ 1 if angle > 180 else 0 }},1 {{ 250 + 250 * math.cos(math.radians(end_angle)) }},{{ 250 + 250 * math.sin(math.radians(end_angle)) }} Z"
                          fill="hsl({{ (360 / total) * index }}, 70%, 80%)"></path>
                    <text x="{{ 250 + 150 * math.cos(math.radians(start_angle + angle / 2)) }}"
                          y="{{ 250 + 150 * math.sin(math.radians(start_angle + angle / 2)) }}"
                          text-anchor="middle" alignment-baseline="middle"
                          transform="rotate({{ start_angle + angle / 2 }}, {{ 250 + 150 * math.cos(math.radians(start_angle + angle / 2)) }}, {{ 250 + 150 * math.sin(math.radians(start_angle + angle / 2)) }})"
                          style="font-size: 14px; font-family: Arial; fill: black;">
                        {{ task }}
                    </text>
                    {% endfor %}
                </g>
            </svg>
        </div>
        <button class="spin-button" onclick="spin()">SPIN</button>
    </div>

    <script>
        let previousRotation = 0;

        function spin() {
            const wheelGroup = document.getElementById('wheel-group');
            const tasks = {{ tasks | tojson }};
            const totalTasks = tasks.length;

            // Calculate rotation
            const spins = Math.floor(Math.random() * 5) + 5; // 5-10 full spins
            const randomRotation = Math.random() * 360;
            const totalRotation = spins * 360 + randomRotation;

            // Rotate the wheel
            wheelGroup.style.transition = "transform 4s cubic-bezier(0.25, 1, 0.5, 1)";
            wheelGroup.style.transform = `rotate(${previousRotation + totalRotation}deg)`;

            // Determine the winning task
            setTimeout(() => {
                const normalizedRotation = (totalRotation % 360);
                const segmentAngle = 360 / totalTasks;
                const winningIndex = Math.floor((360 - normalizedRotation + segmentAngle / 2) / segmentAngle) % totalTasks;

                alert(`Selected Task: ${tasks[winningIndex]}`);
            }, 4000);

            previousRotation += totalRotation;
        }
    </script>
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
        tasks = ["No tasks available"]

    return render_template_string(HTML_TEMPLATE, tasks=tasks, math=math)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)