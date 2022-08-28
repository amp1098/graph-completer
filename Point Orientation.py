# To check if two line segments intersect, we need to understand "orientation". An ordered triple of points in a plane
# can be either counterclockwise, clockwise or collinear.
#       b
#     ^   \              clockwise
#   /       v
#  a<--------c
#
#       c
#     /  ^               counterclockwise
#   v      \
#  a-------->b
#
#  a----->b------>c      collinear
#
# How does one algorithmically tell the orientation of a set of three points in 2-space?
