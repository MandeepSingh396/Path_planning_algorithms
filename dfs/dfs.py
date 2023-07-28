from pickletools import uint8
import numpy as np
from numpy import genfromtxt
import matplotlib.pyplot as plt
from PIL import Image
from moviepy.editor import ImageSequenceClip
import cv2
import os
import shutil
from numba import jit

class Node():

    def __init__(self, parent_pos = None, pos = None):
        self.parent_pos = parent_pos
        self.pos = pos

    def __eq__(self, other):
        return self.pos == other.pos

# @jit
def DFS(grid, start_pos, end_pos, save_path):
    start_node = Node(None, start_pos)
    end_node = Node(None, end_pos)
    grid[start_node.pos[0]][start_node.pos[1]] = 200
    grid[end_node.pos[0]][end_node.pos[1]] = 200
    open_list = []
    closed_list = []

    open_list.append(start_node)
    count = 1000
    i=0
    nodes_explored = 0
    path_count = 0
    print("Exploring the grid***********************")
    while(len(open_list) > 0):
        count+=1
        current_node = open_list[len(open_list)-1]
        current_index = len(open_list)-1
        # print(current_node.pos)
        if i!=0:
            grid[current_node.pos[0]][current_node.pos[1]] = 50

        # plt.imshow(grid)
        # file_name = save_path + "/" +str(count)+".png"
        # plt.savefig(file_name)
        # plt.close()

        open_list.pop(current_index)
        nodes_explored += 1
        closed_list.append(current_node)

        if current_node == end_node:
            print("\n Calculating path***********************")
            current = current_node
            while current is not start_node:
                count+=1
                path_count += 1
                grid[end_node.pos[0]][end_node.pos[1]] = 200
                grid[current.pos[0]][current.pos[1]] = 100
                # plt.imshow(grid)
                # file_name = save_path +"/" +str(count)+".png"
                # plt.savefig(file_name)
                current = current.parent_pos
            return grid, nodes_explored, path_count
        
        children = []
        for new_position in [(1,0),(-1,0),(0,-1),(0,1)]:
            node_position = (current_node.pos[0] + new_position[0], current_node.pos[1] + new_position[1])
            if node_position[0] > end_pos[0] or node_position[0] < 0 or node_position[1] > end_pos[1] or node_position[1] < 0:
                continue
            if grid[node_position[0]][node_position[1]] == 0:
                continue

            new_node = Node(current_node, node_position)
            children.append(new_node)

        
        for child in children:
            flag = False
            for item in closed_list:
                if(item.pos == child.pos):
                    flag = True
                    break
            # for item in open_list:
            #     if(item.pos == child.pos):
            #         flag = True
            #         break

            if flag == True:
                continue

            if flag == False:
                open_list.append(child)
        i+=1

def make_video(fps, path, video_file):
    print("Making video***********************")
    print("Creating video {}, FPS={}".format(video_file, fps))
    clip = ImageSequenceClip(path, fps = fps)
    clip.write_videofile(video_file)
    shutil.rmtree(path)

def main():

    save_path = os.path.join("dfs_data")
    if os.path.exists(save_path):
        shutil.rmtree(save_path)
        os.mkdir(save_path)
    else:
        os.mkdir(save_path)

    grid = genfromtxt("../Data/grid128x128/128x128grid -35%_coverage.csv", delimiter = ",")
    start_pos = (0,0)
    end_pos = (127,127)

    path, nodes_explored, path_count = DFS(grid, start_pos, end_pos, save_path)
    # video_file = 'dfs_50.mp4'
    # make_video(150, save_path, video_file)
    fig = plt.gcf()
    fig.set_size_inches(10,10)
    plt.imshow(path)
    fig.savefig('dfs_path_128x128.png', dpi=100)
    print("Total nodes explored", nodes_explored)
    print("Path count", path_count)
    print("Image saved")

if __name__ == '__main__':
    main()


