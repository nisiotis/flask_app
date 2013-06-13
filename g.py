
def do_g():
    from flask import send_file
    from flask import Response
    from matplotlib.pyplot import figure
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    fig1 = figure(figsize=(5.33,4), facecolor = 'white')
    ax = fig1.add_axes([0.02,0.02,0.98,0.98], aspect='equal')

        # Some plotting to ax

    canvas=FigureCanvas(fig1)
    res = Response(response = send_file(canvas.savefig('test.png'), mimetype="image/png"),
                        status=200,
                        mimetype="image/png")
    
    fig1.clear()
    return res

