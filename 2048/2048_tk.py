import tkinter as tk
from random import randint
import numpy as np

class Application(tk.Frame):
    def __init__(self, master=None):
        self.table = np.array([[0]*4]*4)
        self.turn = 0


        super().__init__(master, padx = 30, pady=10)
        self.pack()
        self.create_widgets()


    def create_widgets(self):

        #text thing
        self.text_thing = tk.Text(self, font=('Helvetica', '30'), bg="#eee")
        self.text_thing.pack(side="top")
        self.text_thing["height"] = 4
        self.text_thing["width"] = 4


        # command buttons
        self.command_button_frame = tk.LabelFrame(self,text="Command Buttons")
        self.command_button_frame.pack(side= "top")

        self.down_button = tk.Button(self.command_button_frame, text="V", command=lambda: self.press("down"))
        self.down_button.pack(side="bottom")

        self.up_button = tk.Button(self.command_button_frame, text="^", command=lambda: self.press("up"))
        self.up_button.pack(side="top")

        self.left_button = tk.Button(self.command_button_frame, text="<", command=lambda: self.press("left"))
        self.left_button.pack(side="left")

        self.right_button = tk.Button(self.command_button_frame, text=">", command=lambda: self.press("right"))
        self.right_button.pack(side="right")



        # quit Button
        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=root.destroy)
        self.quit.pack(side="bottom")

    def press(self, direction):
        self.table = move(self.table, direction)
        table_new = get_random(self.table)
        if table_new is self.table:
            # Todo: move cursor to display this text lower
            print("No empty squares: game is over! You survived {} turns \
             with a score of {}. Press any key to quit.".format(self.turn, self.table.max()))

        else:
            self.table = table_new
            self.turn += 1

        self.disp()

    def say_hi(self):
        print("hi there, everyone!")
        self.disp()

    def disp(self):
        # clear the textbox
        self.text_thing.delete("1.0", "1.0 + 5 lines")
        for l in range(1,5):
            list_of_int = list(self.table[l-1, :])
            list_of_str = map(str, list_of_int)
            to_insert = "".join(list_of_str)
            to_insert = to_insert.replace("0", " ")
            #to_insert+= '\n'
            self.text_thing.insert(str(l)+".0", to_insert)






def get_random (table):
    """ Places a random 1 or 2 in an empty square of the table"""
    # count empty slots
    tab = table.flatten()
    count = 0
    for item in tab:
        if item == 0:
            count += 1

    if count == 0:
        # No empty squares, we return None
        return table

    # choose one at random
    selected = randint(1,count)

    # fill it with at random 1 or 2
    count = 0
    index = None
    for idx, item in enumerate(tab):
        if item == 0:
            count += 1
            if count == selected:
                index = idx
                break

    tab[index] = randint(1,2)
    ans = np.reshape(tab, (4,4))
    return ans


def reduce_row(row):
    """ reduces one row, in the direction end --> start of list"""
    # remove empty space below
    while 0 in row:
        row.remove(0)

    # combine numbers if possible
    idx = 0
    end = len(row)
    while idx < end:
        if idx < end-1 and row[idx] == row [idx+1] != 0:
            row.pop(idx) #remove item at idx
            row[idx] += 1
            end -= 1
        idx += 1

    # repad with 0's on the other end
    row = row +[0]*(4-len(row))
    return row


def move(table, direction):
    """ Returns a table after the move has been completed"""
    rotations = {"down": 3, "up": 1, "left":0, "right":2}

    k = rotations[direction]
    rotated = np.rot90(table, k) # flip to have the  "down" pointing left (so each row is correctly aligned)
    rot_reduced = []
    for r in rotated:
        rot_reduced.append(reduce_row(r.tolist()))


    ans = np.array(rot_reduced)
    ans = np.rot90(ans, -k)

    return ans



root = tk.Tk()
app = Application(master=root)
app.master.title("2048 game")
app.mainloop()
