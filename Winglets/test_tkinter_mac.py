import tkinter as tk
window = tk.Tk()            #主窗口
window.title('my window')   #窗口标题
window.geometry('200x100')  #窗口尺寸
 

# import handler.drawhandler
# import handler.handler_all
# import handler.buttonhandler
# import handler.geoOperation
# import handler.kdehandler
# import handler.mongohandler
# import handler.wingletstephandler
from handler.drawhandler import DrawAllHandler
print('end')

### 这里是窗口的内容###
 
window.mainloop()           #循环消息，让窗口活起来

