# Conversion of RoadNet Json to SUMO NetXML

# XML Road

```
<edge id="E8" from="J0" to="J16" priority="1" spreadType="center" shape="-20.87,48.49 -5.66,48.43">
  <lane id="E8_0" index="0" speed="13.89" length="15.21"/>
</edge>
```

# JSON Road

```
{'id': 'road_0_1_0',
 'points': [{'x': -300, 'y': 0},
            {'x': 0, 'y': 0}],
 'lanes': [{'width': 3, 'maxSpeed': 11.111},
           {'width': 3, 'maxSpeed': 11.111},
           {'width': 3, 'maxSpeed': 11.111}],
 'startIntersection': 'intersection_0_1',
 'endIntersection': 'intersection_1_1'}
```

# XML Intersection

## Virtual := False

```
<junction id="J7" type="traffic_light" x="70.27" y="51.37" incLanes="E10_0 -E8_0" intLanes=":J7_0_0 :J7_1_0" >
  <request index="0" response="10" foes="10" cont="0"/>
  <request index="1" response="00" foes="01" cont="0"/>
</junction>
```

## Virtual := True

```
<junction id="J8" type="dead_end" x="39.07" y="-13.78" incLanes="-E11_0" intLanes=""/>

<tlLogic id="J0" type="static" programID="0" offset="0">
    <phase duration="42" state="rGGG"/>
    <phase duration="3"  state="ryGG"/>
    <phase duration="42" state="GrGG"/>
    <phase duration="3"  state="yrGG"/>
</tlLogic>
```
