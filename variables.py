data = []
typeD = "dane"
dimension = "experimental"
root = None
separators=(',',';')
custom=(0, 1, 2)
parsedData=[]
arr_x=[]
arr_y=[]
arr_z=[]

class storage:
    def __init__(self) -> None:
        self.data = []
        self.typeD = "dane"
        self.dimension = "experimental"
        self.root = None
        self.separators=(',',';')
        self.custom=(0, 1, 2)
        self.parsedData=[]
        self.arr_x=[]
        self.arr_y=[]
        self.arr_z=[]