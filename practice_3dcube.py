import pyxel
import math

class App:
    def __init__(self):
        pyxel.init(900, 500, "3DCube")
        self.rotation_matrix = self.identity_matrix()
        self.size = 250
        self.speed = 10
        pyxel.run(self.update, self.draw) 
    def identity_matrix(self):
        return [
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
        ]
    
    def matmul(self, A , B):
        result = [[0] * 3 for _ in range(3)]
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    result[i][j] += A[i][k] * B[k][j]
        return result
    
    def rotate_vector(self, m, v):
        x = m[0][0] * v[0] + m[0][1] * v[1] + m[0][2] * v[2]
        y = m[1][0] * v[0] + m[1][1] * v[1] + m[1][2] * v[2]
        z = m[2][0] * v[0] + m[2][1] * v[1] + m[2][2] * v[2]
        return(x, y, z)
    
    def euler_to_matrix(self, x, y, z):
        cx, cy, cz = math.cos(x), math.cos(y), math.cos(z)
        sx, sy, sz = math.sin(x), math.sin(y), math.sin(z)

        Rx = [
            [1, 0, 0],
            [0, cx, -sx],
            [0, sx , cx]
        ]

        Ry = [
            [cy, 0, sy],
            [0, 1, 0],
            [-sy, 0, cy]
        ]
        Rz = [
            [cz, -sz,0],
            [sz, cz, 0],
            [0, 0, 1]
        ]
        return self.matmul(self.matmul(Rz,Ry) ,Rx)
    
    def update(self):
        dx = dy = 0
        # PC操作
        if(pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT)):
            dy += self.speed * 0.01
        if(pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT)):
            dy -= self.speed * 0.01
        if(pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP)):
            dx -= self.speed * 0.01
        if(pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN)):
            dx += self.speed * 0.01
        delta = self.euler_to_matrix(dx,dy,0) #ｘｙ軸に対する角度変化を回転行列に変換
        self.rotation_matrix = self.matmul(delta, self.rotation_matrix) # 変化前の回転行列に変化量の回転行列をかける
    def draw(self):
        pyxel.cls(0)
        half = self.size / 2
        vertices = [
            (-half, half, -half),
            (half, half, -half),
            (half, -half, -half),
            (-half, -half, -half),
            (-half, half, half),
            (half, half, half),
            (half, -half, half),
            (-half, -half, half),
        ]

        rotated_vertices = [self.rotate_vector(self.rotation_matrix, v) for v in vertices]
        screen_vertices = [(x + pyxel.width/2, y + pyxel.height / 2,z) for(x,y,z) in rotated_vertices ]
        edges = [
            (0,1),(1,2),(2,3),(3,0),
            (4,5),(5,6),(6,7),(7,4),
            (0,4),(1,5),(2,6),(3,7)
        ]
        farthest = max(range(8), key=lambda i : screen_vertices[i][2])
        closest = min(range(8), key = lambda i : screen_vertices[i][2])

        for i, (x, y , z) in enumerate(screen_vertices):
            pyxel.circ(x,y,10, 1 if i == farthest else 8 if i == closest else 7)
        
        for a, b, in edges:
            x1, y1 , _ = screen_vertices[a]
            x2, y2, _ = screen_vertices[b]
            if(a == farthest or b == farthest):
                pyxel.line(x1, y1, x2, y2, 1)
            else:
                pyxel.line(x1, y1, x2, y2, 7)

App()

            
    