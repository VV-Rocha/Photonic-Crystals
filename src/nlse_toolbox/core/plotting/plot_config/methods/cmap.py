class CMap:
    def __init__(self, *args, **kwargs):
        self.cmap = "inferno"
        
        super().__init__(*args, **kwargs)
        
    def set_cmap(self, cmap):
        self.cmap = cmap