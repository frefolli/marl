"""
Tools::CityFlow2SUMO

Converts RoadNet and FlowNet format json files to SUMO xml files
"""

from __future__ import annotations
import json
import math

def load_network_json(path: str) -> dict:
  with open(path, "r") as file:
    return json.load(file)

def load_routes_json(path: str) -> list:
  with open(path, "r") as file:
    return json.load(file)

def indentation(indent: int) -> str:
  return "  " * indent

class Point:
  def __init__(self, x: float, y: float) -> None:
    self.x: float = x
    self.y: float = y

  def distance(self, o: Point) -> float:
    return math.sqrt(math.pow(self.x - o.x, 2) + math.pow(self.y - o.y, 2))

  def to_str(self) -> str:
    return "%s,%s" % (self.x, self.y)

  def __repr__(self) -> str:
    return self.to_str()

class Lane:
  def __init__(self, id: str, index: int, speed: float, length: float) -> None:
    self.id: str = id
    self.index: int = index
    self.speed: float = speed
    self.length: float = length

  def to_xml(self, indent: int = 0) -> str:
    return (
        indentation(indent) +
        "<lane id=\"%s\" index=\"%s\" speed=\"%s\" length=\"%s\" shape=\"\"/>" % (
          self.id, self.index, self.speed, self.length
        ))

  def __repr__(self) -> str:
    return self.to_xml(0)

  @staticmethod
  def name(edge_id: str, lane_id: int) -> str:
    return "%s_%s" % (edge_id, lane_id)

class Edge:
  def __init__(self, id: str, from_junction: str, to_junction: str, shape: list[Point], lanes: list[Lane]) -> None:
    self.id: str = id
    self.from_junction: str = from_junction
    self.to_junction: str = to_junction
    self.shape: list[Point] = shape
    self.lanes: list[Lane] = lanes

  def to_xml(self, indent: int = 0) -> str:
    header = (
      indentation(indent) +
      "<edge id=\"%s\" from=\"%s\" to=\"%s\" priority=\"-1\" spreadType=\"center\" shape=\"%s\">" % (
        self.id, self.from_junction, self.to_junction, " ".join([p.to_str() for p in self.shape])
      )
    )
    children = [
      lane.to_xml(indent + 1) for lane in self.lanes
    ]
    footer = indentation(indent) + "</edge>"
    return "\n".join([header] + children + [footer])

  def __repr__(self) -> str:
    return self.to_xml(0)

class InternalEdge:
  def __init__(self, id: str, lanes: list[Lane]) -> None:
    self.id: str = id
    self.lanes: list[Lane] = lanes

  def to_xml(self, indent: int = 0) -> str:
    header = (
      indentation(indent) +
      "<edge id=\"%s\" function=\"internal\">" % (
        self.id
      )
    )
    children = [
      lane.to_xml(indent + 1) for lane in self.lanes
    ]
    footer = indentation(indent) + "</edge>"
    return "\n".join([header] + children + [footer])

  def __repr__(self) -> str:
    return self.to_xml(0)

  @staticmethod
  def name(junction_id: str, connection_id: int) -> str:
    return "%s_%s" % (junction_id, connection_id)

class Junction:
  def __init__(self, id: str, kind: str, point: Point, incoming_lanes: list[str], into_lanes: list[str], requests: list[Request]) -> None:
    self.id: str = id
    self.kind = kind
    self.point = point
    self.incoming_lanes = incoming_lanes
    self.into_lanes = into_lanes
    self.requests: list[Request] = requests

  def to_xml(self, indent: int = 0) -> str:
    header = (
      indentation(indent) +
      "<junction id=\"%s\" type=\"%s\" x=\"%s\" y=\"%s\" incLanes=\"%s\" intLanes=\"%s\" >" % (
        self.id, self.kind, self.point.x, self.point.y,
        " ".join(self.incoming_lanes),
        " ".join(self.into_lanes)
      )
    )
    children = [
      request.to_xml(indent + 1)
      for request in self.requests
    ]
    footer = indentation(indent) + "</junction>"
    return "\n".join([header] + children + [footer])

  def __repr__(self) -> str:
    return self.to_xml(0)

class Request:
  def __init__(self, index: int, response: str, foes: str) -> None:
    self.index: int = index
    self.response: str = response
    self.foes: str = foes

  def to_xml(self, indent: int = 0) -> str:
    return (
        indentation(indent) +
        "<request index=\"%s\" response=\"%s\" foes=\"%s\" cont=\"0\"/>" % (
          self.index, self.response, self.foes
        ))

  def __repr__(self) -> str:
    return self.to_xml(0)

  @staticmethod
  def name(edge_id: str, lane_id: int) -> str:
    return "%s_%s" % (edge_id, lane_id)

class InternalConnection:
  def __init__(self, from_edge: str, to_edge: str, from_lane: int, to_lane: int, direction: str) -> None:
    self.from_edge: str = from_edge
    self.to_edge: str = to_edge
    self.from_lane: int = from_lane
    self.to_lane: int = to_lane
    self.direction: str = direction

  def to_xml(self, indent: int = 0) -> str:
    return (
      indentation(indent) +
      '<connection from="%s" to="%s" fromLane="%s" toLane="%s" dir="%s" state="M"/>' % (
        self.from_edge, self.to_edge, self.from_lane, self.to_lane, self.direction
      )
    )

  def __repr__(self) -> str:
    return self.to_xml(0)

class ViaConnection:
  def __init__(self, from_edge: str, to_edge: str, from_lane: int, to_lane: int, direction: str, index: int, via_junction_lane: str, junction_id: str) -> None:
    self.from_edge: str = from_edge
    self.to_edge: str = to_edge
    self.from_lane: int = from_lane
    self.to_lane: int = to_lane
    self.direction: str = direction
    self.index: int = index
    self.via_junction_lane: str = via_junction_lane
    self.junction_id: str = junction_id

  def to_xml(self, indent: int = 0) -> str:
    return (
      indentation(indent) +
      '<connection from="%s" to="%s" fromLane="%s" toLane="%s" dir="%s" state="M" linkIndex=\"%s\" via=\"%s\" tl=\"%s\"/>' % (
        self.from_edge, self.to_edge, self.from_lane, self.to_lane, self.direction, self.index, self.via_junction_lane, self.junction_id
      )
    )

  def __repr__(self) -> str:
    return self.to_xml(0)

class TLLogic:
  def __init__(self, id: str, phases: list[Phase]) -> None:
    self.id: str = id
    self.phases: list[Phase] = phases

  def to_xml(self, indent: int = 0) -> str:
    header = (
        indentation(indent) +
        "<tlLogic id=\"%s\" type=\"static\" programID=\"0\" offset=\"0\">" % (
          self.id
        ))
    children = [
      phase.to_xml(indent + 1)
      for phase in self.phases
    ]
    footer = "</tlLogic>"
    return "\n".join([header] + children + [footer])

  def __repr__(self) -> str:
    return self.to_xml(0)

class Phase:
  def __init__(self, duration: float, state: str) -> None:
    self.duration: float = duration
    self.state: str = state

  def to_xml(self, indent: int = 0) -> str:
    return (
        indentation(indent) +
        "<phase duration=\"%s\" state=\"%s\"/>" % (
          self.duration, self.state
        ))

  def __repr__(self) -> str:
    return self.to_xml(0)

  @staticmethod
  def name(edge_id: str, lane_id: int) -> str:
    return "%s_%s" % (edge_id, lane_id)

class Network:
  def __init__(self,
               road_edges: list[Edge],
               junctions: list[Junction],
               via_connections: list[ViaConnection],
               internal_connections: list[InternalConnection],
               junction_edges: list[InternalEdge],
               tllogics: list[TLLogic]) -> None:
    self.road_edges: list[Edge] = road_edges
    self.junctions: list[Junction] = junctions
    self.via_connections: list[ViaConnection] = via_connections
    self.internal_connections: list[InternalConnection] = internal_connections
    self.junction_edges: list[InternalEdge] = junction_edges
    self.tllogics: list[TLLogic] = tllogics

  def to_xml(self, indent: int = 0) -> str:
    lines = []
    lines.append(indentation(indent) + '<?xml version="1.0" encoding="UTF-8"?>')
    lines.append(indentation(indent) + '<net version="1.20" junctionCornerDetail="5" limitTurnSpeed="5.50" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/net_file.xsd">')
    for child in self.road_edges:
      lines.append(child.to_xml(indent + 1))
    for child in self.junction_edges:
      lines.append(child.to_xml(indent + 1))
    for child in self.tllogics:
      lines.append(child.to_xml(indent + 1))
    for child in self.junctions:
      lines.append(child.to_xml(indent + 1))
    for child in self.via_connections:
      lines.append(child.to_xml(indent + 1))
    for child in self.internal_connections:
      lines.append(child.to_xml(indent + 1))
    lines.append('</net>')
    return "\n".join(lines)

  def __repr__(self) -> str:
    return self.to_xml(0)

def translate_road(json_road: dict) -> Edge:
  points = [Point(p['x'], p['y']) for p in json_road['points']]
  length = sum([points[i].distance(points[i - 1]) for i in range(1, len(points))])
  lanes = [
    Lane(
      id=Lane.name(json_road['id'], json_lane_idx),
      index=json_lane_idx,
      speed=json_lane['maxSpeed'],
      length=length
    )
    for json_lane_idx, json_lane in enumerate(json_road['lanes'])
  ]
  return Edge(
    id=json_road['id'],
    from_junction=json_road['startIntersection'],
    to_junction=json_road['endIntersection'],
    shape=points,
    lanes=lanes,
  )

def translate_direction(json_direction: str) -> str:
  directions = {
    'go_straight': 's',
    'turn_left': 'l',
    'turn_right': 'r'
  }
  return directions[json_direction]

def translate_tl_intersection(json_intersection: dict) -> tuple[Junction, list[ViaConnection], list[InternalConnection], list[InternalEdge], TLLogic]:
  junction_id = json_intersection['id']
  incoming_lanes = {}
  into_lanes = {}
  via_connections: list[ViaConnection] = []
  internal_connections: list[InternalConnection] = []
  roadToLaneLinks: dict[int, list[int]] = {}
  junction_edges: list[InternalEdge] = []

  for roadLink_index, roadLink in enumerate(json_intersection['roadLinks']):
    from_edge = roadLink['startRoad']
    to_edge = roadLink['endRoad']
    direction = translate_direction(roadLink['type'])
    roadToLaneLinks[roadLink_index] = []
    for laneLink in roadLink['laneLinks']:
      from_lane = laneLink['startLaneIndex']
      to_lane = laneLink['endLaneIndex']
      index = len(via_connections)
      edge_name = InternalEdge.name(junction_id, index)
      lane_name = Lane.name(edge_name, 0)
      
      via_connection = ViaConnection(from_edge, to_edge, from_lane, to_lane, direction, index, lane_name, junction_id)
      internal_connection = InternalConnection(edge_name, to_edge, 0, to_lane, direction)
      junction_lane = Lane(id=lane_name, index=0, speed=3.93, length=2.19)
      junction_edge = InternalEdge(id=edge_name, lanes=[junction_lane])

      roadToLaneLinks[roadLink_index].append(index)
      incoming_lanes[Lane.name(via_connection.from_edge, via_connection.from_lane)] = 0
      into_lanes[Lane.name(via_connection.to_edge, via_connection.to_lane)] = 0
      via_connections.append(via_connection)
      internal_connections.append(internal_connection)
      junction_edges.append(junction_edge)
  n_of_via_connections = len(via_connections)

  phases: list[Phase] = []
  for tl_phase in json_intersection['trafficLight']['lightphases']:
    gyr_map = {c:'r' for c in range(n_of_via_connections)}
    for greenRoadLink_index in tl_phase["availableRoadLinks"]:
      for greenLaneLink_index in roadToLaneLinks[greenRoadLink_index]:
        gyr_map[greenLaneLink_index] = 'G'
    phase_state = "".join([gyr_map[c] for c in range(n_of_via_connections)])
    phase_duration = tl_phase["time"]
    phases.append(Phase(duration=phase_duration, state=phase_state))
  tllogic = TLLogic(id=junction_id, phases=phases)

  junction = Junction(
    id=junction_id,
    kind='traffic_light',
    point=Point(json_intersection['point']['x'], json_intersection['point']['y']),
    incoming_lanes=list(incoming_lanes),
    into_lanes=list(into_lanes),
    requests=[],
  )

  return (junction, via_connections, internal_connections, junction_edges, tllogic)

def translate_virtual_intersection(json_intersection: dict, incoming_map: dict[str, list[str]], into_map: dict[str, list[str]]) -> tuple[Junction]:
  junction_id = json_intersection['id']
  incoming_lanes = incoming_map[junction_id]
  into_lanes = into_map[junction_id]

  junction = Junction(
    id=junction_id,
    kind='dead_end',
    point=Point(json_intersection['point']['x'], json_intersection['point']['y']),
    incoming_lanes=incoming_lanes,
    into_lanes=into_lanes,
    requests=[],
  )

  return (junction,)

def map_incoming_into_junction_edges(edges: list[Edge]) -> tuple[dict[str, list[str]], dict[str, list[str]]]:
  raw_incoming_map: dict[str, dict[str, int]] = {}
  raw_into_map: dict[str, dict[str, int]] = {}

  for edge in edges:
    if edge.to_junction not in raw_incoming_map:
      raw_incoming_map[edge.to_junction] = {}
    if edge.from_junction not in raw_into_map:
      raw_into_map[edge.from_junction] = {}
    for lane in edge.lanes:
      raw_incoming_map[edge.to_junction][lane.id] = 0
      raw_into_map[edge.from_junction][lane.id] = 0

  incoming_map: dict[str, list[str]] = {junction:list(raw_incoming_map[junction].keys()) for junction in raw_incoming_map}
  into_map: dict[str, list[str]] = {junction:list(raw_into_map[junction].keys()) for junction in raw_into_map}

  return incoming_map, into_map

def translate_network(json_network: dict):
  json_roads = json_network['roads']
  json_intersections = json_network['intersections']

  road_edges = [translate_road(json_road) for json_road in json_roads]
  junction_incoming_map, junction_into_map = map_incoming_into_junction_edges(road_edges)

  junctions = []
  via_connections = []
  internal_connections = []
  junction_edges = []
  tllogics = []
  for json_intersection in json_intersections:
    if json_intersection['virtual']:
      _junction, = translate_virtual_intersection(json_intersection, junction_incoming_map, junction_into_map)
      junctions.append(_junction)
    else:
      _junction, _via_connections, _internal_connections, _junction_edges, tllogic = translate_tl_intersection(json_intersection)
      junctions.append(_junction)
      internal_connections += _internal_connections
      via_connections += _via_connections
      junction_edges += _junction_edges
      tllogics.append(tllogic)

  return Network(road_edges, junctions, via_connections, internal_connections, junction_edges, tllogics)

if __name__ == "__main__":
  json_network = load_network_json("../../assets/tools/cityflow2sumo/roadnet_28_7.json")
  json_routes = load_routes_json("../../assets/tools/cityflow2sumo/anon_28_7_newyork_real_double.json")

  network: Network = translate_network(json_network)

  with open("output.net.xml", "w") as file:
    file.write(network.to_xml())
