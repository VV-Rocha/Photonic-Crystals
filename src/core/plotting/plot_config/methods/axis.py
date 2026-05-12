class Axis:
    def set_axis_labels(
        self,
        xaxis_label=None,
        yaxis_label=None,
        zaxis_label=None,
        units=True,
    ):
        if xaxis_label is not None:
            self.xaxis_label = xaxis_label
            if units:
                self.xaxis_label += f" ({self.units})"
        if xaxis_label is not None:
            self.yaxis_label = yaxis_label
            if units:
                self.yaxis_label += f" ({self.units})"
        if xaxis_label is not None:
            self.zaxis_label = zaxis_label
    
    def axis_labels(self,):
        return (self.xaxis_label, self.yaxis_label, self.zaxis_label)