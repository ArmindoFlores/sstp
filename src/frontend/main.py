import matplotlib.pyplot as plt


def main():
    with open("points.txt", "r") as f:
        data = f.readlines()
    data[:] = map(
        eval,
        filter(
            lambda line: line != "\n",
            data
        )
    )
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.grid()
    
    for point in data:
        ax.scatter(*point, color="red")
    
    lim = (min(min(p[0] for p in data), min(p[1] for p in data))-0.5, max(max(p[0] for p in data), max(p[1] for p in data))+0.5)    
    
    ax.set_aspect("equal")
    ax.set_xlim(lim)
    ax.set_ylim(lim)
    
    fig.savefig("result.png", bbox_inches="tight")


if __name__ == "__main__":
    main()