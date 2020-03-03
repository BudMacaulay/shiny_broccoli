import ternary
import matplotlib

fig, tax = ternary.figure()

tax.set_title("Scatter Plot", fontsize=20)
tax.scatter(points, marker='s', color='red', label="Red Squares")
tax.legend()
