import numpy as np

t = np.radians(90)
M = np.array([[np.cos(t), -np.sin(t), 0, 2],
              [np.sin(t), np.cos(t), 0, 0],
              [0, 0, 1, 0],
              [0, 0, 0, 1]])

cube = np.array([[x, y, z, 1] for x in (0, 1) for y in (0, 1) for z in (0, 1)], dtype=float)
print("8 corners as rows:", cube.shape)

one_by_one = np.array([M @ p for p in cube])
all_at_once = cube @ M.T
print("one by one == all at once:", np.allclose(one_by_one, all_at_once))
print("corner (1, 0, 0) ->", np.round(all_at_once[4, :3], 6) + 0.0)
print("corner (1, 1, 1) ->", np.round(all_at_once[7, :3], 6) + 0.0)

frames = np.array([np.eye(4), M, M @ M])
print("3 matrices at once:", frames.shape, "@ corner (1, 0, 0, 1) ->")
print(np.round(frames @ cube[4], 6) + 0.0)
