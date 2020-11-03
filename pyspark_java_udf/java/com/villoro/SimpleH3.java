package com.villoro;

import java.io.IOException;
import com.uber.h3core.H3Core;

class SimpleH3
{ 
    public static String toH3Address(Double longitude, Double latitude, int resolution){
        if (longitude == null || latitude == null) {
            return null;
        }

        try {
            H3Core h3 = H3Core.newInstance();
            return h3.geoToH3Address(longitude, latitude, resolution);
        }
        catch(IOException e) {
            return null;
        }
    }
} 