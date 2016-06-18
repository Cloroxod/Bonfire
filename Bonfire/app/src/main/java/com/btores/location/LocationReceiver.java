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
    private static final int getSignalTimedOutTime = 60000;
    private static final int acccuracyThreshold = 10;
    private static final int secondPerMeter = 5;
    Timer getSignalTimedOut;
    LocationManager lm;
    LocationResultCallback locationResult;
    boolean gps_enabled=false;
    boolean network_enabled=false;
    Location accurateGPS=null;
    Location accurateNetwork=null;

    public boolean getLocation(Context context, LocationResultCallback result)
    {
        // setup callback
        locationResult=result;
        // clear previous data
        accurateGPS=null;
        accurateNetwork=null;

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
        // 1 min and it sends the last location that is active
        getSignalTimedOut=new Timer();
        getSignalTimedOut.schedule(new GetLastLocation(), getSignalTimedOutTime);
        return true;
    }

    LocationListener locationListenerGps = new LocationListener() {
        public void onLocationChanged(Location location) {
            if(location.getAccuracy() <= acccuracyThreshold) {
                getSignalTimedOut.cancel();
                try {
                    lm.removeUpdates(this);
                    lm.removeUpdates(locationListenerNetwork);
                } catch (SecurityException e) {
                    Log.e(TAG, "Premission denied");
                }
                locationResult.locationReceived(location);
            }
            else {
                if(accurateGPS == null) {
                    accurateGPS = location;
                }
                else {
                    long time = (location.getTime() - accurateGPS.getTime())/1000;
                    // uses the most accurate but with how far apart as a threshold
                    if((accurateGPS.getAccuracy() + time/secondPerMeter) >= location.getAccuracy()) {
                        accurateGPS = location;
                    }
                }

            }
        }
        public void onProviderDisabled(String provider) {}
        public void onProviderEnabled(String provider) {}
        public void onStatusChanged(String provider, int status, Bundle extras) {}
    };

    LocationListener locationListenerNetwork = new LocationListener() {
        public void onLocationChanged(Location location) {
            if(location.getAccuracy() <= acccuracyThreshold) {
                getSignalTimedOut.cancel();
                try {
                    lm.removeUpdates(this);
                    lm.removeUpdates(locationListenerGps);
                } catch (SecurityException e) {
                    Log.e(TAG, "Premission denied");
                }
                locationResult.locationReceived(location);
            }
            else {
                if(accurateNetwork == null) {
                    accurateNetwork = location;
                }
                else {
                    long time = (location.getTime() - accurateNetwork.getTime())/1000;
                    // uses the most accurate but with how far apart as a threshold
                    if((accurateNetwork.getAccuracy() + time/secondPerMeter) >= location.getAccuracy()) {
                        accurateNetwork = location;
                    }
                }

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
                // first fetch the signals from cached most accurate from listeners

                // if no most accurate cache exists use last known location from location manager
                if(accurateGPS == null && accurateNetwork == null) {
                    Location net_loc=null, gps_loc=null;
                    if(gps_enabled)
                        gps_loc=lm.getLastKnownLocation(LocationManager.GPS_PROVIDER);
                    if(network_enabled)
                        net_loc=lm.getLastKnownLocation(LocationManager.NETWORK_PROVIDER);

                    // send null if no location is found
                    if(gps_loc == null && net_loc == null) {
                        locationResult.locationReceived(null);
                        return;
                    }
                    // send if only one is enabled
                    if(gps_loc==null){
                        locationResult.locationReceived(net_loc);
                        return;
                    }
                    if(net_loc==null){
                        locationResult.locationReceived(gps_loc);
                        return;
                    }

                    long timeElapsed = (gps_loc.getTime() - net_loc.getTime())/1000;
                    if(gps_loc.getAccuracy() <= (net_loc.getAccuracy()+timeElapsed/secondPerMeter))
                        locationResult.locationReceived(gps_loc);
                    else
                        locationResult.locationReceived(net_loc);
                    return;
                }
                // send if one of the accurate signals is null
                if(accurateNetwork==null){
                    locationResult.locationReceived(accurateGPS);
                    return;
                }
                if(accurateGPS==null){
                    locationResult.locationReceived(accurateNetwork);
                    return;
                }

                long timeElapsed = (accurateGPS.getTime() - accurateNetwork.getTime())/1000;
                if(accurateGPS.getAccuracy() <= (accurateNetwork.getAccuracy()+timeElapsed/secondPerMeter))
                    locationResult.locationReceived(accurateGPS);
                else
                    locationResult.locationReceived(accurateNetwork);
            }catch (SecurityException e) {
                Log.e(TAG, "Premission denied");
            }
        }
    }

}
