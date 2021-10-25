from bokeh.models import CustomJS


def x_trans(source):
    callback = CustomJS(args=dict(source=source), code="""
        const trans_factor = cb_obj.value 
        
        const data = source.data
        var x = data['x']
        var nx = data['nx']

        for (let i = 0; i < x.length; i++) {
            nx[i] = nx[i] + trans_factor
        }

        x = nx

        source.change.emit();
    """)
    return callback


def y_trans(source):
    callback = CustomJS(args=dict(source=source), code="""
        const trans_factor = cb_obj.value 
        
        const data = source.data
        var y = data['y']
        var ny = data['ny']
    
        for (let i = 0; i < y.length; i++) {
            ny[i] = ny[i] + trans_factor
        }

        y = ny

        source.change.emit();
    """)
    return callback


def scale(source):
    callback = CustomJS(args=dict(source=source), code="""
        const scale_factor = cb_obj.value 
        
        const data = source.data
        var x = data['x']
        var y = data['y']

        var nx = data['nx']
        var ny = data['ny']

        for (let i = 0; i < x.length; i++) {
            nx[i] = nx[i] * scale_factor
            ny[i] = ny[i] * scale_factor
        }

        y = ny
        x = nx

        source.change.emit()
    """)
    return callback
