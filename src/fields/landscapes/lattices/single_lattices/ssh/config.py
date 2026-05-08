class SSHConfig:
    def __init__(
        self,
        landscape_config,
        *args,
        **kwargs,
    ):
        self.a = landscape_config["a"]
        self.c = landscape_config["c"]
        self.intra_cell = landscape_config["intra_cell"]
        self.dimerization = landscape_config["dimerization"]

        super().__init__(*args, **kwargs)