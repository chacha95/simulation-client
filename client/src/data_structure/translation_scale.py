class TransScale:
    def __init__(self) -> None:
        self.map_margin: int
        self.trans_factor_x: int
        self.trans_factor_y: int
        self.scale_factor: int

    def get_map_margin(self) -> int:
        return self.map_margin

    def set_map_margin(self, map_margin: int):
        self.map_margin = map_margin

    def get_trans_factor_x(self) -> int:
        return self.trans_factor_x

    def set_trans_factor_x(self, trans_factor_x: int):
        self.trans_factor_x = trans_factor_x

    def get_trans_factor_y(self) -> int:
        return self.trans_factor_y

    def set_trans_factor_y(self, trans_factor_y: int):
        self.trans_factor_y = trans_factor_y

    def get_scale_factor(self) -> int:
        return self.scale_factor

    def set_scale_factor(self, scale_factor: int):
        self.scale_factor = scale_factor
