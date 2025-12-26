import turtle

def push_state(t: turtle.Turtle) -> tuple[tuple[float, float], float]:
    # Save current turtle state (position + heading)
    return (t.position(), t.heading())


def pop_state(t: turtle.Turtle, state: tuple[tuple[float, float], float]) -> None:
    # Restore turtle state (position + heading) without drawing
    (pos, heading) = state
    t.penup()
    t.setposition(pos)
    t.setheading(heading)
    t.pendown()


def draw_y_tip(t: turtle.Turtle, length: float, tip_angle: float) -> None:
    # Draw a small Y-shaped tip at the end of a branch
    state = push_state(t)

    t.left(tip_angle)
    t.forward(length)
    t.backward(length)

    pop_state(t, state)

    t.right(tip_angle)
    t.forward(length)
    t.backward(length)

    pop_state(t, state)


def pythagoras_tree_lines(
    t: turtle.Turtle,
    order: int, # recursion depth
    length: float, # current branch length
    split_angle: float = 30.0, #angle between left/right branches 
    shrink: float = 0.72, # length multiplier for next recursion
    tip_ratio: float = 0.25, # size of small Y tips at leaves
    tip_angle: float = 25.0, # angle of the Y tips
) -> None:
    
    if order == 0:
        # Draw the leaf tip (Y-shape) at the end of the final branch
        t.forward(length)
        draw_y_tip(t, length * tip_ratio, tip_angle)
        t.backward(length)
        return

    # Draw the main branch forward
    t.forward(length)

    # Decrease pen size as depth grows for cleaner view
    old_size = t.pensize()
    t.pensize(max(1, old_size - 1))

    # Save state at branch end, then draw left + right sub-branches
    state = push_state(t)

    t.left(split_angle)
    pythagoras_tree_lines(
        t, order - 1, length * shrink, split_angle, shrink, tip_ratio, tip_angle
    )

    pop_state(t, state)

    t.right(split_angle)
    pythagoras_tree_lines(
        t, order - 1, length * shrink, split_angle, shrink, tip_ratio, tip_angle
    )

    pop_state(t, state)

    # Restore pen size and go back to branch start
    t.pensize(old_size)
    t.backward(length)


def draw_tree(level: int) -> None:
    screen = turtle.Screen()
    screen.bgcolor("white")
    screen.title("Pythagoras Tree (line-based, recursion)")

    t = turtle.Turtle()
    t.hideturtle()
    t.speed(0)
    t.pencolor("#7a2e2e")
    t.pensize(6)

    # Start from bottom center, point upward
    t.penup()
    t.goto(0, -320)
    t.setheading(90)
    t.pendown()

    pythagoras_tree_lines(
        t,
        order=level,
        length=140,
        split_angle=35.0,
        shrink=0.72,
        tip_ratio=0.22,
        tip_angle=25.0,
    )

    screen.mainloop()


if __name__ == "__main__":
    while True:
        try:
            level = int(input("Point level of recursion: "))
            if level < 0:
                raise ValueError
            break
        except ValueError:
            print("Only non-negative integers are accepted!")

    draw_tree(level)