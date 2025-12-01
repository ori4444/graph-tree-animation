from manim import *
import numpy as np


class GraphTree(Scene):
    def construct(self):

        # this is like how much tree go right
        X_STEP = 1.4

        RADIUS = 0.07

        # edges thickness
        STROKE = 1

        # how many nodes in ech lvl
        level_sizes = [1, 5, 9, 13, 22]

        level_ranges = [0.0, 1.5, 2.0, 2.5, 3.0]

        children_pattern = [
            [5],
            [2, 2, 1, 2, 2],
            [2, 1, 2, 1, 2, 1, 2, 1, 1],
            [2, 2, 2, 1, 2, 2, 2, 1, 2, 2, 2, 1, 1]
        ]

        def node(p):
            return Circle(radius=RADIUS, color=WHITE, fill_opacity=1).move_to(p)

        level_positions = []
        for level, (size, yr) in enumerate(zip(level_sizes, level_ranges)):
            ys = np.linspace(yr, -yr, size)
            xs = np.ones(size) * (level * X_STEP)
            level_positions.append(
                [np.array([xs[i], ys[i], 0]) for i in range(size)]
            )

        shift_x = -level_positions[0][0][0]
        for lvl in range(len(level_positions)):
            for i in range(len(level_positions[lvl])):
                x, y, z = level_positions[lvl][i]
                level_positions[lvl][i] = np.array([x + shift_x, y, 0])

        level_nodes = []

        # root node
        root = node(level_positions[0][0])
        level_nodes.append([root])

        label = Text(
            "Tree graph",
            font_size=32,
            font="Montserrat",
            color=WHITE
        )

        label.move_to(root.get_center() + LEFT * 4 + RIGHT * 0.6)

        # show label first
        self.play(FadeIn(label), run_time=1.0)

        # now show the root
        self.play(FadeIn(root), run_time=1.6)

        # build rest levels
        for lvl in range(1, len(level_positions)):

            prev_nodes = level_nodes[lvl - 1]
            prev_pos = level_positions[lvl - 1]
            curr_pos = level_positions[lvl]

            pattern = children_pattern[lvl - 1]

            P = len(prev_pos)
            C = len(curr_pos)

            assert sum(pattern) == C, "pattern mismatch!! kids not same count"

            print(f"\nLEVEL {lvl}, P={P}, C={C}")
            print("pattern:", pattern)

            child_to_parent = []
            for parent_idx, num_kids in enumerate(pattern):
                child_to_parent += [parent_idx] * num_kids

            print("child → parent mapping:", child_to_parent)

            edges = []
            curr_nodes = []

            for i, p in enumerate(curr_pos):
                parent_idx = child_to_parent[i]
                parent_node = prev_nodes[parent_idx]

                edges.append(Line(parent_node.get_center(), p, stroke_width=STROKE))
                curr_nodes.append(node(p))

            self.play(*[Create(e) for e in edges], run_time=1.6)
            self.play(*[FadeIn(n) for n in curr_nodes], run_time=1.2)

            level_nodes.append(curr_nodes)

        self.wait(1.7)
