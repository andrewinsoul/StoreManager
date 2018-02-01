import tkinter as tk, os
import tkinter.ttk as ttk
import check_number as cn
import tkinter.messagebox
from math import sin, cos, radians, sqrt, atan, degrees
main = tk.Tk()
main.resizable(0, 0)
imgicon = tk.PhotoImage(file=os.path.join('c:\\users\\user\\pycharmprojects\\app_store', 'casio_icon.png'))
main.tk.call('wm', 'iconphoto', main._w, imgicon)
main.title('Resultant Calculator')
main.config(bg='sky blue')
frame1 = tk.Frame(main)
frame1.winfo_toplevel().geometry('400x150+450+220')
frame1.config(bg='sky blue')
frame1.grid(sticky=tk.N+tk.S+tk.E+tk.W)
k = 2; index = 0; force_var = tk.StringVar(); ent2 = tk.Entry(main); ent3 = tk.Entry(main)
ent4 = tk.Entry(main); ent5 = tk.Entry(main); lab2 = tk.Entry(main); lab3 = tk.Entry(main); lab4 = tk.Entry(main)
lab5 = tk.Entry(main)
horizontal_var = tk.StringVar(); vertical_var = tk.StringVar(); angle_var = tk.StringVar(); btn2 = tk.Button(main)
frame2 = tk.Frame(main); tupleForce = (); force_list = []
h_force = []; v_force = []; angle_list = []; diagram_list = []; H_ans = []; V_ans = []
a = 450; b = 180; c = 335; d = 330; e = 150; f = 170; g = 270; h = 330
aru45 = 490; bru45 = 100; ard45 = 500; brd45 = 350; alu45 = 170; blu45 = 50; ald45 = 200; bld45 = 350
copyright_label = ''

def resultant():

    def illustration():
        global a, b, c, d, e, f, g, h, aru45, bru45, ard45, brd45, alu45, blu45, ald45, bld45
        def sketch_angle(theta, radius=150, color='red'):
            theta = -radians(theta)
            x = 300 + radius * cos(theta)
            y = 250 + radius * sin(theta)
            can.create_line(300, 250, x, y, arrow='last', width=2, fill=color)
            return x, y

        def illustration2():
            def illustration3():
                pic_window2.withdraw()
                pic_window.deiconify()
                return 0
            pic_window.withdraw()
            pic_window2 = tk.Toplevel(main, takefocus=True, bg='dark turquoise')
            pic_window2.tk.call('wm', 'iconphoto', pic_window2._w, imgicon)
            pic_window2.geometry('600x550+300+81')
            pic_window2.resizable(0, 0)
            can2 = tk.Canvas(pic_window2, width=600, height=500, bg='dark turquoise')
            can2.grid()
            can2.create_line(0, 250, 600, 250, arrow='both', dash=(3, 5))  # create x-axis
            can2.create_text(315, 10, text='+y', font='helvetica 10 bold italic')
            can2.create_line(300, 0, 300, 500, arrow='both', dash=(3, 5))  # create y-axis
            can2.create_text(315, 485, text='-y', font='helvetica 10 bold italic')
            can2.create_text(10, 235, text='-x', font='helvetica 10 bold italic')
            can2.create_text(590, 235, text='+x', font='helvetica 10 bold italic')
            theta = degrees(atan(sum(V_ans) / sum(H_ans)))
            F = sqrt(pow(sum(H_ans), 2) + pow(sum(V_ans), 2))
            F = round(F, 1)
            theta = round(theta, 1)
            if theta == 90:
                theta = radians(theta)
                x = 300 + 150 * cos(theta)
                y = 250 + 150 * sin(theta)
                can2.create_line(300, 250, x, y, arrow='last', width=2, fill='navy')
                can2.create_line(x, y, x, 250, dash=(4, 5))
                can2.create_line(x, y, 300, y, dash=(4, 5))
                can2.create_text(x+10,y-20, text='(Resultant='+str(F)+'N, '+ '\u03B8='+str(90)+'\u2070'+')',
                                 font='purita 10 bold italic')
            elif theta == 180:
                theta = radians(theta)
                x = 300 + 150 * cos(theta)
                y = 250 + 150 * sin(theta)
                can2.create_line(300, 250, x, y, arrow='last', width=2, fill='navy')
                can2.create_line(x, y, x, 250, dash=(4, 5))
                can2.create_line(x, y, 300, y, dash=(4, 5))
                can2.create_text(x + 10, y - 20,
                                 text='(Resultant = ' + str(F) + 'N, ' + '\u03B8 = ' + str(180) + '\u2070' +
                                      ')',
                                 font='purita 10 bold italic')
            elif theta == 270:
                theta = radians(theta)
                x = 300 + 150 * cos(theta)
                y = 250 + 150 * sin(theta)
                can2.create_line(300, 250, x, y, arrow='last', width=2, fill='navy')
                can2.create_line(x, y, x, 250, dash=(4, 5))
                can2.create_line(x, y, 300, y, dash=(4, 5))
                can2.create_text(x + 10, y - 20,
                                 text='(Resultant = ' + str(F) + 'N, ' + '\u03B8 = ' + str(270) + '\u2070' +
                                      ')',
                                 font='purita 10 bold italic')
            elif theta == 360:
                theta = radians(theta)
                x = 300 + 150 * cos(theta)
                y = 250 + 150 * sin(theta)
                can2.create_line(300, 250, x, y, arrow='last', width=2, fill='navy')
                can2.create_line(x, y, x, 250, dash=(4, 5))
                can2.create_line(x, y, 300, y, dash=(4, 5))
                can2.create_text(x + 10, y - 20,
                                 text='(Resultant = ' + str(F) + 'N, ' + '\u03B8 = ' + str(360) + '\u2070' +
                                      ')',
                                 font='purita 10 bold italic')
            else:
                theta1 = radians(theta)
                x = 300 + 150 * cos(theta)
                y = 250 + 150 * sin(theta)
                can2.create_line(300, 250, x, y, arrow='last', width=2, fill='navy')
                can2.create_line(x, y, x, 250, dash=(4, 5))
                can2.create_line(x, y, 300, y, dash=(4, 5))
                can2.create_text(x + 10, y - 20,
                                 text='(Resultant = ' + str(F) + 'N, ' + '\u03B8 = ' + str(theta) + '\u2070' +
                                      ')',
                                 font='purita 10 bold italic')
            btn12 = tk.Button(pic_window2, text='Back to Previous Diagram', bg='dark turquoise', bd=4,
                              command=illustration3, cursor='hand2', font='helvetica 9 bold italic')
            btn12.grid()
            def illustration3_handler(event):
                illustration3()
            btn12.bind('<Return>', illustration3_handler)
            return 0

        main.withdraw()
        pic_window = tk.Toplevel(main, takefocus=True, bg='dark turquoise')
        pic_window.tk.call('wm', 'iconphoto', pic_window._w, imgicon)
        pic_window.geometry('650x590+325+81')
        pic_window.resizable(0,0)
        can = tk.Canvas(pic_window, height=500, width=600, bg='dark turquoise', bd=0)
        can.grid(padx=20, pady=20)
        # print(can.grid_info())
        can.create_line(0, 250, 600, 250, arrow='both', dash=(3,5)) # create x-axis
        can.create_text(315, 10, text='+y', font='helvetica 10 bold italic')
        can.create_line(300, 0, 300, 500, arrow='both', dash=(3,5)) # create y-axis
        can.create_text(315, 485, text='-y', font='helvetica 10 bold italic')
        can.create_text(10, 235, text='-x', font='helvetica 10 bold italic')
        can.create_text(590, 235, text='+x', font='helvetica 10 bold italic')
        x_center, y_center = 300, 250
        for val in diagram_list:
            if (val[1], val[2]) == ('right', 'up'):
                if val[3] == 0:
                    can.create_line(300,250,450+val[0],250, arrow='last', width=2)
                    can.create_text(450, 240, text='(' +str(val[0])+'N'+', '+ str(val[3]) + \
                '\u2070'+')', font='purita 10 bold')
                elif val[3] == 90:
                    can.create_line(300,250,300,100+val[0], arrow='last', width=2)
                    can.create_arc(280, 230, 320, 270, start=0, extent=90 )
                    can.create_text(330, 100, text='(' +str(val[0])+'N'+', '+ str(val[3]) + \
                '\u2070'+')', font='purita 10 bold')
                else:
                    x, y = sketch_angle(val[3], radius=150+val[0])
                    can.create_arc(280, 230, 320, 270, start=0, extent=val[3])
                    can.create_text(x+30, y+5, text='(' +str(val[0])+'N'+', '+ str(val[3]) + \
                '\u2070'+')', font='purita 10 bold')
            elif (val[1], val[2]) == ('right', 'down'):
                if val[3] == 0:
                    can.create_line(300,250,450+val[0],250, arrow='last', width=2)
                    can.create_text(450, 240, text='(' +str(val[0])+'N'+', '+ str(val[3]) + \
                '\u2070'+')', font='purita 10 bold')
                elif val[3] == 90:
                    can.create_line(300,250,300,400+val[0], arrow='last', width=2)
                    can.create_arc(280,230,320,270, start=0, extent=-90)
                    can.create_text(330, 400, text='(' +str(val[0])+'N'+', '+ str(val[3]) + \
                '\u2070'+')', font='purita 10 bold')
                else:
                    x, y = sketch_angle(360-val[3], radius=150+val[0])
                    can.create_arc(280, 230, 320, 270, start=0, extent=-val[3])
                    can.create_text(x+30, y+5, text='(' +str(val[0])+'N'+', '+ str(val[3]) + \
                '\u2070'+')', font='purita 10 bold')
            elif (val[1], val[2]) == ('left', 'up'):
                if val[3] == 0:
                    can.create_line(300,250,150+val[0],250, arrow='last', width=2)
                    can.create_text(150, 240, text='(' +str(val[0])+'N'+', '+ str(val[3]) + \
                '\u2070'+')', font='purita 10 bold')
                elif val[3] == 90:
                    can.create_line(300,250,300,100+val[0], arrow='last', width=2)
                    can.create_arc(280,230,320,270, start=180, extent=-90)
                    can.create_text(330,100, text='(' +str(val[0])+'N'+', '+ str(val[3]) + \
                '\u2070'+')', font='purita 10 bold')
                else:
                    x, y = sketch_angle(180-val[3], radius=150+val[0])
                    can.create_arc(280, 230, 320, 270, start=180, extent=-val[3])
                    can.create_text(x-10, y-5, text='(' +str(val[0])+'N'+', '+ str(val[3]) + \
                '\u2070'+')', font='purita 10 bold')
            else: # (left, down)
                if val[3] == 0:
                    can.create_line(300,250,150+val[0],250, width=2, arrow='last')
                    can.create_text(150, 240, text='(' +str(val[0])+'N'+', '+ str(val[3]) + \
                '\u2070'+')', font='purita 10 bold')
                elif val[3] == 90:
                    can.create_line(300,250,300,400+val[0], arrow='last', width=2)
                    can.create_arc(280,230,320,270, start=270, extent=-90)
                    can.create_text(330, 400, text='(' +str(val[0])+'N'+', '+ str(val[3]) + \
                '\u2070'+')', font='purita 10 bold')
                else:
                    x, y = sketch_angle(180+val[3], radius=150+val[0])
                    can.create_arc(280, 230, 320, 270, start=180, extent=val[3])
                    can.create_text(x-10, y+8, text='(' +str(val[0])+'N'+', '+ str(val[3]) + \
                '\u2070'+')', font='purita 10 bold')
        btn = tk.Button(pic_window, text='Next\nDiagram', font='helvetica 9 bold italic', bg='dark turquoise',
                        bd=4, command=illustration2, cursor='hand2')
        btn.grid()
        def illustration2_handler(event):
            illustration2()
        btn.bind('<Return>', illustration2_handler)
        return 0

    global force_list, h_force, v_force, angle_list, tupleForce, copyright_label
    if not cn.isnumber(force_var.get()):
        tkinter.messagebox.showerror('Invalid input', 'value of force must be a number')
        ent2.delete(0, 'end')

    elif (horizontal_var.get() != 'right' or horizontal_var.get() == 'left') and \
            (horizontal_var.get() == 'right' or horizontal_var.get() != 'left'):
        tkinter.messagebox.showerror('Invalid input', 'Horizontal position must either be left or right')
        ent3.delete(0, 'end')

    elif (vertical_var.get() != 'up' or vertical_var.get() == 'down') and \
            (vertical_var.get() == 'up' or vertical_var.get() != 'down'):
        tkinter.messagebox.showerror('Invalid input', 'Vertical position must either be up or down')
        ent4.delete(0, 'end')

    elif not cn.isnumber(angle_var.get()) or not(0 <= eval(angle_var.get()) <= 90.0):
        tkinter.messagebox.showerror('Invalid input', 'value of angle must be a positive number '
                                                      'less than or equal to 90')
        ent5.delete(0, 'end')

    else:
        tupleForce = (eval(force_var.get()), horizontal_var.get(), vertical_var.get(), eval(angle_var.get()))
        diagram_list.append(tupleForce)
        force_list.append(tupleForce[0])
        if tupleForce[1] == 'right':
            h_force.append(tupleForce[0])
        else:
            h_force.append(-tupleForce[0])
        if tupleForce[2] == 'up':
            v_force.append(tupleForce[0])
        else:
            v_force.append(-tupleForce[0])
        angle_list.append(radians(tupleForce[3]))
        lab2.grid_forget()
        lab3.grid_forget()
        lab2.grid_forget()
        lab1.grid_forget()
        lab4.grid_forget()
        lab5.grid_forget()
        ent3.grid_forget()
        ent2.grid_forget()
        ent4.grid_forget()
        ent5.grid_forget()
        btn2.grid_forget()
        n = 0
        for value in h_force:
            H_ans.append(value * cos(angle_list[n]))
            n += 1

        n = 0
        for value in v_force:
            V_ans.append(value * sin(angle_list[n]))
            n += 1
        ans1 = ''

        def scrollbar_handler_up(event):
            text_ans.yview(tk.SCROLL, -2, 'units')

        def scrollbar_handler_down(event):
            text_ans.yview(tk.SCROLL, 2, 'units')
        frame2.winfo_toplevel().geometry('554x460+430+120')
        scroll_style = ttk.Style()
        scroll_style.configure('odk.Vertical.TScrollbar', troughcolor='light green', bg='navy', width=8)
        scroller = ttk.Scrollbar(frame2, style='odk.Vertical.TScrollbar')
        btn3 = tk.Button(main, text='view illustration', font='helvetica 12 bold italic',
                         bg='dark turquoise', bd=4, command=illustration, cursor='hand2')
        def illustration_handler(event):
            illustration()
        btn3.bind('<Return>', illustration_handler)
        copyright_label = tk.Label(main, text=u'\N{copyright sign}' + ' an Andy Production',
                                   bg='sky blue', font='helvetica 10 bold italic')
        text_ans = tk.Text(frame2, bg='sky blue', font='helvetica 12', width=59, height=18)
        text = 'Force\t\tX-component\t\t  Y-component'
        lab = tk.Label(frame2, text=text,
                       font='helvetica 12 bold italic', bg='sky blue')
        lab.grid(row=0, column=0, pady=5, sticky='nsew')
        for val1, val2, val3 in list(zip(force_list, H_ans, V_ans)):
            ans1 += '       {0: ^9.2f} {1: ^70.4f}{2: ^29.4f}\n'.format(val1, val2, val3)
            ans1 += '_' * 59
            ans1 += '\n'
        text_ans.insert(tk.END, ans1)
        text_ans.config(state=tk.DISABLED)
        frame2.grid()
        text_ans.grid(row=1, column=0, sticky=tk.N + tk.S + tk.E)
        scroller.grid(row=1, column=1, sticky=tk.N + tk.S + tk.W)
        scroller.configure(command=text_ans.yview)
        text_ans.configure(yscrollcommand=scroller.set)
        main.bind('<Up>', scrollbar_handler_up)
        main.bind('<Down>', scrollbar_handler_down)
        btn3.grid(pady=20)
        copyright_label.grid(sticky=tk.E)
        return 0

def calc():
    global angle_var, lab2, ent2, ent3, lab3, ent4, lab4, ent5, lab5, btn2, frame2, diagram_list
    def counter():
        global index
        f_var = force_var.get()
        h_var = horizontal_var.get()
        v_var = vertical_var.get()
        a_var = angle_var.get()
        if not cn.isnumber(f_var):
            tkinter.messagebox.showerror('Invalid input', 'value of force must be a number')
            ent2.delete(0, 'end')
        elif (h_var != 'right' or h_var == 'left') and (h_var == 'right' or h_var != 'left'):
            tkinter.messagebox.showerror('Invalid input', 'Horizontal position must either be left or right')
            ent3.delete(0, 'end')
        elif (v_var != 'up' or v_var == 'down') and (v_var == 'up' or v_var != 'down'):
            tkinter.messagebox.showerror('Invalid input', 'Vertical position must either be up or down')
            ent4.delete(0, 'end')
        elif not cn.isnumber(a_var) or not(0 <= eval(a_var) <= 90):
            tkinter.messagebox.showerror('Invalid input', 'value of angle must be a positive number '
                                                          'less than or equal to 90')
            ent5.delete(0, 'end')
        else:
            tupleForce = (eval(force_var.get()), horizontal_var.get(), vertical_var.get(), eval(angle_var.get()))
            diagram_list.append(tupleForce)
            force_list.append(tupleForce[0])
            if tupleForce[1] == 'right':
                h_force.append(tupleForce[0])
            else:
                h_force.append(-tupleForce[0])
            if tupleForce[2] == 'up':
                v_force.append(tupleForce[0])
            else:
                v_force.append(-tupleForce[0])
            angle_list.append(radians(tupleForce[3]))
            index += 1
            global k
            frame2.grid_forget()
            if k <= int(var1.get()):
                if k == int(var1.get()):
                    btn2.config(text='Compute\n\nResultant', command=resultant, font='helvetica 8 bold italic')
                    def resultant_handler(event):
                        resultant()
                    btn2.bind('<Return>', resultant_handler)
                frame2.grid()
                lab2.config(text='Enter Force ' + str(k) + ': ')
                lab5.config(text='Angle of Force ' + str(k) + ': ')
                ent2.delete(0, 'end')
                ent3.delete(0, 'end')
                ent4.delete(0, 'end')
                ent5.delete(0, 'end')
                k += 1
        return 0
    if var1.get().isdecimal():
        frame1.grid_forget()
        frame2.config(bg='sky blue')
        frame2.winfo_toplevel().geometry('350x250+450+220')
        lab2 = tk.Label(frame2, text='{0:>20s}'.format('Enter Force 1: '), width=20, font='helvetica 10 bold',
                        bg='sky blue')
        ent2 = tk.Entry(frame2, textvariable=force_var, font='helvetica 10 bold')
        lab3 = tk.Label(frame2, text='Horizontal Position: ', width=20, font='helvetica 10 bold', bg='sky blue')
        ent3 = tk.Spinbox(frame2, values=('right', 'left'), textvariable=horizontal_var,
                          font='helvetica 10 bold', wrap=True)
        lab4 = tk.Label(frame2, text='Vertical Position: ', width=20, font='helvetica 10 bold', bg='sky blue')
        ent4 = tk.Spinbox(frame2, values=('up', 'down'), textvariable=vertical_var, font='helvetica 10 bold', wrap=True)
        lab5 = tk.Label(frame2, text='{0:>20s}'.format('Angle of Force 1: '), width=20, font='helvetica 10 bold',
                        bg='sky blue')
        ent5 = tk.Entry(frame2, textvariable=angle_var, font='helvetica 10 bold')
        if int(var1.get()) == 1:
            btn2 = tk.Button(text='Compute\n\nResultant', command=resultant, font='helvetica 8 bold italic',
                             cursor='hand2', bg='dark turquoise', bd=4)
            def resultant_handler1(event):
                resultant()
            btn2.bind('<Return>', resultant_handler1)
        else:
            btn2 = tk.Button(frame2, text='continue', cursor='hand2', command=counter, font='helvetica 12 bold italic',
                         bd=4, bg='dark turquoise')
            def counter_handler(event):
                if int(var1.get()) == k-1:
                    resultant()
                else:
                    counter()
            btn2.bind('<Return>', counter_handler)
        ent3.delete(0, 'end')
        ent4.delete(0, 'end')
        frame2.grid()
        lab2.grid(row=0, column=0, pady=12)
        ent2.grid(row=0, column=1)
        lab3.grid(row=1, column=0, pady=10)
        ent3.grid(row=1, column=1)
        lab4.grid(row=2, column=0, pady=10)
        ent4.grid(row=2, column=1)
        lab5.grid(row=3, column=0, pady=10)
        ent5.grid(row=3, column=1)
        btn2.grid(columnspan=4, column=0, pady=20)
    else:
        tkinter.messagebox.showerror('Error', 'value must be an integer')
        ent1.delete(0, 'end')
    return 0

lab1 = tk.Label(frame1, text='Number of Coplanar Force: ', width=25, bg='sky blue', font='helvetica 10 bold')
var1 = tk.StringVar()
ent1 = tk.Entry(frame1, textvariable=var1, font='helvetica 10 bold')
btn1 = tk.Button(frame1, text='continue', cursor='hand2', command=calc, font='helvetica 12 bold italic',
                 bd=4, bg='dark turquoise')
def calc_handler(event):
    calc()
btn1.bind('<Return>', calc_handler)
lab1.grid(row=0, column=0, pady=10, padx=5)
ent1.grid(row=0, column=1, sticky=tk.E+tk.W)
btn1.grid(row=3, column=0, columnspan=16, pady=50, padx=150)
main.mainloop()
