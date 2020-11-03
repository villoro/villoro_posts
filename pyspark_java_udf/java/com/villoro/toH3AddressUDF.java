package com.villoro;

import java.io.IOException;
import com.uber.h3core.H3Core;
import org.apache.spark.sql.api.java.UDF3;

public class toH3AddressUDF implements UDF3<Double, Double, Integer, String> {

    private H3Core h3;

    @Override
    public String call(Double longitude, Double latitude, Integer resolution) throws Exception {

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
