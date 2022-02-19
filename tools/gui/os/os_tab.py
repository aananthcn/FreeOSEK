import tkinter as tk
from tkinter import ttk

class OsTab:
    OS_StrVar = []
    sg_oscfg = None
    sg_tasks = None

    def __init__(self, oscfg, tasks):
        self.sg_oscfg = oscfg
        if not oscfg:
            self.create_empty_os_config()
        self.sg_tasks = tasks
        ncfgs = len(self.sg_oscfg)
        for i in range(ncfgs):
            self.OS_StrVar.insert(i, tk.StringVar())


    def __del__(self):
        del self.OS_StrVar[:]
        self.sg_oscfg = None


    def draw(self, tab):
        # 1) CPU / SoC - Label + Edit-box
        label = tk.Label(tab, text="CPU / SoC name")
        label.grid(row=1, column=1, sticky="w")
        textb = tk.Entry(tab,text="Entry", width=30, textvariable=self.OS_StrVar[0])
        self.OS_StrVar[0].set(self.sg_oscfg["CPU"])
        textb.grid(row=1, column=2)
    
        # 2) OS Name - Label + Edit-box
        label = tk.Label(tab, text="Image Name")
        label.grid(row=2, column=1, sticky="w")
        textb = tk.Entry(tab, text="Entry", width=30, textvariable=self.OS_StrVar[1])
        self.OS_StrVar[1].set(self.sg_oscfg["OS"])
        textb.grid(row=2, column=2)
    
        # 3) OSEK Standard - Label + Combo-box
        label = tk.Label(tab, text="OSEK Standard")
        label.grid(row=3, column=1, sticky="w")
        cmbsel = ttk.Combobox(tab, width=27, textvariable=self.OS_StrVar[2], state="readonly")
        cmbsel['values'] = ("STANDARD", "EXTENDED")
        self.OS_StrVar[2].set(self.sg_oscfg["STATUS"])
        cmbsel.current()
        cmbsel.grid(row=3, column=2)

        # 4) STARTUPHOOK - Label + Combo-box
        label = tk.Label(tab, text="STARTUPHOOK")
        label.grid(row=4, column=1, sticky="w")
        cmbsel = ttk.Combobox(tab, width=27, textvariable=self.OS_StrVar[3], state="readonly")
        cmbsel['values'] = ("FALSE", "TRUE")
        self.OS_StrVar[3].set(self.sg_oscfg["STARTUPHOOK"])
        cmbsel.current()
        cmbsel.grid(row=4, column=2)
    
        # 5) ERRORHOOK - Label + Combo-box
        label = tk.Label(tab, text="ERRORHOOK")
        label.grid(row=5, column=1, sticky="w")
        cmbsel = ttk.Combobox(tab, width=27, textvariable=self.OS_StrVar[4], state="readonly")
        cmbsel['values'] = ("FALSE", "TRUE")
        self.OS_StrVar[4].set(self.sg_oscfg["ERRORHOOK"])
        cmbsel.current()
        cmbsel.grid(row=5, column=2)

        # 6) SHUTDOWNHOOK - Label + Combo-box
        label = tk.Label(tab, text="SHUTDOWNHOOK")
        label.grid(row=6, column=1, sticky="w")
        cmbsel = ttk.Combobox(tab, width=27, textvariable=self.OS_StrVar[5], state="readonly")
        cmbsel['values'] = ("FALSE", "TRUE")
        self.OS_StrVar[5].set(self.sg_oscfg["SHUTDOWNHOOK"])
        cmbsel.current()
        cmbsel.grid(row=6, column=2)

        # 7) PRETASKHOOK - Label + Combo-box
        label = tk.Label(tab, text="PRETASKHOOK")
        label.grid(row=7, column=1, sticky="w")
        cmbsel = ttk.Combobox(tab, width=27, textvariable=self.OS_StrVar[6], state="readonly")
        cmbsel['values'] = ("FALSE", "TRUE")
        self.OS_StrVar[6].set(self.sg_oscfg["PRETASKHOOK"])
        cmbsel.current()
        cmbsel.grid(row=7, column=2)

        # 8) POSTTASKHOOK - Label + Combo-box
        label = tk.Label(tab, text="POSTTASKHOOK")
        label.grid(row=8, column=1, sticky="w")
        cmbsel = ttk.Combobox(tab, width=27, textvariable=self.OS_StrVar[7], state="readonly")
        cmbsel['values'] = ("FALSE", "TRUE")
        self.OS_StrVar[7].set(self.sg_oscfg["POSTTASKHOOK"])
        cmbsel.current()
        cmbsel.grid(row=8, column=2)

        # 9) OS_STACK_SIZE - Label + Edit-box
        label = tk.Label(tab, text="OS STACK SIZE")
        label.grid(row=9, column=1, sticky="w")
        textb = tk.Entry(tab, text="Entry", width=30, textvariable=self.OS_StrVar[8])
        self.OS_StrVar[8].set(self.sg_oscfg["OS_STACK_SIZE"])
        textb.grid(row=9, column=2)
        
        # 10) IRQ_STACK_SIZE - Label + Edit-box
        label = tk.Label(tab, text="IRQ STACK SIZE")
        label.grid(row=10, column=1, sticky="w")
        textb = tk.Entry(tab, text="Entry", width=30, textvariable=self.OS_StrVar[9])
        self.OS_StrVar[9].set(self.sg_oscfg["IRQ_STACK_SIZE"])
        textb.grid(row=10, column=2)
        
        # 11) OS_CTX_SAVE_SZ - Label + Edit-box
        label = tk.Label(tab, text="CONTEXT SAVE SIZE FOR TASKS ")
        label.grid(row=11, column=1, sticky="w")
        textb = tk.Entry(tab, text="Entry", width=30, textvariable=self.OS_StrVar[10])
        self.OS_StrVar[10].set(self.sg_oscfg["OS_CTX_SAVE_SZ"])
        textb.grid(row=11, column=2)

        # 12) TASK_STACK_SIZE - Label + Edit-box
        label = tk.Label(tab, text="TASK STACK SIZE (Total)")
        label.grid(row=12, column=1, sticky="w")
        textb = tk.Entry(tab, text="Entry", width=30, textvariable=self.OS_StrVar[11], state="readonly")
        self.OS_StrVar[11].set(self.sg_oscfg["TASK_STACK_SIZE"])
        textb.grid(row=12, column=2)
        
        # 12) Update TASK_STACK_SIZE Button
        select = tk.Button(tab, width=6, text="Update", command=self.update)
        select.grid(row=15, column=3)


    def update(self):
        self.backup_data()
        # Recalculate parameters and update
        task_stack_size = 0
        n_tasks = len(self.sg_tasks)
        for tsk in self.sg_tasks:
            task_stack_size += (int(self.sg_oscfg["OS_CTX_SAVE_SZ"]) + int(tsk["STACK_SIZE"]))
        
        self.OS_StrVar[14].set(task_stack_size)


    def backup_data(self):
        # Backup to system generator global variables
        self.sg_oscfg["CPU"]                   = self.OS_StrVar[0].get()
        self.sg_oscfg["OS"]                    = self.OS_StrVar[1].get()
        self.sg_oscfg["STATUS"]                = self.OS_StrVar[2].get()
        self.sg_oscfg["STARTUPHOOK"]           = self.OS_StrVar[3].get()
        self.sg_oscfg["ERRORHOOK"]             = self.OS_StrVar[4].get()
        self.sg_oscfg["SHUTDOWNHOOK"]          = self.OS_StrVar[5].get()
        self.sg_oscfg["PRETASKHOOK"]           = self.OS_StrVar[6].get()
        self.sg_oscfg["POSTTASKHOOK"]          = self.OS_StrVar[7].get()
        self.sg_oscfg["OS_STACK_SIZE"]         = self.OS_StrVar[8].get()
        self.sg_oscfg["IRQ_STACK_SIZE"]        = self.OS_StrVar[9].get()
        self.sg_oscfg["OS_CTX_SAVE_SZ"]        = self.OS_StrVar[10].get()
        self.sg_oscfg["TASK_STACK_SIZE"]       = self.OS_StrVar[11].get()
    
    
    def create_empty_os_config(self):
        # Backup to system generator global variables
        self.sg_oscfg["CPU"]                   = ""
        self.sg_oscfg["OS"]                    = ""
        self.sg_oscfg["STATUS"]                = "STANDARD"
        self.sg_oscfg["STARTUPHOOK"]           = "FALSE"
        self.sg_oscfg["ERRORHOOK"]             = "FALSE"
        self.sg_oscfg["SHUTDOWNHOOK"]          = "FALSE"
        self.sg_oscfg["PRETASKHOOK"]           = "FALSE"
        self.sg_oscfg["POSTTASKHOOK"]          = "FALSE"
        self.sg_oscfg["OS_STACK_SIZE"]         = "512"
        self.sg_oscfg["IRQ_STACK_SIZE"]        = "512"
        self.sg_oscfg["OS_CTX_SAVE_SZ"]        = "128"
        self.sg_oscfg["TASK_STACK_SIZE"]       = "0"