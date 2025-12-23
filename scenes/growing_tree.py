from manim import *
import numpy as np


class GrowingTree(Scene):
    def construct(self):

        FONT = "DejaVu Sans Mono"
        RADIUS = 0.1

        GRAPH_SHIFT = UP * 1.2 + RIGHT * 0.2
        TREE_SHIFT = RIGHT * 5

        SLOW = 0.8

        # =========================
        # 1. BFS – Mathematical Form
        # =========================
        algo_data = [
            ("BFS(G = (V,E), s)", 0),
            ("dist(s) ← 0 ,  Q ← [s]", 0),
            ("", 0),
            ("while Q ≠ ∅:", 0),
            ("u ← pop(Q)", 1),
            ("for all v ∈ N(u):", 1),
            ("if v ∉ Visited:", 2),
            ("Visited ← Visited ∪ {v}", 3),
            ("dist(v) ← dist(u) + 1", 3),
            ("push(Q, v)", 3),
        ]

        algo_lines = VGroup()
        indents = []

        for text, indent in algo_data:
            if text == "":
                line = Rectangle(width=0.01, height=0.28, fill_opacity=0, stroke_opacity=0)

            else:
                line = Text(text, font=FONT, font_size=12, weight=BOLD)

            algo_lines.add(line)
            indents.append(indent)

        algo_lines.arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        for line, indent in zip(algo_lines, indents):
            line.shift(RIGHT * 0.6 * indent)

        algo_lines.to_edge(LEFT, buff=0.4).to_edge(UP, buff=0.3)

        underline = Line(
            algo_lines[0].get_left(),
            algo_lines[0].get_right(),
            color=YELLOW,
            stroke_width=3
        ).shift(DOWN * 0.15)

        def goto_line(i):
            self.play(
                underline.animate.become(
                    Line(
                        algo_lines[i].get_left(),
                        algo_lines[i].get_right(),
                        color=YELLOW,
                        stroke_width=3
                    ).shift(DOWN * 0.15)
                ),
                run_time=SLOW
            )

        # =========================
        # 2. Graph definition (LEFT – STATIC)
        # =========================
        adjacency = {
            0: [1, 2],
            1: [0, 3, 4],
            2: [0, 5, 6],
            3: [1, 7],
            4: [1, 7, 8],
            5: [2, 8],
            6: [2, 9],
            7: [3, 4, 10],
            8: [4, 5, 11],
            9: [6],
            10: [7],
            11: [8],
        }
        adjacency[10].append(8)
        adjacency[8].append(10)

        adjacency[6].append(5)
        adjacency[5].append(6)

        adjacency[9].append(11)
        adjacency[11].append(9)

        names = {i: chr(65 + i) for i in adjacency}

        node_pos = {
            0: np.array([-0.8, 0.4, 0]),
            1: np.array([-1.8, 1.2, 0]),
            2: np.array([0.2, 1.2, 0]),
            3: np.array([-2.8, 0.2, 0]),
            4: np.array([-1.8, -0.6, 0]),
            5: np.array([0.2, 0.2, 0]),
            6: np.array([1.2, -0.6, 0]),
            7: np.array([-2.8, -1.4, 0]),
            8: np.array([-0.8, -1.6, 0]),
            9: np.array([1.2, -1.6, 0]),
            10: np.array([-1.8, -2.4, 0]),
            11: np.array([0.2, -2.4, 0]),
        }

        node_mobs = {}
        node_group = VGroup()
        edge_group = VGroup()

        for i, p in node_pos.items():
            c = Circle(RADIUS, color=WHITE, fill_opacity=1,stroke_width=1).move_to(p)
            c.set_fill(BLUE_E)
            t = Text(names[i], font=FONT, font_size=16).next_to(c, UP, buff=0.08)
            node_mobs[i] = VGroup(c, t)
            node_group.add(node_mobs[i])

        for u in adjacency:
            for v in adjacency[u]:
                if u < v:
                    edge_group.add(
                        Line(
                            node_mobs[u][0].get_center(),
                            node_mobs[v][0].get_center(),
                            color=GREY,
                            stroke_width=2
                        )
                    )

        graph = VGroup(edge_group, node_group).shift(GRAPH_SHIFT)

        # =========================
        # 3. BFS Tree (RIGHT – ACTIVE)
        # =========================
        bfs_nodes = {}
        bfs_edges = VGroup()
        dist_labels = {}

        for i in node_pos:
            bfs_nodes[i] = node_mobs[i].copy()

        bfs_group = VGroup(bfs_edges, *bfs_nodes.values())
        bfs_group.move_to(graph.get_center() + TREE_SHIFT)

        # =========================
        # 4. Queue
        # =========================
        queue_text = Text("Q = ∅", font=FONT, font_size=18)
        queue_text.next_to(VGroup(graph, bfs_group), DOWN, buff=0.4)

        def update_queue(q):
            new = Text(f"Q = [{', '.join(names[i] for i in q)}]", font=FONT, font_size=18)
            new.move_to(queue_text)
            return queue_text.animate.become(new)

        # =========================
        # Legend (color meaning)
        # =========================
        legend_items = [
            (BLUE_E, "Unvisited"),
            (YELLOW, "Visited"),
        ]

        legend = VGroup()
        for color, text in legend_items:
            dot = Circle(
                radius=0.08,
                fill_opacity=1,
                color=color
            ).set_fill(color)
            label = Text(text, font=FONT, font_size=14)
            item = VGroup(dot, label).arrange(RIGHT, buff=0.15)
            legend.add(item)

        legend.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        legend.to_corner(DL, buff=0.3)

        # =========================
        # 5. Static layout
        # =========================
        self.play(FadeIn(algo_lines), FadeIn(graph), FadeIn(queue_text),FadeIn(legend), run_time=1.2)
        self.add(underline)
        goto_line(0)


        # =========================
        # 6. BFS Animation
        # =========================
        visited = set()
        queue = []
        dist = {0: 0}

        goto_line(1)
        visited.add(0)
        queue.append(0)
        node_mobs[0][0].set_fill(YELLOW)

        self.play(update_queue(queue), run_time=SLOW)

        label0 = Text("0", font=FONT, font_size=14).next_to(bfs_nodes[0], UP, buff=0.1)
        dist_labels[0] = label0
        bfs_group.add(label0)

        self.play(FadeIn(bfs_nodes[0]), FadeIn(label0), run_time=SLOW)

        active_circle = None
        active_circle_left = None

        while queue:
            goto_line(4)  # u ← pop(Q)
            u = queue.pop(0)
            self.play(update_queue(queue), run_time=SLOW)

            # ✅ סימון אדום רק בגרף השמאלי על u (הקודקוד שממנו עוברים על שכנים)
            if active_circle_left:
                self.play(FadeOut(active_circle_left), run_time=0.2)

            active_circle_left = Circle(
                radius=RADIUS * 1.6,
                color=RED,
                stroke_width=4
            ).move_to(node_mobs[u][0].get_center())

            self.play(FadeIn(active_circle_left), run_time=0.2)

            goto_line(5)  # for all v ∈ N(u):
            for v in adjacency[u]:

                goto_line(6)  # if v ∉ Visited:
                if v not in visited:
                    # =========================
                    # Visited
                    # =========================
                    goto_line(7)  # Visited ← Visited ∪ {v}
                    visited.add(v)

                    # 🔴 צביעה — רק בגרף השמאלי
                    node_mobs[v][0].set_fill(YELLOW)

                    # 🔵 בנייה מיידית בגרף הימני
                    edge = Line(
                        bfs_nodes[u][0].get_center(),
                        bfs_nodes[v][0].get_center(),
                        color=GREY,
                        stroke_width=2
                    )

                    bfs_edges.add(edge)

                    self.play(
                        FadeIn(bfs_nodes[v]),  # קודקוד ימין
                        Create(edge),  # צלע ימין
                        run_time=SLOW
                    )

                    # =========================
                    # Distance
                    # =========================
                    goto_line(8)  # dist(v) ← dist(u) + 1
                    dist[v] = dist[u] + 1

                    lbl = Text(
                        str(dist[v]),
                        font=FONT,
                        font_size=14
                    ).next_to(bfs_nodes[v], UP, buff=0.1)

                    dist_labels[v] = lbl
                    bfs_group.add(lbl)

                    self.play(FadeIn(lbl), run_time=SLOW)

                    # =========================
                    # Push to queue
                    # =========================
                    goto_line(9)  # push(Q, v)
                    queue.append(v)
                    self.play(update_queue(queue), run_time=SLOW)
        # =========================
        # 7. Final transition
        # =========================
        title = Text("BFS Distance Tree", font=FONT, font_size=28).to_edge(UP)

        self.play(
            FadeOut(algo_lines),
            FadeOut(underline),
            FadeOut(queue_text),
            FadeOut(legend),
            FadeOut(active_circle_left) if active_circle_left else FadeOut(
                VGroup()),
            run_time=1
        )

        self.play(
            graph.animate.scale(1.3).to_edge(LEFT, buff=0.6),
            bfs_group.animate.scale(1.3).to_edge(RIGHT, buff=0.6),
            FadeIn(title),
            run_time=1.5
        )

        self.wait(3)
