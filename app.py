import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import logic as core
#import variables as var




class ctkApp:
        
    def __init__(self):

        #setting global app GUI
        ctk.set_appearance_mode("dark")
        self.root = ctk.CTk()
        self.root.geometry("1200x680")
        self.root.title("Wykreślarka danych")
        self.root.update()

        #normalized GUI variables
        self.standard_w = 300
        self.small_w = 95
        self.standard_h = 45
        self.standard_relx = 0.025

        #GUI variables (later exported to backend)
        self.slider_var = ctk.IntVar(value=0)
        self.type_var = ctk.StringVar(value="dane")
        self.dimensions_var = ctk.StringVar(value="2D")



        #frame for graph
        self.frame = ctk.CTkFrame(master=self.root,
                                  height= self.root.winfo_height()*0.95,
                                  width = self.root.winfo_width()*0.66,
                                  fg_color="transparent")
        self.frame.place(relx=0.33, rely=0.025)

        #label "zakres danych"
        self.label = ctk.CTkLabel(self.root, 
                                  text="zakres danych", 
                                  fg_color="transparent",
                                  width=self.standard_w,
                                  height=self.standard_h,
                                  anchor="center",

                                  )
        self.label.place(relx= 0.025,rely=0)

        #lower end of data chown
        self.input_low =  ctk.CTkEntry(master=self.root,
                                   placeholder_text=-10,
                                   justify='center',
                                   width=self.standard_w*0.46,
                                   height=self.standard_h,
                                   corner_radius=5,
                                   )
        self.input_low.place(relx=self.standard_relx,rely=0.08)

        #higher end of data shown
        self.input_high =  ctk.CTkEntry(master=self.root,
                                   placeholder_text=10,
                                   justify='center',
                                   width=self.standard_w*0.46,
                                   height=self.standard_h,
                                   corner_radius=5,
                                   )
        self.input_high.place(relx=self.standard_relx+0.135,rely=0.08)

        #label "obrót wykresu"
        self.label2 = ctk.CTkLabel(self.root, 
                                  text="obrót wykresu", 
                                  fg_color="transparent",
                                  width=self.standard_w,
                                  height=self.standard_h,
                                  anchor="center",

                                  )
        self.label2.place(relx= self.standard_relx,rely=0.15)


        #slider and label storing the degree of graph's rotation
        self.label_int_slider = ctk.CTkLabel(self.root, 
                                  textvariable=self.slider_var, 
                                  fg_color="transparent",
                                  width=self.standard_w,
                                  height=self.standard_h,
                                  anchor="center",

                                  )
        self.label_int_slider.place(relx= self.standard_relx,rely=0.2)
        
        self.slider = ctk.CTkSlider(master=self.root,
                                    width=self.standard_w,
                                    height=20,
                                    from_=0,
                                    to=270,
                                    number_of_steps=3,
                                    variable=self.slider_var,
                                    #command=self.update_surface
                                    )
        self.slider.place(relx=self.standard_relx,rely=0.25)


        #Button refreshing the graph using new area and rotation (in practice used to apply new area)
        self.buttonLoad = ctk.CTkButton(master = self.root,
                               text="Update graph",
                               width=self.standard_w,
                               height=self.standard_h,
                               command=self.update_graph
                               )
        self.buttonLoad.place(relx=self.standard_relx, rely=0.32)




        #option menu and variable with the type of data provided
        self.type = ctk.CTkOptionMenu( self.root,
                                        values=["funkcja (experimental)", "dane"],
                                        command=self.type_callback,
                                        variable=self.type_var,
                               width=self.standard_w,
                               height=self.standard_h,
                               )
        self.type.place(relx=self.standard_relx,rely=0.4)



        #option menu and variable with the dimension of data provided

        self.dimensions = ctk.CTkOptionMenu( self.root,
                                        values=["2D", "3D"],
                                        command=self.dimensions_callback,
                                        variable=self.dimensions_var,
                               width=self.standard_w,
                               height=self.standard_h,
                               )
        self.dimensions.place(relx=self.standard_relx,rely=0.48)




        #label and entry fields for data separators (only for data mode)
        self.label_separator = ctk.CTkLabel(self.root, 
                                  text="separatory\nwartości\t\t\tkrotki ", 
                                  fg_color="transparent",
                                  width=self.standard_w,
                                  height=self.standard_h/2,
                                  anchor="center",

                                  )
        self.label_separator.place(relx= self.standard_relx,rely=0.56)

        self.input_values_separator =  ctk.CTkEntry(master=self.root,
                                   placeholder_text=",",
                                   justify='center',
                                   width=self.standard_w*0.46,
                                   height=self.standard_h,
                                   corner_radius=5,
                                   )
        self.input_values_separator.place(relx=self.standard_relx,rely=0.62)

        self.input_tuple_separator =  ctk.CTkEntry(master=self.root,
                                   placeholder_text=";",
                                   justify='center',
                                   width=self.standard_w*0.46,
                                   height=self.standard_h,
                                   corner_radius=5,
                                   )
        self.input_tuple_separator.place(relx=self.standard_relx+0.135,rely=0.62)


        #label and entry fields for variables (only for function mode)
        self.label_separator = ctk.CTkLabel(self.root, 
                                  text="zmienne funkcji", 
                                  fg_color="transparent",
                                  width=self.standard_w,
                                  height=self.standard_h/2,
                                  anchor="center",

                                  )
        self.label_separator.place(relx= self.standard_relx,rely=0.7)

        self.input_var1 =  ctk.CTkEntry(master=self.root,
                                   placeholder_text="x",
                                   justify='center',
                                   width=self.standard_w*0.30,
                                   height=self.standard_h,
                                   corner_radius=5,
                                   #state="disabled",
                                   )
        self.input_var1.place(relx=self.standard_relx, rely=0.74)

        self.input_var2 =  ctk.CTkEntry(master=self.root,
                                   placeholder_text="y",
                                   justify='center',
                                   width=self.standard_w*0.30,
                                   height=self.standard_h,
                                   corner_radius=5,
                                   #state="disabled",
                                   )
        self.input_var2.place(relx=self.standard_relx+0.088, rely=0.74)

        self.input_var3 =  ctk.CTkEntry(master=self.root,
                                   placeholder_text="z",
                                   justify='center',
                                   width=self.standard_w*0.30,
                                   height=self.standard_h,
                                   corner_radius=5,
                                   #state="disabled",
                                   )
        self.input_var3.place(relx=self.standard_relx+0.175, rely=0.74)



        #field for entering data
        self.entry = ctk.CTkEntry(
                                self.root, 
                                placeholder_text="tutaj wprowadź dane",
                                width=self.standard_w,
                                height=self.standard_h,
                                corner_radius=5,
                                )
        self.entry.place(relx=self.standard_relx,rely=0.82)




        #buttons for loading and saving the data 
        self.buttonLoad = ctk.CTkButton(master = self.root,
                               text="Load",
                               width=self.small_w,
                               height=self.standard_h,
                               command=self.load_graph
                               )
        self.buttonLoad.place(relx=self.standard_relx, rely=0.9)
        self.buttonData = ctk.CTkButton(master = self.root,
                               text="Save data\n(.txt)",
                               width=self.small_w,
                               height=self.standard_h,
                               state="disabled",
                               command=self.save_data
                               )
        self.buttonData.place(relx=0.11, rely=0.9)
        self.buttonSVG = ctk.CTkButton(master = self.root,
                               text="Save Graph\n(.svg)",
                               width=self.small_w,
                               height=self.standard_h,
                               state="disabled",
                               command=self.save_svg
                               )
        self.buttonSVG.place(relx=0.195, rely=0.9)





        #protocol for handling window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        #mainloop initializer (last part of class init)
        self.root.mainloop()




#end of app class




    #function to properly close the GUI and whole app
    def on_closing(self):
        core.plt.close()
        self.root.destroy()
        exit()



    #callback functions

    

    #changing button state depending on input type 
    def type_callback(self, choice):
        
        if choice=="funkcja (experimental)":
            self.input_tuple_separator.configure(state="disabled")
            self.input_values_separator.configure(state="disabled")

        elif choice=="dane":
            self.input_tuple_separator.configure(state="normal")
            self.input_values_separator.configure(state="normal")


    #changing button state depending on input dimension 
    def dimensions_callback(self, choice):
        if choice=="3D":
            self.input_var3.configure(state="normal")

        elif choice=="2D":
            self.input_var3.configure(state="disabled")



    def update_graph(self):
        self.load_graph()
        print("update!")
        #rotation=self.slider_var.get()
        #zakres=[self.input_low.get(), self.input_high.get()]
        #success = core.show_graph(zakres=zakres, rotation=rotation, preparsed=True)
        #self.root.update()
        #if success: print("rotated successfully")
        
        


        #zmiana stanu przycisków zapisu stanu
        #if success:
        #    self.input_low.configure(text_color="white")
        #    self.input_high.configure(text_color="white")
        #else:
        #    self.input_low.configure(text_color="red")
        #    self.input_high.configure(text_color="red")

        
    def load_graph(self):


        #strefa testowa TODO delete in final
        def fcelu(x):return x**2 - x
        def Fcelu(x):
            x1, x2 = x
            return (4*core.np.sin(core.np.pi*x1) + 6*core.np.sin(core.np.pi/x2)) + (x1 - 1)**2 + (x2 - 1)**2
        
        kDane = []
        for i in range(100):
            kDane.append((core.np.random.random()*i, core.np.random.random()*i))

        kDane3 = []
        for j in range(100):
            kDane3.append((core.np.random.random()*j, core.np.random.random()*j, core.np.random.random()*j))

        #debug
        #print("type var:", self.type_var.get())
        #print("slider (rotation) var:", self.slider_var.get())
        #print("dimensions var:", self.dimensions_var.get())
        #print("i low var:", self.input_low.get())
        #print("i high var:", self.input_high.get())
        #print("tuple var:", self.input_tuple_separator.get())
        #print("values var:", self.input_values_separator.get())
        #print("values var:", self.input_var1.get())
        #print("values var:", self.input_var2.get())
        #print("values var:", self.input_var3.get())
        #print("data var:", self.entry.get())


        #core.pokaz_2D_fun(fcelu, root=self.root, rotation=0)

        #core.pokaz_3D_fun(Fcelu, root=self.root, rotation=0, zakres=[-3, 3])
        #core.pokaz_3D_fun_map(Fcelu, root=self.root, rotation=0, zakres=[-3, 3])

        #core.pokaz_2D_dane(kDane3, root=self.root, rotation=0)
        #core.pokaz_3D_dane(kDane3, root=self.root, rotation=0)


        #core.datafy("1,1,1,2;1,2,3,9;2,3,4,9;3,4,5,9;4,5,6,9;5,6,7,9;6,7,8,9")

        #koniec strefy testowej


        #collecting variables (for clarity)
        typeD=self.type_var.get()
        dimension=self.dimensions_var.get()
        data=self.entry.get()
        rotation=self.slider_var.get()
        root=self.root
        zakres=[self.input_low.get(), self.input_high.get()]
        separators = [self.input_values_separator.get(), self.input_tuple_separator.get()]
        custom = [self.input_var1.get(), self.input_var2.get(), self.input_var3.get()]

        #generating graph
        success = core.show_graph(typeD, dimension, data, zakres, rotation, root, separators, custom)
        


        #zmiana stanu przycisków zapisu stanu
        if success:
            self.entry.configure(text_color="white")
            if typeD=="funkcja (experimental)":
                self.buttonData.configure(state="normal")
            else:
                self.buttonData.configure(state="disabled")
            self.buttonSVG.configure(state="normal")
        else:
            self.entry.configure(text_color="red")





    #callback obsługi zapisu do pliku
    def save_data(self):
        core.save_to_data()

    #callback obsługi zapisu do zdjęcia
    def save_svg(self):
        core.save_to_svg()

    #


#app initializer
if __name__ == "__main__":        
    CTK_Window = ctkApp()
    core.var()
    
    