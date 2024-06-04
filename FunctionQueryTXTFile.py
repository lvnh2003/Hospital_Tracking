class Function_TXT:
    def __init__(self):
        self.camera_file = 'cameras.txt'
        self.cameras = self.getCameras()
    def getCameras(self):
        with open(self.camera_file , 'r') as file:
            cameras = [line.strip() for line in file]
        return cameras

    def replaceCamera(self, index, new_link):
        cameras = self.getCameras()
        if 0 <= index < len(cameras):
            cameras[index] = new_link
            with open(self.camera_file, 'w') as file:
                for camera in cameras:
                    file.write(camera + "\n")
        else:
            print("Error: Index out of range")
    def addCamera(self, link):
        with open('cameras.txt', 'a') as file:
            file.write(link + "\n")

