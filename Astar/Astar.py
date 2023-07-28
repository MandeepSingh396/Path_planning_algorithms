from pickletools import uint8
import numpy as np
from numpy import genfromtxt
import matplotlib.pyplot as plt
from PIL import Image
import os
import shutil
from moviepy.editor import ImageSequenceClip


#input the csv file address here in line 11
#input the save folder in line 66
#input the updated start and end pos in line 13 and line 14
#change the limits in line 85
# grid = genfromtxt("50%_32x32_coverage", delimiter = ",")
# print(grid.shape)
# start_pos = (0,0)
# end_pos = (31, 31)

def heuristic(current_pos, end_pos):
    # global end_pos
    # return (abs(end_pos[0] - current_pos[0])+abs(end_pos[1]-current_pos[1]))
    return np.sqrt((end_pos[0] - current_pos[0])**2 + (end_pos[1]-current_pos[1])**2)

def cost(current_pos, start_pos):
    # global start_pos
    # return (abs(start_pos[0] - current_pos[0])+abs(start_pos[1]-current_pos[1]))
    return np.sqrt((start_pos[0] - current_pos[0])**2 + (start_pos[1]-current_pos[1])**2)

class Node():

    def __init__(self, parent_pos = None, pos = None):
        self.parent_pos = parent_pos
        self.pos = pos
        # self.h = heuristic(self.pos)
        self.h = 0
        # self.g = cost(self.pos)
        self.g = 0
        self.f = 0

    def __eq__(self, other):
        return self.pos == other.pos

def astar(grid, start_pos, end_pos, save_path):
    start_node = Node(None, start_pos)
    end_node = Node(None, end_pos)
    sh = grid.shape[0]
    open_list = []
    closed_list = []

    open_list.append(start_node)
    count = 10000
    nodes_explored = 0
    i = 0
    path_count = 0
    while(len(open_list) > 0):
        count+=1
        # count = str(count)
        print("count", i, end = "\r")
        current_node = open_list[0]
        current_index = 0

        for index, item in enumerate(open_list):         #find the node with minimum cost out of all childs in open_list
            if item.f < current_node.f:
                current_node = item
                current_index = index
        
        # print(current_node.pos, current_node.h, current_node.g, current_node.f)

        grid[current_node.pos[0]][current_node.pos[1]] = 50

        plt.imshow(grid)
        file_name = save_path + "/" + str(count) + ".png"
        plt.savefig(file_name)
        plt.close()

        open_list.pop(current_index)
        nodes_explored += 1
        closed_list.append(current_node)

        if current_node == end_node:
            current = current_node
            while current is not start_node:
                count+=1
                path_count += 1
                grid[end_node.pos[0]][end_node.pos[1]] = 200
                grid[current.pos[0]][current.pos[1]] = 100
                plt.imshow(grid)
                file_name = save_path + "/" +str(count)+".png"
                plt.savefig(file_name)
                current = current.parent_pos
            return grid, nodes_explored
        
        children = []
        for new_position in [(1,0), (0,1), (-1,0), (0,-1)]:
            node_position = (current_node.pos[0] + new_position[0], current_node.pos[1] + new_position[1])
            if node_position[0] > sh-1 or node_position[0] < 0 or node_position[1] > sh-1 or node_position[1] < 0:
                continue
            if grid[node_position[0]][node_position[1]] == 0:
                continue

            new_node = Node(current_node, node_position)
            new_node.h = heuristic(new_node.pos, end_pos)
            new_node.g = current_node.g + cost(new_node.pos, current_node.pos)
            new_node.f = new_node.g + new_node.h
            children.append(new_node)

        
        for child in children:
            flag = False
            for closed in closed_list:
                if(closed == child):
                    flag = True
                    break
            for open in open_list:
                if(open == child and child.g >= open.g):
                    flag = True
                    break

            if flag == True:
                continue

            if flag == False:
                open_list.append(child)
        i += 1

def make_video(fps, path, video_file):
    print("Creating video {}, FPS={}".format(video_file, fps))
    clip = ImageSequenceClip(path, fps = fps)
    clip.write_videofile(video_file)
    shutil.rmtree(path)

def main():

    save_path = os.path.join("astar_data")
    if os.path.exists(save_path):
        shutil.rmtree(save_path)
        os.mkdir(save_path)
    else:
        os.mkdir(save_path)

    grid = genfromtxt("../Data/grid50x50/50x50grid -35%_coverage.csv", delimiter = ",")
    start_pos = (0,0)
    end_pos = (49, 49)

    path, nodes_explored = astar(grid, start_pos, end_pos, save_path)
    video_file = 'astar.mp4'
    make_video(150, save_path, video_file)
    plt.imshow(path)
    plt.savefig("path_50x50.png")
    print("Total nodes explored", nodes_explored)
    
if __name__ == '__main__':
    main()

