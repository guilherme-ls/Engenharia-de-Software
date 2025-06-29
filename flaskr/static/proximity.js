// Utility functions for the temperature/proximity bar

function getDistanceFromLatLonInMeters(lat1, lon1, lat2, lon2) {
    const R = 6371000;
    const toRad = x => x * Math.PI / 180;
    const φ1 = toRad(lat1);
    const φ2 = toRad(lat2);
    const Δφ = toRad(lat2 - lat1);
    const Δλ = toRad(lon2 - lon1);

    const a = Math.sin(Δφ / 2) * Math.sin(Δφ / 2) +
              Math.cos(φ1) * Math.cos(φ2) *
              Math.sin(Δλ / 2) * Math.sin(Δλ / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));

    return R * c;
}

function interpolateColor(distance, minDistance, maxDistance) {
    let t;
    if (distance <= minDistance) t = 1;
    else if (distance >= maxDistance) t = 0;
    else t = 1 - ((distance - minDistance) / (maxDistance - minDistance));
    t = Math.max(0, Math.min(1, t));
    const r = Math.round(33 + (244 - 33) * t);
    const g = Math.round(150 + (67 - 150) * t);
    const b = Math.round(243 + (54 - 243) * t);
    return `rgb(${r},${g},${b})`;
}

function updateProximityBar(distance, userLat, userLng, treeLat, treeLng) {
    const maxDistance = 100;
    const minDistance = 5;
    let percent;
    if (distance <= minDistance) {
        percent = 100;
    } else if (distance >= maxDistance) {
        percent = 0;
    } else {
        percent = 100 - ((distance - minDistance) / (maxDistance - minDistance)) * 100;
    }
    percent = Math.max(0, Math.min(100, percent));
    const color = interpolateColor(distance, minDistance, maxDistance);
    const bar = document.getElementById('proximity-bar');
    if (bar) {
        bar.style.width = percent + "%";
        bar.style.background = color;
    }
}

function startProximityWatch(treeCoords, hasShownGeoAlertObj) {
    let proximityWatchId = null;
    if (!navigator.geolocation) {
        if (!hasShownGeoAlertObj.value) {
            alert("Geolocalização não suportada ou permitida no seu navegador.");
            hasShownGeoAlertObj.value = true;
        }
        return;
    }
    function tryStart() {
        if (treeCoords && typeof treeCoords.lat === "number" && typeof treeCoords.lng === "number") {
            if (proximityWatchId !== null) {
                navigator.geolocation.clearWatch(proximityWatchId);
            }
            proximityWatchId = navigator.geolocation.watchPosition(
                function(pos) {
                    if (!pos || !pos.coords) {
                        if (!hasShownGeoAlertObj.value) {
                            alert("Não foi possível obter sua posição. Certifique-se de que o GPS está ativado e que você está em um local com sinal.");
                            hasShownGeoAlertObj.value = true;
                        }
                        updateProximityBar(0, undefined, undefined, treeCoords.lat, treeCoords.lng);
                        return;
                    }
                    const userLat = pos.coords.latitude;
                    const userLng = pos.coords.longitude;
                    const treeLat = treeCoords.lat;
                    const treeLng = treeCoords.lng;
                    const distance = getDistanceFromLatLonInMeters(userLat, userLng, treeLat, treeLng);
                    updateProximityBar(distance, userLat, userLng, treeLat, treeLng);
                },
                function(err) {
                    const treeLat = treeCoords.lat;
                    const treeLng = treeCoords.lng;
                    updateProximityBar(0, undefined, undefined, treeLat, treeLng);
                    if (!hasShownGeoAlertObj.value) {
                        if (err.code === 1) {
                            alert("Permissão de localização negada. Ative a localização.");
                        } else if (err.code === 2) {
                            alert("Não foi possível obter sua posição. Certifique-se de que o GPS está ativado e que você está em um local com sinal.");
                        } else if (err.code === 3) {
                            alert("Tempo esgotado ao tentar obter localização.");
                        }
                        hasShownGeoAlertObj.value = true;
                    }
                },
                { enableHighAccuracy: true, maximumAge: 1000, timeout: 10000 }
            );
        } else {
            setTimeout(tryStart, 200);
        }
    }
    tryStart();
}
