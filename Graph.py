import tkinter as tk
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib import cm
import numpy as np
from tkinter import *
import ctypes

ctypes.windll.shcore.SetProcessDpiAwareness(1)

root = tk.Tk()
root.title("Complete Graph Of N Points")
root.geometry('1080x720')

frame = tk.Frame(root)  # buttons and stuff go here
frame.grid(row=0, column=0, sticky=N)
root.grid_rowconfigure(0, weight=5)
root.grid_columnconfigure(0, weight=2)

plot_frame = tk.Frame(root)  # plot window goes here
plot_frame.grid(row=0, column=3, rowspan=1, columnspan=2)
root.grid_columnconfigure(1, weight=1)

toolbarFrame = Frame(master=root)  # toolbar goes here
toolbarFrame.grid(row=2, column=0, columnspan=2, sticky=W)

# --- variable assignment ---
rand_var = tk.BooleanVar(name="Random Generation", value=False)
circ_var = tk.BooleanVar(name="Circle Lock", value=True)
point_var = tk.StringVar(name="Number of Points", value="6")
width_var = tk.StringVar(name="Width of Lines", value="0.003")
x_l_lim_var = tk.StringVar(name="x lower lim", value="-1")
x_u_lim_var = tk.StringVar(name="x upper lim", value="1")
y_l_lim_var = tk.StringVar(name="y lower lim", value="-1")
y_u_lim_var = tk.StringVar(name="y upper lim", value="1")

# --- labels and fields ---
label_names = ["Number of Points", "Line Width", "x lower limit", "x upper limit", "y lower limit", "y upper limit"]

for i in label_names:
    tk.Label(frame, text=i).grid(sticky="W", row=label_names.index(i), column=0)

text_vars = [point_var, width_var, x_l_lim_var, x_u_lim_var, y_l_lim_var, y_u_lim_var]

for i in text_vars:
    tk.Entry(frame, textvariable=i, width=10).grid(sticky="W", row=text_vars.index(i), column=1)

check_vars = [rand_var, circ_var]
check_labels = ["Random Generation", "Circle Lock"]

row_start = len(label_names)  # the minus 1 because .grid positions start at 1
for a, b in zip(check_labels, check_vars):  # iterates through both check_vars and check_labels at once
    tk.Checkbutton(frame, text=a, variable=b, onvalue=True, offvalue=False).grid(sticky="W", row=row_start, column=0)
    row_start += 1

# --- figures/frames to be placed in the root window ---
fig = Figure(figsize=(5, 5), dpi=100, facecolor='white', tight_layout=True)
canvas = FigureCanvasTkAgg(fig, master=plot_frame)  # A tk.DrawingArea.

toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)  # helpful toolbar to let people zoom in and stuff
toolbar.grid(row=1, column=2, ipadx=10)


# --- misc ---
def t_point(p, s_1, s_2):  # transforms numbers (p) from s_1 = [a,b] to s_2 = [c,d] using a linear transformation
    return (((p - s_1[0]) * (s_2[1] - s_2[0])) / (s_1[1] - s_1[0])) + s_2[0]


def avg(s):  # finds mean of a list
    count = 0
    total = 0
    while count < len(s):
        total += s[count]
        count += 1
    return total / len(s)


def lineavg(val):
    rand_gui = rand_var.get()
    circ_gui = circ_var.get()
    x_l_lim_gui = int(x_l_lim_var.get())
    x_u_lim_gui = int(x_u_lim_var.get())
    y_l_lim_gui = int(y_l_lim_var.get())
    y_u_lim_gui = int(y_u_lim_var.get())


    counting = 0

    x_list = (int(val) + counting) * [0]
    y_list = (int(val) + counting) * [0]

    if rand_gui and circ_gui:
        for i in range(0, len(x_list)):
            t = np.random.uniform(0, 2 * np.pi)
            x_list[i] = np.cos(t) * x_u_lim_gui
            y_list[i] = np.sin(t) * y_u_lim_gui
    if (rand_gui is True) and (circ_gui is False):
        for i in range(0, len(x_list)):
            x_list[i] = np.random.uniform(x_l_lim_gui, x_u_lim_gui)
            y_list[i] = np.random.uniform(y_l_lim_gui, y_u_lim_gui)
    if (rand_gui is False) and (circ_gui is True):
        for i in range(0, len(x_list)):
            t = t_point(i, [0, len(x_list)], [0, 2 * np.pi])
            x_list[i] = np.cos(t) * x_u_lim_gui
            y_list[i] = np.sin(t) * y_u_lim_gui
    if (rand_gui is False) and (circ_gui is False):
        print("Please have at least one checkbox selected.")

    lengths = []
    p = 0
    while p <= len(x_list):
        q = len(x_list)
        while q >= 0:
            distV = np.sqrt(
                ((x_list[p - 1] - x_list[q - 1]) * (x_list[p - 1] - x_list[q - 1])) +
                (y_list[p - 1] - y_list[q - 1]) * (y_list[p - 1] - y_list[q - 1])
            )  # distance of each line as it is generated
            lengths.append(distV)
            q -= 1
        p += 1

    return avg(lengths)


# --- update function ---
def update():
    fig.clear()

    counting = 0

    # --- variable updaters ---
    rand_gui = rand_var.get()
    point_gui = point_var.get()
    width_gui = width_var.get()
    circ_gui = circ_var.get()
    x_l_lim_gui = int(x_l_lim_var.get())
    x_u_lim_gui = int(x_u_lim_var.get())
    y_l_lim_gui = int(y_l_lim_var.get())
    y_u_lim_gui = int(y_u_lim_var.get())

    x_list = (int(point_gui) + counting) * [0]
    y_list = (int(point_gui) + counting) * [0]

    # --- assigning random points ---
    if rand_gui and circ_gui:
        for i in range(0, len(x_list)):
            t = np.random.uniform(0, 2 * np.pi)
            x_list[i] = np.cos(t) * x_u_lim_gui
            y_list[i] = np.sin(t) * y_u_lim_gui
    if (rand_gui is True) and (circ_gui is False):
        for i in range(0, len(x_list)):
            x_list[i] = np.random.uniform(x_l_lim_gui, x_u_lim_gui)
            y_list[i] = np.random.uniform(y_l_lim_gui, y_u_lim_gui)
    if (rand_gui is False) and (circ_gui is True):
        for i in range(0, len(x_list)):
            t = t_point(i, [0, len(x_list)], [0, 2 * np.pi])
            x_list[i] = np.cos(t) * x_u_lim_gui
            y_list[i] = np.sin(t) * y_u_lim_gui
    if (rand_gui is False) and (circ_gui is False):
        print("Please have at least one checkbox selected.")

    # --- plotting ---
    splot = fig.add_subplot()
    splot.axis('Equal')
    splot.grid(False)
    # splot.axis('off')
    splot.set_xlim([-1, 1])
    splot.set_ylim([-1, 1])

    splot.scatter(x_list, y_list, color='blue', s=10)

    # setting up colormap for lines
    cmap = cm.get_cmap('hot_r')
    # I need to get the length of any given line and scale it to fit within [0,1]

    # initializing list of lengths to find average
    lengths = []

    p = 0
    while p <= len(x_list):
        q = len(x_list)
        while q >= 0:
            V = np.array([[
                (x_list[p - 1] - x_list[q - 1]), (y_list[p - 1] - y_list[q - 1])
            ]])
            distV = np.sqrt(
                ((x_list[p - 1] - x_list[q - 1]) * (x_list[p - 1] - x_list[q - 1])) +
                (y_list[p - 1] - y_list[q - 1]) * (y_list[p - 1] - y_list[q - 1])
            )  # distance of each line as it is generated
            lengths.append(distV)
            distVnorm = t_point(distV, [0, 1.6], [0, 1])  # normalized distance to [0,1]
            splot.quiver(
                x_list[q - 1], y_list[q - 1], V[:, 0], V[:, 1], color=cmap(distVnorm),
                angles='xy', scale_units='xy', scale=1,
                headwidth=1, headlength=0,
                width=float(width_gui))
            q -= 1
        p += 1

    print(avg(lengths))

    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=0)


def avgplot():
    point_gui = int(point_var.get())
    x_l_lim_gui = int(x_l_lim_var.get())
    x_u_lim_gui = int(x_u_lim_var.get())
    y_l_lim_gui = int(y_l_lim_var.get())
    y_u_lim_gui = int(y_u_lim_var.get())
    circ_gui = circ_var.get()

    fig.clear()

    x_range = range(1, point_gui)
    y_range = []
    y_range2 = []

    for element in x_range:
        y_range.append(lineavg(element))

    distx = abs(x_u_lim_gui) + abs(x_l_lim_gui)
    disty = abs(y_u_lim_gui) + abs(y_l_lim_gui)

    splot = fig.add_subplot()
    # splot.axis('Equal')
    splot.grid(False)
    if circ_gui:
        splot.title.set_text("Average Length of Random Line in " + str(distx) + "x" + str(disty) + " Oval")
    else:
        splot.title.set_text("Average Length of Random Line in " + str(distx) + "x" + str(disty) + " Box")
    # splot.axis('off')
    splot.set_xlabel("# of Points")
    splot.set_ylabel("Length")
    splot.set_xlim([-1, point_gui + 1])
    splot.set_ylim([-1, y_u_lim_gui + 1])

    splot.scatter(x_range, y_range, color='blue', s=10)

    for element in x_range:  # creating a constant function to estimate convergence
        y_range2.append(np.sqrt(np.pi / 2))

    splot.scatter(x_range, y_range2, s=5)

    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=0)


# --- key press handler ---
def return_key_pressed(event):
    update()


def plus_points():
    point_var.set(str(int(point_var.get()) + 1))
    update()


def minus_points():
    if int(point_var.get()) > 1:
        point_var.set(str(int(point_var.get()) - 1))
        update()
    else:
        point_var.set("0")
        update()


def save_fig():
    fig.savefig(
        "Saved Graphs/(points_" + str(point_var.get()) + "_rand_" + str(rand_var.get()) + ").png",
        dpi=200,
        bbox_inches='tight',
        pad_inches=0
    )


root.bind("<Return>", return_key_pressed)

submit_button = Button(master=frame, text="Update", command=update)
submit_button.bind("<Return>", return_key_pressed)
submit_button.grid(row=len(text_vars) + len(check_vars), column=0)

plus_button = Button(master=frame, text="+", command=plus_points)
plus_button.grid(row=0, column=2)

minus_button = Button(master=frame, text="-", command=minus_points)
minus_button.grid(row=0, column=3)

avgplot_button = Button(master=frame, text="AvgPlot", command=avgplot)
avgplot_button.grid(row=len(text_vars) + len(check_vars) + 1, column=0)

savefig_button = Button(master=frame, text="Save graph as .png", command=save_fig)
savefig_button.grid(row=len(text_vars) + len(check_vars) + 2, column=0)

root.mainloop()
