import numpy as np
import os
import math


def get_max_v(file):
    flag = False
    with open(file, "r") as f:
        max_v = 0
        while True:
            line = f.readline()
            if line == "\n":
                continue
            if not line:
                break
            values = line.split()
            if values[0] == "v":
                flag = True
                for v in values[1:]:
                    if abs(float(v)) > max_v:
                        max_v = abs(float(v))
            elif values[0] != "v" and flag == True:
                return max_v
    return max_v


def get_offset(file):
    flag = False
    max_values = np.array([-math.inf, -math.inf, -math.inf])
    min_values = np.array([math.inf, math.inf, math.inf])
    counter = 0
    with open(file, "r") as f:
        while True:
            line = f.readline()
            if line == "\n":
                continue
            if not line:
                break
            values = line.split()
            if values[0] == "v":
                counter += 1
                flag = True
                for i, v in enumerate(values[1:]):
                    if float(v) > max_values[i]:
                        max_values[i] = float(v)
                    if float(v) < min_values[i]:
                        min_values[i] = float(v)
            elif values[0] != "v" and flag == True:
                break
    return np.max(abs(max_values-min_values)), (min_values + max_values) / 2


def loadMaterial(cls, filename):
    contents = {}
    mtl = None
    dirname = os.path.dirname(filename)

    for line in open(filename, "r"):
        if line.startswith("#"):
            continue
        values = line.split()
        if not values:
            continue
        if values[0] == "newmtl":
            mtl = contents[values[1]] = {}
        elif mtl is None:
            raise ValueError("mtl file doesn't start with newmtl stmt")
        elif values[0] == "map_Kd":
            # load the texture referred to by this declaration
            mtl[values[0]] = values[1]
            imagefile = os.path.join(dirname, mtl["map_Kd"])
            mtl["texture_Kd"] = cls.loadTexture(imagefile)
        else:
            mtl[values[0]] = list(map(float, values[1:]))
    return contents


class ObjLoader:
    buffer = []

    @staticmethod
    def search_data(data_values, coordinates, skip, data_type):
        for d in data_values:
            if d == skip:
                continue
            if data_type == "float":
                coordinates.append(float(d))
            elif data_type == "int":
                coordinates.append(int(d) - 1)

    @staticmethod  # sorted vertex buffer for use with glDrawArrays function
    def create_sorted_vertex_buffer(indices_data, vertices, textures, normals):
        for i, ind in enumerate(indices_data):
            if i % 3 == 0:  # sort the vertex coordinates
                start = ind * 3
                end = start + 3
                ObjLoader.buffer.extend(vertices[start:end])
            elif i % 3 == 1:  # sort the texture coordinates
                start = ind * 2
                end = start + 2
                ObjLoader.buffer.extend(textures[start:end])
            elif i % 3 == 2:  # sort the normal vectors
                start = ind * 3
                end = start + 3
                ObjLoader.buffer.extend(normals[start:end])

    @staticmethod  # TODO unsorted vertex buffer for use with glDrawElements function
    def create_unsorted_vertex_buffer(indices_data, vertices, textures, normals):
        num_verts = len(vertices) // 3

        for i1 in range(num_verts):
            start = i1 * 3
            end = start + 3
            ObjLoader.buffer.extend(vertices[start:end])

            for i2, data in enumerate(indices_data):
                if i2 % 3 == 0 and data == i1:
                    start = indices_data[i2 + 1] * 2
                    end = start + 2
                    ObjLoader.buffer.extend(textures[start:end])

                    start = indices_data[i2 + 2] * 3
                    end = start + 3
                    ObjLoader.buffer.extend(normals[start:end])

                    break

    @staticmethod
    def show_buffer_data(buffer):
        for i in range(len(buffer) // 8):
            start = i * 8
            end = start + 8
            print(buffer[start:end])

    @staticmethod
    def load_model(file, sorted=True, centered=False, size=1.0):
        vert_coords = []  # will contain all the vertex coordinates
        tex_coords = []  # will contain all the texture coordinates
        norm_coords = []  # will contain all the vertex normals

        all_indices = []  # will contain all the vertex, texture and normal indices
        indices = []  # will contain the indices for indexed drawing

        offset = [0, 0, 0]
        with open(file, "r") as f:
            if centered:
                max_v, offset = get_offset(file)
            while True:
                line = f.readline()
                if not line:
                    break
                if line == "\n":
                    continue
                values = line.split()
                if values[0] == "v":
                    if centered:
                        for i, value in enumerate(values):  # normalize
                            if i == 0:
                                continue
                            values[i] = f"{size*(float(value) - offset[i-1])/max_v}"
                    ObjLoader.search_data(values, vert_coords, "v", "float")
                elif values[0] == "vt":
                    ObjLoader.search_data(values, tex_coords, "vt", "float")
                elif values[0] == "vn":
                    ObjLoader.search_data(values, norm_coords, "vn", "float")
                elif values[0] == "f":
                    for value in values[1:]:
                        val = value.split("/")
                        ObjLoader.search_data(val, all_indices, "f", "int")
                        indices.append(int(val[0]) - 1)
                """ elif values[0] == "mtllib":
                    loadMaterial(os.path.join(os.path.dirname(file), values[1])) """

        if sorted:
            # use with glDrawArrays
            ObjLoader.create_sorted_vertex_buffer(
                all_indices, vert_coords, tex_coords, norm_coords
            )
        else:
            # use with glDrawElements
            ObjLoader.create_unsorted_vertex_buffer(
                all_indices, vert_coords, tex_coords, norm_coords
            )

        # ObjLoader.show_buffer_data(ObjLoader.buffer)

        buffer = (
            ObjLoader.buffer.copy()
        )  # create a local copy of the buffer list, otherwise it will overwrite the static field buffer
        ObjLoader.buffer = []  # after copy, make sure to set it back to an empty list

        return np.array(indices, dtype="uint32"), np.array(buffer, dtype="float32")
