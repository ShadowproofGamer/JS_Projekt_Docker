import numpy as np
import matplotlib.pyplot as plt
import matplotlib.backends.backend_svg as pltSvg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
import variables as var

#print(matplotlib.get_backend())
#var = ""
#def init():
#    var = variables.storage()
#
#class var:
#    def __init__(self) -> None:
#        self.data = []
#        self.typeD = "dane"
#        self.dimension = "experimental"
#        self.root = None
#        self.separators=(',',';')
#        self.custom=(0, 1, 2)
#        self.parsedData=[]
#        self.arr_x=[]
#        self.arr_y=[]
#        self.arr_z=[]
#

def save_to_data():
    #x, y, z = (var.arr_x[5::5],var.arr_y[5::5],var.arr_z[5::5])
    x, y, z = (var.arr_x[1::1],var.arr_y[1::1],var.arr_z[1::1])
    new_str = f'{var.arr_x[0]},{var.arr_y[0]},{var.arr_z[0]}'
    for i in range(len(x)):
        #new_str.__add__(f';{x[i]},{y[i]},{z[i]}')
        new_str+=f';{x[i]},{y[i]},{z[i]}'
    try:
        f = open("dataFile.txt", "w")
        f.write(new_str)
        f.close()
        return True
    except:
        print("failed to save data!")
        return False



def save_to_svg():
    plt.savefig(fname="savedGraph.png")



def datafy(data:str, separators:list[str]|tuple[str]=(',',';'), custom=(0, 1, 2), dimension="2D"):
    new_data = [[float(d) for d in n.split(separators[0])] for n in data.split(separators[1])]
    #print(new_data)
    if len(new_data[0])>2:
        try:
            result_data = [[d[custom[0]], d[custom[1]], d[custom[2]]] for d in new_data]
            #print(result_data)
            return result_data
        except:
            result_data = [[d[0], d[1], d[2]] for d in new_data]
            #print(result_data)
            return result_data
    elif len(new_data[0])==2 and dimension=="2D":
        return new_data
    else:
        raise Exception
       


def show_graph(typeD=var.typeD, dimension=var.dimension, data=var.parsedData, zakres:list|tuple=[-10, 10], rotation:int=0, root=var.root, separators=(',',';'), custom=var.custom, preparsed=False):
    #TODO parsing data into "graph-accepted" formats
    #TODO parsing zakres, separators i custom
    if not preparsed:
        try:
            #zakres to float
            try:
                zakres = [float(d) for d in zakres]
            except:
                zakres = [-10, 10]

            #checking separators
            if len(separators[0])<1 or len(separators[1])<1:
                separators=(',',';')

            #parsing if type dane
            if typeD=="dane":
                try:
                    custom = [int(d) for d in custom]
                except:
                    custom = [0,1,2]
                new_data = datafy(data, separators, custom)

            elif typeD=="funkcja (experimental)":
                #adjusting variables
                if len(custom[0])<1:
                    custom[0]="x"
                if len(custom[1])<1:
                    custom[1]="y"
                if len(custom[2])<1:
                    custom[2]="z"
            #parsing if type funkcja (2D)
                if dimension=="2D":
                    if len(custom[0])<1:
                        custom[0]="x"
                    if len(custom[1])<1:
                        custom[1]="y"
                    if len(custom[2])<1:
                        custom[2]="z"

                    def newF(x, c=custom):
                        return eval(data, {"np":np}, {c[0]: x, "sin": np.sin, "cos": np.cos, "tan":np.tan, "abs": np.abs, "pi": np.pi, "sqrt": np.sqrt, "e":np.e})
                    new_data = newF


                #parsing if type funkcja (3D)
                if dimension=="3D":

                    def newF(mat, c=custom):
                        x, y, *z = mat
                        return eval(data, {"np":np}, {c[0]: x, c[1]:y, "sin": np.sin, "cos": np.cos, "tan":np.tan, "abs": np.abs, "pi": np.pi, "sqrt": np.sqrt, "e":np.e })
                    new_data = newF


        except:
            return False



        var.typeD=typeD
        var.data=data
        var.dimension=dimension
        #var.data=new_data
        var.root=root
        var.separators=separators
        print(custom)
        var.custom=custom
        print(var.custom)
        var.parsedData=new_data

    #if preparsed (graph update)
    else:
        new_data=var.parsedData
        print("preparsed!")
        print(new_data, zakres, rotation, root, custom)

    #print("parsed!")
    try:
        #choosing appropriate graph for data provided
        if typeD=="dane" and dimension=="2D":
            pokaz_2D_dane(new_data, zakres, rotation, root)
        elif typeD=="dane" and dimension=="3D":
            pokaz_3D_dane(new_data, zakres, rotation, root)
        elif typeD=="funkcja (experimental)" and dimension=="2D":
            pokaz_2D_fun(new_data, zakres, rotation, root, custom)
        elif typeD=="funkcja (experimental)" and dimension=="3D":
            pokaz_3D_fun(new_data, zakres, rotation, root, custom)
    except:
        return False

    
    
    #returns success
    return True
       


def pokaz_2D_fun(Fcelu, zakres:list|tuple=[-10, 10], rotation:int=0, root=None, custom=["x", "y", "z"]):
    plt.close()

    os_x = np.linspace(zakres[0], zakres[1], 2500)
    macierz_Z = Fcelu(os_x)

    fig, ax = plt.subplots(figsize=(7,6))

    ax.plot(os_x, macierz_Z)
    ax.set_xlabel(custom[0], fontsize=14)
    ax.set_ylabel(custom[1], fontsize=14)

    #print("macierz 2D:", macierz_Z.reshape(1, -1))
    #print("x: ", os_x.reshape(1, -1))
    
    if root:
        canvas = FigureCanvasTkAgg(fig,master=root)
        canvas.draw()
        canvas.get_tk_widget().place(relx=0.33, rely=0.025)
        root.update()
        
        
    else:
        plt.show()

    var.arr_x = os_x
    var.arr_y = macierz_Z
    var.arr_z = [0 for i in os_x]


#TODO config graph of function 3d
def pokaz_3D_fun(Fcelu, zakres:list|tuple=[-10, 10], rotation:int=0, root=None, custom=["x", "y", "z"]):
  plt.close()

  os_x1 = np.linspace(zakres[0], zakres[1], 50)
  os_x2 = np.linspace(zakres[-2], zakres[-1], 50)
  siatka_X1, siatka_X2 = np.meshgrid(os_x1, os_x2)
  macierz_Z = Fcelu([siatka_X1, siatka_X2])

  #print("macierz 2D: ", macierz_Z.reshape(1, -1))
  #print("x: ", siatka_X1.reshape(1, -1).tolist())
  #print("y: ", siatka_X2.reshape(1, -1).tolist())


  #print(len(os_x2)==len(var.arr_z))
  #print(len(siatka_X1.reshape(1, -1).tolist())==len(var.arr_z))
  #print(len(var.arr_z))
  #print(len(os_x2)==len(var.arr_z[0]))
  #print(len(var.arr_z[0]))


  fig, ax = plt.subplots(figsize=(7,6), subplot_kw={'projection':'3d'})
  if rotation==270:
    ax.plot_surface(-siatka_X2, siatka_X1, macierz_Z, cmap='Spectral_r')
    ax.set_xlabel(custom[1], fontsize=14)
    ax.set_ylabel(custom[0], fontsize=14)
  elif rotation==180:
    ax.plot_surface(-siatka_X1, -siatka_X2, macierz_Z, cmap='Spectral_r')
    ax.set_xlabel(custom[0], fontsize=14)
    ax.set_ylabel(custom[1], fontsize=14)
  elif rotation==90:
    ax.plot_surface(siatka_X2, -siatka_X1, macierz_Z, cmap='Spectral_r')
    ax.set_xlabel(custom[1], fontsize=14)
    ax.set_ylabel(custom[0], fontsize=14)
  else:
    ax.plot_surface(siatka_X1, siatka_X2, macierz_Z, cmap='Spectral_r')
    ax.set_xlabel(custom[0], fontsize=14)
    ax.set_ylabel(custom[1], fontsize=14)

  ax.set_zlabel(custom[2], fontsize=14)
  
  if root:
    canvas = FigureCanvasTkAgg(fig,master=root)
    canvas.draw()
    canvas.get_tk_widget().place(relx=0.33, rely=0.025)
    root.update()
    
    
  else:
    plt.show()

  var.arr_x = siatka_X1.reshape(1, -1).tolist()[0]
  var.arr_y = siatka_X2.reshape(1, -1).tolist()[0]
  var.arr_z = macierz_Z.reshape(1, -1).tolist()[0]



#TODO config graph of function 2d
def pokaz_3D_fun_map(Fcelu, zakres:list|tuple=[-10, 10], rotation:int=0, root=None):
    plt.close()

    #x_pocz, x_opt = x_historia[0], x_historia[-1]
    os_x1 = np.linspace(zakres[0], zakres[1], num=100)
    os_x2 = np.linspace(zakres[-2], zakres[-1], num=100)
    siatka_X1, siatka_X2 = np.meshgrid(os_x1, os_x2)
    macierz_Z = Fcelu([siatka_X1, siatka_X2])

    fig, ax = plt.subplots(figsize=(7,6))

    if rotation==270:
        cplot = ax.contourf(-siatka_X1, siatka_X2, macierz_Z, 10, cmap='Spectral_r', alpha=1)
        clines = ax.contour(-siatka_X1, siatka_X2, macierz_Z, 10, colors='black')
        ax.set_xlabel(r'y', fontsize=16)
        ax.set_ylabel(r'x', fontsize=16)
    elif rotation==180:
        cplot = ax.contourf(-siatka_X1, -siatka_X2, macierz_Z, 10, cmap='Spectral_r', alpha=1)
        clines = ax.contour(-siatka_X1, -siatka_X2, macierz_Z, 10, colors='black')
        ax.set_xlabel(r'x', fontsize=16)
        ax.set_ylabel(r'y', fontsize=16)
    elif rotation==90:
        cplot = ax.contourf(siatka_X1, -siatka_X2, macierz_Z, 10, cmap='Spectral_r', alpha=1)
        clines = ax.contour(siatka_X1, -siatka_X2, macierz_Z, 10, colors='black')
        ax.set_xlabel(r'y', fontsize=16)
        ax.set_ylabel(r'x', fontsize=16)
    else:
        cplot = ax.contourf(siatka_X1, siatka_X2, macierz_Z, 10, cmap='Spectral_r', alpha=1)
        clines = ax.contour(siatka_X1, siatka_X2, macierz_Z, 10, colors='black')
        ax.set_xlabel(r'x', fontsize=16)
        ax.set_ylabel(r'y', fontsize=16)


    ax.set_aspect('equal')
    ax.clabel(clines)
    fig.colorbar(cplot)
    if root:
        canvas = FigureCanvasTkAgg(fig,master=root)
        canvas.draw()
        canvas.get_tk_widget().place(relx=0.33, rely=0.025)
        root.update()
        
        
    else:
        plt.show()

    return fig, ax



def pokaz_3D_dane(data, zakres:list|tuple=[-10, 10], rotation:int=0, root=None):
    plt.close()

    xs = []
    ys = []
    zs = []
    for x, y, z in data:
       xs.append(x)
       ys.append(y)
       zs.append(z)

    xs = np.array(xs)
    ys = np.array(ys)
    zs = np.array(zs)

    fig, ax = plt.subplots(figsize=(7,6), subplot_kw={"projection": "3d"})
    if rotation==270:
        ax.scatter(xs=-xs, ys=ys, zs=zs)
        ax.set_xlabel(r'y', fontsize=16)
        ax.set_ylabel(r'x', fontsize=16)
    elif rotation==180:
        ax.scatter(xs=-xs, ys=-ys, zs=zs)
        ax.set_xlabel(r'x', fontsize=16)
        ax.set_ylabel(r'y', fontsize=16)
    elif rotation==90:
        ax.scatter(xs=xs, ys=-ys, zs=zs)
        ax.set_xlabel(r'y', fontsize=16)
        ax.set_ylabel(r'x', fontsize=16)
    else:
        ax.scatter(xs=xs, ys=ys, zs=zs)
        ax.set_xlabel(r'x', fontsize=16)
        ax.set_ylabel(r'y', fontsize=16)
    #ax.scatter(xs=xs, ys=ys, zs=zs)
    #ax.set(xticklabels=[],
    #       yticklabels=[],
    #       zticklabels=[])

    if root:
        canvas = FigureCanvasTkAgg(fig,master=root)
        canvas.draw()
        canvas.get_tk_widget().place(relx=0.33, rely=0.025)
        root.update()
        
        
    else:
        plt.show()

    #return fig, ax


def pokaz_2D_dane(data, zakres:list|tuple=[-10, 10, -10, 10], rotation:int=0, root=None):
    plt.close()

    var_x = []
    var_y = []
    for x, y, *z in data:
       var_x.append(x)
       var_y.append(y)

    var_x = np.array(var_x)
    var_y = np.array(var_y)

    fig, ax = plt.subplots(figsize=(7,6))

    if rotation==270:
        ax.scatter(x=-var_x, y=var_y)
        ax.set_xlabel(r'y', fontsize=16)
        ax.set_ylabel(r'x', fontsize=16)
    elif rotation==180:
        ax.scatter(x=-var_x, y=-var_y)
        ax.set_xlabel(r'x', fontsize=16)
        ax.set_ylabel(r'y', fontsize=16)
    elif rotation==90:
        ax.scatter(x=var_x, y=-var_y)
        ax.set_xlabel(r'y', fontsize=16)
        ax.set_ylabel(r'x', fontsize=16)
    else:
        ax.scatter(x=var_x, y=var_y)
        ax.set_xlabel(r'x', fontsize=16)
        ax.set_ylabel(r'y', fontsize=16)

    #ax.scatter(x=var_x, y=var_y)

    if root:
        canvas = FigureCanvasTkAgg(fig,master=root)
        
        canvas.draw()
        canvas.get_tk_widget().place(relx=0.33, rely=0.025)
        root.update()
        
        
    else:
        plt.show()

    #return fig, ax