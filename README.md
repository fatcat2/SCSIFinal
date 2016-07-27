Requires Python 2.7, OpenCV, and NumPy.

A set of programs designed to track multiple objects in a frame, using Camshift for object continuity.
It will detect contours after screening for a specific range of HSV values, supplied as two tuples, then use the minimum area rectangle thereof to determine the (rough) center. Both are then passed to a set of TrackedObjects, each of which has its own Camshift built in. The Skeleton class contains a list of pairs of references to TrackedObjects, and will draw lines between each pair.

Proposal: