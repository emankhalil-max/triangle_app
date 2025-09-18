from flask import Flask, render_template, request, url_for, Response
import matplotlib
matplotlib.use('Agg')  
import matplotlib.pyplot as plt
import io
import math

app = Flask(__name__)

# Storing the triangle sides globally
triangle_sides = None

# ===== Triangle class =====
class Triangle:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def is_valid(self):
        return self.a + self.b > self.c and self.a + self.c > self.b and self.b + self.c > self.a

    def type(self):
        if self.a == self.b == self.c:
            return "Equilateral"
        elif self.a == self.b or self.a == self.c or self.b == self.c:
            return "Isosceles"
        else:
            return "Scalene"

    def perimeter(self):
        return self.a + self.b + self.c

    def area(self):
        s = self.perimeter() / 2
        return round(math.sqrt(s * (s - self.a) * (s - self.b) * (s - self.c)), 2)

# ===== Flask Routes =====
@app.route("/", methods=["GET", "POST"])
def index():
    global triangle_sides
    result = {}

    if request.method == "POST":
        try:
            a = float(request.form["a"])
            b = float(request.form["b"])
            c = float(request.form["c"])
            triangle = Triangle(a, b, c)

            if triangle.is_valid():
                result["type"] = triangle.type()
                result["perimeter"] = triangle.perimeter()
                result["area"] = triangle.area()
                triangle_sides = (a, b, c)
            else:
                result["error"] = "Not a valid triangle."
                triangle_sides = None
        except:
            result["error"] = "Please enter valid numbers."
            triangle_sides = None

    return render_template("index.html", result=result)

@app.route("/plot_triangle")
def plot_triangle():
    global triangle_sides
    if not triangle_sides:
        return "No triangle to display", 400

    a, b, c = triangle_sides

    # Triangle coordinates
    A = (0, 0)
    B = (c, 0)
    # Cosine rule to find angle at B
    cos_angle = (a**2 + c**2 - b**2) / (2 * a * c)
    cos_angle = max(min(cos_angle, 1), -1)
    angle = math.acos(cos_angle)
    C = (a * math.cos(angle), a * math.sin(angle))

    # Plotting triangle
    fig, ax = plt.subplots()
    x = [A[0], B[0], C[0], A[0]]
    y = [A[1], B[1], C[1], A[1]]
    ax.plot(x, y, "b-", linewidth=2)
    ax.fill(x, y, "skyblue", alpha=0.5)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("Your Triangle", fontsize=14)

    # Returning image
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    return Response(buf.getvalue(), mimetype="image/png")

if __name__ == "__main__":
    app.run(debug=True)
