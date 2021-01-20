import matplotlib.pyplot as plt
import numpy as np

def display_rgb(rgb_tuple)->None:


    plt.rcdefaults()
    fig, ax = plt.subplots()

# Example data
    people = ('Tom', 'Dick', 'Harry', 'Slim', 'Jim')
    y_pos = np.arange(len(people))
    performance = 3 + 10 * np.random.rand(len(people))
    error = np.random.rand(len(people))

    ax.barh(y_pos, performance, xerr=error, align='center', color=[rgb_tuple])
    ax.set_yticks(y_pos)
    ax.set_yticklabels(people)
    ax.invert_yaxis()  # labels read top-to-bottom
    plt.show()
    fig.savefig(f"./data/{rgb_tuple}.jpeg")