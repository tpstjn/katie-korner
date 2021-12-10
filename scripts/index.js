let map, infoWindow;

function initMap() {

  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 41.15633702474994, lng: -80.11574326048795 },
    zoom: 20,
    mapTypeId: 'satellite'
  });
  infoWindow = new google.maps.InfoWindow();

  const gccKK = document.createElement("button");

  gccKK.textContent = "Grove City Location";
  gccKK.classList.add("custom-map-control-button");
  map.controls[google.maps.ControlPosition.TOP_CENTER].push(gccKK);
  gccKK.addEventListener("click", () => {
    // Try HTML5 geolocation.
      const pos = {
        lat: 41.15633702474994, 
        lng: -80.11574326048795
      }

        infoWindow.setPosition(pos);
        infoWindow.setContent("Location found.");
        infoWindow.open(map);
        map.setCenter(pos);
        },
        () => {
          handleLocationError(true, infoWindow, map.getCenter());
        }
      );
      
  const chipKK = document.createElement("button");

  chipKK.textContent = "Chippewa Location";
  chipKK.classList.add("custom-map-control-button");
  map.controls[google.maps.ControlPosition.TOP_CENTER].push(chipKK);
  chipKK.addEventListener("click", () => {
    // Try HTML5 geolocation.
      const pos = {
        lat:40.77894847955464, 
        lng:-80.38341388103947
      }

        infoWindow.setPosition(pos);
        infoWindow.setContent("Location found.");
        infoWindow.open(map);
        map.setCenter(pos);
        },
        () => {
          handleLocationError(true, infoWindow, map.getCenter());
        }
      );

  const beavKK = document.createElement("button");
  beavKK.textContent = "Ohio Location";
  beavKK.classList.add("custom-map-control-button");
  map.controls[google.maps.ControlPosition.TOP_CENTER].push(beavKK);
  beavKK.addEventListener("click", () => {
    // Try HTML5 geolocation.
      const pos = {
        lat:40.79027044842654, 
        lng:-80.28802090856078
      }

        infoWindow.setPosition(pos);
        infoWindow.setContent("Location found.");
        infoWindow.open(map);
        map.setCenter(pos);
        },
        () => {
          handleLocationError(true, infoWindow, map.getCenter());
        }
      );
}

function handleLocationError(browserHasGeolocation, infoWindow, pos) {
  infoWindow.setPosition(pos);
  infoWindow.setContent(
    browserHasGeolocation
      ? "Error: The Geolocation service failed."
      : "Error: Your browser doesn't support geolocation."
  );
  infoWindow.open(map);
}