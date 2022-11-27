import tkinter as tk


class Handle(object):
    """Represents the handle object at the end of the slider.

These can be moved by the mouse to modify the values."""
    def __init__(self, coordinates, color, canvas):
        self.x0, self.y0, self.x1, self.y1, self.x2, self.y2, self.x3, self.y3 = coordinates
        self.color = color
        self.canvas = canvas

    def draw(self):
        self.polygon = self.canvas.create_polygon(self.x0, self.y0, self.x1, self.y1, self.x2, self.y2, fill=self.color)
        self.line = self.canvas.create_line(self.x2, self.y2, self.x3, self.y3, width=2)

    def move(self, dx, dy):
        self.canvas.move(self.polygon, dx, dy)
        self.canvas.move(self.line, dx, dy)
        self.x0 += dx
        self.x1 += dx
        self.x2 += dx
        self.x3 += dx

class Slider2Scale(object):
    """Represents a scale with two sliders.

This scale can be used to set both ends of a range of an integer variable."""
    def __init__(self, parent, bg="white", var1=0, var2=100, size=(180,40)):
        self.frame = tk.Frame(parent)
        self.frame.grid(row=0, column=0)
        A, B = size
        self.a = B // 4
        self.variablePixelRange = A - self.a
        self.pixelMin, self.pixelMax = self.a//2, A - self.a//2
        self.canvas = tk.Canvas(self.frame, bg=bg, width=A, height=B)
        self.canvas.grid(row=0, column=0, sticky=tk.W+tk.E)
        self.canvas.bind('<ButtonPress-1>', self.mouseClick)
        self.canvas.bind('<ButtonRelease-1>', self.mouseRelease)
        self.canvas.bind('<B1-Motion>', self.mouseMove)
        self.canvas.create_rectangle(self.a//2, self.a, A - self.a//2, B - self.a, fill="lightgrey")
        self.variableMin, self.variableMax = var1, var2
        self.variableRange = self.variableMax - self.variableMin
        self.var1 = tk.IntVar()
        self.var1.set(var1)
        self.entry1 = tk.Entry(self.frame, width=4, textvariable=self.var1)
        self.entry1.grid(row=1, column=0, sticky=tk.W)
        h1x0, h1y0, h1x1, h1y1, h1x2, h1y2 = 0, B, self.a, B, self.a//2, B - self.a
        h1x3, h1y3 = h1x2, h1y2 - 2 * self.a
        h1color = "red"
        self.handle1 = Handle((h1x0, h1y0, h1x1, h1y1, h1x2, h1y2, h1x3, h1y3), h1color, self.canvas)
        self.handle1.draw()
        self.var2 = tk.IntVar()
        self.var2.set(var2)
        self.entry2 = tk.Entry(self.frame, width=4, textvariable=self.var2)
        self.entry2.grid(row=1, column=0, sticky=tk.E)
        h2x0, h2y0, h2x1, h2y1, h2x2, h2y2 = A - self.a, 0, A, 0, A - self.a//2, self.a
        h2x3, h2y3 = h2x2, h2y2 + 2 * self.a
        h2color = "blue"
        self.handle2 = Handle((h2x0, h2y0, h2x1, h2y1, h2x2, h2y2, h2x3, h2y3), h2color, self.canvas)
        self.handle2.draw()
        self.movingHandle = 0 #0: none, 1: left, 2: right

    def setMin(self, x):
        self.var1.set(x)
        self.variableMin = x
        self.variableRange = self.variableMax - self.variableMin

    def setMax(self, x):
        self.var2.set(x)
        self.variableMax = x
        self.variableRange = self.variableMax - self.variableMin
        
    def mouseClick(self, event):
        """Event to handle left mouse click.

If you click on one of the handles, you can move it and thereby change one of the range values.
It determines, which handle is to be moved."""
        x, y = event.x, event.y
        if (x >= self.handle1.x0 and x <= self.handle1.x1):
            if (y >= self.handle1.y2 and y <= self.handle1.y0) or (y >= self.handle1.y0 and y <= self.handle1.y2):
                self.movingHandle = 1
        if (x >= self.handle2.x0 and x <= self.handle2.x1):
            if (y >= self.handle2.y2 and y <= self.handle2.y0) or (y >= self.handle2.y0 and y <= self.handle2.y2):
                self.movingHandle = 2

    def mouseRelease(self, event):
        """Event to handle left mouse release.

It you release the left mouse button after moving a handle, it switches off handle movement."""
        self.movingHandle = 0

    def mouseMove(self, event):
        """Event to handle mouse movement.

If you click on one of the handles, it becomes the moving handle.
By moving the mouse, you can drag this handle and thereby change one of the range values."""
        if self.movingHandle == 1:
            dx, dy = event.x - self.handle1.x2, 0
            if self.handle1.x2 + dx < self.handle2.x2 and self.handle1.x2 + dx >= self.pixelMin:
                self.handle1.move(dx, dy)
                var1 = self.variableMin + int( round( ( (self.handle1.x2 - self.a//2) / self.variablePixelRange ) * self.variableRange ) )
                self.var1.set(var1)
        elif self.movingHandle == 2:
            dx, dy = event.x - self.handle2.x2, 0
            if self.handle2.x2 + dx > self.handle1.x2 and self.handle2.x2 + dx <= self.pixelMax:
                self.handle2.move(dx, dy)
                var2 = self.variableMin + int( round( ( (self.handle2.x2 - self.a//2) / self.variablePixelRange ) * self.variableRange ) )
                self.var2.set(var2)

    def destroy(self):
        self.frame.destroy()


if __name__ == "__main__":
    root = tk.Tk()

    frame = tk.Frame(root)
    frame.grid(row=0, column=0)
    canvasW, canvasH = 400, 52
    defaultbg = root.cget('bg')
    var1, var2 = 0, 89
    slider2scale = Slider2Scale(frame, defaultbg, var1, var2)

    root.mainloop()

