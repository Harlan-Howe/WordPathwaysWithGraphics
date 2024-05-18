import math
import random
from typing import List, Tuple
import cv2
import numpy as np
from WordPathKeeperFile import Word_Pair

neutral_radius = 40
edge_attraction_factor = 0.00075
edge_repulsion_multiplier = 0
mutual_repulsion_factor = 0.5
border_force = 15
border_range = 10
max_effective_d_for_edges = 100.0
min_movement = 0.0125
canvas_size = 800

class WordGraphVisualizer:

    def __init__(self, words, edges:List[Word_Pair]):
        self.words = words
        self.edges = edges
        self.word_locs: List[List[float]] = []
        for i in range(len(words)):
            new_value:List[float] = [random.randint(0,canvas_size),random.randint(0,canvas_size)]
            self.word_locs.append(new_value)
        self.net_forces: List[List[float]] = [[0, 0] for i in range(len(self.words))]
    def draw_graph(self):
        canvas = np.zeros((canvas_size,canvas_size,3),dtype=float)
        for edge in self.edges:
            u: List[float] = self.word_locs[edge[0]]
            v: List[float] = self.word_locs[edge[1]]
            cv2.line(img=canvas, pt1=(int(u[0]), int(u[1])),
                     pt2=(int(v[0]), int(v[1])), color=(1.0, 1.0, 1.0), thickness= 1)

        for word_id in range(len(self.words)):
            cv2.line(img=canvas, pt1 = (int(self.word_locs[word_id][0]), int(self.word_locs[word_id][1])),
                     pt2 = (int(self.word_locs[word_id][0]+self.net_forces[word_id][0]),
                            int(self.word_locs[word_id][1]+self.net_forces[word_id][1])),
                     color = (0.0,0.0,1.0), thickness = 2)


        for word_id in range(len(self.words)):
            cv2.putText(img=canvas,text=self.words[word_id],org=(int(self.word_locs[word_id][0]-10),
                                                            int(self.word_locs[word_id][1]-5)),
                        fontFace=cv2.FONT_HERSHEY_PLAIN,
                        fontScale= 1,
                        color=(0,1.0,0))



        cv2.imshow("canvas",canvas)
        cv2.waitKey(2)

    def find_net_forces(self):
        self.net_forces:List[List[float]] = [[0, 0] for i in range(len(self.words)) ]


        for word_id in range(len(self.words)):
            for edge in self.edges:
                if edge[0] == word_id or edge[1] == word_id:
                    F = self.force_from_edge(edge, attraction_factor=0.00075, repulsion_multiplier=-3,forward= True)
                    if edge[0] == word_id:
                        self.net_forces[word_id][0] += F[0]
                        self.net_forces[word_id][1] += F[1]
                    else:
                        self.net_forces[word_id][0] -= F[0]
                        self.net_forces[word_id][1] -= F[1]
            for word_id2 in range(word_id):
                dx = self.word_locs[word_id][0] - self.word_locs[word_id2][0]
                dy = self.word_locs[word_id][1] - self.word_locs[word_id2][1]
                d_squared = math.pow(dx,2)+math.pow(dy,2)
                if d_squared>neutral_radius:
                    self.net_forces[word_id][0] += dx/d_squared * mutual_repulsion_factor
                    self.net_forces[word_id][1] += dy/d_squared * mutual_repulsion_factor
                    self.net_forces[word_id2][0] -= dx/d_squared * mutual_repulsion_factor
                    self.net_forces[word_id2][1] -= dy/d_squared * mutual_repulsion_factor

            self.net_forces[word_id][0] += border_force * math.exp(-self.word_locs[word_id][0] / border_range)
            self.net_forces[word_id][1] += border_force * math.exp(-self.word_locs[word_id][1] / border_range)
            self.net_forces[word_id][0] -= border_force * math.exp(-(canvas_size-self.word_locs[word_id][0])/border_range)
            self.net_forces[word_id][1] -= border_force * math.exp(-(canvas_size - self.word_locs[word_id][1]) / border_range)
    def force_from_edge(self, edge:Word_Pair,
                        attraction_factor:float,
                        repulsion_multiplier: float,
                        forward:bool) -> Tuple[float, float]:
        u: List[float] = self.word_locs[edge[0]]
        v: List[float] = self.word_locs[edge[1]]

        dx = u[0] - v[0]
        dy = u[1] - v[1]

        d = min(max_effective_d_for_edges,math.sqrt(math.pow(dx,2)+math.pow(dy,2)))
        F_mag = attraction_factor * math.pow(d - neutral_radius, 2)
        if d<neutral_radius:
            F_mag *= repulsion_multiplier

        fx = -F_mag * dx/d
        fy = -F_mag * dy/d

        if not forward:
            fx *= -1
            fy *= -1

        return fx, fy

    def update_locations_from_forces(self) -> bool:
        madeAChange = False
        for word_id in range(len(self.words)):
            self.word_locs[word_id][0] += self.net_forces[word_id][0]
            self.word_locs[word_id][1] += self.net_forces[word_id][1]
            if (self.net_forces[word_id][0] > min_movement or self.net_forces[word_id][1] > min_movement):
                madeAChange = True

        return madeAChange

    def spread_out(self):
        moved = True
        while moved:
            self.find_net_forces()
            moved = self.update_locations_from_forces()
            self.draw_graph()
