from manim import *
import numpy as np


class GraphTree(Scene):
    def construct(self):

        # =========================
        # Layout constants
        # =========================
        LEFT_X_BUFF = 0.3
        MID_X = -0.7
        RIGHT_X = 2.2
        INDENT_X = 0.45

        FONT = "DejaVu Sans"

        # =========================
        # Tree parameters (UPDATED)
        # =========================
        X_STEP = 1.4
        RADIUS = 0.07

        # ⬇️ UPDATED LEVEL SIZES
        level_sizes = [1, 5, 8, 11]
        level_ranges = [0.0, 1.5, 2.0, 2.5]

        # ⬇️ UPDATED CHILDREN PATTERN
        children_pattern = [
            [5],
            [2, 2, 1, 3, 0],   # 6 nodes
            [2, 1, 4, 1, 1, 2] # 9 nodes
        ]

        # =========================
        # Algorithm text
        # =========================
        def spacer(h=0.25):
            return Rectangle(width=0.01, height=h, fill_opacity=0, stroke_opacity=0)

        algo_data = [
            ("BFS(G, s)", 0),
            ("", 0),
            ("dist[s] = 0", 0),
            ("enqueue(Q, s)", 0),
            ("", 0),
            ("while Q not empty:", 0),
            ("u = dequeue(Q)", 1),
            ("for each neighbor v of u:", 1),
            ("if v not visited:  // (tree: skip)", 2),
            ("dist[v] = dist[u] + 1", 3),
            ("enqueue(Q, v)", 3),
        ]

        algo_lines = VGroup()
        indent_levels = []

        for text, indent in algo_data:
            line = spacer() if text == "" else Text(text, font=FONT, font_size=18)
            algo_lines.add(line)
            indent_levels.append(indent)

        algo_lines.arrange(DOWN, aligned_edge=LEFT)
        for line, indent in zip(algo_lines, indent_levels):
            line.shift(RIGHT * indent * INDENT_X)

        algo_lines.to_edge(LEFT, buff=LEFT_X_BUFF).to_edge(UP, buff=0.4)

        # =========================
        # Speed control
        # =========================
        nodes_built = 0

        def speed():
            if nodes_built < 4:
                return 5
            return max(0.05, 0.8 ** (nodes_built - 4))

        # =========================
        # Underline
        # =========================
        underline = Line(LEFT, RIGHT, stroke_width=3, color=YELLOW)

        def goto_line(i):
            target = Line(
                algo_lines[i].get_left(),
                algo_lines[i].get_right(),
                stroke_width=3,
                color=YELLOW
            ).shift(DOWN * 0.12)

            self.play(
                underline.animate.become(target),
                run_time=0.25 * speed()
            )

        # =========================
        # Queue
        # =========================
        queue_text = Text("Queue: []", font=FONT, font_size=20)
        queue_text.next_to(algo_lines, DOWN, buff=0.6)
        queue_text.align_to(algo_lines, LEFT)

        def update_queue(q):
            content = ", ".join(names[i] for i in q)
            new = Text(f"Queue: [{content}]", font=FONT, font_size=20)
            new.move_to(queue_text, aligned_edge=LEFT)
            return queue_text.animate.become(new)

        # =========================
        # Tree structure
        # =========================
        level_positions = []
        for lvl, (size, yr) in enumerate(zip(level_sizes, level_ranges)):
            ys = np.linspace(yr, -yr, size)
            xs = np.ones(size) * (lvl * X_STEP)
            level_positions.append([np.array([xs[i], ys[i], 0]) for i in range(size)])

        for lvl in range(len(level_positions)):
            for i in range(len(level_positions[lvl])):
                level_positions[lvl][i][0] -= level_positions[0][0][0]

        adjacency = {}
        node_positions = {}
        idx = 0
        for lvl in range(len(level_positions)):
            for p in level_positions[lvl]:
                adjacency[idx] = []
                node_positions[idx] = p
                idx += 1

        cur = 0
        nxt = 1
        for pat in children_pattern:
            for k in pat:
                for _ in range(k):
                    adjacency[cur].append(nxt)
                    nxt += 1
                cur += 1

        names = {i: chr(ord('A') + i) for i in node_positions}

        # =========================
        # Full tree
        # =========================
        full_tree = VGroup(
            *[Line(node_positions[u], node_positions[v], color=GREY)
              for u in adjacency for v in adjacency[u]],
            *[VGroup(
                Circle(radius=RADIUS, color=GREY, fill_opacity=1).move_to(p),
                Text(names[i], font=FONT, font_size=14).next_to(p, UP, buff=0.04)
            ) for i, p in node_positions.items()]
        ).scale(0.85).move_to([MID_X, 0, 0])

        # =========================
        # BFS tree
        # =========================
        bfs_nodes = {}

        def bfs_node(i, d):
            p = node_positions[i].copy()
            p[0] += RIGHT_X
            return VGroup(
                Circle(radius=RADIUS, color=BLUE, fill_opacity=1).move_to(p),
                Text(f"{names[i]} (d={d})", font=FONT, font_size=14).next_to(p, UP, buff=0.04)
            )

        # =========================
        # Show layout
        # =========================
        self.play(FadeIn(algo_lines), FadeIn(queue_text), FadeIn(full_tree), run_time=1.2)

        underline.become(
            Line(algo_lines[2].get_left(), algo_lines[2].get_right(), color=YELLOW)
            .shift(DOWN * 0.12)
        )
        self.add(underline)

        # =========================
        # BFS
        # =========================
        visited, dist, queue = set(), {}, []

        goto_line(2)
        visited.add(0)
        dist[0] = 0

        goto_line(3)
        queue.append(0)
        self.play(update_queue(queue), run_time=0.3)

        bfs_nodes[0] = bfs_node(0, 0)
        self.play(FadeIn(bfs_nodes[0]), run_time=0.4)
        nodes_built += 1

        while queue:
            goto_line(5)
            goto_line(6)
            u = queue.pop(0)
            self.play(update_queue(queue), run_time=0.25 * speed())

            goto_line(7)
            for v in adjacency[u]:
                goto_line(8)
                if v not in visited:
                    visited.add(v)

                    goto_line(9)
                    dist[v] = dist[u] + 1

                    edge = Line(
                        bfs_nodes[u][0].get_center(),
                        node_positions[v] + RIGHT * RIGHT_X,
                        color=BLUE
                    )
                    self.play(Create(edge), run_time=0.25 * speed())

                    bfs_nodes[v] = bfs_node(v, dist[v])
                    self.play(FadeIn(bfs_nodes[v]), run_time=0.25 * speed())
                    nodes_built += 1

                    goto_line(10)
                    queue.append(v)
                    self.play(update_queue(queue), run_time=0.2 * speed())

        # =========================
        # Final freeze
        # =========================
        self.wait(4)
