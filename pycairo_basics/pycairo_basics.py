#!/usr/bin/env python

    #what I downloaded in the terminal before running this!!!!
    #`conda create -n motifmark`
    #`conda activate motifmark`
    #`conda install -c conda-forge pycairo`

import cairo

#assigning the width and height of the image
width, height = 200, 200

#making the parameters (the size of the output) and naming the output
surface = cairo.SVGSurface("pycairo_basics.svg", width, height)
#making the content onto the surface
context = cairo.Context(surface)

#everything below is drawing ontop of the surface --------------------

#drawing a red horizontal line
context.set_line_width(5)
context.set_source_rgba(0.5, 0, 0) #red
context.move_to(50,25)
context.line_to(150,25)
context.stroke()

#drawing a blue vertical line
context.set_line_width(5)
context.set_source_rgb(0, 0, 1) #blue
context.move_to(175,50)
context.line_to(175,150)
context.stroke()

#drawing a rectangle
context.set_source_rgb(0.5, 0.5, 1) #light purple
context.rectangle(50,50,100,100)    #(x0,y0,x1,y1) (x_start, y_start, x_distance, y_distance)
context.fill()
surface.finish()

