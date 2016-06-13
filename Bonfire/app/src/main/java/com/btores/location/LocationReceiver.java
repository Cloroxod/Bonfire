package com.btores.location;

/**
 * Created by Zach on 6/12/2016.
 */
import java.util.Timer;
import java.util.TimerTask;
import android.content.Context;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.os.Bundle;
import android.util.Log;

import com.btores.bonfire.MessageFragment.LocationResultCallback;

public class LocationReceiver {
    private static final String TAG = "LocationReceiver";

    Timer timerTimedOut;
    LocationManager lm;
    LocationResultCallback locationResult;
    boolean gps_enabled=false;
    boolean network_enabled=false;

    public boolean getLocation(Context context, LocationResultCallback result)
    {
        // setup callback
        locationResult=result;
        if(lm==null)
            lm = (LocationManager) context.getSystemService(Context.LOCATION_SERVICE);

        // check if gps and network are enabled
        try{gps_enabled=lm.isProviderEnabled(LocationManager.GPS_PROVIDER);}catch(Exception ex){}
        try{network_enabled=lm.isProviderEnabled(LocationManager.NETWORK_PROVIDER);}catch(Exception ex){}

        if(!gps_enabled && !network_enabled)
            return false;
        try {
            // tries to get new location
            if (gps_enabled)
                lm.requestLocationUpdates(LocationManager.GPS_PROVIDER, 0, 0, locationListenerGps);
            if (network_enabled)
                lm.requestLocationUpdates(LocationManager.NETWORK_PROVIDER, 0, 0, locationListenerNetwork);

        }catch (SecurityException e) {
            Log.e(TAG, "Premission denied");
        }
        // 2 min and it sends the last location that is active
        timerTimedOut=new Timer();
        timerTimedOut.schedule(new GetLastLocation(), 120000);
        return true;
    }

    public
    LocationListener locationListenerGps = new LocationListener() {
        public void onLocationChanged(Location location) {
            timerTimedOut.cancel();
            locationResult.locationReceived(location);
            try {
                lm.removeUpdates(this);
                lm.removeUpdates(locationListenerNetwork);
            }catch (SecurityException e) {
                Log.e(TAG, "Premission denied");
            }
        }
        public void onProviderDisabled(String provider) {}
        public void onProviderEnabled(String provider) {}
        public void onStatusChanged(String provider, int status, Bundle extras) {}
    };

    LocationListener locationListenerNetwork = new LocationListener() {
        public void onLocationChanged(Location location) {
            timerTimedOut.cancel();
            locationResult.locationReceived(location);
            try {
                lm.removeUpdates(this);
                lm.removeUpdates(locationListenerGps);
            }catch (SecurityException e) {
                Log.e(TAG, "Premission denied");
            }
        }
        public void onProviderDisabled(String provider) {}
        public void onProviderEnabled(String provider) {}
        public void onStatusChanged(String provider, int status, Bundle extras) {}
    };

    class GetLastLocation extends TimerTask {
        @Override
        public void run() {

            try {
                lm.removeUpdates(locationListenerNetwork);
                lm.removeUpdates(locationListenerGps);
            }catch (SecurityException e) {
                Log.e(TAG, "Premission denied");
            }
            Location net_loc=null, gps_loc=null;
            if(gps_enabled)
                gps_loc=lm.getLastKnownLocation(LocationManager.GPS_PROVIDER);
            if(network_enabled)
                net_loc=lm.getLastKnownLocation(LocationManager.NETWORK_PROVIDER);

            //if there are both values use the latest one
            if(gps_loc!=null && net_loc!=null){
                if(gps_loc.getTime()>net_loc.getTime())
                    locationResult.locationReceived(gps_loc);
                else
                    locationResult.locationReceived(net_loc);
                return;
            }

            if(gps_loc!=null){
                locationResult.locationReceived(gps_loc);
                return;
            }
            if(net_loc!=null){
                locationResult.locationReceived(net_loc);
                return;
            }
            locationResult.locationReceived(null);
        }
    }

}
