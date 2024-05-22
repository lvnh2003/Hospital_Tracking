class Function_TXT():
    def getCameras(self):
        with open('cameras.txt', 'r') as file:
            cameras = [line.strip() for line in file]
        return cameras