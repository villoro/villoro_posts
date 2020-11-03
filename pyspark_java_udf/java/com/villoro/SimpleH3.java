package com.villoro;

import java.io.IOException;
import com.uber.h3core.H3Core;

class SimpleH3
{ 

    private static H3Core h3;

    public static String toH3Address(Double longitude, Double latitude, int resolution){
        
        if (h3 == null) {
            try {
                h3 = H3Core.newInstance();
            }
            catch(IOException e) {
                return null;
            }
        }

        if (longitude == null || latitude == null) {
            return null;
        } else {
            return h3.geoToH3Address(longitude, latitude, resolution);
        }
    }
} 