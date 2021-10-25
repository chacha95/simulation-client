from bokeh.models.callbacks import CustomJS

callback = CustomJS(args=dict(xr=plot.x_range), code="""
// JS code in here

const a = 10;

// the model that triggered the callback is cb_obj
const b = cb_obj.value

""")