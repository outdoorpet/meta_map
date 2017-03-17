var map = L.map('map').setView([0, 0], 0);
var layer = new L.StamenTileLayer("toner");
layer.addTo(map);


var activeIcon = L.divIcon({
    className: 'svg-marker',
    html: '<svg xmlns="http://www.w3.org/2000/svg" version="1.1" style="margin: 0 auto; width: 20px; height:20px;"><polygon style="fill:Red; stroke:#666666; stroke-width:2; stroke-opacity:0.5"points="0,0 20,0 10,20"/></svg>',
    iconSize: L.point(20, 20),
    iconAnchor: L.point(10, 20),
    popupAnchor: L.point(0,-20)
});

var passiveIcon = L.divIcon({
    className: 'svg-marker',
    html: '<svg xmlns="http://www.w3.org/2000/svg" version="1.1" style="margin: 0 auto; width: 20px; height:20px;"><polygon style="fill:#3D8EC9; stroke:#666666; stroke-width:2; stroke-opacity:0.5"points="0,0 20,0 10,20"/></svg>',
    iconSize: L.point(20, 20),
    iconAnchor: L.point(10, 20),
    popupAnchor: L.point(0,-20)
});

var stations = {};

function addStation(station_id, latitude, longitude) {
    var marker = L.marker([latitude, longitude], {
        icon: passiveIcon
    }).bindPopup(station_id).on("click", circleClick);


    marker.status = "--";

    marker.myCustomStationID = station_id;

    marker.addTo(map);

    stations[station_id] = {
        "marker": marker,
        "latitude": latitude,
        "longitude": longitude};

    setMarkerInactive(stations[station_id]);
}

function setMarkerActive(value) {
    if (value.marker.status != "active") {
        var pos = map.latLngToLayerPoint(value.marker.getLatLng()).round();
        value.marker.setIcon(activeIcon);
        value.marker.setZIndexOffset(101 - pos.y);
        value.marker.status = "active";
    }
}

function setMarkerInactive(value) {
    if (value.marker.status != "passive") {
        var pos = map.latLngToLayerPoint(value.marker.getLatLng()).round();
        value.marker.setIcon(passiveIcon);
        value.marker.setZIndexOffset(100 - pos.y);
        value.marker.status = "passive";
    }
}

function setAllInactive() {
    _.forEach(stations, function(value, key) {
        setMarkerInactive(value);
    });
}


function setAllActive() {
    _.forEach(stations, function(value, key) {
        setMarkerActive(value);
    });
}


function highlightStation(station_id) {
    setAllInactive();
    var value = stations[station_id];
    setMarkerActive(value)
}


function circleClick(e) {
        var clickedCircle = e.target;

    highlightStation(clickedCircle.myCustomStationID)
    clickedCircle.openPopup();
}
