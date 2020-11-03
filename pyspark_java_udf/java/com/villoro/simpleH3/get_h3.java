package com.villoro.simpleH3;

import java.io.IOException;
import com.uber.h3core.H3Core;
import org.apache.spark.sql.api.java.UDF2;

public class get_h3 implements UDF2<Double, Double, String> {

    @Override
    public String call(Double longitude, Double latitude) throws Exception {

        if (longitude == null || latitude == null) {
            return null;
        }

        try {
            H3Core h3 = H3Core.newInstance();
            return h3.geoToH3Address(longitude, latitude, 3);
        }
        catch(IOException e) {
            return null;
        }
    }
}
