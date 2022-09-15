import pymel.core as pm

# get the first object that's selected
try:
    prop = pm.selected()[0]
    prop_transform = prop.getTransform()                          #holds transform node
    # prop_shape = prop.getShape()                                  #holds shape node
except IndexError:  
    raise IndexError('Nothing selected, unsure what to run on. Please select something')

#center the prop by the pivot
pm.move(0, 0, 0, prop_transform, rotatePivotRelative = True)

#Grab pivot in worldSpace
#Assume the mesh's rotate pivot = scale pivot
pivot = prop.getPivots(worldSpace = True)[0]


bb = pm.exactWorldBoundingBox(prop_transform)
bb_min_x = bb[0]    #x-min of object in world space
bb_max_x = bb[3]    #x-max of object in world space

radius = max(bb_max_x, abs(bb_min_x))

#Create the CTRLS with radius bigger than the boundingBox

master_ctrl = pm.circle(c = (0, 0, 0), r = radius + radius * 0.5, name = 'master_CTRL')
pm.rotate(master_ctrl, 90, 0, 0)
pm.makeIdentity(master_ctrl[0], apply = True, scale = True, translate = True, rotate = True);

offset_ctrl = pm.circle(c = (0, 0, 0), r = radius + radius * 0.3, name = 'offset_CTRL')
pm.rotate(offset_ctrl, 90, 0, 0)
pm.makeIdentity(offset_ctrl[0], apply = True, scale = True, translate = True, rotate = True);

# Basic parenting Hierarchy
pm.parent(offset_ctrl, master_ctrl, s = True, r = True);
geo_grp_name = pm.group(prop, name = prop_transform + '_GEO_GRP') 
pm.parentConstraint(offset_ctrl, geo_grp_name);